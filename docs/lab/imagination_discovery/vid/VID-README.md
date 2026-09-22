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

## Generative design, round 2 (blind-tell repair)

v1 failed V-BLIND (judges named blur/template tells unprompted; only
3/5 "unsure"). Round 2 rewrote the render path around six repairs;
all mechanical bars still govern. No template primitives anywhere
(no rect/blotch/fill placement calls; grep-audited).

- **One anchored sun** (fixed all 48 frames, upper-left, ~29° elevation,
  dir-to-sun (-620,+620,483)). Per-pixel finite-difference normals from
  height taps at ±1 px drive diffuse, specular, foam shading, crest
  lit/shadow sides, and the basin lee shadow — all from the same light.
- **Material-logic color** (the global palette-anchor field is gone):
  depth → water color (shallow bioluminescent teal → mid deep blue →
  deep indigo), foam → near-white, glints → warm white, scatter glow in
  sunlit shallows. A very-low-frequency shelf field gives shallow banks
  and deeper channels outside the basin, so large-scale hue variation
  has content logic.
- **The migrating abyssal basin** (replaces the static navy blob):
  center travels ~250 px over the sequence on a slow deterministic
  path, radius 165–235 px and depth morph; internal fbm texture;
  wave trains bend around it (tangential swirl deflection of the chop
  sampling coords); broken foam rim where currents strike its edge;
  soft lee shadow on the anti-sun side.
- **Sharp content at every scale, per pixel**: thresholded crest-line
  ridges with lit/shadow sides, crisp sunlit edges on steep wave faces,
  micro-striations lifting the mid-tones, per-pixel ripple shading.
  Specular glints are baseline-subtracted (only surfaces tilted toward
  the sun *more* than flat water glint) — sparse, sized by wave scale,
  never an all-over mirror wash, never a random-dot overlay.
- **Temporal model** (film-grain philosophy): persistent = swell +
  basin path (2 time cells); changing = advected chop (~3 px/frame),
  fast ripple, traveling/morphing basin, evolving foam streaks — real
  scene evolution; grain = ±2 LSB per-pixel deterministic hash dither.
- Fully per-pixel evaluation at 1024 (no coarse grid); frame-by-frame
  BMP emission (3,145,782-byte buffer, under the 2^25 slice cap).

## Bar results (round-2 full run, 2026-09-22)

| Bar | Result |
|---|---|
| V-RES | 48/48 files, 1024×1024 24-bit, 3,145,782 bytes each — PASS |
| V-SHARP (f0) | grad ratio 1.259 (bar ≥ 1.20) — PASS |
| V-SHARP (f23) | grad ratio 1.277 — PASS |
| V-SHARP (f47) | grad ratio 1.266 — PASS |
| V-TEMP | per-pair mean\|Δ\|/255: min 7.34%, max 8.21%, mean 7.77% ∈ [0.5%, 15%] — PASS |
| V-DET | clean rerun → manifest sha256 `ff91dad8…794f0b0c` identical, 48/48 frames byte-identical — PASS |
| V-COMP | zero primitive-placement calls in generator source — PASS |

V-BLIND is out of scope for this crew (separate judging crew follows).

## Bugs found and fixed during iteration

1. **Mirror-wash specular** (round 2): half-vector only ~30° from
   vertical, so flat water gave sd≈861 everywhere → whole frame glinted.
   Fixed by baseline-subtracted glints (only slopes tilted sunward of
   flat water) plus a faint diffuse-following sheen.
2. **Binary lee shadow** (round 2): hard 560/720/1000 steps drew a
   visible circular contour around the basin. Replaced with a smooth
   two-sample falloff.
3. **Shift-scaled hash was linear** (v1, 2026-09-22): `((h>>22)*1000)>>41`
   produced a near-linear ramp in lattice coords for this
   single-multiply mixer — verified bit-identical against a Python port,
   so znc was correct and the scaling choice was wrong. Replaced with
   low-bit `% 1001` (f3_hash2 pattern). First symptom: perfectly straight
   diagonal "crest" lines.
4. **NUL in output path** (v1): `o_frame_path` copied `dir.len` bytes
   including the NUL from `o_zcstr_copy` — fixed to stop at NUL.
5. `@import` needs the substrate mirrored relative to cwd
   (`substrate/R33_NATIVE_IO_V1.zag`).

## Known limits

- The sequence does not loop (3D noise is not periodic in time; fine for
  a 48-frame shot, would need periodic time lattice for a loop).
- Render cost ~3.5 s/frame single-core on the lab VM (~3 min for 48).
