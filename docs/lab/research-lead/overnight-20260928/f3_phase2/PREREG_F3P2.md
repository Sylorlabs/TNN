# PREREG_F3P2: F3 Phase 2 -- OP-PROP + Per-Rule Refutation, T-DISJ

Date: 2026-09-30. Worker: F3 Phase 2 Builder.
Design: `68aa2f6e8` (section 2 refutation semantics, section 9 T-DISJ bar,
section 11 build-order item 2). Phase 1: `720bb095e` (PHASE1-TESTED).
Status: PREREGISTRATION. No implementation exists yet. Pure Zag. No Python.

## 1. What Phase 2 changes (vs Phase 1)

Phase 1 (frozen `720bb095e`) enumerates Cartesian-product hypotheses with
k=1 rule per effect variable and kills whole hypotheses on disagreement.
Phase 2 replaces this with design section 2 semantics:

- H_V is ONE rule set per effect variable, initialized with ALL OP-PROP
  candidates as separate singleton rules (up to the disclosed cap of 4).
- A RULE R is refuted only by a false-positive observation: all literals
  of R hold at observation time t and V(t)=0. Refuted rules are removed
  from H_V; the set survives while any rule covers the data.
- A hypothesis (rule set) is eliminated only when a refutation leaves it
  with no rule covering a positive observation AND OP-PROP cannot cover
  it. Elimination is per-rule, never per-hypothesis while any rule
  survives.

## 2. Test world: T-DISJ (W4 disjunction)

World: `f2_ood/world_ood4.zag` (committed in `9cef7f9d4`, unmodified,
concatenated AFTER the learner file at build time, exactly as Phase 1
did with the autosci2 worlds).
Sealed truth: Y(t) = X(t-1) OR Z(t-2). Two true sufficient causes.
Control: frozen F2 kills the true rule (Z->Y,d2) on this world
(OOD-TESTED W4). w_goal_mode()=0.

## 3. Frozen predictions

- P-PROP: OP-PROP proposes exactly 2 candidates for Y: (X,+,1) and
  (Z,+,2). No candidates for X or Z. (Derived by hand from the passive
  schedule: X pulsed at t=2,5; Z pulsed at t=6,9; every other singleton
  literal is refuted by the 12-step passive trace.)
- P-INIT: the initial rule set for Y has nrules=2.
- P-CONV: at convergence nrules_Y=2 with both true rules present.
- P-REFUTE-NONE: zero RULE_REFUTED log lines naming a true rule
  ((X,+,1) or (Z,+,2)) on the real rule set. F-DISJ does not fire.
- P-DRILL: a disclosed mechanism self-test on a SCRATCH copy of the
  rule set (not the learner's real state): poisoned set
  {(X,+,1),(Z,+,2),(X,+,2)} is run through the same trial machinery;
  (X,+,2) is refuted and removed, both true rules retained,
  verdict line DRILL-PASS. This exercises the refutation code path,
  which the real T-DISJ run should NOT trigger.
- P-GOAL: GOAL_REAL=1 (mode-0 plan executed for real; the oracle
  witness [SX,W] achieves Y=1).
- P-COST: total real experiments (rule trials + drill) <= 6.
- P-DET: 3 runs byte-identical (md5), zero stderr bytes, exit code 0.

## 4. Falsifiers

- F-DISJ: any RULE_REFUTED line for (X,+,1) or (Z,+,2) on the real
  rule set (a true rule removed without replacement).
- F-PROP: the candidate set for Y is not exactly {(X,+,1),(Z,+,2)}.
- F-DRILL: the drill fails to remove (X,+,2), or removes a true rule.
- F-GOAL: GOAL_REAL=0.
- F-PURITY: any python3 invocation at any stage; any em/en-dash byte
  in source or logs (UTF-8 sequences E2 80 93 / E2 80 94).
- F-DET: the 3 raw logs are not byte-identical.

## 5. Kill bars

- K1: per-rule refutation implemented (RULE_REFUTED removal path,
  set-survives semantics); the drill proves the path is live.
- K2: T-DISJ tested per section 3; both true rules retained at
  convergence; goal achieved within the cost bound.
- K3: pure Zag (znc + sh + grep + git + md5sum only); 3/3
  byte-identical; zero em/en-dash bytes; zero stderr bytes.

## 6. Build (frozen)

  ZNC=/home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc
  D=docs/lab/research-lead/overnight-20260928/f3_phase2
  cat $D/f3_p2.zag ../f2_ood/world_ood4.zag > $D/run_p2.zag
  $ZNC $D/run_p2.zag -o $D/bin_p2
  $D/bin_p2 > $D/raw_p2_r1.txt 2> $D/raw_p2_r1.err   (x3)

World file concatenated from its committed frozen path, unmodified.
The learner NEVER reads the sealed law; it sees only the w_* interface.
The world's own w_verify (F2-format) is not called; the learner emits
its own F3P2 verdict lines, which the build script greps.

## 7. Honest scope (frozen)

Phase 2 is OP-PROP + per-rule refutation only. Not in scope:
multi-literal rules (OP-GROW is Phase 3), OP-SPLIT, OP-VAR,
EXTEND/STOP (Dcur fixed at 4), verification stream, REVISE, doubt
gating, history use. The drill is a mechanism self-test on a scratch
copy, disclosed as such; it is not a world result. No L3 claim.
Promotion steps 4-11 remain for any SURVIVES discussion.
