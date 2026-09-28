# K3 — Content+Position Hybrid Identity Arm

## Identity

- **Arm ID:** K3
- **Family:** IDENT
- **Name:** Content+position hybrid
- **Frozen spec:** `~/workspace/tnn-lab/units/arms/briefs/K3.json` (commit b0b9140c0edaf6fc678edea9e9fd4bf9cf485aca)
- **Mechanism:** Composite both schemes are secretly asking for: content-payload + position-reference. Third arm in the K-vs-L bake-off.

## Authority

Per coordinator correction 2026-09-21:
1. `~/workspace/tnn-lab/units/arms/briefs/K3.json`
2. Coordinator's verbatim frozen §3 row
3. Nothing else previously written by the coordinator

The brief and verbatim row agree. The original "self-describing IDs / literal headers / ID IS the chunk" dispatch is **void**.

## Identity Model

A unit's identity is the PAIR `(id_content, id_pos)`:

### Position Component (id_pos)
- **Format:** `(stream, seg, off)` — position records, eternal
- **Encoding:** `position_id = (corpus << 24) | unit_index`
- **Properties:**
  - Never reused (eternal)
  - Segment-sealed at ingest end
  - Re-ingest of the same position revives the same record
- **What recall() takes:** The position ID (what the caller holds)

### Content Component (id_content)
- **Format:** SHA-256(span) — 32-byte content digest
- **Storage:** Dedup table owns the bytes; identical spans share one payload record
- **Refcounted:** Payloads track reference counts
- **Properties:**
  - Content-addressed (not position-addressed)
  - Deduplicated across the entire store

### The Hybrid
- **Payloads** are content-addressed (dedup table keyed by SHA-256)
- **References** are position-addressed (slot table keyed by position ID)
- **Revision:** Re-points a position record to a new payload; emits `OP_REVISE_LINK`
- **Lookup:** `recall(pid)` → slot → payload → bytes

## Chunking

- **Fixed 64-byte grid** (inherited from B-64; the bake-off is about IDENTITY, not segmentation)
- Unit `i` of corpus `c`:
  - `position_id = (c << 24) | i`
  - `span = [i*64, min(i*64+64, len))`

## Data Structures

### Slot Table (Position → Payload)
- **Key:** Position ID (`pid`)
- **Value:** Slot index
- **Fields per slot:**
  - `pids`: Position ID
  - `offs`: Byte offset in source
  - `lens`: Byte length
  - `corps`: Corpus ID
  - `flags`: Live/dead/patched bits
  - `shifts`: A15 probe shift amount
  - `pidx`: Payload index
  - `pays`: Payload handle
  - `dgs`: Cached SHA-256 digest (32 bytes)
- **Hash:** `slot_hash(pid) = (pid * 2654435761) % cap`
- **Probing:** Linear probe

### Dedup Table (Content → Payload)
- **Key:** SHA-256 digest (32 bytes)
- **Value:** Payload index
- **Fields per entry:**
  - `dt_dg`: Digest bytes (32)
  - `dt_pay`: Payload index
  - `dt_ref`: Reference count
  - `dt_occ`: Occupied flag
- **Hash:** `dt_hash(w0) = (w0 * 2654435761) % dt_cap` (w0 = first digest word)
- **Probing:** Linear probe with digest comparison + byte-confirm

### Payload Store
- **Fields:**
  - `pay_bytes`: Payload data (64 bytes max per payload)
  - `pay_lens`: Payload length
  - `pay_dt`: Dedup table index
  - `pay_free`: Free list
- **Allocation:** `pay_alloc()` from free list or bump pointer
- **Release:** `pay_release()` decrements refcount, frees if zero

### Audit Ledger
- **Entry size:** 16 words (64 bytes)
- **Layout:** `op@0, slot@4, rc@8, b1..b5@12..28, a1..a5@32..48, stage@52, d1@56, d2@60`
- **Ops:** `OP_INGEST`, `OP_REVISE_LINK`, `OP_SEAL`, `OP_SCAN`, `OP_REFUSE`, `OP_TDC`, etc.

### A15 Swap Probe Patches
- **Capacity:** 256 patches (fixed)
- **Each patch:** 64 bytes (XOR-masked payload)
- **Purpose:** Provisional A15 64-remap ID-swap schedule (see Ambiguities)

## M1–M8 Modes

### M1: Recall & Boundary
- Ingests corpus (prose or code)
- Probes 64 positions for recall correctness
- Measures boundary detection (first/last byte of each chunk)
- **A15 probe:** Patches ID layer so probed pid resolves to (slot+1); verifies side-channel

### M2: Multi-Corpus
- Ingests t1_prose, t1_code, t2_prose, t2_code, t3
- Tests cross-corpus identity isolation

### M3: Churn
- Ingests prose + code, then churn_fresh
- Tests revision and link re-pointing

### M4: Recall by Content
- Ingests prose and code
- Tests content-based lookup

### M5: Cost/Audit
- Measures slot table bytes, ledger bytes, allocation trace
- Baseline mode: empty store, spin 300M cycles

### M6: Dedup
- Ingests t1_prose and t1_code
- Measures deduplication ratio

### M7: Edit & Lookup
- Ingests prose, performs edits, verifies lookup
- **Note:** Edit schedule unfrozen (see Ambiguities A7/A8)

### M8: Determinism Gate
- 5 perturbations × 2 runs each
- Perturbations: clean, frag, aslr, starve, freelist
- Requires byte-identical artifacts across all 10 runs
- **Mode:** `m8-1x <cdir> <outdir> <perturbation>`

## Bake-Off Metrics (K vs L)

K3 competes against pure schemes K1 and L1 on 5 identity-bake-off metrics. If K3 beats both on ≥3/5, K3 becomes the identity substrate and the pure schemes become components. If K3 loses, it dies as a candidate.

**Note:** The 5 specific metrics are defined in the frozen prereg. Sibling K1/L1 results are required for final verdict.

## Implementation Notes

### Allocator
- `halloc(s, n)`: Traced allocator; logs every allocation to 4MB trace buffer
- `nio_alloc(n)`: Substrate allocator; max 32MB per allocation (enforced)
- All large arrays explicitly initialized (no reliance on zeroed memory)

### SHA-256
- Pure Zag implementation (`R33_NATIVE_SHA256_V2.zag`)
- Called per 64-byte unit during ingest for content ID
- **Performance note:** This is the dominant cost; see BUILD_LOG.md

### Determinism
- Zero RNG in all paths
- Byte-identical reruns required
- Allocation trace ensures deterministic layout

## Ambiguities (Frozen)

- **A15:** Provisional 64-remap ID-swap schedule; scorecard marked `PROVISIONAL-PENDING-FREEZE`
- **A7/A8:** M7 edit and lookup schedules unfrozen
- **A17:** M8 large-capacity interpretation uses combined M1+M3 (provisional)
- **Scorecard:** Frozen `scorecard_assemble.py` is B-64-specific (hardcodes arm, M1 probe N/A, M7 null)

## Corrections Acknowledged

1. **First correction (2026-09-21):** Replaced erroneous "self-describing IDs / literal headers / ID IS the chunk" dispatch with content+position hybrid. The original dispatch and recall/swap kill bar are void.
2. **Second correction (2026-09-21):** Established authority order: (1) `K3.json` brief, (2) coordinator's verbatim frozen §3 row, (3) nothing else. The earlier §3 quote was a memory paraphrase, not verbatim.
