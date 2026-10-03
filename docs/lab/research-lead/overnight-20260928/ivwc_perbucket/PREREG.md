# PREREG.md -- IVWC-PERBUCKET: per-bucket bars and bar margin for the hybrid

Frozen: 2026-10-03. This document fixes the experimental design
and the kill bars K1..K11. It must be committed ALONE (with
NAMECHECK.md, no implementation) before any implementation work.
The prereg commit must strictly precede the implementation
commit. Amending a bar after results invalidates the verdict.

## 1. What this wave is

IVWC-HYBRID (BUILD-FAIL K5/K6/K7) falsified "best of both" for
the bias-corrected hybrid C = P - bias_bkt with a single global
bar (PASS iff C >= T_hyb, T_hyb = mean sealed C): it repairs one
pure-approach error per regime but introduces one boundary error
per regime on exact bar-boundary ties -- s=10@wp15 (adj=21 ==
thyb=21, true FAIL) and s=5@wp45 (adj=17 == thyb=17, true FAIL) --
landing 9/12 on both key regimes: = X3 below OF in-distribution,
between the two under law change. The hybrid's own report
suggests the follow-up this wave runs: per-bucket bars or a bar
margin.

Question: does a hybrid with per-bucket bars (different
verification bars per bias bucket) or a bar margin (the score
must clear the bar, not merely touch it) achieve strict
dominance -- beat oracle-free in-distribution AND beat expand3
under law change? A negative result is a valid outcome, provided
the mechanism is shown.

### The two variants (frozen)

Both variants keep the hybrid's trained machinery verbatim:
train phase (24 cases, wp=15), per-bucket bias means bias_b =
mean(P_tr - E_tr), adjusted score C = P - bias_bkt, and the
learner-computed global bar T_hyb = mean sealed C. Only the
verdict rule changes. No researcher-set constant enters either
verdict path; every bar is learner-computed from sealed
predictions plus learned biases (no world data).

- Variant MG (bar margin): PASS iff C > T_hyb (strict
  inequality). Theory motivation, fixed before any run: with
  integer discretization, an exact tie between a bias-corrected
  point estimate and a transductive batch-mean bar is a
  discretization artifact; a verification bar should require the
  score to clear the bar, not merely touch it. This is the
  minimal margin (effectively +1 in integer arithmetic). Any
  larger fixed margin would be a researcher-set constant fitted
  to the published boundary values -- governance forbids it --
  so the strict form is the only honest margin under test.
- Variant PB (per-bucket bars): PASS iff C >= T_b, where T_b =
  mean sealed C over sealed cases in bucket b (learner-computed;
  empty bucket -> global T_hyb fallback, learner-computed,
  reported if triggered). Theory motivation: the bias correction
  is per-bucket, so the bar may be per-bucket too; a global batch
  mean mixes buckets with systematically different score scales
  (learned biases 0/4/15/16), which is exactly what created the
  boundary ties.

Ablations (consequence-content, mirroring hybrid K8): the same
train-eff shuffle (rotate by 7) relearns shuffled biases; the
shuffled-bias variants MGsh (C_sh > T_shyb) and PBsh (C_sh >=
T^sh_b) are scored on the sealed cases with the same labels.
The internal-prediction component is identical under the
shuffle, so any accuracy drop isolates the consequence-training
contribution to each variant.

Incorporated by reference (verbatim copies): world generator,
belief generator, step physics, true-world stepper,
NAV+GATHER composer, `belief_execute`, `verifier_train`,
`verifier_check`, all train/sealed seeds, the wp=15/30/45 dial --
from ivwc_hybrid/src/ivwc_hybrid.zag. In-program comparison arms
on the same sealed cases with ONE shared label ge =
(eff >= T_pred), T_pred = mean sealed P: rule OF (P >= T_pred),
rule X3 (frozen trained bucket table), rule HYB (original hybrid,
C >= T_hyb, re-anchored as a finding, not a bar), rule MG, rule
PB, rule MGsh, rule PBsh.

## 2. Frozen kill bars

Notation per sealed shift: acc_mg = #{verdict_MG == ge}/12;
acc_pb, acc_mgsh, acc_pbsh likewise; acc_of, acc_x3, acc_h for
the OF/X3/original-hybrid arms; maj = majority share of ge.

- K1 (commit before signal / training-diet hygiene): PASS iff
  (a) the world-call counter is unchanged across the train
  COMMIT block, (b) unchanged across the train PREFF block,
  (c) unchanged across each shift's sealed VERDICT COMMIT block,
  AND (d) the section-5 audits confirm code ordering, the
  LEARNER section contains no world-truth tokens, and
  `world_execute(` occurs exactly 3 times in the source (1
  definition + train CONSEQ call site + sealed SCORING call
  site). The train CONSEQ observations are the declared
  consequence-training diet, not a leak: they occur strictly
  before any sealed verdict, on train cases only.
- K2 (determinism): PASS iff 3 runs byte-identical (equal
  sha256).
- K3 (replication anchor, wp=15): PASS iff in-program acc_of15
  == 10 AND acc_x315 == 9. Guards bit-identity of the shared
  sealed setup and both pure rules against the published runs.
- K4 (replication anchor, wp=45): PASS iff in-program acc_of45
  == 8 AND acc_x345 == 10. Same guard under law change.
- K5 (per-bucket best-of-both, wp=15): PASS iff acc_pb15 >=
  acc_of15 AND acc_pb15 >= acc_x315.
- K6 (per-bucket best-of-both, wp=45): PASS iff acc_pb45 >=
  acc_of45 AND acc_pb45 >= acc_x345.
- K7 (margin best-of-both, wp=15): PASS iff acc_mg15 >=
  acc_of15 AND acc_mg15 >= acc_x315.
- K8 (margin best-of-both, wp=45): PASS iff acc_mg45 >=
  acc_of45 AND acc_mg45 >= acc_x345.
- K9 (strict dominance, the task's question): PASS iff
  (acc_pb15 > acc_of15 AND acc_pb45 > acc_x345) OR
  (acc_mg15 > acc_of15 AND acc_mg45 > acc_x345). Either variant
  strictly beats the per-regime winners on their home regimes.
- K10 (consequence-content ablation, wp=15): PASS iff
  acc_pbsh15 < acc_pb15 AND acc_mgsh15 < acc_mg15 (strict).
  Shuffling the consequence mapping must strictly degrade each
  variant: the trained-bias content (not the bar change alone)
  drives the variants' verdicts.
- K11 (non-degenerate, wp=15): PASS iff acc_pb15 > maj15 AND
  acc_mg15 > maj15 (strict).

Verdict: BUILD-PASS iff K1..K11 all PASS. Any FAIL yields
BUILD-FAIL naming the failed bar(s). Interpretation is fixed
now: K5-K8 PASS + K9 FAIL = "per-bucket bars / margin rescue the
hybrid to parity with the per-regime winners but strict
dominance is falsified"; K5 or K7 FAIL = "that variant inherits
a pure approach's weakness in-distribution"; K6 or K8 FAIL =
"that variant inherits a pure approach's weakness under law
change"; K10 FAIL = "a variant's accuracy does not depend on the
consequence content". VOID conditions: any forbidden-interpreter
invocation (PROCESS-FAIL), or any amendment to this prereg after
implementation begins.

## 3. What is NOT claimed

Mechanism test of hybrid-verdict bar variants, not a
composition-novelty or L3 claim. The composer is fixed; the
claims concern whether per-bucket bars or a bar margin let the
hybrid strictly dominate the pure approaches on the two
dissociation regimes. One wall-density law-change axis; item law,
belief noise, and energy budget fixed. The sealed scoring pass is
harness ground truth used ONLY for scoring, never observed by
the learner. The consequence-training diet (24 train true
outcomes at wp=15) is declared in section 1, not hidden. The
wp=30 shift is recorded as a finding, not a bar.

## 4. Frozen predictions (from published data, not a probe)

- MG: predicted 10/12 @wp15 (= OF) and 10/12 @wp45 (= X3).
  Rationale: per the published hybrid per-case analysis, the
  only hybrid errors beyond the per-regime winners are the two
  exact ties (s=10@15, s=5@45); strict inequality flips exactly
  those two verdicts to match the true labels. Caveat, measured
  not assumed: if any correctly-verdict'd case also sits exactly
  on its bar, strict inequality would flip it too and the
  numbers move accordingly. Predicted bars: K7 PASS, K8 PASS,
  K9 FAIL (parity, no strict win).
- PB: genuinely unknown. The sealed per-bucket C means are not
  derivable from the published reports, and no probe was run
  (the hybrid's committed runs/*.txt were deliberately not read:
  they contain the per-case sealed triples and reading them
  would destroy this experiment's blindness). The hypothesis
  under test is that per-bucket bars recover the boundary cases
  without breaking correct ones.

## 5. Frozen audit commands (run at report time, shell only)

- A1 (phase ordering): in src/ivwc_perbucket.zag, the train
  COMMIT and train PREFF call sites (learner_compose /
  belief_execute, no world_execute) textually precede the train
  CONSEQ block's world_execute call site; within each sealed
  shift, the VERDICT COMMIT block (learner_compose /
  belief_execute, no world_execute) textually precedes the
  SCORING block's world_execute call site. Verified by reporting
  grep -n line numbers.
- A2: the LEARNER section (between the `// ===== LEARNER =====`
  and `// ===== MAIN =====` markers) contains zero occurrences
  of `world_buf` or `world_off`.
- A3: zero occurrences of `expected|answer|key|target` in the
  .zag (grep -c -E).
- A4: zero occurrences of `correct|reference_plan|gold` in the
  .zag (grep -c -E).
- A5: sha256 equality across runs/ivwc_perbucket-run{1,2,3}.txt.
- A6 (diet): `grep -o "world_execute(" src/ivwc_perbucket.zag |
  wc -l` == 3 (one definition, train CONSEQ call site, sealed
  SCORING call site); WC-FINAL printed == 60 (24 train + 36
  sealed).
- A7 (learner information diet): the LEARNER section contains
  zero occurrences of `world_` (grep -c).

## 6. Why the bars discriminate, and calibration note

- K3/K4 pin the experiment to the published dissociation: they
  fail if the shared setup or either pure rule drifted by even
  one case (exact equality, not a threshold). Hand-verified
  before freezing: with T_pred labels, OF's rule gives 10/12 @
  wp=15 (errors s=0,s=3) and 8/12 @ wp=45 (errors s=0,s=3,s=4,
  s=5); X3's bkt==1 rule gives 9/12 @ wp=15 (errors s=3,s=5,s=10)
  and 10/12 @ wp=45 (errors s=0,s=4) -- matching the published
  cross-wave numbers.
- K5/K6 operationalize "per-bucket best of both": they fail if
  the per-bucket variant falls below either pure approach on
  either regime.
- K7/K8 do the same for the margin variant. The predicted
  10/10 (section 4) would pass both by matching the per-regime
  winners.
- K9 is the strict form of the task's question: it fails if
  neither variant strictly beats OF in-distribution AND X3 under
  law change. Note it is deliberately weaker than hybrid's K7
  (which demanded beating both pure approaches on both regimes):
  the task asks for beating each per-regime winner on its home
  regime.
- K10 fails if a variant's accuracy does not depend on the
  consequence CONTENT (then the variant would be a bar trick,
  not a hybrid).
- K11 fails on degenerate always-PASS/always-FAIL variants.

Calibration: bar DIRECTIONS are theory-motivated and were fixed
before any implementation. NO probe of any kind was run before
this prereg (no /tmp mechanism probe, no reading of the hybrid's
committed per-case run outputs). K3/K4 are hand-verified against
published runs (section 6, first bullet); the MG prediction in
section 4 is derived from the published per-case analysis, not
from any execution of this wave's design; K5-K11 directions
follow from the hypothesis stated in section 1. The frozen
verdict is computed from the three post-prereg runs of the
committed source.
