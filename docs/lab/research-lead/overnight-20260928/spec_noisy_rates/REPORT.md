# SPEC-NOISY-RATES: REPORT

**Lane:** docs/lab/research-lead/overnight-20260928/spec_noisy_rates/
**Date:** 2026-10-03
**Status:** Non-ledger (claim minting paused). Local commits only, never pushed.
**Verdict: BUILD-PASS (8/8 frozen kill bars)**

## Summary

Implemented the follow-up lane SPEC-ADAPTIVE-SWITCH recommended: the
adaptive policy switch now runs on **noisy real-world-style arrivals**
with **EWMA rate estimation and a confidence-interval margin test**.
150 episodes (25 drift/query cells x 6 arms: fixed lazy, fixed eager,
adaptive at L = 0, 1, 3, 7 work units), one binary, pure Zag,
safebin-built, 3/3 byte-identical
(sha256 4c6f2b1b8e775b4f64a56abc35b0b6421a20da2e6287dd8e016b6e4f0131210a).

How it works: drift and query arrivals are exogenous per-tick events
from two independent two-state Markov-modulated Bernoulli processes
(burst/quiet, 5x rate ratio, mean rate exactly 1/M and 1/N), driven by
a seeded LCG reset per episode so all 6 arms of a cell see the
identical arrival sequence. The adapt arm tracks per-tick EWMA rate
estimates (alpha = 1/16, fixed point events/1024 ticks) plus empirical
EWMA variance, forms approx-95% intervals (n_eff = 31), and converts
them to a conservative price interval [plo, phi] by monotonicity.
At checkpoints (elapsed 32..128) it commits eager iff L > phi
(strict, the parent's strict-> on the UPPER bound), lazy iff L < plo
(strict), else keeps observing; undecided at 128 budget-defaults to
lazy. After a decisive commit, re-checks continue to tick 256 and flip
only on opposite-decisive intervals (decisiveness IS the hysteresis).
Eager commits run a sync restamp (+1 rebuild), guaranteeing zero
post-commit refusals.

Answers to the task's three questions:

1. **Does the adaptive switch still work with noisy estimates, or
   does it thrash? It works and does not thrash.** Portfolio J =
   rb + rf*L over 25 cells: adapt ties fixed lazy exactly at L = 0
   (1106 = 1106; the switch can never fire eager at L = 0) and beats
   it at L = 1, 3, 7 (1686 < 2212; 2398 < 4424; 3251 < 8848). Total
   policy flips across 100 adapt episodes: **3** (bar: <= 10) -- and
   all 3 are single eager->lazy self-corrections on boundary/noisy
   cells, never oscillation. Vs fixed eager (2501): adapt wins at
   L = 0, 1, 3 and loses at L = 7 -- the same crossover pattern as the
   deterministic parent lane.
2. **What is the estimation error?** Mean relative EWMA rate error vs
   realized per-episode rates: **0.45 (drift) / 0.44 (query)** (bar:
   <= 0.6). Mean absolute price error where the price is defined
   (qh >= 1): **1.79 rebuilds** (bar: <= 2.0). Where qh = 0 (14
   episodes, no queries observed yet) the per-avoided-refusal price is
   mathematically undefined -- the guard value is not an estimate
   (Amendment A1). Rate-interval future coverage is only **52%/50%**:
   EWMA intervals are LOCAL-rate intervals (n_eff = 31 ticks) and
   under burstiness the local rate differs from the future
   long-window rate; early checkpoints also carry burn-in bias with
   SE ~= 0 on deterministic M=1/N=1 cells. The decision-relevant
   calibration -- price-interval vs realized post-commit price --
   covers at **73%** (bar: >= 70%): the ratio partially cancels
   common-mode errors and the box bounds are conservative.
3. **When should the switch commit vs keep observing?** Commit exactly
   when the 95%-ish price interval excludes L on one side (eager iff
   the whole interval is below L, lazy iff the whole interval is above
   L); otherwise keep observing on the honest lazy path. In numbers:
   82/100 episodes commit decisively (52 eager, 30 lazy), 63 of them
   at the first checkpoint (elapsed 32); 18 ride the full budget to
   128 and default lazy -- concentrated on rare-stream cells where
   qlo ~= 0 blows up the price upper bound (abstention is the correct
   behavior: with ~0 queries observed the price is genuinely
   unbounded above). The confidence threshold is the 2-SE interval;
   the "keep observing" region is precisely the interval straddling L.

## What was tested

Assembly: `nr_full.zag` = da_base + rb_world + et_world + da_module +
da_learn + rb_fix + et_spec + rr_spec + ld_spec (all reused
byte-unmodified, da_learn.zag explicitly untouched) + nr_spec.zag
(noisy-rate policy layer) + nr_main.zag (harness). Repro:
`./nr_build.sh`.

Sample lines (M=4 N=4, realized D=50 Q=92, true price 0):

    CELL M=4 N=4 P=adapt L=0 ... tc=128 cm=0 ... sel=0 flips=0 ... rebuilds=36 refusals=36
    CELL M=4 N=4 P=adapt L=1 ... tc=32 cm=2 ... sel=1 flips=0 ... od=4 rs=47 rebuilds=51 refusals=4

At L=1 the switch commits eager at elapsed 32 on the local price
interval [0, 0] (dh=87, qh=522) and pays 51 rebuilds / 4 refusals vs
the lazy twin's 36 rebuilds / 36 refusals. At L=0 it rides to budget
and is field-equal to its lazy twin.

The three flips (all single, all eager->lazy, none oscillating):

- M=1 N=2 L=1: committed eager at tc=80, flipped lazy later. True
  price 1.21 > 1 -- the correction was right (boundary cell).
- M=1 N=4 L=3: committed eager at tc=32, flipped lazy. True price
  3.0 = L -- strict-> says lazy; the correction was right.
- M=16 N=16 L=1: committed eager at tc=32 on dh=0/qh=39, flipped
  lazy. True price 0 < 1 (eager "right" by price), but realized
  od=3 made lazy cheaper (J=6 vs ~13) -- the flip saved money anyway.

Kill-bar adjudication: K1 prereg commits 9427292d0 -> 43463abf0 ->
6f7215608 strictly precede the implementation commit (git log order
on the lane dir; no implementation file in any prereg commit). K2
safebin, no python3/python, pinned znc sha256 verified in-script. K3
build clean, exit 0, empty stderr, 3/3 byte-identical stdout, 150
CELL lines. K4 fixed arms anchor on the noisy world (lazy:
answered=Q, kb=2Q, rf=rb<=min(D,Q); eager: rb=D, rf=0, kb=2Q),
cross-arm (D,Q) identical (seeded noise), 23/25 cells differ from the
deterministic grid. K5 rate errors 0.45/0.44 <= 0.6; price error 1.79
<= 2.0 (qh>=1, n=86); price-interval coverage 0.73 >= 0.70. K6 82
decisive (>= 30), 3 flips (<= 10), zero L=0 eager commits, full
structural accounting (never-eager episodes field-equal to lazy
twins; eager commits satisfy rs = 1+(D-Dc), od <= min(Dc,Qc),
rf = od). K7 adapt = lazy exactly at L=0, strictly beats lazy at
L=1,3,7. K8 ASCII-only, no world literals, one fn main, reused
sources `git diff --quiet` clean including da_learn.zag. **8/8 PASS.**

## Tested findings

1. **The margin test is the honest executable form of the parent's
   recommendation #2.** The strict-> comparison becomes: commit eager
   iff L clears the UPPER price bound, lazy iff L is below the LOWER
   bound, else observe. The interval, not the point estimate, drives
   the decision -- and the portfolio shows it works under noise.
2. **Abstention concentrates where it should.** The 18 budget
   episodes are rare-stream cells (qlo ~= 0 -> phi explodes; dlo ~= 0
   -> plo collapses). With ~0 queries observed the price really is
   unbounded above; refusing to commit eager is correct, not timid.
   Default-lazy on abstention mirrors the parent's strict-> boundary
   behavior and is field-equal to the lazy twin (costs nothing extra).
3. **Local estimators, global decisions.** EWMA with n_eff=31 tracks
   the local rate; under 5x burstiness the local rate can be far from
   the episode mean (e.g. dh=87 vs true 256 at M=4 N=4). Rate-interval
   future coverage is 52% -- a real, reported miscalibration for
   absolute rates. But the price RATIO partially cancels common-mode
   burst effects, the box bounds are conservative, and the switch
   still wins economically. Lesson for question 3: size the
   confidence term for the DECISION's estimand (the price), not for
   absolute rates.
4. **Burn-in is the deterministic-cell trap.** At M=1/N=1 the streams
   are deterministic (rate-1 processes cannot be noisy), SE ~= 0, and
   the zero-initialized EWMA sits ~13% low at the first checkpoint --
   systematically uncovered. The decision is unaffected (bias cancels
   in the ratio), but any future absolute-rate use must initialize or
   wait out burn-in.
5. **The crossover vs fixed eager survives noise.** Adapt beats eager
   at L=1 (1686 < 2501) and L=3 (2398 < 2501), loses at L=7
   (3251 > 2501) -- quantitatively the same pattern as the
   deterministic parent (1801/2297/2869 vs 2480). The observation cost
   of adaptivity under noise does not change the crossover location.
6. **Flips are self-correction, not thrash.** 3/100 episodes flipped,
   each exactly once, each eager->lazy, two on strict-boundary cells
   where the correction was provably right. The decisiveness
   requirement as hysteresis works: no oscillation observed.

## Honest scope limits

- One drift type (unrelated, repeatable) and one query family (RET),
  inherited from the parent lane; the switch is per-family.
- Stationary bursty world: the Markov-modulated process has fixed
  parameters per cell. Regime CHANGE (parameters shifting mid-episode)
  is not tested; the alpha=1/16 EWMA would adapt, but commit/flip
  behavior under nonstationarity is an open lane.
- L is a caller-stated policy input in work units, not itself
  measured (same caveat as the parent).
- The 95% intervals are Wald-style (2-SE, empirical variance); no
  exact small-sample calibration is claimed. Price-interval coverage
  is 73%, not 95%.
- Rate intervals are local (n_eff=31); they must not be used as
  future-rate predictors (52% coverage). Only the price interval is
  decision-calibrated.
- Refusals, not wall-clock latency, are the deadline currency; the
  ~10.3 us rebuild anchor is inherited from SPEC-ADAPTIVE-SWITCH, not
  re-measured here.

## Recommendations

1. Any future lane that consumes EWMA rate estimates for absolute
   (non-ratio) purposes must handle burn-in explicitly (initialize
   from the first block or delay the first checkpoint); the decision
   here was immune only because the bias cancels in the price ratio.
2. If the switch is ever extended to nonstationary worlds, the
   commit-vs-observe rule should gain a regime-change detector; the
   current flip rule (opposite-decisive intervals) is the natural
   substrate, and the 3 observed flips suggest it self-corrects rather
   than oscillates.
3. The price-interval construction (monotone box bounds on
   max(0,d-q)/q) is reusable wherever a ratio decision needs a
   confidence margin; the qlo~=0 blowup is a feature (honest
   abstention), not a bug to be smoothed away.
4. Do not "fix" the 52% rate-interval coverage by widening intervals
   ad hoc -- it would destroy decisiveness (K6a). The right response
   is the one taken here: calibrate the DECISION's estimand.

## Process notes

- Pure Zag throughout; safebin mandatory (`which python3`/`which python`
  empty, recorded in NAMECHECK.md Step 0); pinned znc
  znc_linux_x86_64_abed8aa1 (sha256-verified in nr_build.sh); no Python
  invoked at any point. Output analysis via grep/cmp/awk/shell only.
- Git: `/usr/bin/git` directly; explicit pathspecs; commits local,
  never pushed. One index.lock contention hit on the amendment commit;
  retried with backoff per the shared-workspace discipline (lock left
  untouched).
- Two tooling iterations, neither touching frozen bars: (1) K6a
  55->30 by transparent pre-implementation amendment after
  hand-analysis showed rare-stream cells honestly abstain (Amendment
  A1 covers a second pre-implementation correction: K5 price-error
  restricted to qh>=1 where the price is defined, price-interval
  coverage replacing rate-interval future coverage as the
  decision-relevant bar); (2) the K6d `od=` field extractor matched
  inside `plod=` -- fixed with a leading-space anchor in the bash
  helpers (the binary output was always correct; only the checker was
  wrong).
- No amendments after implementation began. The implementation commit
  follows the three prereg commits in git log order (K1).
- `da_learn.zag` not modified (separate lane only, per task).
- Repro: `./nr_build.sh` assembles the binary, builds with the pinned
  znc, runs 3x (byte-identity + all kill bars). All sources and logs
  are in this lane directory.
