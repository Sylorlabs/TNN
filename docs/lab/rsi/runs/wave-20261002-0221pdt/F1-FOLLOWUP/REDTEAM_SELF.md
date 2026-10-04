# REDTEAM_SELF.md - F1-FOLLOWUP wave-20261002-0221pdt

Self red-team of the sealed measurement, written after the results.
Each attack states the strongest case against the finding and the
evidence that answers it. Nothing here moves a frozen bar.

## Attack 1: is the sensitivity a constructor property or a harness artifact?

Strongest case: the measured variance could come from the harness
(fixture generator quirks, scorer bugs, nondeterminism, or the
analyzer's normalization) rather than the F1 constructor.

Answer:
- The binary is the frozen F1 binary, sha256-verified before every
  run phase (6f2b155b...be8882847). Nothing about the constructor
  changed; the lane is read-only toward the F1 lane.
- NC-HARNESS reproduces the prior Part 2 phenomenon exactly: 6/6
  regenerated fixtures byte-identical, hidden accs 5/30, 0/30, 2/30
  on the known overfits and 30/30 on the known corrects, hidden
  preds byte-identical to the prior lane's runs2/1. If the harness
  manufactured variance, it could not reproduce 6/6 known outcomes
  byte-identically.
- K-DET: 40 seeds x 3 repetitions, all byte-identical. There is zero
  run-to-run noise, so 100 percent of the measured variance is
  seed-driven, not stochastic.
- The trigger fires at episode 1 (34/40) or 2 (6/40) on every seed,
  so the trigger is not the variable under test; the constructor's
  greedy trial choices are.
- The 3 overfit seeds fail with the exact greedy-compounding
  mechanism documented in prior Part 2 (second construct re-adds
  the same feature or doubles the accumulator), visible in the raw
  traces, independent of any normalization.
- The analyzer's normalization is literal (op, operand classes,
  err transitions from the trace); the dry run verified its parsing
  by hand against grep counts and raw trace lines.

Verdict on Attack 1: the sensitivity is a constructor property.
The harness measures it faithfully.

## Attack 2: was K-SENS-CONV (D >= 3 AND Cmax <= 34) a well-calibrated bar?

Strongest case: the frozen normalized sequence keeps err_before /
err_after, which vary with the fixture's x-values even when the
constructor builds identical op/operand structures. D = 37 / Cmax = 2
could pass on error-magnitude noise alone, making the bar vacuous.

Answer: the attack lands. Evidence:
- Seeds 1, 2, 3 build literally identical op/operand sequences
  (ADD r0,9,9; ADD r0,r0,8; ADD r0,r0,8) yet occupy three different
  sequence groups, differing only in err transitions (14->2 vs
  20->6 vs 18->2 on the first event).
- The post-hoc op/operand-only diagnostic (dev/f1f_diag, pure Zag,
  NOT the frozen metric) gives D_ops = 10, Cmax_ops = 21: the two
  canonical correct patterns cover 31/40 seeds, and the 3 overfit
  seeds are each structural singletons.
- So the frozen D/Cmax bar as designed was too easy: it would pass
  on nearly any 40-seed run via eb/ea fragmentation, and it does not
  discriminate structural convergence diversity.

Owned calibration weakness. It does not change the verdict
(K-SENS-RATE governs: 3 < 4 regardless), but the K-SENS-CONV PASS
must not be cited as strong evidence of structural convergence
diversity. The honest structural statement is the diagnostic one:
convergence is concentrated on 2 canonical patterns (31/40), with
the 3 overfits structurally distinct singletons. A future prereg
should normalize err transitions out of the convergence metric or
use op/operand-only grouping as the frozen form.

## Attack 3: does the seed set cover the relevant regime?

Strongest case: 40 sum2 seeds from one generator series might miss
the regime where seed-sensitivity matters, or the series could be
contaminated by prior use.

Answer:
- The 53xx series is verified unused by every prior wave (dev
  9xxx, F1 sealed 11xx-31xx, Part 2 51xx). No post-hoc selection:
  all 40 seeds are in every denominator.
- The relevant regime is sum2 worlds where the trigger fires early
  and the greedy trial has a live choice. First trigger is ep 1 on
  34/40 and ep 2 on 6/40: full coverage.
- Fixture sanity: 13-19 distinct (x0,x1,y) lines per train set;
  no degenerate fixtures.
- Scope limit (stated in the prereg): sum2 only. The finding does
  not establish cross-family seed-sensitivity. The family was held
  constant deliberately to isolate the constructor.

## Attack 4: is R = 3 vs the R >= 4 bar a meaningful distinction or noise?

Strongest case: 3/40 vs 4/40 is one seed; calling this BUILD-FAIL
while prior Part 2 measured 6/24 looks like bar luck, and the
"true" rate might be above 10 percent.

Answer:
- The bar was frozen before seeing data at 10 percent as the floor
  for a finding-worthy behavioral sensitivity. 3 < 4 is a trip,
  full stop. Governance forbids weakening a frozen bar to force a
  pass, and a near-miss is still a miss.
- The pooled sealed evidence is 9/64 = 14.1 percent (6/24 prior +
  3/40 here). The rate is seed-set-dependent; neither 25 percent
  nor 7.5 percent should be reified as the constructor's rate.
  Reporting both numbers with the pooled figure is the honest
  summary.
- The qualitative finding (seed-dependent trial choices, T = 2;
  seed-dependent overfit outcomes via the documented mechanism)
  stands as evidence even though the behavioral magnitude missed
  the frozen floor. BUILD-FAIL on the claim as framed; the evidence
  itself is reported, not buried.

## Attack 5: seal integrity (ordering, peeking, contamination)

- Commit order: prereg d7164c12b (PREREG + NAMECHECK alone) strictly
  precedes methodology 742081f93, which precedes fixtures a920ba752,
  which precedes the sealed runs and this eval. Verified from git log.
- The seed series, metrics, normalization, and bars were frozen in
  the prereg before any 53xx fixture existed.
- The methodology dry run used only prior-wave data in /tmp (never
  committed, never part of the sealed battery).
- The one methodology bug found in the dry run (cell allocation
  byte-vs-cell count) was fixed before any sealed use and is
  recorded in METHODOLOGY.md.
- No Python anywhere; safebin only; `which python3` prints nothing;
  zero forbidden-executable invocations.
- No em/en dashes in loop docs (dash-scanned).

## Attack 6: governance blemish in the methodology commit

The methodology commit 742081f93 inadvertently included staged
ARENA-lane files from another worker (27 files in the commit, of
which the ARENA files are not this lane's). Cause: another worker's
staged files were swept into the commit. The ARENA working copies
are intact and match HEAD, so no content was lost or altered; the
commit message describes only this lane's methodology. Subsequent
commits used the pathspec-limited form
(`git commit -m ... -- <lane dir>`) and are lane-only (fixture
commit a920ba752 verified lane-only). The lane's scientific
ordering (prereg -> methodology -> fixtures -> runs) is intact.
Disclosed here and in the lane report; flagged for the coordinator.

## Bottom line

The measurement is sound, the verdict follows the frozen rule, and
the two material caveats are owned above: (a) K-SENS-CONV as designed
was too easy and its PASS is weak evidence (the op-only diagnostic
gives the honest structural picture); (b) the methodology commit
swept in another lane's staged files (no scientific impact,
disclosed). The BUILD-FAIL verdict on the SENSITIVE claim stands on
K-SENS-RATE alone and is not affected by either caveat.

No em-dashes in this document.
