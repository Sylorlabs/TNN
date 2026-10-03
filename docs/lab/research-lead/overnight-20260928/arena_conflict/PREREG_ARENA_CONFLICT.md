# Prereg Amendment: Arena Conflict Handling (C6)

Date: 2026-09-30 UTC
Worker: Arena Conflict Worker
Parent: Arena Compositional (ARENA-COMPOSITION, 0.632, 0f6f1790d)
Amends: PREREG_ARENA_COMPOSITION.md

## Diagnosis

### C6 conflict (0.000): Conflicting evidence never stored

The arena teaches 3 conflicts as exposure events:
`{"t":"x","e":"<entity>","a":"<attr>","v1":"<val1>","s1":"archive","v2":"<val2>","s2":"scout"}`

Each exposure presents TWO conflicting values for the same
entity/attribute pair, with source labels ("archive" and "scout").

The contestant v3 expo handler processes only `t:"f"` (fact),
`t:"k"` (correction), and `t:"r"` (relation). Conflict events
(`t:"x"`) fall through to `tick(W)` (no-op). The conflicting values
are received but never stored.

The C6 test items use format `conflict|<entity>|<attr>` with the
expected answer being `v1|v2` (both values, pipe-separated). The
scorer awards full credit (1000) if the reply contains BOTH v1 and
v2 as substrings; partial credit (500) for exactly one.

The contestant v3 test handler has no `conflict` branch; all such
questions return "UNKNOWN".

This is a missing capability (conflicting evidence tracking), not a
bug. It requires new storage for value pairs and a new answer
format, both built on DEVINT1's existing mechanisms.

Note: even if conflicts were routed through learn_fact, the
fact_store has update semantics (new value overwrites old). Both
values must be retained, so a separate conflict store is required.

## Planned changes

### Change 1: Conflict storage (new store, DEVINT1 mechanisms)

Add a conflict store at W offset 11072: 32 entries x 64B
(0..15: entity, 16..31: attr, 32..47: value1, 48..63: value2).
This uses free space (11072..13120); relations end at 11072,
state is 16384.

New functions:
- `conf_store(W,e,a,v1,v2)`: store (e,a,v1,v2) quadruple. If
  (e,a) already exists, update both values (same update semantics
  as fact_store, but preserving the pair).
- `conf_get(W,e,a,out1,out2)`: find (v1,v2) for (e,a). Returns 1
  if found, 0 otherwise. Exact string match on e and a.
- `conf_count(W)`: number of stored conflicts.
- `learn_conflict(W,e,a,v1,v2)`: build raw string "e a v1 v2",
  feed through lex_feed (DEVINT1 lexicon), conc_touch for each
  part (DEVINT1 concepts), then conf_store for exact retrieval.
  This mirrors learn_fact, extended to value pairs.

In the expo handler, add:
- If `evtype` is `"x"` (conflict): extract `e`, `a`, `v1`, `v2`.
  Call `learn_conflict(W,e,a,v1,v2)`.

### Change 2: Conflict answer (generic, not hardcoded)

In the test handler, add:
- If head is `"conflict"`: p1=entity, p2=attr.
  `conf_get(W,p1,p2,tmp1,tmp2)`. If found, answer is
  `v1|v2` (pipe-separated, matching the expected format).
  If not found, answer UNKNOWN.

This is generic conflict retrieval over learned pairs. It does not
contain the entity names, attribute names, or values from any test
item. It works for any (entity, attr) pair where both conflicting
values were learned.

## Kill bars

K1: After changes, C6 must score above 0.000 (was 0/3).
     If C6 remains at 0.000, the conflict mechanism is broken.

K2: Total must exceed 0.632 (was 43/68).
     Expected: 43 + 3 (C6) = 46/68 = 0.676.
     If total does not exceed 0.632, FAIL.

K3: No regression. C1, C2, C3, C4, C5, C7, C11, C13, C14 must
     remain at 1.000. If any drop, the changes broke existing
     functionality.

K4: Pure Zag. Zero Python. Zero em dashes.
     If any Python is used, the wave is void.

K5: Arena world and scoring unmodified. Sealed seed not viewed.
     If world_gen.zag or arena.zag are modified, or the seed is
     viewed, the run is invalid.

K6: Determinism. 3/3 full arena runs must produce identical scores
     and byte-identical cognitive outputs (excluding rss_kb/ms).
     If not deterministic, FAIL.

K7: Generality. The conflict handler must not contain hardcoded
     entity names, attribute names, or values from the C6 test
     items. Verification: grep the committed source for the
     specific test entity/attr/value strings; they must not appear
     in logic. Additionally, all 3 taught conflicts must be stored
     (conf_count == 3 after exposures).

## What is NOT being done

- C8 inquiry, C9 causal, C10 procedure, C12 transfer, C15 goal,
  C16 language: out of scope. These require new mechanisms.

## Honest scope

This adds genuine conflicting-evidence tracking: both values are
retained (not overwritten), and the answer reports the conflict
explicitly. It is bounded: the mechanism stores the pair as taught;
it does not resolve which source is correct, weigh source
reliability, or perform belief revision. The answer format
(`v1|v2`) matches what the scorer rewards. Still 0 on inquiry,
causal, procedure, transfer, goal, language.

## Success criteria

BUILD-PASS if K1 through K7 all pass.
BUILD-FAIL if any kill bar fails.
