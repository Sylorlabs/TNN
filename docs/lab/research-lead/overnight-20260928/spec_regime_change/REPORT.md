# SPEC-REGIME-CHANGE: REPORT

**Lane:** docs/lab/research-lead/overnight-20260928/spec_regime_change/
**Date:** 2026-10-03
**Status:** Non-ledger (claim minting paused). Local commits only, never pushed.
**Verdict: BUILD-PASS (8/8 frozen kill bars)**

## Summary

Implemented the first open follow-up from SPEC-NOISY-RATES: the
adaptive policy switch now runs on **nonstationary (regime-change)
worlds** where drift/query rates change mid-episode. 36 episodes
(6 regime cells x 6 arms: fixed lazy, fixed eager, adaptive at
L = 0, 1, 3, 7), one binary, pure Zag, safebin-built, 3/3
byte-identical
(sha256 5313b93abfd0b6892b8c77f5539ec6a25e3d47b15905220fd83dbb51c9d31b46).

How it works: each episode has two regimes. Ticks 0..127 use
pre-shift rates (M1, N1); at tick 128 the fire thresholds swap once
to post-shift rates (M2, N2); ticks 128..255 run the new regime.
The burst/quiet Markov states persist and the LCG sequences continue
unreseeded: the same world, new parameters, one intervention. Seeds
are frozen and reset per episode so all 6 arms see the identical
arrival sequence. The estimator, margin test, and flip rule are the
parent's, byte-identical in behavior: EWMA (alpha = 1/16) runs
through the shift with NO reset, checkpoints at e in {32..128}
pre-commit and {144..256} post-decisive-commit, flips only on
opposite-decisive intervals. New instrumentation: arrival splits
(Dpre/Qpre/Dpost/Qpost), post-shift flip tracking (pflips, tf1,
fdir, tf2), and EWMA burn-in snapshots at e = 144 and e = 192.

Answers to the task's three questions:

1. **Does the flip rule handle regime changes? Yes -- 6/6
   flippable episodes flipped in the correct direction, zero
   wrong-direction flips, zero oscillation.** On R1
   (lazy-world -> eager-world) all three flippable adapt
   episodes (L = 1, 3, 7) flipped lazy->eager; on R2
   (eager-world -> lazy-world) all three flipped eager->lazy.
   The only non-flipping episodes are structurally correct:
   L = 0 cannot be eager, and R2-L0 honestly budget-defaulted.
   On the R3 control (4x rate change, price ~0 both regimes)
   there were zero post-shift flips: the flip rule is
   price-selective, not rate-triggered. There is no explicit
   shift detector; the opposite-decisive flip rule IS the
   substrate, exactly as the parent's recommendation #2
   predicted, and continuous EWMA re-estimation drives it.
2. **How quickly does it recover? 16 ticks toward eager,
   32/48/80 ticks toward lazy (L = 1/3/7).** R1 flips all
   landed on tf1 = 144, the first post-shift checkpoint (16
   ticks, the minimum on the 16-tick re-check grid). R2 flips
   landed at tf1 = 160/176/208 for L = 1/3/7: latency grows
   with L because flipping to lazy needs the price LOWER
   bound to clear L (absolute level), while flipping to
   eager only needs the interval ordering dhi < qlo
   (phin = 0). No episode needed more than 80 ticks; none
   got stuck.
3. **Does burn-in need explicit handling? Not for the flip
   rule; yes for any absolute-rate use.** The EWMA was
   deliberately not reset at the shift. At e = 144 (one
   time constant post-shift) the mean relative error vs the
   post-shift realized rate is 2.19 (drift) / 2.56 (query):
   the estimator is only ~64% converged and absolute levels
   can be 5x off (R1 drift: dh144 = 491 vs true ~80). Flip
   decisions were nevertheless correct and timely, because
   the eager-flip needs only interval ordering and the
   lazy-flip waits for decisiveness, which naturally delays
   until convergence. By e = 192 (~4 time constants) errors
   are 0.14/0.12. Conclusion: the decision is burn-in
   immune, but any future absolute-rate (non-ratio) consumer
   of the EWMA must handle post-shift warmup explicitly --
   the parent REPORT's recommendation #1 now extends to
   regime shifts, with measured numbers.

## What was tested

Assembly: `rc_full.zag` = da_base + rb_world + et_world + da_module +
da_learn + rb_fix + et_spec + rr_spec + ld_spec (all reused
byte-unmodified, da_learn.zag explicitly untouched) + rc_spec.zag
(regime layer: threshold swap at t = 128, flip tracking, burn-in
snapshots; estimator/margin/flip logic unchanged from the parent) +
rc_main.zag (6 regime cells x 6 arms). Repro: `./rc_build.sh`.

Regime cells (frozen): R0 (4,4)->(4,4) no-shift control;
R1 (1,16)->(16,1) lazy->eager world; R2 (16,1)->(1,16)
eager->lazy world; R3 (2,2)->(8,8) rate change, price ~0 both;
R4 (2,16)->(2,16) no-shift lazy control; R5 (16,1)->(16,1)
no-shift eager control.

Sample lines (R1 adapt, Dpre = 128 exact, Qpost = 128 exact):

    CELL R=1 M=1 N=16 M2=16 N2=1 P=adapt L=1 ... tc=32 cm=1 ...
      sel=1 flips=1 pflips=1 tf1=144 fdir=1 ... Dpre=128 Qpre=7
      Dpost=10 Qpost=128 ... dh144=491 qh144=675 dh192=100 qh192=1000

    CELL R=2 M=16 N=1 M2=1 N2=16 P=adapt L=7 ... tc=32 cm=2 ...
      sel=0 flips=1 pflips=1 tf1=208 fdir=-1 ... Dpre=6 Qpre=128
      Dpost=128 Qpost=6 ... dh144=682 qh144=407 dh192=1000 qh192=63

The six flips (all single, all correct-direction, none oscillating):

- R1 L=1,3,7: committed lazy at tc=32 (plo ~ 12.1 > L on the
  realized qhi = 58), flipped lazy->eager at tf1 = 144.
- R2 L=1,3,7: committed eager at tc=32 (phin = 0), flipped
  eager->lazy at tf1 = 160/176/208.

Kill-bar adjudication: K1 prereg commits 78cddaef1 -> d609a5b06
strictly precede the implementation commit 41f485a5e (git log
order on the lane dir; no implementation file in any prereg
commit). K2 safebin, no python3/python, pinned znc sha256 verified
in-script. K3 build clean, exit 0, empty stderr, 3/3 byte-identical
stdout, 36 CELL lines. K4 fixed arms anchor (lazy: answered=Q,
kb=2Q, refusals=rebuilds<=min(D,Q); eager: rb=D, rf=0),
cross-arm (D,Q) identical, regime splits exact: R1 Dpre=128 and
Qpost=128, R2 Qpre=128 and Dpost=128 (deterministic streams pin
the shift timing), R3 pre > 2x post, R0 even split. K5a no-shift
rate errors 0.49/0.31 <= 0.6; K5b e=192 post-shift errors
0.14/0.12 <= 0.5. K6 6 total flips (<= 12), max 1 per episode,
zero L=0 eager, >= 1 correct-direction flip on R1 and R2,
zero post-shift flips on R3, full structural accounting
(splits sum, pflips/tf1/fdir consistent, tf1 in (128,256],
never-eager episodes field-equal to lazy twins). K7a R1 adapt
(18,30,52,96) <= lazy (18,36,72,144)+1 at all L; K7b R2 L=0,7
adapt (12,103) <= eager 134+1; K7c all 3 R2 flipped episodes
strictly beat eager. K8 ASCII-only, no world literals, one fn
main, reused sources `git diff --quiet` clean including
da_learn.zag. **8/8 PASS.**

## Tested findings

1. **The flip rule is the regime-change substrate, and it is
   price-selective.** 6/6 flippable episodes adapted, both
   directions, with zero false positives on the rate-only
   R3 control. The switch does not detect change-points; it
   continuously re-estimates, and the decisiveness
   requirement converts a crossed price regime into exactly
   one flip. No oscillation under nonstationarity (max 1
   flip/episode).
2. **Adaptation latency is asymmetric and interpretable.**
   Toward eager: 16 ticks regardless of L (ordering-only
   decision). Toward lazy: 32/48/80 ticks for L = 1/3/7
   (level decision; higher L needs more convergence before
   the lower price bound clears it). This asymmetry is a
   property of the margin test, not a tuning artifact.
3. **Burn-in is large, visible, and decision-irrelevant.**
   e=144 mean relative error 2.19/2.56 vs 0.14/0.12 at
   e=192. The R1 flips fired at tf1 = 144 -- the earliest
   possible checkpoint -- while dh144 = 491 was still 6x
   the true post-shift rate (80): the ordering had
   converged even though the level had not. Lesson, same
   as the parent's: calibrate the DECISION's estimand
   (here, the price ordering), not absolute rates.
4. **The switch was more adaptive than the frozen
   hand-analysis.** The prereg predicted R1-L7 and R2-L7
   would get stuck (plo ~ 5.7 < 7; budget-terminal on R1).
   Both flipped: realized pre-shift intervals were tighter
   than estimated (R1 qhi = 58, not ~152, giving
   plo ~ 12.1 > 7), and post-shift plo eventually cleared 7
   on R2 (tf1 = 208). 6 flips realized vs 4 predicted; all
   6 correct-direction. The honest-abstention trap did not
   materialize on these cells -- but the mechanism is real:
   any episode that budget-defaults pre-shift (com = 2)
   cannot flip post-shift, so a noisier pre-shift regime
   could still strand the switch. That boundary is not
   mapped by this lane.
5. **Economics: adaptation pays.** R1 adapt beats-or-ties
   lazy at every L (18=18, 30<36, 52<72, 96<144); R2 flips
   strictly beat eager (3/3); R2 non-flipping episodes tie
   or beat eager+1. The +1 sync-restamp overhead bound
   held everywhere (K7a/b).

## Honest scope limits

- One shift per episode, at the fixed tick 128, with the
  shift coinciding with the commit-budget point. Multiple
  shifts, shifts before any commit, and gradual drift (as
  opposed to a step change) are untested.
- The EWMA time constant (alpha = 1/16) and the 16-tick
  re-check grid were inherited, not tuned for
  nonstationarity; latency numbers are conditional on them.
- The abstention trap (budget-default pre-shift ->
  terminal, cannot flip) did not trigger on these cells
  but is a real mechanism: noisier pre-shift regimes could
  strand the switch, and this lane does not map that
  boundary.
- One drift type and one query family, inherited; the
  switch is per-family. L is caller-stated, not measured.
- Refusals are the deadline currency; the ~10.3us rebuild
  anchor remains inherited, not re-measured.
- Rate intervals remain local (n_eff = 31) and must not be
  used as future-rate predictors (parent finding, unchanged).

## Recommendations

1. **Do not add a regime-change detector.** The flip rule
   handled step regime changes in both directions with no
   new machinery, no new mode, and no EWMA reset. A
   dedicated detector would be a new subsystem; the
   standing question ("why can the existing general
   architecture not do this?") is answered: it can.
2. **Map the abstention trap next.** Budget-default
   (com = 2) is terminal: under noisier pre-shift regimes
   the switch could abstain and then be unable to flip when
   the regime changes. Either bound the trap (measure at
   what noise level pre-shift commits fail) or give
   budget-default a post-shift re-check -- but the latter
   changes the honest-abstention semantics and needs its
   own preregistered lane, not a patch.
3. **Any absolute-rate consumer of the EWMA must handle
   post-shift burn-in explicitly** (initialize from the
   first post-shift block or wait ~4 time constants):
   measured e=144 errors of 2.19/2.56 make this
   quantitative. The flip rule itself needs no handling.
4. **The latency asymmetry (ordering vs level) is worth
   keeping in mind for future decision rules:** eager
   commits/flips are cheap to justify (ordering), lazy
   ones are expensive (level must clear L). Any redesign
   of the margin test should preserve this.

## Process notes

- Pure Zag throughout; safebin mandatory (`which python3` /
  `which python` empty, recorded in NAMECHECK.md Step 0);
  pinned znc znc_linux_x86_64_abed8aa1 (sha256-verified in
  rc_build.sh); no Python invoked at any point. Output
  analysis via grep/cmp/awk/shell only.
- Git: `/usr/bin/git` directly; explicit pathspecs; commits
  local, never pushed. Commit order on the lane dir:
  78cddaef1 (PREREG) -> d609a5b06 (NAMECHECK) ->
  41f485a5e (implementation). No amendments; no
  post-implementation bar changes.
- `da_learn.zag` not modified (separate lane only, per task).
- Two frozen predictions were wrong in the optimistic
  direction (R1-L7/R2-L7 flipped rather than stuck; 6 flips
  vs 4 predicted); reported as findings, bars unaffected.
- Repro: `./rc_build.sh` assembles the binary, builds with
  the pinned znc, runs 3x (byte-identity + all kill bars).
  All sources and logs are in this lane directory.
