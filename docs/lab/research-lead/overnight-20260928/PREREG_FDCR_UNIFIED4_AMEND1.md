# PREREG H-FDCR-UNIFIED4 AMENDMENT 1 (pre-execution)

**Date:** 2026-09-29
**Amends:** PREREG_FDCR_UNIFIED4.md (commit a69dbb78f), section R1,
  `noadd_record` contract.
**Status:** Authored BEFORE any build, run, or test execution. No
  implementation output has been observed. Kill bars K-FU4-1..K-FU4-5
  and all fixtures are UNCHANGED.

## Change

The frozen prereg says `noadd_record` must "never record a subject
that is already a concept member (defensive check via
con_find_member_str)". This is refined to: never record a subject
that is already a member of the TARGET concept c
(`con_find_member_str(W, s)==c` skips; any other concept does not
skip).

## Rationale

The merge repair (R2, con_merge_into step 1) records overflow
members of the absorbed concept c2 as NOADD voters for the
survivor ci. At record time those subjects are still members of
c2 (deactivation is step 4). An any-concept membership check
would wrongly reject exactly the records the merge path exists
to create, silently re-introducing a vote loss at the merge
boundary. Scoping the check to the target concept preserves the
defensive intent (a NOADD entry for a member of c is redundant:
con_vote_concept prefers membership) while letting absorbed
members become voters. The check remains non-load-bearing in both
frozen call sites; no kill bar, fixture, or expected value is
affected.

## Governance

- Amendment authored before any compilation or execution of
  unified_fdcr4.zag; no result has been observed.
- Kill bars, fixtures, and PASS criteria are byte-identical to
  the frozen prereg.
- No em dashes in loop documentation.
