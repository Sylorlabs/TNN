# D-VID-1 "alien ocean" — video pipeline (2026-09-22)

Pure-Zag 1024×1024 × 48-frame 24-bit BMP generator. Frozen prereg:
`../PREREG.md` (commit `988255e64dfc`). Built with
`../../toolchain/bin/znc_linux_x86_64_abed8aa1 --no-zagd --no-analyze --no-foreground-cache`.

## Files

| File | Role |
|---|---|
| `ocean.zag` | Deliverable generator (pure Zag, zero RNG) |
| `substrate/R33_NATIVE_IO_V1.zag` | nio allocator/syscall wrappers (mirrored from toolchain; `@import` resolves relative to cwd) |
| `verify_vid.py` | VERIFY ONLY — measures V-RES/V-SHARP/V-TEMP, writes SHA256SUMS |
| `frames/dvid1_f00.bmp` … `dvid1_f47.bmp` | 48 output frames |
| `frames/SHA256SUMS` | per-frame SHA-256 manifest |

## Generative design, round 3 (fundamental rebuild, 2026-09-22)

Round 2 passed all mechanical bars but blind judges still rejected it
as "a procedural shader/texture, not a scene." Round 3 rebuilt the
generator as a deterministic integer fixed-point **perspective ocean
renderer** with an actual scene. Five round-2 tells repaired:

1. **Tiled uniform sparkle → gone.** The repeating sparkle field is
   removed. Highlights are sun-driven specular from per-pixel
   finite-difference normals, evaluated at full resolution.
2. **Vortex stamp → rotating 3D currents.** The static navy blob is
   replaced by a migrating depression with four rotating spiral arms
   in the heightfield (arm factor modulates material color), slow
   center migration, and arm-driven foam. Soft radial falloff; real
   occlusion via the column y-buffer.
3. **Global RGB retint → material-driven color.** Depth → water color
   (trough indigo → crest teal), sun diffuse, fresnel to horizon sky,
   subsurface scatter, foam white, distance fog. No global grade.
4. **Highlights at full resolution.** Normals from 1-px finite
   differences of the heightfield; foam breakup hashed per pixel;
   dither is ±2 LSB deterministic hash.
5. **Actual scene.** Horizon line, visible sun + sky, six rock spires
   breaking the horizon (explicit analytical ray pass with waterline
   occlusion), foreground/midground/background depth layering,
   atmospheric falloff to horizon color.

Architecture: far-to-near per-column water marcher (1536 samples,
linear in inverse depth, five 6144-byte arenas), x32 subpixel y-buffer,
explicit spire ray pass after water/sky, deterministic ±2-LSB dither.
Zero RNG. Frame buffer 3,145,782 bytes (under 2^25 slice cap).

## Bar results (round-3 full run, 2026-09-22)

| Bar | Result |
|---|---|
| V-RES | 48/48 files, 1024×1024 24-bit, 3,145,782 bytes each — PASS |
| V-SHARP (f0) | grad ratio 1.607 (bar ≥ 1.20) — PASS |
| V-SHARP (f23) | grad ratio 1.595 — PASS |
| V-SHARP (f47) | grad ratio 1.543 — PASS |
| V-TEMP | per-pair mean\|Δ\|/255: min 8.59%, max 10.75%, mean 9.78% ∈ [0.5%, 15%] — PASS |
| V-DET | clean rerun → manifest sha256 `400ae5c6…938b26ac9` identical, 48/48 frames byte-identical — PASS |
| V-COMP | zero primitive-placement calls in generator source — PASS |

V-BLIND is out of scope for this crew (separate judging crew follows).

## Bugs found and fixed during iteration (round 3)

1. **Spire profile collapsed to zero** (2026-09-22): smoothstep
   `s1*(3000-2*t01)/1000000` was integer-scaled wrong → rock height
   zero. Fixed with `3*s1 - 2*t01*s1/1000`. Spires moved to explicit
   analytical ray pass (voxel z-samples miss narrow needles).
2. **1-px black horizon gap**: floor/ceil disagreement between water
   and sky coverage. Fixed `ytop=(ybuf+31)/32`.
3. **Horizontal stripe gaps**: `y0` used ceil, `y1` used floor →
   unwritten 1-px gaps between marcher segments. Fixed `y0=syfp/32`
   (floor). This was the dominant visual artifact.
4. **Arm factor range mismatch**: `arm` is 0..1000 (ridge*fall/1000),
   not 0..6500; shader and debug assumed 6500 → invisible spiral.
   Fixed ranges.
5. **Stale `vrr`**: vortex radius constant not updated when arm
   radius changed 95→160. Fixed to 160*160.
6. **Spire 5 hidden** behind spire 0: moved x -1650→-2100 at z=3900.

## Known limits (round 3)

- The spiral vortex is mechanically present (rotating arms in
  heightfield, arm-modulated color, migrating center) but visually
  subtle; the depression reads as a dark region rather than a crisp
  whirlpool.
- The sequence does not loop (3D noise not periodic in time).
- Render cost ~2.5 s/frame single-core (~2 min for 48).
