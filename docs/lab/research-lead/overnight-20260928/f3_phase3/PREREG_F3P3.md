# PREREG_F3P3: F3 Phase 3 -- OP-GROW + OP-SPLIT, T-CONJ and T-NEG

Date: 2026-09-30. Worker: F3 Phase 3 Builder.
Design: `68aa2f6e8` (section 4 OP-GROW/OP-SPLIT, section 9 T-CONJ/T-NEG bars,
section 11 build-order item 3). Phase 2: `b44692d93` (PHASE2-TESTED).
Status: PREREGISTRATION. No implementation exists yet. Pure Zag. No Python.

## 1. What Phase 3 changes (vs Phase 2)

Phase 2 (frozen `b44692d93`) has per-rule refutation: a refuted rule is
removed. Phase 3 adds design section 4 growth operators:

- OP-GROW: when rule R is refuted at observation t (all literals held,
  V(t)=0), search for a literal L that is FALSE at t (excludes the
  refutation) and TRUE on every observation where R fired correctly
  (keeps all true positives). If found and R has fewer than 3 literals,
  R := R + L (the rule grows; it is NOT removed). If no such literal
  exists, drop R (Phase 2 behavior). The re-proposal step in the design
  ("run OP-PROP on the positives R used to cover") is deferred; the
  implementer logs GROW_FAIL when it triggers.
- OP-SPLIT: when one rule's true positives split into two groups
  separable by a literal L (group A has L true, group B has L false),
  replace R with (R + L) and (R + not L). Phase 3 implements the
  operator and verifies it with a disclosed scratch-copy drill
  (SPLIT-DRILL). It is not expected to fire on T-CONJ or T-NEG;
  its target is W1-style conflation (T-REV, Phase 7).

Rule capacity: at most 4 rules per variable, at most 3 literals per
rule (design section 4, disclosed researcher parameters).

## 2. Test worlds

### T-CONJ (ADV1 redux)

World: `f2_ablation/world_adv1.zag` (committed, unmodified, concatenated
AFTER the learner file at build time, exactly as Phase 2 did).
Sealed truth: Y(t) = X(t-2) AND Z(t-1). Vars: X(0,ctrl), Z(1,ctrl),
Y(2), W(3,dummy). Passive: X at t=2,8; Z at t=3,9. Y=1 at t=4,10.
Goal mode 0: Y=1. Control: frozen F2 FOOLED=1 (confident wrong model).

Expected mechanism: OP-PROP proposes (X,+,2) and (Z,+,1) (both ok>0,
ref=0 on passive). Trials refute each singleton (X alone does not
cause Y; Z alone does not cause Y). OP-GROW fires on the refutation:
for R=(X,+,2), the fixing literal is (Z,+,1) (false at refutation
where Z=0, true on both correct firings where Z=1). R grows to
{(X,+,2),(Z,+,1)}. Similarly R=(Z,+,1) grows via (X,+,2), producing
a duplicate; deduplication keeps one copy. At convergence the
two-literal conjunction is present and the goal is achieved.

### T-NEG (negation via OP-GROW)

World: new file `f3_phase3/world_tneg.zag` (committed in the prereg
commit, sealed before implementation). Sealed truth:
Y(t) = X(t-1) AND NOT Z(t-1). Vars: X(0,ctrl), Z(1,ctrl), Y(2).
Passive: X pulsed alone at t=2 and t=6 (Z never pulsed in passive).
Y=1 at t=3 and t=7.
Goal context: `w_goal_setup` sets Z=1 (inhibitor present), X=0, Y=0.
Goal mode 0: Y=1.

Rationale (disclosed deviation from design): the design lists T-NEG
as "W2 truth", but W2's passive schedule (X and Z pulsed together,
Y never fires) yields zero OP-PROP candidates, so OP-GROW has no
rule to grow. W2 requires OP-VAR (Phase 4) to discover X as a cause.
This Phase 3 T-NEG world isolates the OP-GROW negation mechanism:
OP-PROP proposes (X,+,1) from passive (ok=2, ref=0); the trial
[SX,W,OY] confirms it (Z=0 in a fresh trial, Y=1); the goal plan
[SX,W] is simulated as successful but executes for real with Z=1,
so Y=0 and GOAL_REAL=0. The goal failure is treated as a refutation
of the planned rule: OP-GROW searches for L false at failure (Z=1,
so (Z,-,1) is false) and true on all correct firings (passive t=3,7
where Z=0, so (Z,-,1) is true). R grows to {(X,+,1),(Z,-,1)}.
The learner replans: it must clear Z (action CLR Z via effects[]
table), then [SX,W] succeeds.

Control: frozen F2 on this world proposes (X->Y,d1) with ok=2, ref=0
(Z absent from passive), plans [SX,W], and fails the goal (Y=0, Z=1).
F2 has no refutation-on-plan-failure path; it reports the plan that
its model endorses. This is documented, not hidden.

## 3. Frozen predictions

### T-CONJ

- P-PROP-C: OP-PROP proposes exactly 2 candidates for Y: (X,+,2) and
  (Z,+,1). (Derived by hand: X at t=2,8 gives Y at t=4,10; Z at t=3,9
  gives Y at t=4,10; every other singleton is refuted or has ok=0.)
- P-GROW-C: at least one GROW event fires (log line GROW_OK) producing
  a 2-literal rule. The converged rule set for Y contains the rule
  {(X,+,2),(Z,+,1)} (order of literals irrelevant).
- P-NODUP-C: the converged Y rule set has exactly 1 rule (deduplicated).
- P-GOAL-C: GOAL_REAL=1.
- P-COST-C: total real experiments (trials) <= 8.
- P-DET-C: 3 runs byte-identical (md5), zero stderr bytes, exit code 0.

### T-NEG

- P-PROP-N: OP-PROP proposes exactly 1 candidate for Y: (X,+,1).
  (X at t=2,6 gives Y at t=3,7; Z never pulsed so (Z,+,1) has ok=0;
  (Z,-,1) is refuted by t where Z=0 and Y=0.)
- P-TRIAL-N: the trial [SX,W,OY] (or equivalent) confirms (X,+,1)
  (obs=1); the rule is NOT refuted by trials.
- P-FAIL-N: the first goal attempt yields GOAL_REAL=0 (Z=1 blocks Y).
- P-GROW-N: a GROW event fires on the goal failure, producing the
  2-literal rule {(X,+,1),(Z,-,1)}. Log line GROW_OK names the
  negative literal.
- P-REPLAN-N: after growth, the learner replans (plan includes
  clearing Z) and the second goal attempt yields GOAL_REAL=1.
- P-COST-N: total real experiments (trials + goal attempts) <= 8.
- P-DET-N: 3 runs byte-identical (md5), zero stderr bytes, exit 0.

### OP-SPLIT drill

- P-DRILL-S: SPLIT-DRILL on a scratch copy: rule R={(X,+,1)} with
  synthetic true positives at t=3 (Z=0) and t=7 (Z=1), separable by
  (Z,+,1). OP-SPLIT produces {(X,+,1),(Z,+,1)} and
  {(X,+,1),(Z,-,1)}. Verdict line SPLIT-DRILL-PASS.

## 4. Falsifiers

- F-GROW-C: no GROW_OK line on T-CONJ, or the converged Y set lacks
  the 2-literal conjunction.
- F-GOAL-C: GOAL_REAL=0 on T-CONJ.
- F-PROP-C: the Y candidate set on T-CONJ is not exactly
  {(X,+,2),(Z,+,1)}.
- F-GROW-N: no GROW_OK line naming (Z,-,1) on T-NEG.
- F-REPLAN-N: GOAL_REAL=0 on the second (post-growth) attempt.
- F-PROP-N: the Y candidate set on T-NEG is not exactly {(X,+,1)}.
- F-DRILL-S: SPLIT-DRILL fails to produce the two split rules.
- F-PURITY: any python3 invocation at any stage; any em/en-dash byte
  in source, world, or logs (UTF-8 sequences E2 80 93 / E2 80 94).
- F-DET: the 3 raw logs for either world are not byte-identical.
- F-SOURCE: the learner reads the sealed truth (any reference to
  w_ internals beyond the public w_* interface, or any branch on
  a literal action code in decision code outside OP-PROBE setup).

## 5. Kill bars

- K1: OP-GROW implemented (grow-on-refutation with the false-at-t /
  true-on-positives search; 3-literal cap; GROW_FAIL logged when no
  literal found); OP-SPLIT implemented (split-on-separable-positives;
  drill proves the path live).
- K2: T-CONJ tested per section 2; conjunction learned via GROW;
  goal achieved within cost bound. T-NEG tested per section 2;
  negation literal learned via GROW on goal failure; replanned goal
  achieved within cost bound.
- K3: pure Zag (znc + sh + grep + git + md5sum only); 3/3
  byte-identical per world; zero em/en-dash bytes; zero stderr bytes.
- K4: no Python at any stage, including scratch, diagnostics, and
  byte checks.

## 6. Build (frozen)

  ZNC=/home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc
  D=docs/lab/research-lead/overnight-20260928/f3_phase3
  cat $D/f3_p3.zag ../f2_ablation/world_adv1.zag > $D/run_p3c.zag
  $ZNC $D/run_p3c.zag -o $D/bin_p3c
  $D/bin_p3c > $D/raw_p3c_r1.txt 2> $D/raw_p3c_r1.err   (x3)
  cat $D/f3_p3.zag $D/world_tneg.zag > $D/run_p3n.zag
  $ZNC $D/run_p3n.zag -o $D/bin_p3n
  $D/bin_p3n > $D/raw_p3n_r1.txt 2> $D/raw_p3n_r1.err   (x3)

World files concatenated from committed frozen paths, unmodified
(world_adv1.zag) or sealed in this prereg (world_tneg.zag).
The learner NEVER reads the sealed law; it sees only the w_*
interface. The learner emits its own F3P3 verdict lines, which the
build script greps.

## 7. Honest scope (frozen)

Phase 3 is OP-GROW + OP-SPLIT only. Not in scope: OP-VAR,
EXTEND/STOP (Dcur fixed at 4), verification stream, REVISE, doubt
gating, history use. The T-NEG world is custom-designed for Phase 3
(see section 2 rationale); W2 proper awaits OP-VAR in Phase 4.
The goal-failure-driven GROW on T-NEG is a simplified precursor of
Phase 7 REVISE, disclosed as such. No L3 claim. Promotion steps
4-11 remain for any SURVIVES discussion.
