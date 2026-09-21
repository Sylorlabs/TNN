# C-W — Delimiter chunks (whitespace) — Arm Specification

Family: CTRL (control arm). Track A representation bake-off, round r1, scale 1x.
Worktree: `units/arms/C-W/` (implementation: `cl/arm.zag`, substrate:
`substrate/R33_NATIVE_IO_V1.zag`, `substrate/R33_NATIVE_SHA256_V2.zag`).
Pure Zag, zero randomness, byte-identical reruns.

## 1. Mechanism (frozen prereg §3, quoted)

> "One deterministic scan; C-W cuts at whitespace/newline. Maximal runs become
> chunks (lossless), IDs in stream order. Prices the confound: 'how much of the
> smart arms' win is just rediscovering whitespace?'"

## 2. Chunking rule (literal implementation)

- One left-to-right scan per corpus. Frozen delimiter set: **space (32), tab
  (9), LF (10), CR (13)** — byte-exact, no Unicode handling (corpora are bytes).
- Every **maximal run** of delimiter bytes and every maximal run of
  non-delimiter bytes becomes one chunk. Delimiter runs are chunks too (the
  scan is lossless: concatenating all chunks reproduces the corpus byte-exact).
- Chunk `i` = `[offs[i], offs[i+1])`; `offs` is the (n+1)-entry u32 table built
  by the scan. No chunk is ever empty; no byte belongs to two chunks.
- IDs: `(corpus << 24) | chunk_index`, assigned in stream order. Corpus codes:
  1=prose, 2=code, 3=t1_prose, 4=t1_code, 5=t2_prose, 6=t2_code, 7=t3,
  8=churn, 9=fresh. IDs are positional arithmetic, not stored keys.

Measured chunk counts (r1 corpora, independent python rescan matches exactly):

| corpus | bytes | chunks | max chunk len |
|---|---|---|---|
| prose | 5,422,721 | 1,926,956 | 63 |
| code | 9,515,341 | 2,446,768 | 239 |
| t1_prose | 542,273 | 191,612 | 33 |
| t1_code | 951,535 | 230,320 | 84 |
| t2_prose | 4,436,268 | 1,643,028 | 19 |
| t2_code | 225,065 | 53,386 | 133 |
| t3 | 1,048,576 | 25,009 | 1,047 |
| churn_fresh | 448,000 | 146,993 | 145 |

## 3. Store layout

Open-addressed hash table over 7 parallel u32 arrays
(`ids, offs, lens, corps, flags, shifts, pidx`), capacity chosen per mode.
`pidx[slot]` = patch index when the `F_PATCH` flag is set, -1 otherwise;
occupancy is the `F_OCC` flag bit. `cw_init` explicitly zeroes `flags`/`ids`
and sets `pidx` to -1 over all `cap` slots, so slot placement never depends
on heap garbage (znc does not reliably zero fresh heap; the M8 `frag`
perturbation deliberately reshuffles it).
Hash: `x = id*2654435761; x ^= x>>16; x *= 2246822519` (wrapping i32),
linear probe from `h mod cap`. Full table: `slot_insert` returns -1 and the
caller evicts the oldest unpinned unit (FIFO by insertion queue) and retries.

- `ingest`: deliberate add of one unit; logs `ADD_UNIT` (op 0x01, d1 =
  chunk_index, d2 = 0, b1..b5 = first 5 stored words, stage = 1).
- `recall`: exact byte compare of the stored span against the corpus; returns
  length on full match, 0 on miss.
- `kill`: clears the slot, logs `KILL` (0x02). `pin`: sets flag bit 1, logs
  `PIN` (0x03). `weaken`: audited annotation only (op 0x04); does not alter
  stored bytes. `promote`: logs `PROMOTE` (0x09). `revise`: clears
  trainer-planted `shift`/`patch` fields, preserves the unit ID, logs
  `REVISE` (0x0A).
- Eviction: oldest unpinned first (insertion queue); pinned units are never
  evicted by the arm. Force-pins are external/trainer operations.

## 4. Non-ID classification (frozen)

Per `ARM_INTERFACE.md` §9, `cw` is provisionally **non-ID**: chunk IDs are
positional arithmetic and the arm keeps no persistent ID→storage mapping that
outlives the positional computation (lookup is by unit key through the hash
table, but the ID itself encodes corpus+index, so no ID layer exists to attack).
Consequences, implemented literally:

- M1 ID-swap probe: N/A (nothing to swap; note recorded in code).
- M7: hit rate / reuse rate / dedup savings all N/A (`null`); the arm reports
  `m7_reread_bytes` = total bytes re-read across the 5,000 deterministic
  lookups `(l*37) % n`, plus the every-100th-chunk trainer-edit round whose
  byte patches are stored in the patch area and audited.

## 5. Audit ledger (§6 opcodes)

One 64-byte entry per deliberate op: `op, slot, rc, b1..b5, a1..a5, stage,
d1, d2` (all little-endian u32). Opcodes used: `ADD_UNIT` 0x01, `KILL` 0x02,
`PIN` 0x03, `WEAKEN` 0x04, `PROMOTE` 0x09, `REVISE` 0x0A, `REFUSE` 0x08,
`EVICT` 0x0B. `SCAN_COMMIT` (0x07) is **not** used: the arm's deliberate op is
the per-chunk ingest and the ledger records every exercised op (§5), keeping
M5 comparable with the B-64 validator's per-unit ADDs. See AMBIGUITIES-CW.md.

**Ledger sharding (build note, not a prereg change).** `nio_alloc` refuses any
single slice over 2^25 bytes (33,554,432) and returns an empty slice, so a
monolithic ledger (123 MB for M1-prose) is impossible. The ledger is 16 shards
of 500,000 entries (32,000,000 bytes each, 8M entries / 512 MB max). Shard
count per mode derives from the sized entry capacity; the logical entry order
is unchanged and every consumer (M3 liveness scan, M5/M8 `ledger.bin` writes,
M8 ledger hash) walks shards in order. Semantics are identical to one flat
ledger.

## 6. Mode implementations

- **M1** (`m1-1x-prose|code`): ingest all chunks, probe all chunks, recall all
  chunks. Reports recall/boundary in tenths of a percent, unit count.
- **M2** (`m2-t1|t2-prose|code`, `m2-t3-1x`): 50-episode loop, 3-consecutive-100%
  stop. Episode 0 probes the empty store (expected 0%), then ingests the full
  tier, then probes. ETC is 1 mechanically (the store is exact). T3 ingests
  the 25,009 synthetic chunks. Emits the M9 curve for t1 tiers.
- **M3** (`m3-1x`): V = 1,000 valuable chunks (every k-th over prose+code),
  ingested and pinned; phase 1: 3,000 fresh 64 B ingests; phase 2: 3,000
  fresh-only kills; 50 weaken annotations on every 20th valuable; phase 3:
  4,000 ingests at capacity 4,000 with oldest-unpinned eviction. Measures
  survival of valuable (bar ≥ 90.0%), fresh recall of the last 500
  (bar ≥ 80.0%), liveness = management-op count in ledger window [n_p1, n_p3)
  (bar ≥ 700), and the freeze tripwire (CLEAR vs FROZEN-UNDER-PRESSURE).
- **M4** (`m4-1x-prose|code`): ingest the corpus, plant 100 boundary defects
  (cyclic ±1..±32 shifts) and 100 content defects (xor/rename patches), then
  up to 20 revision episodes (revise all 200, verify; stop when all verified).
  Reports boundary/content revision tenths, kill rate, and the kill-substitution
  flag.
- **M5** (`m5-baseline`, `m5-1x`): learns prose (n + 500 fresh ingests, 500
  kills), reports units/KB (bar ≥ 3.0), audit entries/KB (bar ≤ 10), ledger
  bytes and entries; writes `ledger.bin`.
- **M6** (`m6-p2c-1x`, `m6-c2p-1x`): train on one corpus (3 episodes or to
  95%), transfer to the other; reports recall/boundary/revision tenths and the
  transfer tax; the memorizer control runs the same legs via `mem_bin`.
- **M7** (`m7-1x`): non-ID path (see §4).
- **M8** (`m8-1x`, N=5 adversarial gate): full M1+M3 on prose+code plus 500
  fresh units, kills, weakens. Artifacts per run: `store_hashes.txt` (one
  `chunk<i> <hex>` line per 1 MB logical chunk of the slot-region stream:
  ids, offs, lens, corps, flags, shifts, pidx, then the insertion queue),
  `store_chain.txt`, `ledger.bin` (shard-order), `ledger_chain.txt`,
  `alloc_trace.txt`. The slot region is hashed **without materialising** the
  171 MB image (1 MB staging buffer walks the 8 arrays in fixed order); the
  ledger hash is staged the same way (`ns_sha256` caps input at ~33.5 MB).
  Stdout (`M8,<m1p>,<m1c>,<ledger_entries>`) is perturbation-agnostic.

## 7. Determinism

Zero RNG in the binary (no RNG substrate is even linked). All iteration is
index-ordered; eviction is FIFO; the allocation trace records only the arm's
own `halloc` calls (untraced scratch uses raw `nio_alloc`). Slot-table
`flags`/`ids` are explicitly zeroed at init so placement cannot depend on
heap garbage. Every battery leg runs twice with stdout diffed; M8
additionally requires byte-identical artifacts (`store_hashes.txt`,
`store_chain.txt`, `ledger.bin`, `ledger_chain.txt`, `alloc_trace.txt`,
`stdout.txt`, `stderr.txt`) across all 10 runs (5 perturbations × 2 reruns) —
the perturbations (heap fragmentation, 1.2 MB ASLR pad, entropy/clock
starvation, freelist order) must not change any artifact byte.

## 8. Known toolchain constraints honoured

- No slice over 2^25 bytes is ever allocated or indexed (ledger sharding §5,
  1 MB hash staging §6, per-mode capacity review).
- Struct slice fields are aliased to locals before indexed access
  (`w.*.field[i]` codegen rule).
- `_zag_arg` results are never freed; `_zag_strcmp` == 1 means equal.
- Battery workdirs live under `~/workspace` (`/tmp` is a 512 MB tmpfs).
