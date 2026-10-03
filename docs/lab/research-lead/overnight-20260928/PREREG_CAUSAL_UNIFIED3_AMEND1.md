# Amendment 1 to PREREG_CAUSAL_UNIFIED3 (transparent, re-frozen)

**Date:** 2026-09-29
**Amends:** PREREG_CAUSAL_UNIFIED3.md (commit 613886ade)
**Status:** FROZEN (this commit). Corrected implementation follows strictly after.
**Reason:** Pre-commit testing of the R1 repair exposed an over-broad absorb.

## What testing showed

The frozen R1 said: "If a conflicted entry covers (a, state): absorb the
episode into that entry." Implemented literally, the first conflicted entry
in the K-CU3-1 flood has mask 0 (`[any]`), so `cond_matches` is true for
every state. A genuinely new state (3,3,3) was absorbed into the conflicted
entry and its query withheld. That breaks the X-CU2-3 liveness boundary
(normal learning must stay intact after a flood), which the red team
recorded as a required informational boundary and which K-CU3-1f checks.

## The correction (frozen)

R1 is narrowed: `find_conflicted` returns the most specific ST_CONFL()
entry covering (a, state) **that holds a live (non-superseded) episode at
the exact state (s0,s1,s2)**. Episodes at genuinely new states still take
the pre-existing fresh-entry path (v2 behavior, unchanged).

Why this is the right scope:

- The X-CU2-1 bypass is a same-state attack: one more episode at the exact
  contradicted state (2,0,0). The exact-state requirement closes it: the
  conflicted entry holds the original contradiction episodes at (2,0,0),
  so the bypass episode is absorbed and the withhold is durable.
- The red team's recommended direction says "subsequent episodes at that
  (action, state)" (emphasis on the same state). The amendment implements
  exactly that.
- New-state learning is untouched, so the X-CU2-3 boundary holds.

## Kill-bar adjustments

- K-CU3-1(c): unchanged in letter (CONFLICTED-ABSORB note emitted for the
  (2,0,0) bypass episode), now also verified to be exact-state scoped.
- K-CU3-1f (fresh-state learning intact) is the regression guard for this
  amendment: it FAILED under the unscoped R1 (r=0 on (3,3,3)) and must PASS
  under the amended R1.
- Flood behavior note: under the amended R1, the 10th contradiction's
  episodes take the fresh-entry path (no live (2,0,1) episode exists in the
  conflicted entry yet), then that entry is marked ST_CONFL on contest-cap
  exhaustion, exactly as in v2. nct stays 8.

All other bars (K-CU3-1a/b/d/e, K-CU3-2, K-CU3-3, K-CU3-4) unchanged.
Kill criteria unchanged.

## Artifacts

- PREREG_CAUSAL_UNIFIED3_AMEND1.md (this file)
- Implementation and evidence commits follow after this freeze.
