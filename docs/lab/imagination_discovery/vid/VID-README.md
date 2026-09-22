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

## Generative design (no template primitives)

Every pixel derives from deterministic integer-hash value noise
(`o_hash2`/`o_hash3`: 64-bit wrap mix, masked to 63 bits, `% 1001`
low-bit scaling — the battle-tested `f3_hash2` pattern). Scene builders
contain zero rect/band/blotch/fill/gradient placement calls (grep-audited).

- **Multi-scale**: smooth large-scale fields (depth, hue, drift, warp
  displacement) are evaluated on a 257×257 coarse grid per frame
  (5 channels × u16) and bilinearly sampled per pixel — smooth by
  construction. All SHARP detail (crest filaments, ripple, sparkle,
  ±2-LSB film-grain dither) is evaluated per pixel at full 1024
  resolution. No blur pass exists anywhere.
- **Domain warping**: the warp field displaces the sampling coordinates
  of the crest/ripple/swell fields (±90 px), so fine detail swirls
  coherently with the large-scale currents.
- **Color**: three palette anchors (deep indigo → teal → violet) blended
  by smoothstep-weighted mixes driven by the hue field; luminance from
  depth+drift; foam on wave crests; specular glints where ripple peaks
  meet crest; deterministic sparkle; fine dither only.

## Temporal model (film-grain: persistent + changing + grain)

- **Persistent** (strongly time-correlated): depth / hue / drift fields
  are 3D value noise with LOW time frequency (2–4 time cells over the
  48-frame sequence) — the same sea throughout, slowly evolving.
- **Changing** (time-correlated, faster): wave-crest filaments
  (2D ridged fBm) are advected 160 px in x over the sequence; the fine
  ripple field is 3D noise at higher time frequency (8 time cells).
  Waves visibly travel; nothing shimmers independently per frame.
- **Grain** (uncorrelated, tiny): per-pixel deterministic hash dither
  ±2 LSB, different every frame — anti-banding film grain.

## Bar results (first full run, 2026-09-22)

| Bar | Result |
|---|---|
| V-RES | 48/48 files, 1024×1024 24-bit, 3,145,782 bytes each — PASS |
| V-SHARP (f0) | grad ratio 1.928 (bar ≥ 1.20) — PASS |
| V-SHARP (f23) | grad ratio 1.915 — PASS |
| V-SHARP (f47) | grad ratio 1.881 — PASS |
| V-TEMP | per-pair mean\|Δ\|/255: min 1.88%, max 2.24%, mean 2.02% ∈ [0.5%, 15%] — PASS |
| V-DET | clean rerun → manifest sha256 `b1658185…9f1a134ce96deb5` identical, 48/48 frames byte-identical — PASS |
| V-COMP | zero primitive-placement calls in generator source — PASS |

V-BLIND is out of scope for this crew (separate judging crew follows).

## Bugs found and fixed during iteration

1. **Shift-scaled hash was linear** (2026-09-22): `((h>>22)*1000)>>41`
   produced a near-linear ramp in lattice coords for this
   single-multiply mixer — verified bit-identical against a Python port,
   so znc was correct and the scaling choice was wrong. Replaced with
   low-bit `% 1001` (f3_hash2 pattern). First symptom: perfectly straight
   diagonal "crest" lines.
2. **NUL in output path**: `o_frame_path` copied `dir.len` bytes
   including the NUL from `o_zcstr_copy` — fixed to stop at NUL.
3. `@import` needs the substrate mirrored relative to cwd
   (`substrate/R33_NATIVE_IO_V1.zag`).

## Known limits

- The sequence does not loop (3D noise is not periodic in time; fine for
  a 48-frame shot, would need periodic time lattice for a loop).
- Foam wisps read slightly "scratchy" at full res in dense areas —
  aesthetic, for the blind judges.
- Render cost ~1.6 s/frame single-core on the lab VM (~75 s user for 48).
