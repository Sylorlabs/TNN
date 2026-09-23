# R2-7 Build Notes

## Toolchain
- Pinned compiler: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- Pure Zag, zero RNG in decision paths, byte-identical reruns.

## Source
- `src/r27.zag` (main, ~1,900 lines)
- `src/R33_NATIVE_IO_V1.zag` (copied substrate)
- `src/R33_NATIVE_SHA256_V2.zag` (copied substrate)
- `src/gen_r2a.py` (offline fixture generator, Python — NOT in TNN decision path)

## Build
```bash
cd src
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 r27.zag \
  --no-zagd --no-analyze --no-foreground-cache -o /tmp/r27_sense
```

## Compiler issues encountered
1. `chal_cid` → `reg_challenge` (typo from broad sed).
2. `nio_open_root` uses O_DIRECTORY — cannot open regular files. Fixed with
   direct `_zag_raw_syscall(2, ...)` O_RDONLY.
3. R2FX magic constant: 0x52324658 = 1379026520 (not 1377794904).
4. `cs` buffer 16 bytes too small for [outcome:i32][stat1:i64][stat2:i64]
   (needs 20). Fixed to 24 bytes.
5. Motion direction: R2FX generator moves WINDOW, content appears opposite —
   negate for truth. Legacy moves window opposite so content matches label —
   do NOT negate. (Two generators, opposite conventions, documented.)
6. Shape classification: moment-based circularity failed (integer division
   precision loss, rotation-sensitive). Switched to bbox fill-ratio:
   CIRCLE~0.785, SQUARE~0.59 (rotated), TRIANGLE~0.5. Thresholds: >=0.70
   CIRCLE, <0.55 TRIANGLE, else SQUARE.
7. `jname` mapping: tid==2 expects 0=CIRCLE, 1=TRIANGLE, 2=SQUARE. Fixed
   sh_form to match (was swapped).
8. Ledger: 8 null bytes from `cl=cl+8` without writing "fixture=". Fixed to
   actually write the bytes. Also fixed `p` not reset between loops.
9. Audit buffer: allocated 8MB but tried to read 33MB. Fixed to consistent
   8MB.

## Fixture generation
- Master seed: 20260923
- R2FX format: 8×u32 LE header [magic, task, index, family, fo, fl, go, gl]
- F and G spans are non-overlapping, disjoint bytes.
- Counts: 5,100 normal (r2n), 4,815 adversarial (r2a), 5,000 second
  presentations (r2a2).
- Note: Frozen prose says 4,260 generated normals, but per-task counts sum
  to 5,100. Documented, not silently amended. Using 5,100.

## Threshold freezing
Thresholds were tuned during development against the 370 primary (not the
scored R2A suite). As of 2026-09-23, the registry (REGISTRY.md) is FROZEN.
No further tuning after running the official bars.
