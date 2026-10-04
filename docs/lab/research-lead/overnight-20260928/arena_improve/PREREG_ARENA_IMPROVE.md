# Prereg Amendment: Arena Contestant Improvement

Date: 2026-09-30 UTC
Worker: Arena Contestant Improvement Worker
Parent: I1 (ARENA-RUN-COMPLETE, 0.352)
Amends: ARENA_PREREG_AMEND4.md (d64fc521b)

## Diagnosis

### C14 restart (0.500): NOT a serialization bug

The 3 failing C14 items are the "corrected" facts (entities 6,7,8).
The world sends correction exposures as `{"t":"k","e":...,"a":...,"old":...,"new":...}`.
The contestant's expo handler only processes `t:"f"` (fact) events.
Correction events (`t:"k"`) fall through to `tick(W)` (no-op).

The state persists correctly (16384 bytes, byte-identical across save/load).
The 3/6 score reflects a missing capability (C5 correction), not a
serialization failure.

### C5 correction (0.000): Missing handler

Same root cause. Corrections are received but ignored.

### C3 paraphrase (0.000): Missing question format

C3 uses `fact2|entity|attr` question format. The contestant's test handler
only matches head `"fact"`. The underlying facts are identical to C1.
This is a format robustness gap, not a reasoning gap.

## Planned changes

### Change 1: Correction handling (fixes C5 and C14)

In the expo handler, add:
- If `evtype` is `"k"` (correction): extract `e`, `a`, `new`.
  Call `learn_fact(W,e,a,new)`.
- `learn_fact` already calls `fact_store`, which UPDATES existing
  entity+attr entries. No new storage mechanism needed.
- This uses DEVINT1's actual mechanisms: lex_feed, conc_touch,
  rule_touch, fact_store. The correction is learned as a new fact
  that overwrites the old value, exactly as DEVINT1 would learn
  any updated association.

### Change 2: Paraphrase format (fixes C3)

In the test handler, accept head `"fact2"` as an alias for `"fact"`.
Both trigger the same `fact_get` lookup. This is format robustness
for the existing retrieval mechanism, not a new capability.

## Kill bars

K1: After changes, C14 must score 6/6 (was 3/6).
     If C14 remains below 6/6, the correction hypothesis is wrong.

K2: After changes, C5 must score 6/6 (was 0/6).
     If C5 remains 0/6, the handler is not working.

K3: After changes, C3 must score 6/6 (was 0/6).
     If C3 remains 0/6, the format hypothesis is wrong.

K4: C1, C2, C7, C11, C13 must remain at 1.000 (no regression).
     If any drop, the changes broke existing functionality.

K5: Total must exceed 0.352 (was 24/68).
     Expected: 24 + 6 (C5) + 3 (C14 delta) + 6 (C3) = 39/68 = 0.574.
     If total does not exceed 0.352, FAIL.

K6: Pure Zag. Zero Python. Zero em dashes.
     If any Python is used, the wave is void.

K7: Arena world/ and scoring unmodified.
     If world_gen.zag or arena.zag are modified, the run is invalid.

K8: Sealed seed not viewed. No tuning to seed.
     If the seed is viewed, the run is invalid.

## What is NOT being done

- C4 composition (2-hop): Requires relation learning. Out of scope.
- C6 conflict: Requires reliability weighting. Out of scope.
- C8 inquiry, C9 causal, C10 procedure, C12 transfer, C15 goal, C16 language:
  All out of scope. These require new mechanisms, not fixes.

## Success criteria

BUILD-PASS if K1 through K8 all pass.
BUILD-FAIL if any kill bar fails.
