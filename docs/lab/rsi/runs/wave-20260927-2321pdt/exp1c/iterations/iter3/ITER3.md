# EXP1c Retune Iteration 3

Wave: wave-20260927-2321pdt
Date: 2026-09-27 (PDT)
Status: calibration complete, C1 PASS, C2 PASS, C3 PASS

## Frozen references

- Frozen prereg: commit 8b456736b,
  docs/lab/rsi/runs/wave-20260927-1121pdt/preregs/PREREG_EXP1C_FROZEN.md
- Redrafted section 7: commit d9e96ad913052921d712a843440f8948334191b6
  (correct minimum enumeration cost 1134 primitive-action ticks; claims of
  completion before tick 600 and at least 600 choice ticks withdrawn; runs
  must report enum_done, enum_tick, n_distinct, replans; no post-enumeration
  plans means K7 fails and the run is VOID)
- Frozen world: docs/lab/invention/survival/src/world.zag,
  git blob fff8af2493bc6dbe9de6fc76f9a6206d887d586a (verified)
- Pinned compiler: src/tools/toolchain/znc_linux_x86_64_abed8aa1,
  SHA-256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
  (verified)

## Commit order (frozen)

1. This file plus the iteration-3 variants and calibration medians.
2. The full experiment and the deterministic rerun.
3. The Zag-generated evidence note.
4. Optional: one additional retune family only if iteration 3 fails C3.

This commit is milestone 1. No run output commits exist yet.

## Family design: dispersed-mote

Iteration 3 keeps the stationary-mote family constraints from iteration 2
(velocity zero, lo < hi, range width at most two) and adds one more:
start, home, crystals, and all six motes lie on the same side of the void
pair, so the H9 void-step refusal cannot trap any scripted strategy.
Twelve variants, void pairs (10,11), (4,5), (16,17). Variant 8 had a mote
on its start cell 18 at first draft; the emitter showed it, and it was
moved to 19 before calibration. Variant parameters are in
iterations/iter3/variants3.txt, produced by x1c_emit.zag.

## Mode check

x1c_check.zag runs xp_check_all on all 12 variants. Result: ALL_PASS=1,
exit code 0. Calibration and the full runner are gated on this check;
either prints CALIB_BLOCKED / RUN_BLOCKED and exits nonzero on failure.

## Calibrators

Three scripted strategies, no learning, each run 1200 ticks per variant:

- f0 pure forage: eat a mote on the cell, else step toward the nearest
  mote, else wait. Storm-blind and dormancy-blind by design.
- f1 stormflee: flee an active storm when in the zone and unsheltered
  (the world's own w_reflex_storm), else forage exactly like f0.
- f2 patrol: open-loop oscillation on [home-2, home+2], no target seeking.
  Eats only ACTIVE motes on its cell, storms send it home to wait, energy
  below 25 runs the taught survival reflex. Genuinely different decision
  rule, not a parameter tweak.

## Corrected C3 check (binding fix)

The 1721pdt false claim and the 2021pdt red-team finding are corrected
here: the "qualitatively distinct" qualifier is checked IN ZAG by comparing
complete per-variant (ticks, e_end) outcome vectors, not medians. Two
strategies count as distinct iff their (ticks, e_end) pairs differ in at
least one variant. C3 passes iff all three calibrator medians are at
least 720 AND all three strategy pairs are vector-distinct. A parameter
variant with identical outcomes is not a distinct strategy; if no third
distinct passing strategy existed, this file would record C3 NOT-MET.

## Calibration results (byte-identical across two runs)

SHA-256 f0b1d41b254dd441aa53ecd5d73f80b9c79c9f4aa13ea058239dc82ea9bccb57
for both calib1.txt and calib2.txt.

Medians (ticks survived, 12 variants):

- f0: 1200 (all 12 variants survived the full 1200 ticks)
- f1: 1200 (all 12 variants survived the full 1200 ticks)
- f2: 1200 (all 12 variants survived the full 1200 ticks)
- P-probe (taught ward strategy): 1200
- Z-probe (fixed-seed LCG): 50

Per-variant outcome vectors (ticks, end energy), f0 / f1 / f2:

- v0: (1200,145) (1200,184) (1200,197)
- v1: (1200,162) (1200,195) (1200,192)
- v2: (1200,181) (1200,181) (1200,178)
- v3: (1200,161) (1200,170) (1200,173)
- v4: (1200,140) (1200,187) (1200,183)
- v5: (1200,181) (1200,181) (1200,199)
- v6: (1200,141) (1200,193) (1200,187)
- v7: (1200,160) (1200,150) (1200,178)
- v8: (1200,182) (1200,182) (1200,180)
- v9: (1200,181) (1200,181) (1200,194)
- v10: (1200,181) (1200,195) (1200,170)
- v11: (1200,181) (1200,181) (1200,199)

Vector diffs (variants where (ticks, e_end) differ):

- d01 (f0 vs f1): 7
- d02 (f0 vs f2): 12
- d12 (f1 vs f2): 12

C3 verdict: PASS. All three medians are 1200 (>= 720) and every pair is
vector-distinct.

Probes: C1 probe P median 1200 (>= 960, PASS). C2 probe Z median 50
(< 300, PASS).

## P-probe variance (honest note)

The P probe survived all 1200 ticks in 10 variants but died in v7
(605 ticks, energy 0) and v9 (967 ticks, energy 0). Both deaths happened
during a storm while sheltering at home: with energy below 25 the taught
Phase 4b survival reflex fires at home (Phase 4a only applies when not on
home) and walks toward the nearest mote, leaving the shelter during the
storm. This is the taught text implemented as written, not a bug in the
implementation. Median is still 1200, so C1 passes, but the variance is
real and is reported here rather than smoothed over.

## M5 discard/stop reason

Proceed to the full experiment. Reason cites only C1, C2, C3: C1 PASS
(P-probe median 1200 >= 960), C2 PASS (Z-probe median 50 < 300), C3 PASS
(three vector-distinct strategies, each median 1200 >= 720). No retune
iteration is consumed beyond this one; the wave keeps its one optional
additional family in reserve.
