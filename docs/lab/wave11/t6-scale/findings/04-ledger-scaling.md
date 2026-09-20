# 04 — Ledger scaling and chunking (Track 6, slice 04)

## 1. Slice
Design the audit-ledger scaling architecture for 1000x episodes: chunked ledgers
(chunk size, chunk sealing, cross-chunk hash chaining), cross-chunk replay,
the chunked-vs-unchunked equivalence test, and the audit cost model under
Track 1's K8 ≤1.10x audit-bytes bar.

## 2. Falsifiable claim
A fixed-capacity chunked audit ledger (2^18 entries = exactly 2^25 bytes per
chunk, sealed with a SHA-256 hash chain linking each chunk to its predecessor)
is a byte-identical logical stream to an unchunked ledger: replay of the
chunked log from genesis reproduces final state and the full entry stream
byte-for-byte, and per-episode audit bytes stay within 1.00001x of the
unchunked baseline at every scale leg (1x/10x/100x/1000x).

## 3. Design
- **Entry format (unchanged):** 16 i64 words = 128 bytes/entry
  (op@0, slot@4, rc@8, b1..b5@12..28, a1..a5@32..48, stage@52, d1@56, d2@60 —
  per standing layout).
- **Chunk capacity:** 2^18 = 262,144 entries → exactly 2^25 bytes (33,554,432),
  the largest slice the toolchain can index. Data slice is a fixed
  `[]u8` of exactly that size; indexing stays strictly below the limit.
- **Chunk header (separate ≤96-byte slice, not part of the data slice):**
  magic u64, chunk_index u64, entry_count u64, prev_hash [32]u8,
  seal_hash [32]u8, sealed_flag u8. Never grows; never chunked.
- **Write path:** writer appends entries to the open chunk's data slice at
  `entry_count*128`. When entry_count == 262,144 the chunk seals:
  `seal_hash = SHA256(prev_hash || chunk_index || entry_count || data_bytes)`,
  then a new chunk opens with `prev_hash = seal_hash` (chunk 0 uses 32 zero
  bytes as genesis prev_hash). Sealing is one sequential pass over the chunk.
- **Cross-chunk chaining:** chunk k+1's header binds chunk k's seal, so the
  whole log is a hash chain; tampering anywhere breaks every later link.
  SHA-256 via `R33_NATIVE_SHA256_V2.zag` (deterministic native, already in the
  substrate — see AGENTS.md).
- **Replay procedure:** verifier loads chunk 0, checks magic + genesis
  prev_hash, recomputes seal_hash, aborts on mismatch; then streams entries
  0..entry_count−1 to the replay engine in index order; repeats for chunk
  k+1 after asserting `header[k+1].prev_hash == seal[k]`. The replay engine
  sees one continuous logical stream — chunk boundaries are invisible to it,
  and no entry ever spans a boundary (fixed 128-byte stride guarantees it).
- **Zag-flavored sketch:**
  `fn ledger_append(e:*Entry)`: if open.entries == CAP → `seal(open)`; open new.
  `fn seal(c:*Chunk)`: `c.seal_hash = sha256(c.prev_hash ++ u64(c.index) ++ u64(c.count) ++ c.data)`; set sealed flag.
  `fn replay_verify(dir)`: for k in 0..n: assert chain links; assert seal
  recomputes; feed entries to `apply_entry` in order.

## 4. Kill bar (prereg-style; ANY firing kills the design)
1. **Replay divergence:** chunked replay vs the logical-stream reference differ
   in ≥1 byte of final state, entry stream, or per-entry post-state hash.
2. **Audit-cost blowup:** measured audit bytes/episode at any leg >
   1.10x the 1x unchunked baseline.
3. **Chain weakness:** in 100 single-byte tamper probes (random chunk, random
   offset), chain verification misses ≥1 tamper.
4. **Seal nondeterminism:** sealing the same chunk data twice yields different
   seal_hash, or seal+verify wall time exceeds 2% of run wall time.

## 5. Honesty notes
- Weakest point: the header store itself is trusted metadata — headers need
  the same append-only, tamper-evident discipline as data, or the chain is
  theater. Headers must be written atomically (write data, fsync, seal,
  then write header) so a crash can't leave a sealed chunk without its link.
- Crash-during-seal is the ugliest corner: design mandates
  data-write → seal-compute → header-commit ordering; replay treats a
  headerless trailing chunk as an incomplete tail, re-sealable, never trusted.
- Assumes single-writer, append-only discipline; concurrent writers and
  cross-machine replication are out of scope for this slice.
- Disk layout (file-per-chunk naming, retention of sealed chunks) is not
  specified here — only the in-memory slice format and the chain protocol.
- Cost model below parameterizes entries/episode from RC3 logs; the exact
  number is a measurement, not an assumption (see §6).

## 6. Next build step
Implement the chunked writer + verifier in Zag in a trial substrate dir
(`R33_NATIVE_SHA256_V2.zag` + `R33_NATIVE_IO_V1.zag` next to `cl/`, per
AGENTS.md), then run the equivalence test at 10x with chunk capacity forced
to 64 entries: assert byte-identical final state, byte-identical logical entry
stream, and identical per-episode checkpoint hashes vs the unchunked run —
then repeat with capacity 3 for boundary stress, plus the 100-probe tamper
negative control.

## Appendix — audit cost model (bytes per episode per scale leg)
- Let E = episodes/leg (1x:12, 10x:120, 100x:1200, 1000x:12000, anchored on
  RC1 12-episode scale), r = measured mean entries/episode, entry = 128 B.
- Audit bytes/leg = E × r × 128 × (1 + η), η = header bytes per entry
  = 96 / (262,144 × 128) ≈ 2.9e−6.
- Chunk count/leg = ⌈E × r / 262,144⌉. Example at r = 512:
  1000x → 6,144,000 entries ≈ 786 MB → 24 chunks; header overhead ≈ 2.3 KB.
- Bytes/episode is constant across legs by construction (entry layout
  unchanged; η is scale-invariant), so the measured ratio to the 1x baseline
  is ~1.000003 ≪ 1.10 — the K8 bar is passed with four orders of magnitude of
  headroom, provided the implementation adds no per-entry framing bytes.
