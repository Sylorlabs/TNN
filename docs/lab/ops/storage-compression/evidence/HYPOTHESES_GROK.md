# Storage-compression hypotheses — GROK-4.6 (via UnoRouter)

- **Model:** grok-4.6 (grok-4.7 is delisted from UnoRouter as of 2026-09-22; grok-4.6 used per task instructions, no silent substitution)
- **Date:** 2026-09-22
- **Source:** `~/workspace/skills/unorouter/bin/unorouter.py chat --model grok-4.6` (streaming transport; non-streaming call hit Cloudflare 524 on the gateway)
- **Context given:** 92 B/fact store (24B slot + 4B dense id→slot index + 64B audit-ledger entry), install ~6.2µs/fact, recall O(1) at 1–3.2M probes/sec, pure Zag, zero RNG, byte-identical reruns; FL1–FL4 already found (92→36 B/fact). Hard constraints: facts explicit/countable/addressable, revisable/deletable, zero randomness, deterministic byte-identical reruns, pure Zag, one unified system.

Everything below the divider is GROK-4.6's response, VERBATIM (no edits).

---

**Proposed compression schemes (beyond FL1-FL4)**

**(a) Ledger delta encoding across entries**
Mechanism sketch: Ledger becomes a delta stream. First entry stores full 20B compacted struct (FL2). Each subsequent entry stores 16 signed i32 deltas (zigzag + varint-like bit packing in Zag: 2-6 bits per field typical). Replay starts at empty state; cumulative deltas rebuild each slot exactly. Arena allocates contiguous ledger buffer; no external libs.
Expected bytes/fact: 11B (assumes avg 2.5B delta/entry on 16 fields; validated on synthetic add sequences with 40% repeat fields).
Speed impact: install ~8% faster (fewer writes/ops); recall neutral (state build once at load, O(n) replay amortized over lifetime, not on critical path).
KILL BAR: If measured replay time (byte-identical state after full ledger) increases >5% vs original 20B encoding on 1M-fact log, or checksum fails on reconstruction, kill it.

**(b) Text payload interning**
Mechanism sketch: Global intern arena (vector of {len,u8*} pairs, 12B overhead each). Facts store 4B intern index (instead of raw payload). On add, binary-search intern table (deterministic Zag impl, no rand) to reuse or append. Payloads currently live in separate 64B buffers per fact; move to shared pool.
Expected bytes/fact: 19B (assumes payload avg 48B/fact with 65% dedup; index 4B + reduced payload).
Speed impact: install neutral-to-slower (lookup cost); recall neutral (index O(1) indirection).
KILL BAR: If dedup ratio <40% on payload distribution (measured via unique strings in test corpus), or install probes/sec drops below 5M, kill it.

**(c) Per-pass slot delta encoding**
Mechanism sketch: Slots array stores deltas vs prior pass (clock factored out per FL4). First slot in pass absolute; subsequent deltas on lifecycle/strength/value (8B packed). Replay: start pass with clock, apply deltas. Arena reuses slot buffer across passes.
Expected bytes/fact: 27B (assumes 60% field stability across passes).
Speed impact: install faster (delta writes); recall neutral (still direct array access via index).
KILL BAR: If pass-delta encoding increases slot-replay ops >3% on 10k-fact pass transition (byte check), kill it.

**(d) Cold-fact tiering**
Mechanism sketch: Slot gains 1B freq/cold flag. On recall count > T (e.g. 20), migrate slot payload+fields to separate cold arena (compressed 12B slots via bit packing + RLE). Maintain 4B id→cold-offset indirection table (linear probe, sized to 2M). Hot slots stay in main 24B array.
Expected bytes/fact: 31B (assumes 15% facts cold; main tier 24B, cold tier 12B).
Speed impact: recall neutral if cold hit-rate <5%; otherwise 1.8× slower per hit (tier jump).
KILL BAR: If overall recall probes/sec drops below 2.5M probes/sec on cold-heavy probe battery (20% cold facts), kill it.

**(e) Columnar transposition + bit packing**
Mechanism sketch: 4 separate packed arrays (lifecycle[ n ] 10-bit, strength[ n ] 10-bit, clock[ n ] 8-bit, value[ n ] 64-bit). Id directly indexes arrays (base[id] + field_offset). No 4B dense index; slots computed via pointer arithmetic. Main array still 24B but fields bit-packed; ledger unchanged.
Expected bytes/fact: 26B (assumes 3 fields pack to 1B each + value 8B).
Speed impact: recall neutral-to-faster (better cache per field); install neutral.
KILL BAR: If packed access adds >2 cycles/fact (measured on probe battery), kill it.

**(f) Additional schemes**
- Ledger RLE on constant fields: 8B/fact (run-length on i32 repeats).
- Value bit-packing (if <2^60 distribution): 5B/fact.
- Tombstone reuse without index: 0B index (free-list reuse), but requires 1B bitmap; conditional on no deletes.
- Arena-level compression on ledger buffer (Zag custom): 9B/fact.

**What the inspection missed**
- Dense index 4B is largely removable under reuse: direct id*packed_slot_size arithmetic if we maintain a free-list + compact-on-delete (tombstone + sliding window).
- Value/i64 is already 8B; if numeric facts dominate, interning the 64-bit values themselves (arena of unique i64) saves another 4B via 4B index.
- Ledger contains 9 always-zero words per FL2; many adds are "append new slot" with predictable deltas—store op-only + 1B slot-id delta, collapsing to 8B/entry.
- Clock per-pass (FL4) + strength/lifecycle (FL3) create cross-field correlation; a 2D delta table (clock vs strength) can be stored as 3B instead of 8B sparse.
- 24B slot wastes 4B on id (removed) + 4B on fixed 1000/1 constants; remaining 16B can be bit-packed into 12B with 2-bit for lifecycle/strength.
- Audit replay is O(n) amortized; instead of full 20B entries, store a trie of add operations (Zag node pool) for 6B/fact on high-repeat sequences.
- Payloads "elsewhere" are un-interned; the 4B index + arena already present in slot design is the exact hook for interning without changing layout.
- No waste in randomness (already zero) or O(1) recall (already enforced); all savings must preserve id->slot mapping and tombstone semantics.

These are all testable in Zag; each includes concrete kill criteria to avoid regression.
