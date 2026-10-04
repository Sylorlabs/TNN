# AMENDMENT to PREREG_CAUSALV.md (H-CAUSALV)

Date: 2026-09-29
Amends: causal3/PREREG_CAUSALV.md (commit 82e877e47)

## Gap found during development

The prereg freezes a fewest-cells preference for the split search but does
not define the tie-break when an equality candidate and a threshold candidate
resolve the same entry with the same number of cells.

## Frozen tie-break (effective this amendment, before authoritative runs)

When EQ and THR candidates for the same variable both fully resolve an
entry with an equal cell count, the learner enumerates and prefers the
THR candidate. Rationale: the threshold is the compact ordered
representation and constrains unseen values (0..vmax) rather than only the
observed equality cells.

## What changed in implementation

Development runs exposed the gap: equality was winning ties by enumeration
order. The search now enumerates THR before EQ within a variable so the
fewest-cells winner prefers THR on ties. No frozen score threshold is
altered. No observation, probe, or baseline file is altered.

## Scope

This amendment covers the tie-break only. It does not retroactively alter
commit 82e877e47. Authoritative H-CAUSALV executions run after this
amendment commit.
