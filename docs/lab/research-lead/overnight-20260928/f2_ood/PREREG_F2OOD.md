# PREREG: F2 Out-of-Distribution Test

Date: 2026-09-30. Worker: F2 OOD Worker.
Status: FROZEN. Committed before any implementation.

## Background

F2 (autosci2, BUILD-PASS at 1eb66765d) is an enumerate-then-select
autonomous scientist. Hypothesis family: single-cause rules
[c,e,d,cx,cv], one rule per effect variable, delay 1..4, optional single
binary context. Candidates come only from passive correlations
(cnt>=2, perfect prediction on passive). Experiments discriminate by
disagreement; the loop stops at nalive==1 or exhaustion.

Promotion steps 1-6 are done (prereg, implementation, sealed eval,
reproduction, memorization control, ablation/alternative-explanation).
This is step 7: OOD test.

Known boundaries from ablation (1f3a9511c):
- ADV1 (conjunctive truth, out of family): fooled confidently, GOAL_REAL=0.
- ADV2 (silent cause): missed entirely, PLAN none found.

## OOD world designs

All four worlds use the FROZEN learner verbatim
(md5 de95a49350f42122da5fb0a8dd445eba, from commit 1eb66765d).
Each world differs from training worlds A (confounded chain) and B
(contextual single-cause) in the FORM of the causal law, not just
parameter values. Goal mode 0 (final-state goal) for all.

### W1: hysteretic memory (temporal aggregation)

- Vars: X(0), Y(1). nctrl=1, ctrl=[X]. ctxvar=-1.
- Sealed truth: Y(t) = 1 iff X(s)=1 for some s in {t-1,t-2,t-3}.
- Passive: t=1: X=1; t=4: X=0; t=7: X=1; t=10: X=0.
- Goal: Y=1.
- Structural axis: memory/aggregation over a window. No single-lag
  positive rule is the true law, though several fit passive data.
- Hand-derived expectations (falsifiable):
  - Y candidates: (X->Y,d1), (X->Y,d2), (X->Y,d3). d4 excluded
    (X(3)=1 but Y(7)=0). NHYP=3.
  - First disagreement experiment [SX,W,OY] kills d2 and d3;
    survivor is (X->Y,d1), the SHORTEST delay (first-disagreement bias).
  - Plan [SX,W]; GOAL_REAL=1 (goal succeeds by luck).
  - Post-hoc pulse [SX,W,CX,W,OY] (harness-side, not charged):
    survivor predicts Y=0, truth gives Y=1. Survivor is FALSE.
- Prediction P-W1: survivor=(X->Y,d1), nalive==1, GOAL_REAL=1,
  post-hoc actual=1 vs predicted=0.

### W2: inhibition (negation)

- Vars: X(0), Z(1), Y(2). nctrl=2, ctrl=[X,Z]. ctxvar=-1.
- Sealed truth: Y(t) = X(t-1) AND NOT Z(t-1).
- Passive: t=2: X=1; t=3: Z=1; t=5: X=0; t=6: Z=0.
- Goal: Y=1.
- Structural axis: negation is not in F2's vocabulary. No positive
  single-cause rule can express inhibition.
- Hand-derived expectations (falsifiable):
  - Y candidates: ZERO at every delay 1..4 (X and Z overlap, so every
    positive rule is refuted by passive).
  - Spurious candidate (X->Z,d1) exists (confound, like World A's D).
  - NHYP=1, zero experiments, PLAN none found.
  - Oracle witness [SX,W] achieves Y(1)=1 on the true world.
- Prediction P-W2: candn[Y]=0, PLAN none found, witness_goal=1.
  F2 declares the goal impossible though it is achievable.

### W3: long delay (timescale outside search vocabulary)

- Vars: X(0), Y(1). nctrl=1, ctrl=[X]. ctxvar=-1.
- Sealed truth: Y(t) = X(t-5).
- Passive: t=1: X=1; t=3: X=0; t=7: X=1; t=9: X=0.
- Goal: Y=1.
- Structural axis: the cause exists but its delay (5) exceeds DMAX=4.
  Maps the enumerate boundary at the delay parameter exactly.
- Hand-derived expectations (falsifiable):
  - Y candidates: ZERO (every d<=4 refuted: X pulses never followed
    by Y within 4 steps).
  - ne=0, NHYP=1, PLAN none found.
  - Oracle witness [SX,W,W,W,W,W] achieves Y(5)=X(0)=1.
- Prediction P-W3: ne=0, nhyp=1, PLAN none found, witness_goal=1.
  F2 cannot distinguish "no cause" from "cause beyond search depth".

### W4: disjunctive causation (redundant sufficient causes)

- Vars: X(0), Z(1), Y(2). nctrl=2, ctrl=[X,Z]. ctxvar=-1.
- Sealed truth: Y(t) = X(t-1) OR Z(t-2).
- Passive: t=2: X=1; t=5: X=0; t=7: Z=1; t=9: Z=0.
- Goal: Y=1.
- Structural axis: multi-cause sufficiency. F2's hypothesis space
  assumes exactly one cause per effect; the world has two true
  sufficient causes.
- Hand-derived expectations (falsifiable):
  - Y candidates: (X->Y,d1) and (Z->Y,d2). Both are TRUE of the world.
  - First disagreement experiment [SX,W,OY] kills (Z->Y,d2),
    a TRUE rule, because the space frames hypotheses as exclusive.
  - Survivor (X->Y,d1); plan [SX,W]; GOAL_REAL=1.
- Prediction P-W4: survivor=(X->Y,d1), (Z->Y,d2) killed,
  GOAL_REAL=1. F2 converges on a partial truth and discards a true
  hypothesis with full confidence.

## Kill bars

- K1 PASS iff: all four worlds implemented exactly as specified above
  (variables, sealed laws, passive schedules, goals), each differing
  structurally (aggregation, negation, timescale, disjunction) from
  training worlds A and B.
- K2 PASS iff: for each world, measured and reported: candidates per
  variable, NHYP, survivor set, experiments run, GOAL_REAL,
  oracle-witness goal, and the prereg prediction confirmed or refuted
  with the observed value stated. A refuted prediction does not fail
  K2; hiding it does.
- K3 PASS iff: pure Zag at every stage (znc, bash, grep, git only;
  zero Python invocations), zero em-dash or en-dash bytes in wave docs
  (byte-checked), frozen learner used verbatim (md5 verified),
  3/3 byte-identical runs per world (md5s recorded), exit 0, zero
  stderr except documented harness notes.

## Verdict rule

Report OOD-TESTED with per-world findings. No SURVIVES claim is made
here; this is promotion step 7 (OOD), feeding steps 8-11.

## Falsification of this prereg

If any hand-derived expectation above is wrong (different survivor,
different candidate count, different goal outcome), the expectation is
marked REFUTED and the observed value is reported. The OOD finding
stands on the observation, not the prediction.
