# Arm P — Emergent Vocabulary: Specification

## Identity

- **Arm:** P
- **Family:** ACQ (Acquisition)
- **Mechanism:** Emergent vocabulary via co-recall crystallization
- **ID Arm:** Yes (ARM_INTERFACE.md §9, CONFIRMED)

## Frozen Parameters

- **K = 7** — promotion threshold: co-recalls in distinct episodes (frozen A-34)
- **W = 200** — vote window in episodes (frozen A-34)

## Mechanism

Boundaries emerge from co-recall: pairs recalled together ≥K times in W
episodes are promoted to words; episode-indexed ring eviction; sensitivity
calibrations at K/2, 2K.

### Co-recall Voting

- Pair table keyed by (corpus, grid index a, grid index b), a<b, open-addressed.
- Only ADJACENT same-corpus pairs (b==a+1) can promote. A word is a contiguous
  byte span per the glossary; promoting disjoint spans would break it.
- Each recall of adjacent pair (a,b) in a distinct episode increments votes.
- Votes reset if the W-episode window expires without re-vote.

### Promotion

- When votes ≥ K within W episodes, the pair promotes to a word:
  - New counter ID, provenance=emergent (MK_WORD)
  - Span covers both 64-byte units (128 bytes total)
  - F_WORD flag set, F_LIVE set
  - Byte content = concatenation of the two unit bytes

### Episode-indexed Ring Eviction

- Insertion ring tracks slot insertion order.
- `p_evict`: FIFO from ring head, advancing `ins_head`. O(n) total.
  Used by M3 survival test (232k evictions, performance-critical).
- Binding trial uses inline LRU (min `last_rep`) for recency-sensitive
  eviction: stale units die, recently-used words survive.

### Word Review (Churn)

- `p_word_review`: scans live words; kills those with zero pair-votes in
  last W episodes AND zero recalls in last W episodes.
- Deliberate kill mechanism for the binding churn criterion.
- Emits OP_KILL audit entries.

## Operations

All required operations implemented:
- **ingest**: `p_ingest` — dedup via ID table, tombstone reuse
- **recall**: `p_recall` — ID → (offset,length,corpus) → bytes, updates last_rep
- **kill**: `p_kill` — clears F_LIVE, audit OP_KILL
- **pin/promote**: `p_pin` — sets F_PIN; promotion via `p_promote_pair`
- **weaken**: `p_weaken` — clears F_PIN (or reduces strength)
- **revise**: `p_revise` — preserves ID, emits REVISE, updates bytes
- **trainer boundary/content defects**: via revise with defect markers
- **trainer mark valuable**: `p_pin` with trainer provenance
- **evict**: `p_evict` — FIFO from insertion ring

## Constraints

- Pure Zag cognition. Zero RNG in AI decision paths.
- Byte-identical reruns. Any differing M8 artifact byte = DISQUALIFIED.
- `_zag_arg` is non-owned; never free it.
- `_zag_strcmp` returns 1 on equality.
- Never compare slices with `==`.
- Alias large-struct array fields before indexed access.
- Never index a slice over 2^25 bytes.
- Audit entries: 16 little-endian u32 words; stage@52, d1@56, d2@60.

## Modes

Normal modes (each emits exactly one METRIC_JSON; unknown modes exit nonzero):
- `m1-1x-prose`, `m1-1x-code` — recall + boundary + ID-swap probe
- `m2-t1-prose`, `m2-t1-code` — tier-1 word growth
- `m2-t2-prose`, `m2-t2-code` — tier-2 word growth
- `m2-t3-1x` — tier-3 word growth
- `m3-1x` — 999-episode survival, eviction pressure
- `m4-1x-prose`, `m4-1x-code` — revision (boundary/content defects)
- `m5-baseline`, `m5-1x` — crystallization + byte-exact learning
- `m6-p2c-1x`, `m6-c2p-1x` — cross-corpus transfer
- `m7-1x` — dedup/reuse
- `m8-1x` — determinism (byte-identical run0/run1)

Arm-local modes:
- `mbind-1x` — binding kill trial (P-local, not in shared harness)
