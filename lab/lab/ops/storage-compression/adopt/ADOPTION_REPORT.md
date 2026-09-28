# S5 Default Adoption Report

**Date:** 2026-09-23  
**Status:** CANONICAL S5 STORE PROVEN AT 1M SCALE

## What was built

The canonical S5 default store: `ops/storage-compression/adopt/s5_store.zag`
(824 lines, pure Zag, zero RNG). It implements the trial's S5 design with
production-hardening for the mutation paths the trial did not test.

**S5 components (from trial):**
- **S3** — Dense identity: `id == slot`, no index.
- **S4** — Derived audit: successful adds reconstructible from ordered slots;
  only non-derivable events (revises, deletes, failures, episodes) logged.
- **S5** — Width-tagged values: 1/2/4/8 bytes per value from chunk (min,max).

**Production hardenings (new in this implementation):**
1. **Flat manifest, not hash chain.** The trial's chained hash
   (`chain[c] = H(chain[c-1] || chunk_c)`) makes sealed-chunk mutation O(tail):
   revising chunk 0 of 245 re-hashes ~5MB. The flat manifest
   (`chash[c] = SHA256(chunk_c)`, `seal = SHA256(chashes || events || metadata)`)
   preserves the tamper-evidence property (byte modification, reorder,
   truncation, event-log tamper all detected) with O(chunk) mutation.
2. **Deferred hashing.** Chunk hashes are recomputed in bulk at `sc_seal_final`,
   not on every revise/delete. (The pure-Zag SHA256 does ~375KB/s; per-mutation
   rehashing made 100k revises take 7+ minutes. Bulk rehash: 45s for the full
   1M workload.) Contract: manifest valid only after seal; bytes are truth.
3. **20-byte event records** (not 16). Revise head/cont carry 17 bytes of
   payload; 16B records overflowed by 1 byte (found by testing, fixed).
4. **Explicit revise/delete semantics** with tombstones, width-overflow
   reseal, and a replay-consistency checker.

## 1M-scale proofs

### Add-only (trial parity)
```
N=1,000,000, cslots=4096, profile=T
written_bytes=5,009,177 → 5.01 B/fact
manifest_verify=0, replay_check=0
```
Beats the trial's 5.53 B/fact (less overhead in the canonical implementation).

### With mutation (production path)
```
N=1,000,000, 100,000 revises, 50,000 deletes
written_bytes=9,994,057 → 9.99 B/fact (10.52 per live fact)
manifest_verify=0, replay_check=0
tamper: slot_byte_flip→1, event_byte_flip→2, restored→0
failure probes: all correct (dupe→1, absent→1, double-delete→2, ...)
```
**9.99 B/fact vs 92 B/fact baseline = 9.2× smaller**, with full revise/delete.

### Determinism
Two 1M runs: byte-identical digest (`3c42dc7408a88fe3`) and seal
(`cd612dba...`). Zero RNG; splitmix64 workload.

### Chunk equivalence
cslots=512 vs cslots=4096, N=2000, identical digests (`5f7974c96b5fedd5`).
Logical state is chunk-size-independent.

### Width overflow
Revise forcing a value outside the chunk's tagged width triggers
re-seal at a wider width; manifest and replay remain consistent.
(Honest cost: adversarial overflow forces w=8 → 17.1 B/fact on that workload.)

### Mixed widths
Profile M (heavy tail): 17.02 B/fact at 10k, all checks pass.

## B/fact summary

| Workload | B/fact | vs 92 baseline |
|----------|--------|----------------|
| Add-only, small ints (trial-like) | 5.01 | 18.4× |
| +10% revise, +5% delete | 9.99 | 9.2× |
| Mixed widths (heavy tail) | 17.02 | 5.4× |
| Adversarial width-overflow | 17.11 | 5.4× |

## What "default" means

The canonical S5 store in `ops/storage-compression/adopt/` is the reference
implementation for TNN fact storage. New storage work should use it.

## NOT done: live driver integration

`scale/driver/scale_learner.zag` (1163 lines) still uses the old layout
(24B slots, dense index, 16-word audit, 92 B/fact). Integrating S5 requires:
1. Resolving the `ScStore` name collision (both files define it).
2. Porting the learner's storage calls to the S5 API.
3. Regression-testing the full learning path.

This is planned but was not attempted here — a hasty port of a working
1163-line driver risks regressions. The proven canonical store is the
prerequisite; integration is the next step.

## Files

- `ops/storage-compression/adopt/s5_store.zag` — canonical store
- `ops/storage-compression/adopt/workload.zag` — proof driver
- `ops/storage-compression/adopt/R33_NATIVE_SHA256_V2.zag` — hash (copied)
- `ops/storage-compression/adopt/R33_NATIVE_IO_V1.zag` — IO (copied)
- `ops/storage-compression/adopt/ADOPTION_REPORT.md` — this file

## Reproduce

```bash
cd ops/storage-compression/adopt
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 workload.zag -o workload --no-analyze
./workload 4096 1000000 0 42 0 0   # add-only, expect 5.01 B/fact
./workload 4096 1000000 0 42 0 1   # with mutation, expect 9.99 B/fact
```
