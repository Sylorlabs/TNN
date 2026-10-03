# SPEC-NOISY-RATES: PREREG (frozen kill bars)

**Lane:** docs/lab/research-lead/overnight-20260928/spec_noisy_rates/
**Date:** 2026-10-03
**Status:** Non-ledger (claim minting paused). Prereg committed strictly
before any implementation file exists.

## Parent result this builds on

SPEC-ADAPTIVE-SWITCH (BUILD-PASS 9/9) made the rule L > (W(k)-1)*C
executable: a 16-tick warmup on the deterministic power-of-2 grid gives
exact observed rates (16 = grid LCM), the exact rational price
pnum/pden = max(0,Dw-Qw)/Qw, and the strict comparison L*pden > pnum.
Its REPORT recorded caveat (b): "Deterministic grid; real-world noisy
rate estimation (EWMA/confidence) is untested -- suggested as a
follow-up lane, not a patch." Its recommendation #2: "If rate
estimation ever moves off the deterministic grid, the pnum/pden
rational should gain a confidence term; the strict-> comparison then
becomes a margin test, which is a new lane, not a patch to this one."
This lane IS that new lane. It builds on SPEC-ADAPTIVE-SWITCH without
redesigning it: same 25 cells, same 6 arms, same cost model
J = rb + rf*L, same fixed-arm dynamics, same reused sources
byte-unmodified (da_learn.zag explicitly untouched).

## Questions (frozen)

1. Does the adaptive switch still work with noisy rate estimates, or
   does it thrash (repeated policy flips)?
2. What is the estimation error -- how far off are the EWMA rate
   estimates from realized rates?
3. When should the switch commit vs keep observing -- what is the
   confidence threshold rule?

## Design (frozen)

**Noisy world.** T = 256 ticks. Drift and query arrivals are exogenous
per-tick events from two INDEPENDENT two-state Markov-modulated
Bernoulli processes (bursty, irregular), one per stream, with
parameters derived from the cell (M, N):

- State s in {0 = quiet, 1 = burst}; every episode starts quiet.
- Per tick, per stream, in this order: draw u1 (31-bit uniform);
  if s == 1 and u1 < 2^31/8 -> s = 0 (mean burst length 8 ticks);
  if s == 0 and u1 < 2^31/24 -> s = 1 (mean quiet length 24 ticks),
  both tests against the OLD s. Then draw u2 (31-bit uniform);
  the event fires iff (s == 1 and u2 < THR_PB) or
  (s == 0 and u2 < THR_PQ).
- THR_PB(M) = min(2^31, (5 * 2^31) / (2 * M)) -- burst fire prob
  pB = min(1, 2.5/M). THR_PQ(M) = max(0, ((4 * 2^31 / M) - THR_PB)/3)
  -- quiet fire prob pQ = (4/M - pB)/3, floored at 0. All threshold
  arithmetic in i64; thresholds stored as i64 (2^31 exceeds i32).
- Stationary P(burst) = (1/24)/(1/8 + 1/24) = 1/4; mean fire rate =
  0.25*pB + 0.75*pQ = 1/M exactly for M >= 2. At M = 1 (or N = 1),
  pB = pQ = 1: the event fires every tick deterministically (a rate-1
  process cannot be noisy). Burst/quiet fire ratio is 5x at every
  M >= 2: uniform burstiness across the grid.
- PRNG: LCG s <- (s * 1103515245 + 12345) mod 2^31, i64 arithmetic,
  mod hand-rolled (s - (s/2147483648)*2147483648); no shift ops needed,
  comparisons use the raw 31-bit state. Seeds (frozen): drift stream
  seed = M*1000003 + N*101 + 17; query stream seed =
  M*101 + N*1000003 + 917. Seeds reset at each episode start, so all 6
  arms of a cell see the IDENTICAL arrival sequence (identical realized
  D, Q); arrivals never depend on the arm's policy (4 draws per tick
  regardless of arm).
- Deterministic: integer arithmetic only, no wall-clock, no float in
  the experiment binary; 3/3 byte-identical runs required (K3).

**Rate estimator (adapt arm only).** Fixed point: rates in events per
1024 ticks. Per tick with samples d_t, q_t in {0,1}, alpha = 1/16:

- dh <- (15*dh + 1024*d_t)/16, starting dh = 0. Same for qh.
- Empirical EWMA variance: dev_d = 1024*d_t - dh_old (pre-update dh);
  ed <- (15*ed + dev_d*dev_d)/16, starting ed = 0. Same for eq.
- Effective sample size n_eff = (2-alpha)/alpha = 31.
  SE_d = isqrt(ed/31) (integer Newton sqrt, fixed 12 iterations).
- Approx 95% CI: dlo = max(0, dh - 2*SE_d), dhi = dh + 2*SE_d.
  Same for qlo, qhi.

**Price interval (margin test).** price = max(0, d-q)/q is increasing
in d and decreasing in q, so conservative integer bounds are:

- phi (upper): phin = max(0, dhi - qlo), phid = max(qlo, 1).
- plo (lower): plon = max(0, dlo - qhi), plod = max(qhi, 1).
- Point estimate at commit: pnum = max(0, dh - qh), pden = max(qh, 1).

**Commit vs observe (frozen threshold rule).** Checkpoints at elapsed
ticks e in {32, 48, 64, 80, 96, 112, 128} (first checkpoint at 32 so
EWMA burn-in has decayed: (15/16)^32 ~ 0.13 residual; burn-in bias is
common-mode and cancels in the price ratio). After a decisive commit,
re-checks continue at e in {144, 160, ..., 256}.

- Decide via nr_decide: eager-decisive iff L*phid > phin (strict, the
  parent's strict-> on the UPPER bound); lazy-decisive iff
  L*plod < plon (strict, L below the LOWER bound); else undecided.
  (phi >= plo always, so the two cannot co-fire; proof in REPORT.)
- Pre-commit, at each checkpoint e <= 128: if eager-decisive, commit
  eager: run a SYNC restamp immediately (+1 rebuild; guarantees zero
  post-commit refusals since drift is processed before query each
  tick), record tc = e, cm = 2, Dc/Qc = counts so far, snapshot the
  estimates. If lazy-decisive, commit lazy (cm = 1, no restamp).
  If undecided at e = 128, budget-default to lazy (cm = 0, terminal:
  no further checkpoints).
- Post-decisive-commit, at each later checkpoint: flip policy iff the
  interval is decisive on the OPPOSITE side (the decisiveness
  requirement IS the hysteresis: no flip on point-estimate crossing).
  Flip to eager runs a sync restamp. Count flips.
- Pre-commit the arm runs the honest lazy path (identical code to the
  fixed-lazy arm); L = 0 can never commit eager (needs 0 > phin >= 0).

**Arms.** pol 0 = fixed lazy, pol 1 = fixed eager (restamp on every
drift; parent dynamics unchanged), pol 2 = adaptive as above with
L in {0, 1, 3, 7}. 25 cells x 6 arms = 150 episodes, one CELL line
each. Fixed arms carry tc = -1, cm = 0, zeroed estimate fields.

**CELL line (adapt):**

    CELL M=<M> N=<N> P=adapt L=<L> C=1 tc=<tc> cm=<cm> Dc=<Dc> Qc=<Qc>
         dh=<dh> qh=<qh> dlo=<dlo> dhi=<dhi> qlo=<qlo> qhi=<qhi>
         pnum=<pnum> pden=<pden> plon=<plon> plod=<plod>
         phin=<phin> phid=<phid> sel=<sel> flips=<flips>
         D=<D> Q=<Q> od=<od> rs=<rs> rebuilds=<rb> answered=<an>
         refusals=<rf> kb=<kb>

tc = elapsed ticks at decisive commit, 128 on budget-default; cm: 0 =
budget-default lazy, 1 = decisive lazy, 2 = decisive eager; sel =
final policy; od = on-demand rebuilds (acc cell 0), rs = restamps,
rb = od + rs. Fixed arms: same line with tc=-1, cm=0, zeroed
estimate/interval fields, flips=0, od/rb per parent accounting.

**Cost model (frozen, unchanged).** J = rb + rf*L per line, C = 1.

## Frozen predictions (not bars; recorded before running)

- Noise: all cells with M > 1 or N > 1 should show (D, Q) !=
  (256/M, 256/N) on most cells (K4 bars >= 20/25).
- Estimation: mean relative EWMA error vs realized per-episode rates
  should sit well under 0.6/stream; the noisiest cells (M = N = 16,
  ~16 expected events, bursty) dominate the mean.
- Commit: clearly-separated cells commit decisively well before the
  128 budget; near-boundary cells (price ~= L) mostly ride to budget
  and default lazy, mirroring the parent's strict-> boundary behavior.
- Thrash: flips should be ~0; the interval-decisiveness flip rule
  should not oscillate.
- Portfolio: adaptive should still beat fixed lazy at L in {1,3,7}
  (any single net-positive eager commit makes it strict, since
  never-eager episodes are field-equal to their lazy twins) and tie
  exactly at L = 0. Vs fixed eager: reported as finding, not barred
  (parent found L=7 loses to eager).

## Kill bars (frozen)

- **K1.** Prereg commit strictly precedes the implementation commit
  (verified git log order on this lane directory). No implementation
  file may exist in the prereg commit.
- **K2.** Safebin mandatory: `which python3` and `which python` return
  nothing; pinned znc sha256
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef.
- **K3.** znc builds the assembly clean (no `: error`, exit 0);
  nr_bin exits 0 on all 3 runs; stderr empty on all 3 runs; stdout
  3/3 byte-identical (cmp + sha256). Exactly 150 CELL lines per run.
- **K4 (noisy anchoring).** All 25 lazy lines: answered = Q, kb = 2Q,
  refusals = rebuilds, rebuilds <= min(D, Q). All 25 eager lines:
  rebuilds = D, answered = Q, refusals = 0, kb = 2Q. Cross-arm:
  D and Q identical across the 6 arms within each cell (seeded-noise
  design). Noise-present: >= 20 of 25 cells have
  (D, Q) != (256/M, 256/N) (fails if the periodic grid was wired back
  in).
- **K5 (estimation error).** Over the 100 adapt lines, with true per-
  1024-tick rates 4D and 4Q (T = 256): mean |dh - 4D|/max(4D, 4) <=
  0.6 AND mean |qh - 4Q|/max(4Q, 4) <= 0.6. Mean absolute price error
  |pnum/pden - max(0, D-Q)/max(Q, 1)| <= 2.0 rebuilds. Coverage: the
  commit-time interval [dlo, dhi] covers the realized post-commit rate
  1024*(D-Dc)/(256-tc) in >= 70% of adapt episodes, and likewise
  [qlo, qhi] for queries (interval calibration under burstiness).
- **K6 (commit behavior / no thrash / structural accounting).**
  (a) >= 55 of 100 adapt episodes commit decisively (cm in {1,2}) by
  e = 128 -- the switch actually decides rather than punting to
  budget. (b) Total policy flips across all 100 adapt episodes <= 10
  (no thrash). (c) At L = 0: zero episodes with cm = 2 or sel = 1
  (eager structurally impossible at L = 0). (d) Every adapt line:
  answered = Q, kb = 2Q, rebuilds = od + rs, refusals = od. Episodes
  with flips = 0 and cm in {0,1}: od/rf field-equal to the lazy twin
  of the same cell and rs = 0 (honest warmup: never-eager episodes
  ARE lazy). Episodes with flips = 0 and cm = 2: rs = 1 + (D - Dc)
  (sync restamp + one restamp per post-commit drift) and
  od <= min(Dc, Qc) (pre-commit lazy only, zero post-commit refusals).
- **K7 (portfolio under noise).** Per-L totals of J = rb + rf*L over
  the 25 cells: L = 0: adapt total = lazy total exactly (the switch
  can never fire eager at L = 0). L in {1, 3, 7}: adapt total <
  lazy total strictly. (Adaptive vs fixed eager per L is a reported
  finding, not barred -- same status as the parent's L = 7 result.)
- **K8 (hygiene / governance).** ASCII-only lane sources; no world
  literals (901/902) in nr_spec.zag, nr_main.zag; exactly one
  `fn main` in the assembled binary; reused sources byte-unmodified
  (`git diff --quiet` on da_base.zag, da_module.zag, da_learn.zag,
  rb_world.zag, rb_fix.zag, et_world.zag, et_spec.zag, rr_spec.zag,
  and ../spec_lazy_default/ld_spec.zag); da_learn.zag in particular
  NOT modified (separate lane only); commits local with explicit
  pathspecs, never pushed.

## What would falsify the lane

- Realized (D, Q) equal the deterministic grid on >= 6 cells (K4):
  the noise is not actually noisy.
- Mean EWMA relative error > 0.6/stream (K5): the estimator is broken
  or biased (a correct EWMA on this stationary bursty process sits
  far below this ceiling; the ceiling catches sign/unit/divergence
  bugs, not legitimate noise).
- Interval coverage < 70% (K5): the confidence term is miscalibrated
  under burstiness (e.g. variance underestimated).
- Decisive commits < 55 (K6a): the margin test never fires -- the
  confidence term swallowed the switch.
- Flips > 10 (K6b): the switch thrashes under noise.
- Adaptive total not beating lazy total at any L > 0 (K7): noisy
  estimates make the switch pure overhead or actively harmful.
- Any L = 0 eager commit (K6c): the strict inequality is violated.
