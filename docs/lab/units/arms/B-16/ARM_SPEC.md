# ARM_SPEC.md — B-16 (Fixed-size chunks, S=16), family CTRL

**Status:** FROZEN PREREG build. Prereg commit `b0b9140c0eda`, branch `tnn-native-lab`.
**Crew:** ARM CREW B-16, Track A representation bake-off.
**Classification:** non-ID layer (ARM_INTERFACE.md §9 provisional list: `b16`).
Chunk ID = index arithmetic, no stored ID→storage mapping → M1 swap probe
`N/A (no ID layer)`, M7 `N/A (no ID layer)` + informational re-read-bytes footnote.

## 1. Mechanism (prereg §3, verbatim)

> Aligned blocks of size 16; chunk ID = index (no table). Isolates "does
> boundary placement matter, or just existence?"

The stream is tiled into aligned 16-byte blocks: chunk `k` covers bytes
`[k*16, (k+1)*16)`. Unit ID = `(corpus_id << 24) | k` — pure arithmetic, no
chunk table. A memory entry holds one chunk's `(offset, len, corpus)`; recall
re-reads the retained corpus buffer at the recorded span. Organs (2), (3), (5)
idle — boundaries are imposed by fiat at time zero, never hypothesized or
revised. No `CUT_*` audit ops are ever emitted; the ledger sees only standard
memory ops (`ADD_UNIT` with `d1=chunk_index`). An optional per-slot
`use_count` is not maintained — B-16 keeps no reuse stats at all (stats arrays
exist only "for M3 reporting" in the design; the harness computes M3 from the
ledger, so B-16 omits them).

## 2. What this arm is

- **Control, not contender.** Same role as B-64 (the harness validator): prove
  the harness measures what it claims, and give the other B sizes a
  granularity point on the tradeoff curve (P-B3: B-64 dominates on M2, B-16/B-8
  on fine-grained recall).
- **Unit = chunk.** Every metric ingests and recalls 16-byte chunks. A 64-byte
  probe span = four B-16 IDs (design doc §B). The M3 churn phases ingest fresh
  *chunks* (16B each), so the fresh byte range is `churn_fresh.bin[0:48000]`
  rather than the `[0:192000]` the interface text quotes for the 64-byte-chunk
  validator — see AMBIGUITIES-B16.md B16-A1. The schedule *structure* (3,000
  ingests / 3,000 kills / 4,000 at-capacity ingests, V=1,000 every k-th,
  50 weakens, last-500-fresh sample, C_M3=4,000) is identical to the
  validator's literal implementation.

## 3. Implementation

Single source: `cl/arm.zag` (entry `fn main()i32`), pure Zag, zero RNG in any
decision path. Substrate: verbatim `R33_NATIVE_SHA256_V2.zag` +
`R33_NATIVE_IO_V1.zag`. One binary; `argv[1]` selects the trial mode
(ARM_INTERFACE.md §3 mode table, `-1x` suffixes); `argv[2]` corpus root;
`argv[3]`/`argv[4]` outdir/perturbation for `m8-1x` only.

Data structures (per instance):
- Seven `cap × u32` slot arrays: ids, offs, lens, corps, flags, shifts, pidx
  (28 B/slot) + insertion-order queue (`ins_cap × i32`). Slot placement =
  multiplicative hash of the unit ID with linear probing — a pure function of
  the ID (order-independent; the M8 `freelist` perturbation is a verified no-op).
- Audit ledger: 16-word (64B) entries, frozen opcode namespace. **Sharded**
  (8 × 262144 entries = 16MB/shard) because B-16's M8 ledger (~950k entries,
  ~60MB) exceeds the znc 2^25 per-slice indexing limit. See §5.
- Flags: OCC/LIVE/PIN/WEAK/SHIFT/PATCH (documented policies: weaken = audited
  annotation, never touches bytes; eviction = FIFO oldest-unpinned; trainer
  defect ops recorded and reconciled by `revise` via flag-clear after probing).

Op semantics (interface §5 vocabulary): `ingest` = deliberate add (loud
`REFUSE` rc=1 when full); `recall(id)` resolves ID→slot→bytes live through the
slot hash; `kill` = tombstone (ID never reused); `pin`/`promote` = valuable
marking (B-16's mechanism: pin); `weaken` = processed annotation; `revise` =
drop recorded shift/patch after verifying against source (same ID + `REVISE`
entry; kill+re-add never used); `trainer_defect_boundary/content` =
external ops, logged; `trainer_mark_valuable` = pin; `evict` = FIFO
oldest-unpinned, audited.

## 4. Determinism

- No RNG, no wall-clock, no pointer-keyed maps, all-integer arithmetic,
  index-order iteration. Global tie-break irrelevant (placement is ID-derived).
- Ledger fields contain no addresses/clocks. Alloc trace logs `A <size>` /
  `F <size>` only (perturbation-induced raw allocs bypass the trace).
- Every battery leg runs twice with stdout diffed; M8 runs 5 perturbations ×
  2 reruns with byte-exact artifact comparison (K-DET gate).

## 5. Deviations from the b64 validator (all forced, all documented)

1. **Ledger sharding** (8 × 262144-entry shards): forced by the 2^25 indexing
   limit. `b_led` routes by `(led_n >> 18, (led_n & 0x3FFFF) * 64)`; beyond
   capacity → silent `LEDGER-BOUND` drop (dead code in practice: M8 sizes
   2,097,152 entries).
2. **M8 `ledger_chain.txt`** = `sha256(concat of per-shard sha256(used bytes),
   shard order)` instead of `sha256(whole ledger bytes)` — same limit.
   M8 compares each arm only against itself (C13), so this is gate-safe.
3. **M8 `store_hashes.txt`**: chunk digests taken per slot-array in ≤2^20
   windows, chunk indices sequential across the 8 arrays in fixed order
   (ids, offs, lens, corps, flags, shifts, pidx, ins); chain =
   `sha256(concat of chunk digests)` exactly as the validator. Satisfies the
   contract's "one line per ≤2^20 chunk of the raw slot-region bytes" with
   window boundaries aligned to array starts.
4. **M3 fresh units are 16B chunks** (B16-A1): byte range `[0:48000]`, not
   `[0:192000]`. Unit-count schedule identical.

## 6. Kill criterion (binding, prereg §3)

- **Retirement:** B-16 retires from future batteries when another B size
  strictly dominates it on M1, M2, and M3 on both corpora.
- **Family kill:** B as a family is killed as a contender the moment any smart
  arm beats the best B size by ≥2x on M3 at equal-or-better M1. (Evaluated by
  the coordinator across arms; not decidable from this arm's row alone.)

## 7. Files

- `cl/arm.zag` — the arm (this spec's implementation)
- `substrate/` — verbatim R33 copies
- `ARM_SPEC.md` (this file), `BUILD_LOG.md`, `AMBIGUITIES-B16.md`,
  `VERDICT.md`, `scorecard_r1_1x.json`, `logs/` (raw battery logs) — all at the
  arm root, mapping to repo `docs/lab/units/arms/B-16/`
