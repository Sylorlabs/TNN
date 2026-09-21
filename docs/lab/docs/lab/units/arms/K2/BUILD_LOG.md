# BUILD LOG — K2 (64-bit FNV-1a Identity)

**Date:** 2026-09-21
**Builder:** ARM CREW K2 (Track A)
**Source:** `~/workspace/tnn-lab/units/arms/K2/cl/arm.zag` (pure Zag)
**Compiler:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
**Binary:** `~/workspace/tnn-lab/units/arms/K2/work/k2_bin` (native, ~260KB)

## Lineage

The initial implementation used a malformed semantic-ID mechanism. Per the
coordinator's correction, it was deleted and replaced with the literal K2
specification: K1 with `ID = FNV-1a-64(content)`. The void semantic-ID
mechanism is not reported (per coordinator instruction).

## Defects Found and Fixed During Development

1. **Audit field packing (frozen layout violation).** `record_op` wrote
   a1..a5 as 8-byte `qput` at 4-byte spacing (overlapping, clobbering
   stage@52's neighbors). Fixed to 4-byte `iput` per the frozen 64-byte
   layout: op@0, slot@4, rc@8, b1..b5@12..28, a1..a5@32..48, stage@52,
   d1@56, d2@60. Callers passing 64-bit IDs now truncate with `as i32`.

2. **M7 round-2 tail overread (panic).** The else branch computed the tail
   unit length as `n*64 - l*64` (=64) instead of the true remainder (=1),
   reading 63 bytes past the corpus end. Fixed to `bb.len - l*64`, capped
   at 64. Also fixed `bb.*.len` → `bb.len` (bb is a local struct, not a
   pointer; the former is a codegen error).

3. **M6 c2p arena under-sizing (false transfer failure).** The transfer
   trial sized the arena for indomain+transfer only, but the M2-criterion
   tier-training phase ingests novel T1C material (14,868 units, not
   grid-aligned with code.bin, so zero dedup). Arena exhausted mid-transfer
   → ~13k refused ingests → 84.5% transfer recall. Fixed by sizing for
   tier+indomain+transfer.

4. **M2 51-episode ledger exceeded znc 2^25 slice limit (panic).** The
   worst-case 51-episode ledger (227MB for T2-prose) sharded into 2×113MB,
   exceeding znc's 33,554,432-byte per-slice index limit. Fixed: M2 ledger
   sized for 8 episodes (K2 deterministically finishes by episode 3);
   `k2_new` caps all shards at 2^25; `record_op` sets a loud `led_bound`
   flag instead of overflowing silently.

5. **Incomplete true-collision chain search (known limitation).**
   `ingest_with_id` byte-compares only the first same-ID table entry. On
   real corpora there are zero true collisions (chain=1 everywhere), so
   this does not affect battery results. The synthetic `t-collision` test
   exercises the chain path deterministically (chain=3, 2 collisions
   counted honestly). Full chain-walk dedup is future work; flagged openly.

6. **M7 lookup schedule.** Implemented the harness validator's literal
   `(l*37)%n` schedule (the earlier round-offset variant was removed).
   A7/A8 (C′ edit bytes, lookup schedule details) remain as-implemented
   per the validator's conventions, flagged as such.

## Compiler Notes

- ~100 analyzer warnings (ignored return values, possible string-buffer
  leaks). Reviewed: none affect correctness or determinism. All
  `_zag_i64_to_str` results are freed at their use sites.
- znc ZNC-2026-09-21-002/003/004 observed and worked around (no slice→`*u8`
  casts; 16-byte slice fields in malloc sizing; no slice-let off local
  struct values).
- Temporary `DBG m7` prints were added during diagnosis and fully removed.
- `.zag-cache/` and all binaries are excluded from commits.

## Verification

- Byte-verified frozen K2 row from ALPHABET_G-L.md before building.
- All 1× modes run clean (rc=0); see raw logs.
- M8: 5 perturbations × 1 run each (2nd rerun per M-34 N=5 is runs 1–5;
  byte-identical double-run verification via m8_compare.py).
- Corpus hashes verified against CORPORA.md before the battery.
