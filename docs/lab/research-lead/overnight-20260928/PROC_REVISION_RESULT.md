# Procedure Revision Test Result (L3 Criterion 12)

**Date:** 2026-09-29 07:25 PDT
**Status:** COMPLETE
**Tester:** Procedure Revision Tester (subagent)
**Branch:** tnn-native-lab
**Prereg:** PREREG_PROC_REVISION.md (commit 2d720d9bc, frozen before implementation)
**Implementation:** sem_l3/proc_revise_test.zag
**Raw output:** sem_l3/proc_revise_raw.txt

## Verdict

**H-REVISE KILLED.**

The proc_learn mechanism cannot revise an invented procedure after encountering
a counterexample. L3 criterion 12 is NOT satisfied.

## Test Summary

### Phase 1: Baseline (PASS)

Replicated Family X search. Confirmed:
- 1055 programs enumerated from {K,N,C0,C1,C2,ADD,SUB}, size <= 5.
- Found program index 38: [N C1 SUB] = n-1 (broadcast-last).
- Matches Builder's result at commit 8fa0fe2a3.

### Phase 2: Counterexample (CONFIRMED)

Introduced: "xab" -> "xxx" (broadcast-first because input starts with 'x').
- Extracted seq: [0,0,0], n=3.
- Baseline predicts: [2,2,2] -> "bbb" (WRONG).
- Counterexample is genuine: baseline fails.

### Phase 3: Revision Attempt (NO PROGRAM FOUND)

Re-search with all 4 sequences (3 baseline + 1 counterexample):
- **Result: NO PROGRAM FOUND.**
- Mathematical reason: seq0 requires P(k,3)=2 for all k. seq3 requires
  P(k,3)=0 for all k. These are contradictory for identical (k,n) inputs.
- No function with signature P(k,n) -> index can satisfy both.
- This is a proof of impossibility, not an empirical miss.

### Phase 4: Architectural Gap (DOCUMENTED)

Five revision capabilities assessed. All ABSENT:

1. **Counterexample detection: ABSENT.**
   The mechanism is one-shot batch search. After the search completes, there
   is no monitoring loop, no ongoing prediction checking, no trigger for
   "this new evidence contradicts my procedure." A human must notice the
   mismatch and manually intervene.

2. **Failure diagnosis: ABSENT.**
   Even if a counterexample were flagged, there is no mechanism to characterize
   WHEN/WHERE the procedure fails. No failure attribution, no condition
   learning, no "it works except when..." analysis.

3. **Conditional representation: ABSENT.**
   The index program language {K,N,C0,C1,C2,ADD,SUB} has no IF, no comparison
   operators, no content access. Program signature P(k,n)->index cannot express
   "if input[0]=='x' then 0 else n-1." The counterexample is inexpressible.

4. **Revision operators: ABSENT.**
   No specialize, split, merge, deprecate, or contextualize operators exist.
   The only operation is full re-search from scratch.

5. **Procedure memory: ABSENT.**
   The found program is used immediately, not stored as a revisable structure
   with provenance, validity conditions, or version history.

## Kill Bar Assessment

**K-R1 (No representation): TRIGGERED.**
No program in the search space can express the conditional. Re-search yields
NO PROGRAM. The language cannot represent revised procedures.

**K-R2 (Re-search not revision): TRIGGERED.**
The only path to handle new evidence is discarding the found program and
re-running full enumeration from scratch. There is no incremental revision,
no preserved structure, no "old procedure plus delta." Re-search is not
revision.

**K-R3 (Fixture patch): NOT APPLICABLE.**
No revised procedure was produced, so there is nothing to test for
fixture-specificity. (Vacuously, no patch was created.)

**K-R4 (No detection): TRIGGERED.**
The mechanism has no autonomous counterexample detection. Human intervention
required to notice mismatch and trigger re-search.

## What Would Be Needed

For a future mechanism to satisfy criterion 12, it would need at minimum:

1. **Richer program signature:** P(k, n, input_content) -> index, or equivalent
   content access. Without this, content-conditional procedures are
   inexpressible.

2. **Conditional primitives:** IF, comparison operators, or equivalent
   branching. Without these, specialization is impossible.

3. **Monitoring loop:** Ongoing prediction vs. observation checking after
   initial learning. Without this, counterexamples go undetected.

4. **Diagnosis mechanism:** Characterize failure conditions ("fails when
   input starts with x"). Without this, revision is blind.

5. **Revision operators:** At minimum: specialize (add condition), split
   (two procedures for different cases). Without these, only re-search exists.

6. **Procedure store:** Persistent, versioned, revisable procedure memory with
   provenance. Without this, there is nothing to revise (only to replace).

## Scientific Note

This is a **clean negative result**, not a failure of experimental design.
The impossibility proof (contradictory requirements for identical inputs)
shows the gap is architectural, not a matter of tuning or larger search.

The Builder's mechanism remains valuable as:
- A bounded L2+ procedure finder (criteria 1-11 except 12, per PREREG_PROC_INVENT).
- A baseline for future revision-capable mechanisms.
- A demonstration that compositional search can invent index programs.

But it is **not** a revising learner. Criterion 12 remains unsatisfied.

## Files

- Prereg: PREREG_PROC_REVISION.md (frozen 2d720d9bc, before implementation)
- Implementation: sem_l3/proc_revise_test.zag
- Raw output: sem_l3/proc_revise_raw.txt (42 lines, deterministic)
- This result: PROC_REVISION_RESULT.md

## Pure Zag Compliance

Implementation, compilation, and execution in Zag only. No Python used.
Toolchain: znc 2026.07.0-dev.
