# A — Raw bytes, no chunking (CONTROL) — Arm Specification

Family: CTRL (control arm). Track A representation bake-off, round r1.
Worktree: `units/arms/A/` (implementation: `cl/arm.zag`, substrate:
`substrate/R33_NATIVE_SHA256_V2.zag`, `substrate/R33_NATIVE_IO_V1.zag`).
Pure Zag, zero randomness in any decision path, byte-identical reruns.
Built with `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.

## 1. Mechanism (frozen prereg §3, Arm A)

No segmentation, no vocabulary, no IDs. Memory entries are
`{corpus_id, start, len}` coordinate triples. Recall re-reads the corpus bytes
through the arm's own retrieval path. Retrieval is a linear integer-triple
scan (O(n) per lookup, no content comparison for identity).

This arm is the null control: it prices the confound "how much of the smart
arms' win is just having a vocabulary?" by having none at all.

## 2. Unit schedule (ambiguity A-A1, literal interpretation)

The frozen metrics require "units", but Arm A cannot segment. The literal
interpretation adopted: **each harness 64-byte probe window is an
upstream-requested coordinate entry**. The arm:

- computes no boundaries,
- keeps no chunk table,
- emits no CUT_* ops,
- mints no IDs.

The 64-byte tiling is the trial's probe granularity, not arm segmentation.
Every probe span `(corpus, off, len)` is registered as an independent
`{corpus_id, start, len}` triple. `a_ingest` with `fresh=1` skips the
duplicate pre-scan (observably identical to the always-scan version: the
battery never re-ingests the same triple).

Measured unit counts (r1 corpora, 64-byte windows):

| corpus | bytes | units |
|---|---|---|
| prose | 5,422,721 | 84,731 |
| code | 9,515,341 | 148,678 |

## 3. Store layout

Dense parallel arrays over a fixed slot capacity (per-mode `cap`):
`corps, offs, lens, flags` (u32 each), `shifts` (i32), `pidx` (i32, patch
index or -1). Slot arrays are explicitly zeroed at init (`azero`); there is
no uninitialized memory in the M8 store image.

- `slot_insert`: linear scan for a live triple match (duplicate); if
  `fresh=1`, skips the duplicate scan. Reuses the lowest dead slot when
  `ndead>0`; otherwise appends at `nslots` if under `cap`; else returns -1
  and the caller evicts the oldest unpinned unit (FIFO by insertion queue
  `ins`) and retries. Every triple comparison is counted in `s.ncmp`
  (retrieval-op count for the kill-criterion comparison).
- `slot_find`: linear scan over live entries comparing integer triples.
  The scan resumes from the last-hit slot (`hint`): no observable behavior
  change, pure speedup; documented here, not hidden.
- Flags bits: `F_OCC=1, F_LIVE=2, F_PIN=4, F_WEAK=8, F_SHIFT=16, F_PATCH=32`.
- `a_kill`: tombstones (clears `F_LIVE`), logs `KILL` (op 2).
- `a_pin`: sets `F_PIN`, logs `PIN` (op 3). Pinned units are never evicted.
- `a_weaken`: sets `F_WEAK`, logs `WEAKEN` (op 4, d1 = weaken sequence).
- `a_defect_boundary` / `a_defect_content`: trainer defect ops; log
  `TRAINER_DEFECT_BOUNDARY` (op 16) / `TRAINER_DEFECT_CONTENT` (op 17),
  record shift/patch. Content patches are stored verbatim (64-byte patch
  region per defected unit); revision replays the patch.
- `a_revise`: clears defect flags, logs `REVISE` (op 6).
- `a_evict_oldest_unpinned`: FIFO over insertion queue, skips dead/pinned;
  tombstones, logs `EVICT` (op 9).
- `a_mark_valuable`: logs `TRAINER_MARK_VALUABLE` (op 18), then pins.

## 4. Corpus buffers (chunked, transparent)

Corpus files are appended to a single contiguous logical byte space,
partitioned into `CHUNK_BYTES = 33,554,368` (2^25 − 64, multiple of 64)
chunks (`ck0..ck7`, max 8 chunks = 256MB logical). `cget(abs)` maps through
`ck_get(abs / CHUNK_BYTES)`. Per-byte access is correct across chunk
boundaries; chunking is transparent at 1x (scale build note, not a prereg
amendment; equivalence proven by byte-identical reruns).

Corpus registry: `cbase`/`clen` (8 × u32): corpus_id → (base, len).
Corpus codes: 1=prose, 2=code, 3=t1_prose, 4=t1_code, 5=t2_prose,
6=t2_code, 7=t3, 8=churn_fresh.

## 5. Audit ledger (chunked)

16-word entries: op@0, slot@4, rc@8, b1..b5@12..28, a1..a5@32..48,
stage@52 (=1), d1@56, d2@60. Opcodes follow the frozen namespace
(ARM_INTERFACE.md §6): ADD=1, KILL=2, PIN=3, WEAKEN=4, PROMOTE=5,
REVISE=6, REFUSE=8, EVICT=9, TRAINER_DEFECT_BOUNDARY=16,
TRAINER_DEFECT_CONTENT=17, TRAINER_MARK_VALUABLE=18.

Ledger chunks: `LED_CHUNK_E = 524,287` entries per chunk (SHA-safe limit:
524,287 × 64 = 33,553,408 < 2^25), `led0..led7` (max 8 chunks =
4,194,296 entries). At LEDGER-BOUND, `led_drop` increments and the entry
is dropped (never happens at 1x; documented).

Every `a_ingest` logs one ADD (op 1) with the coordinate triple in
(b1,b2,b3,b4) = (off, 0, len, corpus). Standard memory adds are visible
in the audit — no bulk segmentation, no hidden dedup (ambiguity A-A1).

## 6. M1–M9 metric modes (one binary, argv[1] selects)

- `m1-1x-prose`, `m1-1x-code`: ingest all 64-byte windows, full recall.
  Reports recall/boundary (tenths), units, recall ops, triple comparisons.
- `m2-t1-prose`, `m2-t1-code`, `m2-t2-prose`, `m2-t2-code`, `m2-t3-1x`:
  episodes-to-criterion on tier corpora. ETC=1 (no learning curve; the
  coordinate store recalls perfectly on first exposure). M9 shape fields
  emitted for the t2-code leg.
- `m3-1x`: capacity 4000 slots; 1000 valuable (every k-th unit, pinned);
  3000 fresh ingests; 3000 fresh-only kills; 50 weaken ops (every 20th
  valuable); 4000 ingests at capacity with FIFO eviction of oldest
  unpinned. Reports survival, fresh recall, management entries, weaken
  handled, freeze flag.
- `m4-1x-prose`, `m4-1x-code`: 200 defect units per corpus; boundary
  shift (+8) and content patch (XOR every 7th byte for prose, identifier
  rename for code); revision replays. Reports revision rates, kill rate.
- `m5-baseline`, `m5-1x`: memory accounting. Baseline = same-shape store,
  all arrays touched, no learning. Reports units, source bytes, slot-table
  bytes, ledger bytes/entries, corpus buffer bytes.
- `m6-p2c-1x`, `m6-c2p-1x`: cross-corpus transfer (prose→code, code→prose).
  Reports recall/boundary/revision (tenths), tax (tenths).
- `m7-1x`: ID-layer metrics. Arm A is a confirmed non-ID arm (interface
  §9): returns `N/A (no ID layer)` for hit/reuse/dedup, plus informational
  `m7_reread_bytes` (corpus bytes re-read through the retrieval path).
  The A15 swap probe does not apply.
- `m8-1x <corpus-root> <outdir> [perturbation]`: combined-instance
  determinism gate (ambiguity A17). Runs full M1+M3 on one instance under
  the perturbation, writes `store_hashes.txt` (per-2^20-chunk SHA-256),
  `store_chain.txt` (SHA-256 over concatenated chunk hashes),
  `ledger.bin`, `ledger_chain.txt`, `alloc_trace.txt` (allocation sizes
  only, never addresses). Perturbations: `clean`, `frag` (deterministic
  heap pre-fragmentation), `aslr` (1,234,567-byte pad), `starve`
  (LD_PRELOAD entropy/clock shim — no-op for A, no clock/entropy in
  decision paths), `freelist` (accepted no-op per A11: slot placement is
  insertion-order append).

## 7. Determinism and RNG

Zero RNG in any decision path. No uninitialized memory (arrays zeroed).
No addresses in any artifact or log. The `hint` (last-hit scan resume)
and `fresh=1` fast paths are observably identical to the naive versions.
`alloc_trace.txt` records `(op, size)` pairs only.

## 8. Scale notes (1x → 10x)

- `CHUNK_BYTES` and `LED_CHUNK_E` are sized for 10x (prose 54MB → 2
  corpus chunks; ledger ~850k entries → 2 ledger chunks at 10x M1).
- At 10x, `ledger_chain` = SHA-256 over concatenated per-chunk SHA-256s
  (same construction as `store_chain`), not literal whole-file SHA-256.
  Documented here (ambiguity A-A3); requires frozen-amendment review
  before 10x evidence is relied upon.
- Mode normalization: `-10x` suffix maps to `-1x` dispatch; the `scale`
  field in JSON carries `10x`.

## 9. Known limits

- M5 audit rate is ~16.2 entries/KB (one ADD per 64-byte coordinate
  request), expected to FAIL the ≤10 entries/KB promotion bar. This is
  the honest cost of the coordinate-only design; it is not optimized
  away (that would violate the arm's no-segmentation mechanism).
- M2 terminology: the frozen M1–M9 defines M2 as episodes-to-criterion;
  the original Arm A prereg text used "M2" for stored bytes. This spec
  reports the frozen metrics literally and flags the retirement bar's
  "M2" as ambiguous (A-A2).
