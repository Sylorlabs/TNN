# ARM C-P Specification — Delimiter Chunks (whitespace + punctuation), family CTRL

**Date:** 2026-09-21
**Arm ID:** C-P (Track A representation bake-off)
**Family:** CTRL (control — deterministic delimiter baseline)

## 1. Segmentation Rule

C-P uses a deterministic one-pass delimiter scan over the raw byte stream.

- **Delimiters:** Whitespace (space `0x20`, tab `0x09`, LF `0x0A`, CR `0x0D`) plus ASCII punctuation `.,;:!?()[]{}"'` (14 bytes: `0x2E 0x2C 0x3B 0x3A 0x21 0x3F 0x28 0x29 0x5B 0x5D 0x7B 0x7D 0x22 0x27`).
- **Chunks:** Maximal runs of non-delimiter bytes become lossless chunks. Delimiter bytes themselves are not stored as chunks (they are implied by chunk boundaries).
- **IDs:** Assigned in stream order: `chunk_id(corpus, idx) = (corpus << 24) | idx`, where corpus is 1=prose, 2=code, 3=t1, 4=t2, 5=t3, 7=fresh/churn.
- **Lossless:** The concatenation of chunk bytes in ID order, with single-byte delimiters reinserted at boundaries, reconstructs the source exactly (verified by byte-diff recall in M1/M2).

**Note on delimiter set:** The frozen prereg/alphabet documents were searched for a definitive punctuation-byte list; none was found with sign-off wording. C-P uses the authorized fallback: whitespace (space, tab, LF, CR) + exactly `.,;:!?()[]{}"'`. No broader set.

## 2. Store

- **Slots:** Open-addressing hash table (FNV-1a 64-bit derived 32-bit index, linear probing). Each slot stores: unit ID, byte offset, byte length, corpus tag, flags (live/pinned/valuable/patched/shifted), shift amount, patch index.
- **Capacity:** M3 uses 4,000 slots (protocol-fixed). Other modes size as `n + n/4 + margin`.
- **Insertion order:** Array of slot indices in insertion order (for eviction).
- **Ledger:** 64-byte entries: op, slot, rc, b1..b5, a1..a5, stage, d1, d2. One `SCAN_COMMIT` per complete deterministic segmentation; individual entries for management ops (pin, kill, weaken, revise, valuable-mark).
- **Patch arena:** Byte buffer for revised content (content defects).
- **Trace:** Allocation trace (halloc/hfree) for M8 determinism evidence.

## 3. Operations

- **ingest:** Scan buffer → chunks → slot_insert each (ID, offset, len, corpus). Logs `SCAN_COMMIT`.
- **recall:** ID → slot_find → read bytes from corpus buffer (or patch arena if patched). Returns length or -1.
- **kill:** Clear `F_LIVE` flag. Logs `KILL`.
- **pin/promote:** Set `F_PINNED`. Logs `PIN`.
- **weaken:** Decrement strength (stored in flags/shift field). Logs `WEAKEN`.
- **revise:** Copy new bytes to patch arena, set `F_PATCH`, record patch index. Logs `REVISE`.
- **trainer defects:** `cp_inject_defect` writes wrong bytes to patch arena (simulates corrupted copy).
- **trainer valuable marking:** `cp_mark_valuable` sets `F_VALUABLE`.
- **eviction:** `cp_evict_oldest_unpinned` scans insertion order for first live unpinned slot, clears it.

## 4. Determinism

- Zero RNG in decision paths. All iteration is in ID order or insertion order.
- Hash table placement is ID-derived (deterministic).
- Byte-identical reruns verified by M8 (5 perturbations × 2 runs).

## 5. M8 Implementation Notes (C-P specific)

Due to delimiter chunking producing 4.48M chunks (vs B64's ~150K 64-byte spans), C-P's M8 uses:

- **Limited ingest:** 200K chunks per corpus (400K total) for the determinism battery. Full recall is covered by M1; M8 tests determinism, not scale.
- **FNV-1a 64-bit** for store segment hashing (instead of SHA-256), because the Zag SHA-256 substrate takes ~3 minutes per M8 run on 168MB of slot tables. FNV-1a is deterministic and sufficient for byte-identical checking. Documented as a C-P-specific optimization.
- **Sparse probe** (stride 10,000) for the M8 sanity check; full probes are in M1.

The 9 store segments (7 slot arrays, insertion array, patch arena used bytes) are each FNV-1a hashed; hashes are chained; ledger and alloc trace are separate artifacts.

## 6. Metrics

- **M1:** recall_tenths, boundary_tenths (per-corpus chunk recall, byte-exact).
- **M2:** episodes, censored, ep0_recall, final_recall, final_boundary (curriculum learning).
- **M3:** survival_tenths, fresh_recall_tenths, mgmt_entries, weaken_handled, freeze, valuable (churn under management).
- **M4:** rev_boundary_tenths, rev_content_tenths, kill_rate_tenths, killsub, episodes (revision under defects).
- **M5:** units_learned, source_bytes_learned, slot_table_bytes, ledger_bytes, ledger_entries, corpus_buffer_bytes (resource pressure).
- **M6:** rec_tenths, bnd_tenths, rev_tenths, tax_tenths (transfer).
- **M7:** hit_rate, reuse_rate, dedup_savings (null: no ID layer), na_reason, reread_bytes.
- **M8:** determinism gate (byte-identical artifacts across perturbations).
- **M9:** shape, takeoff_ep, steepness_tenths, late_gain_tenths (learning curve shape, from M2).
