# Sol hypotheses — TNN storage compression

- **model:** gpt-5.6-sol (via UnoRouter, `~/workspace/skills/unorouter/bin/sol.py`)
- **date:** 2026-09-22
- **context given:** 92 B/fact store (24B slot: id/lifecycle/strength/clock/value; 4B dense id->slot index; 64B audit entry per add); install ~6.2µs/fact; recall O(1) 1–3.2M probes/s; pure Zag; zero RNG; byte-identical reruns; known free lunches FL1–FL4 (post-free-lunch ~36 B/fact); hard constraints: explicit/countable/individually-addressable/revisable/deletable facts, zero randomness, byte-identical reruns, pure Zag, one unified system.
- **collection note:** the full prompt timed out at the provider (HTTP 524, ~126s) on long generations, and one framing attempt returned a stall asking for repo access instead of hypotheses (superseded, contained zero hypotheses). The consultation was therefore gathered as three sequential calls with tightened word caps; Sol's text below is VERBATIM from those three calls (H1–H3 audit compaction; H4–H6 slot/value; H7–H9 inter-structure/cold/missed-waste + ranking + stacked estimate). Known quirk: in Part 3 Sol ranked H1–H6 as "unscorable; definition absent" because it could not see the Part 1/2 definitions — that ranking limitation is an artifact of the split collection, not a judgment on H1–H6.

---
---

--- PART 1: audit-ledger compaction (H1-H3) ---

I’m treating the stated ~36 B/fact as the post-free-lunch total baseline and will make each estimate conditional on explicit workload assumptions. The kill bars will be measurable thresholds, so each proposal can be rejected without relying on intuition.1. **H1: Differential Encoding Across Consecutive Audit Entries**  
   **Mechanism:** Keep a deterministic 32-entry block anchor: full 64B entry at offset 0, followed by deltas. Each delta is `[changed_mask:u16 @0][payload @2]`; mask bits map to the 16 existing words, and changed values use fixed-width or canonical unsigned-varint encoding. Existing per-operation schemas still apply. Anchors permit bounded decoding and byte-identical replay.  
   **Expected:** Assuming two changed words per entry on average, 10–12B/audit entry; roughly 29–34B/fact total.  
   **Speed:** Install adds comparison, mask generation, and encoding, likely 5–15% slower. Fact recall remains O(1).  
   **KILL BAR:** Kill if measured average exceeds 36B/fact, or install throughput falls below 85% of 6.2us/fact.

2. **H2: Run-Length Encoding of Repeated Operation Fields**  
   **Mechanism:** Replace each repeated 32-bit `op` with a deterministic run record: `[op:u8 @0][count:uvarint @1]`, followed by count payloads containing the existing non-op fields. A run closes whenever `op` changes; singleton runs retain the same format. No randomness or dictionary state is required.  
   **Expected:** Assuming mean run length is at least eight, save approximately 3.5B per audit entry, producing roughly 32–34B/fact total.  
   **Speed:** Install performs one operation comparison and counter update; expected overhead is under 5%. Recall is unchanged.  
   **KILL BAR:** Kill if measured mean run length is below four, total savings are under 2B/fact, or install exceeds 6.5us/fact.

3. **H3: Cold Audit Log With Hot Summary Structure**  
   **Mechanism:** Keep an 8B/fact hot summary sidecar: `last_audit_offset:u32 @0` and `revision_or_count:u32 @4`. Move historical audit entries to a deterministic append-only cold log with 32-entry blocks: `[base_slot:u32][entry_count:u16][payload...]`. Cold records use H1/H2-style packing; deletions and revisions append explicit records. Fact lookup remains through the existing dense index and slot.  
   **Expected:** Assuming cold records average 4–8B and the summary is 8B, roughly 30–35B/fact total.  
   **Speed:** Install adds one summary write and cold append, likely 3–8% slower. Ordinary recall remains O(1); history inspection pays block decode cost.  
   **KILL BAR:** Kill if ordinary recall needs cold-log access, hot memory exceeds 36B/fact, or cold-history decode exceeds 1us per requested entry.

---
--- PART 2: slot and value compression (H4-H6) ---

I’ll keep the three entries tightly scoped to the requested storage contract, with explicit byte accounting and falsifiable kill bars. The estimates will distinguish guaranteed layout costs from assumption-dependent savings.1. **H4 — Slot deltas**

   **Mechanism:** Keep the 4B dense id→slot index. Group 16 slots per pass-local block. Store one 12B template (`clock:i32,value:i64`) plus each record’s 1B change mask and varint deltas; retain 2B block offsets for bounded random decode. Restart values every block preserve individual addressing. Expected slot storage: ~7–11B/fact versus the 12B post-free-lunch slot payload; total: ~31–35B/fact. Install cost rises ~3–8% from delta formation and encoding. Recall remains O(1), but requires up to 16 decodes, likely reducing probes ~5–20%. **KILL BAR:** kill if measured changed-field masks plus restart/offset overhead exceed 12B/fact, or p99 recall exceeds 2x current latency.

2. **H5 — Columnar bit-packed storage**

   **Mechanism:** Store 128-slot chunks: `value[128]` at 1024B, `clock[128]` at 512B, and per-field validity/change bitmaps at 16B each. Rare lifecycle/strength revisions use sparse `(slot,value)` overlays; unchanged constants remain absent. Bit-pack clocks only when their observed range permits narrower widths; otherwise retain i32. Dense id→slot addressing becomes column offsets plus slot number. Expected base: 12.0–12.3B/fact for clock/value, plus 0–1B overlays; total: ~32–36B/fact. Install improves locality but adds column writes and bitmap updates, roughly neutral to +10%. Recall needs two column loads, likely within ±10%. **KILL BAR:** kill if production clock/value distributions require full widths and overlays exceed 1B/fact, or recall drops over 15%.

3. **H6 — Exploit i64 value structure**

   **Mechanism:** Use a 1B tag with narrow payload and an escape table. **ASSUMPTION A:** values are repeated strings: intern bytes once, store a 32-bit table pointer; kill if deduplication is below 2:1 or table lookup adds over 15% recall time. **ASSUMPTION B:** values are composite fields: reserve 32 bits for type/flags and pack bounded components into the remaining bits; kill if more than 5% require escapes. **ASSUMPTION C:** values are mostly small signed integers: zigzag-varint payload, with 64-bit escape; kill if median encoded size exceeds 4B or escapes exceed 10%. Expected value storage: ~2–5B/fact, yielding ~30–33B/fact total. Install adds tagging/interning work, potentially 5–20%; recall adds one branch, table access only for strings.

---
--- PART 3: inter-structure redundancy, cold storage, missed waste, ranking (H7-H9) ---

I’ll keep the three proposals narrowly tied to the supplied post-free-lunch state, and I’ll label assumptions where the layout does not establish a fact. The ranking will distinguish “not rankable from the supplied record” from a fabricated estimate for H1–H6.**H7.** If allocated IDs are monotonic, make slot position the ID: slot `n` is implicitly ID `n`. Remove `id@0` and the dense `id -> slot` index; preserve deletion with tombstone slots, and preserve arbitrary IDs only through a sparse exception table. A compact slot becomes `lifecycle@0`, `strength@4`, `clock@8`, `value@12` = 20B, with no per-fact index. Audit records store only the slot position; any explicit ID is emitted only for exception records. Expected reduction: approximately 4B for the slot ID plus 4B for the dense index, from ~36B to ~28B/fact before exceptions. Install should improve modestly through fewer writes; hot recall remains O(1). **KILL BAR:** benchmark or workload evidence shows IDs are non-monotonic, deletion creates too many exceptions, or exception storage exceeds 1B/fact on average.

**H8.** Use two RAM-resident tiers. Hot facts retain direct slots. Cold facts use a 16B packed record: `id_delta@0:u32`, packed lifecycle/strength/clock metadata at `@4:u32`, `value@8:i64`; the index stores a 4B cold-record pointer. Keep audit data in the existing compressed form. With 70% cold facts, expected storage is roughly 18–24B/fact, depending on hot metadata and pointer handling. Hot recall remains about 0.3–1us; cold recall should measure about 2–5us for pointer lookup plus decode, with install 5–8us/fact due to tier classification and encoding. **KILL BAR:** cold recall p99 exceeds exactly 10us, or total recall throughput falls below 1M probes/s under the required workload. Disk-backed cold storage is presumed disallowed by that bar.

**H9.** The remaining waste is likely bit width and alignment. Conditional layout: retain a 16B slot (`id:u32`, packed lifecycle/strength/clock:u32`, `value:i64`), and encode each audit entry in 12B: `word0` contains `op:2`, `slot:24`, `rc:6`; `word1` packs `b1..b5` and `a1..a3` as 4-bit values; `word2` packs `a4,a5,stage,d1,d2` using the remaining bits. This assumes those fields stay within the stated ranges. Expected saving is 4–8B/fact, yielding roughly 28–32B/fact. Install gains from lower bandwidth; recall gains slightly from cache density. **KILL BAR:** any required field exceeds its assigned range, or measured audit overflow/escape records exceed 0.5B/fact.

**Ranking, bytes saved per risk**

1. H7: ~8B, medium risk  
2. H9: ~4–8B, medium-high risk  
3. H8: ~12–18B average, high latency risk  
4. H1: unscorable; definition absent  
5. H2: unscorable; definition absent  
6. H3: unscorable; definition absent  
7. H4: unscorable; definition absent  
8. H5: unscorable; definition absent  
9. H6: unscorable; definition absent  

H1–H6 cannot be meaningfully ordered from the supplied layout. A compatible H7+H9 stack estimates **~24–28B/fact**. H8 can reduce this to approximately **18–24B/fact** only if its measured latency bar passes.
