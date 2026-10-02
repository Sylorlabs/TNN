# Preregistration: Procedure Revision Test (L3 Criterion 12)

**Date:** 2026-09-29 07:20 PDT
**Status:** FROZEN (before implementation)
**Tester:** Procedure Revision Tester (subagent)
**Branch:** tnn-native-lab
**Reference:** PREREG_PROC_INVENT.md (criterion 12 deferred), proc_learn.zag @ 8fa0fe2a3

## Background

PREREG_PROC_INVENT.md deferred criterion 12 (Revision) as "not in v1 scope.
Documented as limitation." This prereg tests that limitation directly.

The Builder's mechanism (proc_learn.zag):
1. Extracts index sequences from (input, output) examples.
2. Enumerates compositional index programs from {K,N,C0,C1,C2,ADD,SUB} up to size 5.
3. Selects smallest program fitting ALL training sequences.
4. Applies to novel inputs.

For Family X (broadcast-last), it found program index 38: [N C1 SUB] = n-1.
RT2 confirmed 8/8 on undisclosed Family X, 85 distinct affine functions solved.

## Hypothesis

**H-REVISE:** The proc_learn mechanism can revise an invented procedure after
encountering a counterexample, satisfying L3 criterion 12.

**Null (H0):** The mechanism cannot revise. It is one-shot batch search with no
detection loop, no conditional representation, and no revision operators.

## Revision Test Design

### Phase 1: Baseline (establish)

Run proc_learn.zag (Family X training) to confirm found program is SUB(N,C1).

Training (from 8fa0fe2a3):
- "abc" -> "ccc" (seq [2,2,2], n=3)
- "xy" -> "yy" (seq [1,1], n=2)
- "defg" -> "gggg" (seq [3,3,3,3], n=4)

Expected: program [N C1 SUB], index 38.

### Phase 2: Counterexample (challenge)

Introduce a training pair where broadcast-last is WRONG and the correct answer
requires a CONDITIONAL procedure:

- inp3 = "xab", out3 = "xxx"
- Correct seq: [0,0,0] (broadcast-FIRST, because input starts with 'x')
- Broadcast-last prediction: [2,2,2] -> "bbb" (WRONG)

This is a minimal conditional: "broadcast-last UNLESS input starts with 'x',
then broadcast-first."

**Why this counterexample:**
- It preserves the original rule's validity on non-x inputs.
- It requires a content-dependent condition (first char == 'x').
- A revising learner should: detect mismatch, diagnose condition, specialize.

### Phase 3: Revision attempt

Add inp3/out3 to training set. Re-run the search (smallest program fitting ALL
four sequences).

**What counts as REVISION (H-REVISE survives):**
- Old procedure preserved (not deleted).
- New conditional/specialized version created.
- Both work on respective cases (non-x inputs -> broadcast-last, x-inputs -> broadcast-first).
- NOT just re-running search from scratch with no incremental structure.

**What does NOT count:**
- Overwriting the old program.
- Fixture-specific patch (works only on exact training inputs).
- Failing permanently with no diagnostic.

### Phase 4: Architectural analysis

Document precisely which revision capabilities are present/absent:
1. Counterexample detection (ongoing monitoring?)
2. Failure diagnosis (characterize WHEN it fails?)
3. Conditional representation (can language express "if"?)
4. Revision operators (specialize, split, merge, deprecate?)
5. Procedure memory (persistent revisable store?)

## Predictions

**If H-REVISE is TRUE:** Phase 3 produces a revised procedure handling both
cases, with old procedure preserved.

**If H0 is TRUE:** Phase 3 yields NO PROGRAM FOUND (no program in {K,N,C0,C1,
C2,ADD,SUB} can express content-conditional), OR the only path is manual
re-search (not revision). Architectural analysis will show missing: detection
loop, conditional primitives, revision operators.

**Prior:** H0 is strongly favored. The primitive set has no IF, no comparison,
no content access. The architecture is one-shot with no monitoring loop.
This test is expected to FALSIFY H-REVISE and precisely document the gap.

## Kill Bars (frozen)

**K-R1 (No representation):** If no program in the search space can express the
conditional (re-search yields NO PROGRAM), then the language cannot represent
revised procedures. H-REVISE KILLED.

**K-R2 (Re-search not revision):** If handling the counterexample requires
discarding the found program and re-running full search from scratch (no
incremental revision, no preserved structure), then the mechanism does not
REVISE. H-REVISE KILLED. (Re-search from scratch is not revision.)

**K-R3 (Fixture patch):** If any "revised" procedure works only on exact
training inputs (no generalization to novel x-inputs like "xhello" or novel
non-x inputs), it is a fixture patch. H-REVISE KILLED.

**K-R4 (No detection):** If the mechanism has no autonomous counterexample
detection (requires human to notice mismatch and manually trigger re-search),
then it lacks a necessary revision component. H-REVISE WEAKENED (not killed,
but bounded: revision requires human in loop).

## Success Bars

H-REVISE SURVIVES only if:
- Phase 3 produces a procedure handling both original and counterexample cases.
- Old procedure structure is preserved (not overwritten).
- Generalizes to novel inputs in both categories.
- K-R1 through K-R3 all pass (not killed).

This would constitute L3 criterion 12 satisfaction.

## Pure Zag

All implementation, search, and testing in Zag. No Python.

## Frozen

No thresholds adjusted post-hoc. If H-REVISE is killed, document the precise
architectural gap for future mechanism design.
