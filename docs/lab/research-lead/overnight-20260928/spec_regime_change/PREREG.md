# SPEC-REGIME-CHANGE: PREREG (frozen kill bars)

**Lane:** docs/lab/research-lead/overnight-20260928/spec_regime_change/
**Date:** 2026-10-03
**Status:** Non-ledger (claim minting paused). Prereg committed strictly
before any implementation file exists.

## Parent result this builds on

SPEC-NOISY-RATES (BUILD-PASS 8/8, 2026-10-03) put the adaptive policy
switch on noisy bursty arrivals with EWMA rate estimation (alpha =
1/16, fixed point events/1024 ticks) and a confidence-interval margin
test. Findings: the switch ties fixed lazy at L = 0 and beats it at
L = 1, 3, 7; 3 flips across 100 adapt episodes, all single
eager->lazy self-corrections, zero oscillation; price-interval
coverage 73%; 82/100 decisive commits. Its REPORT left three open
follow-ups, quoted verbatim: "regime-change (nonstationary) worlds
untested -- the flip rule is the natural substrate; burn-in must be
handled explicitly for any absolute-rate (non-ratio) use of the EWMA;
the ~10.3us rebuild anchor was inherited, not re-measured." This lane
is the first of those three. It builds on SPEC-NOISY-RATES without
redesigning it: same cost model J = rb + rf*L, same EWMA estimator,
same margin-test commit rule, same flip rule (opposite-decisive
intervals), same reused sources byte-unmodified (da_learn.zag
explicitly untouched). The only delta is the world: arrivals are
nonstationary, with drift/query rates changing mid-episode at a
frozen shift tick.

## Questions (frozen)

1. Does the flip rule handle regime changes? (detect the shift?
   adapt to the new regime? or get stuck on the old commit?)
2. How quickly does it recover after a regime change?
   (adaptation latency in ticks from the shift to the flip?)
3. Does burn-in need explicit handling? (EWMA warmup after the
   shift: how large is the transient error, and does it corrupt
   flip decisions?)

## Design (frozen)

**Regime world.** T = 256 ticks. Each episode has two regimes:
ticks 0..127 use pre-shift parameters (M1, N1), ticks 128..255 use
post-shift parameters (M2, N2). The shift tick 128 is frozen and
coincides with the commit-budget point: the e = 128 checkpoint is
the last pre-shift decision, e = 144 the first post-shift
re-check. Arrival mechanics are otherwise identical to the parent:
two independent two-state Markov-modulated Bernoulli processes
(burst/quiet, mean burst 8 ticks, mean quiet 24 ticks, 5x
burst/quiet fire ratio, mean rate exactly 1/M and 1/N for M,N >= 2,
deterministic every-tick fire at M = 1 or N = 1), driven by a seeded
LCG. At the shift, ONLY the fire thresholds change
(TPB/TPQ/TQB/TQQ recomputed from (M2, N2) once, when t == 128);
the burst/quiet Markov states persist and the LCG sequences
continue unreseeded: the same world, new parameters, one
intervention. Seeds are frozen and reset per episode so all 6 arms
of a cell see the identical arrival sequence (arrivals never depend
on the arm's policy; 4 LCG draws per tick regardless of arm):
drift seed = R*1000003 + M1*101 + N1*17 + M2*13 + N2*7 + 17;
query seed = R*1000003 + M1*17 + N1*101 + M2*7 + N2*13 + 917
(i64). All integer arithmetic; 3/3 byte-identical runs required.

**Regime cells (frozen).** Six cells, chosen so the price
p = max(0,D-Q)/Q (per-avoided-refusal rebuild price; eager optimal
iff L > p, strict) moves in known ways:

- R0: (4,4) -> (4,4). No-shift control. Stationary sanity: the
  shift machinery must not disturb stationary behavior.
- R1: (1,16) -> (16,1). Lazy-world -> eager-world. Pre: drift
  every tick, rare queries, p ~ 7+ (lazy optimal at L = 1,3,7).
  Post: rare drift, query every tick, p ~ 0 (eager optimal at
  L >= 1). Tests lazy->eager adaptation.
- R2: (16,1) -> (1,16). Eager-world -> lazy-world. Mirror of R1.
  Tests eager->lazy adaptation.
- R3: (2,2) -> (8,8). Rate change, price ~ 0 both regimes.
  Control: the flip rule must NOT fire on a pure rate change
  with no price-regime change (no spurious flips).
- R4: (2,16) -> (2,16). No-shift lazy-world control (p ~ 7).
- R5: (16,1) -> (16,1). No-shift eager-world control (p ~ 0).

**Estimator, commit rule, flip rule: unchanged from the parent.**
EWMA alpha = 1/16, empirical EWMA variance, n_eff = 31,
approx-95% intervals (2*isqrt(var/31)), price interval by
monotonicity, checkpoints at elapsed e in
{32,...,128} pre-commit and {144,...,256} post-decisive-commit,
eager-decisive iff L*phid > phin (strict), lazy-decisive iff
L*plod < plon (strict), undecided at e = 128 budget-defaults to
lazy (terminal, com = 2, no post-shift re-checks), post-commit
flips only on opposite-decisive intervals. Eager commits and
flips-to-eager run a sync restamp (+1 rebuild). Pre-commit the
adapt arm runs the honest lazy path. The EWMA is NOT reset at the
shift: burn-in after the shift is measured, not handled, because
the question is whether the unmodified estimator + flip rule
copes.

**New instrumentation (appended fields, parent fields kept
verbatim for comparability).** Per-episode arrival splits:
Dpre/Qpre (ticks 0..127), Dpost/Qpost (ticks 128..255).
Post-shift flip tracking: pflips (post-shift flips only),
tf1 (tick of first post-shift flip, 0 if none), fdir
(direction of first post-shift flip: +1 to-eager, -1 to-lazy,
0 none), tf2 (tick of second post-shift flip, 0 if none).
EWMA burn-in snapshots (adapt arm): dh144/qh144 at e = 144
(first post-shift checkpoint, ~1 EWMA time constant after the
shift), dh192/qh192 at e = 192 (~4 time constants).

**Arms.** pol 0 = fixed lazy, pol 1 = fixed eager (parent
dynamics unchanged), pol 2 = adaptive with L in {0, 1, 3, 7}.
6 cells x 6 arms = 36 episodes, one CELL line each.

**CELL line (regime):**

    CELL R=<ri> M=<M1> N=<N1> M2=<M2> N2=<N2> P=<pol> L=<L> C=1
         tc=<tc> cm=<cm> Dc=<Dc> Qc=<Qc> dh=<dh> qh=<qh>
         dlo=<dlo> dhi=<dhi> qlo=<qlo> qhi=<qhi>
         pnum=<pnum> pden=<pden> plon=<plon> plod=<plod>
         phin=<phin> phid=<phid> sel=<sel> flips=<flips>
         pflips=<pflips> tf1=<tf1> fdir=<fdir> tf2=<tf2>
         Dpre=<dpre> Qpre=<qpre> Dpost=<dpost> Qpost=<qpost>
         D=<D> Q=<Q> od=<od> rs=<rs> rebuilds=<rb>
         answered=<an> refusals=<rf> kb=<kb>
         dh144=<dh144> qh144=<qh144> dh192=<dh192> qh192=<qh192>

Parent field semantics unchanged (tc/cm/Dc/Qc/sel/od/rs/rb/an/
rf/kb; dh..phid are commit-time snapshots). New fields are zero
on fixed arms except the arrival splits (meaningful for all
arms). D = Dpre + Dpost, Q = Qpre + Qpost.

**Cost model (frozen, unchanged).** J = rb + rf*L per line, C = 1.

## Frozen predictions (not bars; recorded before running)

- R1 pre-shift: L = 0, 1 commit lazy decisively by e = 32
  (plon ~ 591 > 0 at L = 0; plo ~ 2.7 > 1 at L = 1); L = 3
  commits lazy by ~e = 64 (plo -> ~5.7 as burn-in decays);
  L = 7 rides to budget (plo ~ 5.7 < 7, honest abstention).
  Post-shift: L = 1, 3 flip lazy->eager once dh/qh cross
  (tf1 ~ 152-176, 24-48 ticks after the shift); L = 0 never
  flips (eager impossible); L = 7 is stuck lazy (budget is
  terminal) -- the abstention-under-nonstationarity case.
- R2 pre-shift: L = 1, 3, 7 commit eager at e = 32 (phin = 0
  since dhi ~ 146 < qlo ~ 891); L = 0 rides to budget.
  Post-shift: L = 1, 3 flip eager->lazy (tf1 ~ 152-176);
  L = 7 stuck eager (plo ~ 5.7 < 7, never lazy-decisive);
  L = 0 stuck lazy-budget (harmless).
- R3: pre-shift commits eager or rides to budget (lazy-decisive
  impossible: plo ~ 0 both regimes); zero post-shift flips.
- Total post-shift correct-direction flips predicted: 4
  (R1-L1, R1-L3, R2-L1, R2-L3). No oscillation: the
  decisiveness requirement is the hysteresis, unchanged.
- Burn-in: mean EWMA relative error vs post-shift realized
  rate ~ 2.3 at e = 144 (one time constant: large, by design
  visible), ~ 0.1 at e = 192 (four time constants: converged).
- Economics: R1 flips save vs lazy (each post-flip drift
  costs 1 restamp under eager vs 1+L under lazy, and every
  post-shift drift causes exactly one refused query under
  lazy since queries fire every tick); R2 flips save vs
  eager (Q_rem*(1+L) << D_rem). The stuck episodes (R1-L7,
  R2-L7) tie their pre-shift-optimal twin.

## Kill bars (frozen)

- **K1.** Prereg commit strictly precedes the implementation
  commit (verified git log order on this lane directory). No
  implementation file may exist in the prereg commit.
- **K2.** Safebin mandatory: `which python3` and `which python`
  return nothing; pinned znc sha256
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef.
- **K3.** znc builds the assembly clean (no `: error`, exit 0);
  rc_bin exits 0 on all 3 runs; stderr empty on all 3 runs;
  stdout 3/3 byte-identical (cmp + sha256). Exactly 36 CELL
  lines per run (6 cells x 6 arms).
- **K4 (regime anchoring).** For every cell: all 6 arms see
  identical (D, Q) (seeded-noise + arm-independent shift);
  lazy lines: answered = Q, kb = 2Q, refusals = rebuilds,
  rebuilds <= min(D, Q); eager lines: rebuilds = D,
  answered = Q, refusals = 0, kb = 2Q. Arrival splits show
  the shift (lazy arm): R1: Dpre = 128 and Qpost = 128
  exactly (deterministic streams pin the shift timing),
  Dpost < 32, Qpre < 32; R2: Qpre = 128 and Dpost = 128
  exactly, Dpre < 32, Qpost < 32; R3: Dpre > 2*Dpost and
  Qpre > 2*Qpost; R0: |Dpre-Dpost| <= D/2 and
  |Qpre-Qpost| <= Q/2 (no-shift even split).
- **K5 (estimator under nonstationarity).** (a) No-shift
  cells (R0, R4, R5), adapt episodes, commit-time estimates
  vs realized per-1024-tick rates 4D/4Q: mean
  |dh-4D|/max(4D,4) <= 0.6 AND mean |qh-4Q|/max(4Q,4) <= 0.6
  (the estimator still works when stationary; parent
  measured 0.45). (b) Shift cells (R1, R2, R3), adapt
  episodes, e = 192 snapshots vs realized post-shift
  per-1024-tick rates 8*Dpost/8*Qpost: mean
  |dh192-8*Dpost|/max(8*Dpost,64) <= 0.5 AND mean
  |qh192-8*Qpost|/max(8*Qpost,64) <= 0.5 (the EWMA
  converges to the new regime; the 64 floor keeps the bar
  meaningful when the post-shift stream is near-zero).
  The e = 144 error is REPORTED AS A FINDING (burn-in
  magnitude), not barred.
- **K6 (flip behavior under regime change).** (a) Total
  flips <= 12 across the 24 adapt episodes (no thrash;
  4 correct-direction flips predicted). (b) No episode
  flips more than twice (no oscillation under
  nonstationarity). (c) At L = 0: zero episodes with
  cm = 2 or sel = 1 (eager structurally impossible).
  (d) Structural accounting on every adapt line:
  D = Dpre+Dpost, Q = Qpre+Qpost, answered = Q, kb = 2Q,
  rebuilds = od+rs, refusals = od; (pflips = 0) iff
  (tf1 = 0) iff (fdir = 0); pflips > 0 implies
  128 < tf1 <= 256; flips >= pflips; episodes with
  flips = 0 and cm in {0,1}: od/rf field-equal to the
  lazy twin and rs = 0; episodes with flips = 0 and
  cm = 2: rs = 1+(D-Dc) and od <= min(Dc,Qc).
  (e) Regime response: >= 1 adapt episode on R1 with
  fdir = +1 (lazy->eager post-shift flip) AND >= 1 on R2
  with fdir = -1 (eager->lazy post-shift flip) -- the
  flip rule demonstrably detects and adapts to the shift
  in both directions. (f) R3 (rate change, constant
  price): pflips = 0 on all 4 adapt episodes -- no
  spurious flips when only rates change.
- **K7 (regime economics).** J = rb + rf*L per line.
  (a) R1 (lazy-world -> eager-world): adapt J <= lazy J + 1
  for all L in {0,1,3,7} (the +1 is the honest sync-restamp
  overhead; holds robustly because post-shift every drift
  causes exactly one refused query under lazy, so a
  correct flip can never cost more than lazy+1).
  (b) R2 (eager-world -> lazy-world), L in {0,7}
  (non-flipping): adapt J <= eager J + 1.
  (c) R2 adapt episodes with fdir = -1: J_adapt < J_eager
  strictly (a correct-direction flip must pay off vs
  staying eager).
- **K8 (hygiene / governance).** ASCII-only lane sources; no
  world literals (901/902) in rc_spec.zag, rc_main.zag;
  exactly one `fn main` in the assembled binary; reused
  sources byte-unmodified (`git diff --quiet` on da_base.zag,
  da_module.zag, da_learn.zag, rb_world.zag, rb_fix.zag,
  et_world.zag, et_spec.zag, rr_spec.zag, and
  ../spec_lazy_default/ld_spec.zag); da_learn.zag in
  particular NOT modified (separate lane only); commits
  local with explicit pathspecs, never pushed.

## What would falsify the lane

- Dpre != 128 on R1 (or Qpost != 128): the shift is not
  wired at tick 128, or the deterministic stream broke
  (K4).
- e = 192 EWMA error > 0.5 vs the post-shift rate (K5b):
  the estimator does not track the new regime (stuck at
  the old one, or diverged).
- Zero correct-direction post-shift flips on R1 or R2
  (K6e): the flip rule does not handle regime change --
  either it never committed pre-shift (abstention trap)
  or the opposite-decisive rule cannot fire post-shift.
- Post-shift flips on R3 (K6f): the flip rule fires on
  mere rate changes -- the decisiveness hysteresis is not
  price-selective.
- flips > 12 total or any episode flipping 3+ times
  (K6a/b): the switch thrashes or oscillates under
  nonstationarity.
- R1 adapt J > lazy J + 1 (K7a): a flip actively harms
  vs the naive baseline -- the margin test misfires
  under regime change.
