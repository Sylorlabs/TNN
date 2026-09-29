# H-CAUSAL-UNIFIED4 Amendment 2 (FROZEN)

**Date:** 2026-09-29
**Amends:** PREREG_CAUSAL_UNIFIED4.md (commit 9331cf67a) as amended by
AMEND1 (commit 5593aa542).
**Status:** Frozen before the corrected implementation. The AMEND1 design
was executed (14-check driver); the diagnostic below, not the scores,
motivates this change.

## What broke

A diagnostic dump of the flood workspace showed the conflicted entry is a
single [any] entry holding 18 episodes across 9 states (the 8 tracked
contests all sit on entry 0; the 9th contradiction at (2,0,0) marked the
whole entry ST_CONFL). The AMEND1 "narrow the mask when all live episodes
are at the exact state" condition therefore never fires: live episodes
span 9 states. In-place reactivation (AMEND1) would generalize the
adjudicated law across all 9 states, retiring the withhold at the
still-contradicted (2,0,1) with zero evidence there. That is a soundness
hole in the conflict machinery, not just a test-expectation miss: a
red team can already make the learner confidently predict at a state with
an explicit unresolved contradiction, via a neighboring state's evidence.

## Design change (frozen): carve-out, not in-place reactivation

`conflict_adjudicate` no longer reactivates the conflicted entry in
place. On a contest-criterion win at exact state s in conflicted entry
cf:

1. Create a new entry ni via `new_entry(W, a, 7, cf, seq)` (mask 7, parent
   cf for provenance). Its cond is set to s. If creation fails (entry
   capacity), emit the existing ERROR and return 0; the conflict stands.
2. Every live winner-outcome episode at s is added to ni (shared global
   indices; they stay live). Every live loser-outcome episode at s is
   marked EP_SUP in cf (explicit retirement; losers are not shared with
   ni).
3. Effects are recomputed on ni (`effects_over`, excl=ni); if unresolved,
   `split_attempt` runs on ni (it may re-conflict honestly); then
   `merge_pass` runs.
4. cf stays ST_CONFL with all its other evidence, contests, and withholds
   intact. The UNCONFLICT trace names ni, the scoped cond, the moved
   winner count, and the superseded loser count.

Rationale: adjudication is scoped to the evidence. The resolved state
gets a clean ACTIVE entry carrying exactly the adjudicated law; every
other state's contradiction keeps its withhold. Nothing is silently
forgotten: losers are explicitly superseded, winners are explicitly
moved, and cf remains as the conflict tombstone.

Consequences (frozen):

- nent grows by exactly 1 per adjudication (the carved entry), explicitly
  traced. K-CU4-1c-i and K-CU4-2a are updated: the bar is "no fresh entry
  via the silent learn path", not "nent constant".
- The carved entry's parent is cf (provenance). Merge safety follows the
  existing machinery.
- If the conflicted entry holds live episodes only at s (the simple
  case), the carve-out still applies uniformly; cf becomes a tombstone.

## Bar updates

- K-CU4-1c-i: nent = ne0+1 (exactly the carved entry). The UNCONFLICT
  trace must name the new entry index.
- K-CU4-1c-ii: `find_entry` at (2,0,0) returns an ACTIVE entry (the
  carve-out).
- K-CU4-1c-iii: the ST_CONFL entry covering (2,0,0) holds an EP_SUP
  episode at the exact state (the retired loser).
- K-CU4-1d: unchanged (r=1, predicts (0,0,0)).
- K-CU4-1e: unchanged (r=0 at (2,0,1)); now passes because the carved
  entry is scoped.
- K-CU4-1f: unchanged.
- K-CU4-2a: nent accounting updated as above; the learn path still never
  creates a fresh entry at the conflicted state.
- K-CU4-2b: unchanged (trace names the superseded loser).
- K-CU4-2c: unchanged; the re-contradiction now conflicts the carved
  entry (it is the ACTIVE cover for (2,0,0)).
- K-CU4-3, K-CU4-4, K-CU4-5, K-CU4-6: unchanged.

## Ordering

Committed before the carve-out implementation is built or executed. The
AMEND1 11/14 run is discarded as a design experiment; no verdict is drawn
from it.
