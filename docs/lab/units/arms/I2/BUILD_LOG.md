# I2 — Build Log

**Arm:** I2 (DAG hierarchy)  
**Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`  
**Source:** `units/arms/I2/cl/arm.zag` (single file, includes hierarchy mode)  
**Date:** 2026-09-21

## Build history

1. **Initial port (02:40 UTC):** Copied validated B-64 arm, applied
   `B64→I2` / `b64→i2` renames. Added ID-remap fields (`rm_on`,
   `rm_id`, `rm_slot`), `i2_resolve`, `OP_TSWAP=19`, provisional M1
   (64 swap probes) and M7 (ID-arm) implementations.

2. **Hierarchy mode v1 (03:00 UTC):** Appended `t_hier` (`i2-hier-1x`
   mode): byte-class span segmentation, FNV span IDs, rolling-hash
   window counting (w=2..8, T_co=7), occurrence collection, P=3 parent
   arrays, P=1 comparator, slot-0 arbitration measurement, demotion
   demo, eviction micro-test, JSON evidence output.

3. **Bug fix — slice limit (03:05 UTC):** First run panicked immediately:
   `sp_off` at 59MB exceeded the 2^25-byte slice-indexing limit.
   Fixed with two-pass segmentation (count spans, then exact-size
   allocation).

4. **Bug fix — table capacity (03:30 UTC):** Run hung in span-ID
   assignment; 2M-entry hash table at risk of filling (4.3M spans).
   Enlarged span-ID and window tables to 4M entries (hash split across
   two u32 arrays to stay under 2^25 per slice), added probe-count
   guards that fail loudly instead of hanging.

5. **Bug fix — registry bounds (04:05 UTC):** Eviction micro-test
   panicked: 32-byte corpus registry too small for corpus ID 9.
   Enlarged to 40 bytes.

6. **Final build (04:11 UTC):** Clean compile, `--no-analyze`.
   Binary: `work/i2_bin` (264,088 bytes).

## Verification

- M1 smoke: 100.0/100.0 recall, 64/64 swap probes pass.
- M7 smoke: 100.0% hit, 3.05x reuse, 0.50 dedup — all bars pass.
- `i2-hier-1x` full run: completed, see raw log.
- Determinism: two full runs byte-identical (see scorecard).

## Known limitations

- Segmentation is fixed byte-class (not I1's emergent boundaries);
  documented as a deviation in ARM_SPEC.md §7.
- M1/M7 use provisional A15/A7/A8 conventions, marked
  PROVISIONAL-PENDING-FREEZE.
- Scorecard assembler is I2-specific (B-64 assembler not reused).
