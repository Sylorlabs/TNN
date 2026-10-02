# RESULT_F3P2: F3 Phase 2 -- OP-PROP + Per-Rule Refutation, T-DISJ

Date: 2026-09-30. Worker: F3 Phase 2 Builder.
Prereg: `0071846fa` (committed alone before implementation; verified
ancestor of this result commit via git merge-base --is-ancestor).
Design: `68aa2f6e8` (section 2, section 9 T-DISJ, section 11 item 2).
Phase 1: `720bb095e` (PHASE1-TESTED). Status: PHASE2-TESTED.
Pure Zag. No Python.

## 1. Verdict

**PHASE2-TESTED.** K1 PASS, K2 PASS, K3 PASS. No falsifier fired.

## 2. What was built

`f3_p2.zag` (single file, concatenated BEFORE the frozen
`f2_ood/world_ood4.zag` at build time; the world file is not copied
or modified):

- One rule set per effect variable, initialized with ALL OP-PROP
  candidates as separate singleton rules (cap 4, disclosed).
- Per-rule refutation (design section 2): each rule gets a trial
  (simulated sequence search, depth <= 6, last action OBSERVE of the
  effect var) where the rule fires; the trial runs for real. A false
  positive (rule fired, V=0) refutes EXACTLY that rule; the set
  survives while any rule stands. Refuted rules are spliced out and
  all remaining rules are re-tested (indices shift).
- Trial search never touches the world (w_ncalls checked around it).
- REFUTE-DRILL: disclosed mechanism self-test on a SCRATCH copy of
  the rule set (not learner state): poisoned set
  {(X,+,1),(Z,+,2),(X,+,2)} through the same trial machinery.
- Goal phase (mode 0): plan under the converged rule set with
  L_plan_dnf, execute for real, check w_goal_met.

## 3. Evidence (3/3 byte-identical, md5 7b2e9f68a8c5695254726894eb9ec4cb)

| Check | Frozen bar | Observed |
|---|---|---|
| P-PROP | Y candidates exactly {(X,+,1),(Z,+,2)} | PROP_OK=1 |
| P-CONV | both true rules present at convergence | nrules_Y=2, hasX1=1, hasZ2=1 |
| P-REFUTE-NONE | no true rule refuted | TRUE_REFUTED=0; only RULE_REFUTED is V=Z rule=0 (spurious X@4, section 5) |
| P-DRILL | poison (X,+,2) removed, true rules intact | DRILL-PASS |
| P-GOAL | GOAL_REAL=1 | GOAL_REAL=1 (plan [SX,W]) |
| P-COST | experiments <= 6 | NEXPS=6 (2 Y trials + 1 Z trial + 2 re-trials + 1 drill) |
| P-DET | 3/3 byte-identical, 0 stderr, exit 0 | 3/3 identical, 0 stderr bytes, exit 0 |

Trial detail: [SZ,W,W,OY] confirmed Z@2; [SX,W,OY] confirmed X@1;
[SX,W,W,W,W,OZ] refuted the spurious X@4 for Z (real Z=0 while the
rule fired). After the refutation the Y rules were re-tested and
re-confirmed; ALL_TESTED reached. The world's own oracle line reads
OOD4_WITNESS witness_goal=1.

## 4. Falsifiers

None fired. F-DISJ (true rule removed): no. F-PROP: no (PROP_OK=1).
F-DRILL: no (DRILL-PASS). F-GOAL: no. F-PURITY: no (zero python3
invocations; zero em/en-dash bytes in source and all logs).
F-DET: no (3/3 identical).

## 5. Honest scope and one disclosed correction

Phase 2 is OP-PROP + per-rule refutation only. Not yet:
multi-literal rules (OP-GROW is Phase 3), OP-SPLIT, OP-VAR,
EXTEND/STOP (Dcur fixed at 4), verification stream, REVISE, doubt
gating, history use. The drill is a mechanism self-test on a scratch
copy, disclosed as such. No L3 claim. Promotion steps 4-11 remain for
any SURVIVES discussion.

Correction (disclosed, prereg untouched): the first build's
in-program verdict required nrefuted==0 (no refutation at all),
which is stricter than the frozen prereg: F-DISJ and P-REFUTE-NONE
are defined only over TRUE rules, and K2 requires only that both
true rules are retained. The spurious X@4 rule for Z was correctly
refuted by the mechanism (a passive-schedule coincidence: X pulsed
exactly 4 steps before each Z pulse). The implementation was fixed
to track true_refuted (refutation of Y's (X,+,1) or (Z,+,2)) and the
verdict now matches the frozen prereg text. The prereg commit
`0071846fa` was not amended. The fix is visible in the source diff
of this result commit.

Note: the refutation of the spurious Z rule is genuine evidence for
K1 beyond the drill: per-rule refutation surgically removed a false
passive correlation while the true Y rules survived untouched. F2's
hypothesis-killing has no such surgical path.

## 6. Reproduction

Build (BUILD.sh in this directory):
  cat f3_p2.zag ../f2_ood/world_ood4.zag > run_p2.zag
  znc run_p2.zag -o bin_p2 && ./bin_p2   (x3)
Toolchain: znc 2026.07.0-dev (edition 2026).
Only tools used: znc, sh, grep, git, md5sum, sed. Zero python3.
