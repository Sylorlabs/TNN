# PREREG H-FDCR3: FDCR MERGE/SPLIT Repair

**Date:** 2026-09-29
**Researcher:** FDCR MERGE/SPLIT Repair (subagent)
**Status:** FROZEN (pre-implementation)
**Target:** `rep_v2/fdcr_learn.zag`

## Background

H-FDCR2 closed red-team downgrade 1 (taught-fact confounding) with 6/6
genuine held-out probes. Two downgrades remain OPEN:

**Downgrade 2 (MERGE incomplete):** In fa2_3level.txt, C2
{alive,feathers,size=small} parent=5 and C65 with IDENTICAL intent
parent=6 were not unified. Same for C3/C66. The MERGE spec ("if two
concepts have identical intents, unify them") is violated when
duplicates arise under different parents.

**Downgrade 3 (Spurious SPLITs):** In fa2_3level.txt, C7
{alive,size=small} and C8 {alive,size=large} were created with reason=2
(SPLIT) despite no contradiction in the fixture.

## Root Cause Analysis (pre-implementation, from debug tracing)

Debug tracing (transient, not committed) reveals:

1. SPLIT fires repeatedly on the same concept, creating duplicates
   (C7,C8 then C9,C10 then C11,C12...). MERGE merges each batch, but
   SPLIT creates more. The loop terminates at iter=30 leaving the final
   duplicates (C63,C64) unmerged.

2. The duplicates arise because SPLIT's "check existing child" only
   looks at the DIRECT children of the split parent. C1
   {alive,feathers,size=small} is a child of C3 (root), not a child of
   C4 {alive,feathers}. When SPLIT fires on C4, it does not see C1 as
   an existing child, so it creates a duplicate.

3. C1 should be a child of C4 (more specific parent), not C3. FORM
   links leaves to the FIRST valid parent found, not the MOST SPECIFIC.
   Once linked, the parent is never updated even when a better parent
   is formed later.

4. The spurious SPLIT on the root (C7/C8) fires because the SPLIT
   logic groups members by (member, relation) oset and splits when
   osets differ. For C5 {alive} with 12 members, the s-group has
   size={small}, g-group has size={large}, d/c-group has NO size facts.
   The differing osets trigger SPLIT, but this is variation with
   missing data, not contradiction.

## Proposed Fixes

**Fix A (FORM parent re-linking):** When FORM finds that concept F1's
intent is a proper subset of F2's intent (F1 is the abstraction), link
F2 as child of F1 EVEN IF F2 already has a parent, PROVIDED F1's intent
is LARGER (more specific) than F2's current parent's intent. Update
both the child's parent pointer and the old/new parent's child lists.

**Fix B (SPLIT applicability):** SPLIT on relation R for concept C
fires ONLY IF every member of C has at least one fact for R (in the
relevant phase/context). If any member lacks R entirely, the variation
is missing information, not contradiction. Do not split.

Rationale for Fix B: In K2 (correct split), both E1a and E1b have r3
facts when SPLIT fires. In fa2 (spurious split), d1,d2,c1,c2,c3 have no
size facts when SPLIT fires on the root. The "every member has R" rule
distinguishes these.

## Kill Bars (frozen)

**K-F3-1 (MERGE completeness):** On fa2_3level.txt, after the fix,
there must be NO pair of active concepts with identical intents but
different parents. Specifically: no C65/C66 duplicates of C2/C3.
Verification: grep the concept dump for intent collisions across
parents. PASS if zero collisions.

**K-F3-2 (No spurious SPLIT):** On fa2_3level.txt, after the fix, no
SPLIT child (reason=2) may be created for a relation R on a concept C
where any member of C lacks R facts. Specifically: C7/C8
({alive,size=X} children of root) must NOT exist, because d/c-group
members have no size facts. Verification: concept dump contains no
reason=2 child of the root via the size relation. PASS if absent.

**K-F3-3 (No regression):** All 6/6 H-FDCR2 held-out probes
(heldout_infer.txt) still PASS with identical expected outputs.
Verification: run fdcr_learn on heldout_infer.txt, confirm SCORE 6/6
and each probe matches expected (including WITHHOLD cases).

**K-F3-4 (Determinism):** Three consecutive runs on fa2_3level.txt and
heldout_infer.txt produce byte-identical output. Verification: md5sum
of outputs matches across runs.

**K-F3-5 (K2 still splits correctly):** On k2.txt, SPLIT must still
fire correctly (C1/C2 children of C0 with r3o3a/r3o3b). This ensures
Fix B does not break legitimate contradiction-driven splits.
Verification: concept dump shows the expected split structure.

## What Does NOT Count

- Patching the fixture to avoid the bug.
- Disabling SPLIT entirely.
- Merging concepts with different intents.
- Any Python in implementation, testing, or verification.

## Commit Order

1. This prereg (PREREG_FDCR3.md) — frozen before implementation.
2. Implementation + tests + evidence.
3. Result doc (RESULT_FDCR3.md).

Prereg commit must strictly precede implementation commit.
