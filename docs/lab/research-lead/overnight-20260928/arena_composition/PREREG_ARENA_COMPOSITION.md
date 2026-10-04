# Prereg Amendment: Arena Compositional Capability (C4)

Date: 2026-09-30 UTC
Worker: Arena Composition Worker
Parent: Arena Contestant Improvement (ARENA-IMPROVED, 0.573, 0c5b6c631)
Amends: PREREG_ARENA_IMPROVE.md (568cba875)

## Diagnosis

### C4 compositional (0.000): Relations never learned

The arena teaches 6 relations as exposure events:
`{"t":"r","a":"<entity_a>","r":"<rel_name>","b":"<entity_b>"}`

The contestant v2 expo handler processes only `t:"f"` (fact) and
`t:"k"` (correction). Relation events (`t:"r"`) fall through to
`tick(W)` (no-op). The 6 relations are received but never stored.

The C4 test items use format `hop2|<start>|<rel1>|<rel2>` with the
expected answer being the entity reached by following rel1 from start,
then rel2 from the intermediate. The contestant v2 test handler has no
`hop2` branch; all such questions return "UNKNOWN".

This is a missing capability (relational learning + multi-hop
inference), not a bug. It requires new storage and a new inference
step, both built on DEVINT1's existing mechanisms.

## Planned changes

### Change 1: Relation learning (new storage, DEVINT1 mechanisms)

Add a relation store at W offset 8000: 64 entries x 48B
(0..15: entity_a, 16..31: rel_name, 32..47: entity_b).
This uses free space (8000..11072); facts end at 8000.

New functions:
- `rel_store(W,a,r,b)`: store (a,r,b) triple. If (a,r) already
  exists, update b (same update semantics as fact_store).
- `rel_get(W,a,r,out)`: find b such that (a,r,b) is stored.
  Returns 1 if found, 0 otherwise. Exact string match on a and r.
- `learn_rel(W,a,r,b)`: build raw string "a r b", feed through
  lex_feed (DEVINT1 lexicon), conc_touch for each part (DEVINT1
  concepts), then rel_store for exact retrieval. This mirrors
  learn_fact exactly, extended to triples.

In the expo handler, add:
- If `evtype` is `"r"` (relation): extract `a`, `r`, `b`.
  Call `learn_rel(W,a,r,b)`.

### Change 2: Two-hop inference (generic, not hardcoded)

In the test handler, add:
- If head is `"hop2"`: p1=start entity, p2=rel1, p3=rel2.
  Step 1: `rel_get(W,p1,p2,mid)`. If not found, answer UNKNOWN.
  Step 2: `rel_get(W,mid,p3,ans)`. If not found, answer UNKNOWN.
  Otherwise answer ans.

This is generic 2-hop composition over learned relations. It does not
contain the entity names, relation names, or answers from any test
item. It works for any (start, rel1, rel2) triple where the
intermediate relations were learned.

## Kill bars

K1: After changes, C4 must score 4/4 (was 0/4).
     If C4 remains below 4/4, the composition mechanism is broken.

K2: Total must exceed 0.573 (was 39/68).
     Expected: 39 + 4 (C4) = 43/68 = 0.632.
     If total does not exceed 0.573, FAIL.

K3: No regression. C1, C2, C3, C5, C7, C11, C13, C14 must remain
     at 1.000. If any drop, the changes broke existing functionality.

K4: Pure Zag. Zero Python. Zero em dashes.
     If any Python is used, the wave is void.

K5: Arena world/ and scoring unmodified.
     If world_gen.zag or arena.zag are modified, the run is invalid.

K6: Sealed seed not viewed. No tuning to seed.
     If the seed is viewed, the run is invalid.

K7: Determinism. 3/3 full arena runs must produce identical scores
     and byte-identical cognitive outputs (excluding rss_kb/ms).
     If not deterministic, FAIL.

K8: Generality. The hop2 handler must not contain hardcoded entity
     names, relation names, or answers from the C4 test items.
     Verification: grep the committed source for the specific
     test entity/rel strings; they must appear only in comments
     (if at all), never in logic. Additionally, all 6 taught
     relations must be stored (rel_count == 6 after exposures),
     proving the store is populated from all exposures, not just
     the 4 tested ones.

## What is NOT being done

- C6 conflict, C8 inquiry, C9 causal, C10 procedure, C12 transfer,
  C15 goal, C16 language: out of scope. These require new mechanisms.

## Honest scope

This adds genuine relational learning and 2-hop inference. It is
still bounded: only 2-hop (not n-hop), only exact match (not fuzzy),
only forward chaining (not bidirectional). The mechanism is
compositional but not yet general reasoning.

## Success criteria

BUILD-PASS if K1 through K8 all pass.
BUILD-FAIL if any kill bar fails.
