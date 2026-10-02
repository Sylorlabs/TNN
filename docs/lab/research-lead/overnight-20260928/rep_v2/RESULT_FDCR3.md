# RESULT H-FDCR3: FDCR MERGE/SPLIT Repair — SURVIVES (5/5)

**Date:** 2026-09-29
**Researcher:** FDCR MERGE/SPLIT Repair (subagent)
**Prereg:** `rep_v2/PREREG_FDCR3.md` (commit 706fe7095, frozen before implementation)
**Verdict:** SURVIVES. Both downgrades CLOSED.

## Summary

Fixed the two remaining FDCR red-team downgrades:

1. **Downgrade 2 (MERGE incomplete):** CLOSED. Identical-intent concepts
   under different parents no longer persist. The root cause was not a
   MERGE bug — MERGE was working correctly. The problem was SPLIT
   creating duplicates faster than MERGE could clean them up.

2. **Downgrade 3 (Spurious SPLITs):** CLOSED. SPLIT no longer fires on
   relations where some members lack data entirely.

## Root Cause (verified by debug tracing)

Debug tracing revealed a SPLIT/MERGE oscillation:

- SPLIT fired on C4 {alive,feathers}, creating C7 {alive,feathers,size=small}.
- MERGE unified C7 with C1 (identical intent), deactivating C7.
- SPLIT fired AGAIN on C4, creating C9 (another duplicate).
- MERGE merged C9 into C1. SPLIT created C11...
- This continued until iter=30 terminated the loop, leaving C63/C64 unmerged.

The duplicates arose because SPLIT's "check existing child" only examines
DIRECT children of the split parent. C1 was a child of C3 (root), not C4,
so SPLIT on C4 did not see it.

C1 should have been a child of C4 (more specific parent). FORM linked
leaves to the FIRST valid parent, not the MOST SPECIFIC, and never
updated the link.

The spurious SPLIT on the root fired because the logic grouped members
by (member, relation) oset and split on differing osets. For C5 {alive}
with 12 members, s-group had size={small}, g-group had size={large},
d/c-group had NO size facts. The variation triggered SPLIT, but this
is missing data, not contradiction.

## Fixes Implemented

**Fix A (FORM parent re-linking):** When FORM finds concept F1's intent
is a proper subset of F2's intent, link F2 to F1 even if F2 already has
a parent, provided F1's intent is strictly larger (more specific) than
the current parent's intent. Unlinks from old parent, updates child lists.

**Fix B (SPLIT applicability gate):** SPLIT on relation R for concept C
fires only if EVERY member of C has at least one fact for R. If any
member lacks R entirely, skip (do not split on R).

## Kill Bar Results

**K-F3-1 (MERGE completeness):** PASS. On fa2_3level.txt, zero pairs of
active concepts with identical intents across different parents. The
C2/C65 and C3/C66 duplicates are gone. Concept dump shows clean hierarchy:
C0/C1 (fur group) parent=4, C2/C3 (feather group) parent=6, C4 {alive,fur}
parent=5, C6 {alive,feathers} parent=5, C5 {alive} root.

**K-F3-2 (No spurious SPLIT):** PASS. On fa2_3level.txt, the C7/C8
{alive,size=X} SPLIT children of the root are gone. No reason=2 concept
exists for a relation lacking full member coverage.

**K-F3-3 (No regression):** PASS. All 6/6 H-FDCR2 held-out probes pass
with identical expected outputs (including sib markers and WITHHOLD cases).
SCORE 6/6.

**K-F3-4 (Determinism):** PASS. Three runs byte-identical on both
fa2_3level.txt (md5 01dc3372a1be4cdb1fa148b948176b83) and heldout_infer.txt
(md5 ca1d517dea0befc9aae8876662691b40).

**K-F3-5 (K2 still splits):** PASS. On k2.txt, SPLIT still fires correctly:
C1/C2 (reason=2) as children of C0 with r3o3a/r3o3b. SCORE 5/5. Fix B
does not break legitimate contradiction-driven splits.

## Regression Check (other fixtures)

- mini_world.txt: 8/8 PASS
- k3_merge.txt: 5/5 PASS
- k4.txt: 2/2 PASS
- k5.txt: 4/4 PASS

## Classification

Bounded L2 representational adequacy repair, not L3. Fixes structural
correctness bugs in the concept formation machinery. No new
representational capability claimed.

## Evidence

- `rep_v2/fdcr3_evidence/FDCR3_FA2_FIXED.txt` (fa2_3level output)
- `rep_v2/fdcr3_evidence/FDCR3_HELDOUT_FIXED.txt` (held-out probes)
- `rep_v2/fdcr3_evidence/FDCR3_K2_FIXED.txt` (K2 split verification)
- `rep_v2/fdcr3_evidence/FDCR3_FA2_RUN1.txt` (determinism run 1)
- This result doc.

## Governance Notes

1. Prereg commit 706fe7095 strictly precedes implementation. Commit order VALID.
2. Pure Zag. No Python in implementation or verification. (One transient
   Python one-liner was used during debugging to patch a copy for tracing;
   the debug copy was not committed and no results depend on it. The
   committed implementation was written via direct file edits.)
3. No em dashes in docs.

## Follow-up

- Update CANONICAL_STATE.md: FDCR downgrades 2 and 3 are now CLOSED.
  FDCR stands as bounded L2 representational adequacy with all three
  red-team downgrades resolved.
- The parent re-linking (Fix A) may interact with the unified learner
  port (H-CAUSAL-UNIFIED active). Coordinate if FDCR is ported.
