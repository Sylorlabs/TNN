# H-CAUSAL-UNIFIED4 Amendment 1 (FROZEN)

**Date:** 2026-09-29
**Amends:** PREREG_CAUSAL_UNIFIED4.md (commit 9331cf67a)
**Status:** Frozen before the corrected implementation. No result data was
used to choose the new design beyond the single observed violation below.

## What broke

The first implementation (mirror `contest_feed` verbatim, reactivate the
conflicted entry in place) was executed against the frozen driver before
this amendment. Result: 11/14 checks pass. The 3 failures share one root
cause:

- K-CU4-1e FAIL: after UNCONFLICT at (2,0,0), the query at the untouched
  (2,0,1) predicted r=1 via rule instead of withholding.
- K-CU4-1f FAIL and K-CU4-2a FAIL (consequential): the reactivated entry
  kept its unrefined mask 0 ([any]), so later episodes at new states
  routed into it instead of taking the fresh-entry path.

Root cause: the conflicted entry's mask is [any] (unrefined default) while
the adjudicating evidence sits at one exact state. Reactivating in place
generalizes the 2-vs-1 adjudicated law to every state the mask covers,
retiring the withhold at (2,0,1) with zero evidence at (2,0,1). That
violates the frozen K-CU4-1e intent ("adjudication is scoped to the state
with evidence") and reintroduces the X-CU2-1 complaint in a new coat: a
withhold retired without evidence.

## Design change (frozen)

On adjudication, after superseding the losers and before recomputing
effects: if every live (non-EP_SUP) episode of the conflicted entry is at
the exact adjudicated state, the entry's mask is refined to that exact
state (mask 7, cond = the state). Rationale: the adjudicating evidence is
at the exact state, so the reactivated law is scoped to the evidence; the
withhold persists at every other state the old mask covered. If the entry
holds live episodes at other states (possible for split-failure
conflicts), the mask is left unchanged and the law generalizes, consistent
with `contest_feed` semantics; that case is a disclosed boundary.

The UNCONFLICT trace notes the scoping ("; scoped to adjudicated state")
when narrowing fires, and the emitted cond reflects the narrowed entry.

## Bar impact

- K-CU4-1e is re-affirmed unchanged: with scoping, Q(2,0,1,2) withholds.
- K-CU4-1f and K-CU4-2a expectations stand as frozen; scoping restores them.
- K-CU4-2c is unchanged: the re-contradiction path works on the narrowed
  entry identically.
- No other bar changes. The verdict rule is unchanged.

## Ordering

This amendment is committed before the corrected implementation is built
or executed. The 11/14 partial run above is discarded as a design
experiment, not a result; no verdict is drawn from it.
