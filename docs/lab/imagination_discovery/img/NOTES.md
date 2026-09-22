# IMAGINATION DISCOVERY — Image Pipeline Notes (D-IMG-1, D-IMG-2)

Date: 2026-09-22. Generator: `disc.zag` (pure Zag, compiled with the pinned
`znc_linux_x86_64_abed8aa1` toolchain). Verifier: `verify_bars.py` (Python,
verification + lossless PNG preview only — never in the generation path).

## Pipeline operation

One Zag executable, `disc`, selects the subject from `argv[1]`
(`alien` | `arch`), the output directory from `argv[2]`, and the resolution
from `argv[3]` (`1024` | `2048`). It allocates a single image-sized RGB
buffer, rasterizes the scene **directly at the target resolution, one pixel
at a time**, then emits a bottom-up 24-bit BMP with chunked (≤1 MiB) writes.
BMP is written with `O_TRUNC` (never `O_EXCL`, which fails silently on
existing files). PNGs are lossless re-encodings produced by the Python
verifier for preview only.

## Bypassing the old 512² / 32 MiB cap

The legacy pipeline rasterized onto a 512² working grid (u4f) and upscaled.
`disc.zag` never builds a low-res grid: every pixel's color is computed from
closed-form deterministic noise fields sampled at that pixel's coordinates,
so resolution is a free parameter. The only resolution-dependent cost is one
`w*h*3`-byte buffer, which stays under znc's 2^25-byte single-slice indexing
limit at both 1024² (~3.15 MB) and 2048² (~12.6 MB). No chunking of the
image buffer itself is needed at these sizes.

## Deterministic noise core (shared)

- 32-bit integer coordinate hash (no RNG anywhere; two clean-process reruns
  are byte-identical, SHA-256 verified).
- Fixed-point smooth value noise, multi-octave fBm, ridged fBm, domain
  warping (all integer/fixed-point; the architecture scene additionally uses
  Zag `f64` for its analytic beam geometry while all procedural texture
  remains integer-noise based).
- Monochromatic per-pixel hash dither (±3 LSB) so gradients never band; the
  dither is hash-based texture, not blur, and the sharpness bar still passes
  at 2.4–2.5×.
- Zero axis-aligned filled-primitive placement calls in either scene builder
  (D-COMP grep audit passes); all coverage is per-pixel analytic tests
  (point-in-convex-quad, segment distance, radial falloff).

## D-IMG-1 — Alien planet (`disc alien . 1024`)

Extrasolar surface vista: domain-warped ridged/fBm terrain with separate
broad (relief lighting) and fine (albedo) fields, procedural strata palette,
glowing contour-derived lava veins, aerial perspective, a warped-fBm cloud
deck plus cirrus sampled in sky-UV for isotropy, and a ringed planet with
procedural bands, storms, limb darkening, and terminator shading. A dedicated
broad-crested ridged skyline field keeps the mountain silhouette from going
needle-like.

Notable bug fixed 2026-09-22: the 5-stop/4-stop palette interpolators
indexed one band too many (`vv*5` for 5 stops), pushing interpolation factors
past 1024 and wrapping channels through `&255` into magenta (~1,058 magenta
pixels). Fixed to `vv*4` / `vv*3` with channel clamps before packing;
magenta pixel count after fix: 0.

## D-IMG-2 — Impossible architecture (`disc arch . 1024`)

A Penrose-triangle stone frame: three convex beam quads with cyclic overlap
(beam 0 wins at vertex 1, beam 1 wins at vertex 2, beam 2 wins at vertex 0),
so each beam passes over one neighbor and under the other — the impossible
cycle. Coverage is point-in-convex-quad per pixel; the winner's inner edge
is extended past each miter and its diagonal end-cap is darkened to draw the
occlusion cut. Bevel shading (top-light), stone grain/mottling/cracks from
integer noise, ambient occlusion at the miters, drop shadow, and vignette.

## Measurements (final, 2026-09-22)

| Subject | File | Size | grad(O) | grad(B) | Ratio | D-RES | D-SHARP | D-COMP |
|---|---|---|---|---|---|---|---|---|
| D-IMG-1 alien | `d-img-1_alien_1024.bmp` | 1024×1024 24-bit | 7.813 | 3.257 | 2.399 | PASS | PASS | PASS |
| D-IMG-2 arch  | `d-img-2_arch_1024.bmp`  | 1024×1024 24-bit | 1.850 | 0.750 | 2.468 | PASS | PASS | PASS |

Sharpness bar: `grad(output) ≥ 1.20 × grad(downscale-by-2 then box-upscale-by-2)`.
Both exceed it at ~2.4×.

Determinism (two separate clean processes, final binary):
- alien BMP: `d9b036e6…95c56f4` both runs — identical.
- arch BMP: `b6591516…04f2b9a7` both runs — identical.

Render time (1024², lab VM): alien ~7.8 s, arch ~1.9 s.

### Artifact SHA-256

| File | SHA-256 |
|---|---|
| `d-img-1_alien_1024.bmp` | `d9b036e6f7d34b5dd7f116926fb943b16d1584c66629049b46a23d5be95c56f4` |
| `d-img-1_alien_1024.png` | `9bdf0952d1f8741d3deb3030db601b53bf9cf7dd086349baa4d3f85108d649eb` |
| `d-img-2_arch_1024.bmp`  | `b6591516b3cdfee30f96b917369026319a5a700b129c3037cbef85d604f2b9a7` |
| `d-img-2_arch_1024.png`  | `5d55037658e117e0340f57afbb2cef98b1ff2e7ee84380a6002a64a39a268f33` |
| `disc.zag` | `f13170a220b5fcd0ac0d3197570c2345818ca0d4e9b4b741d1c2113038197f7a` |
| `verify_bars.py` | `a413f6b8537aa46335b5bb829d26326f6c4c91001c488ebd70840de49d11c18f` |

## Limitations (honest)

- No blind quality judgment was performed by this crew; a separate judging
  pass follows. Passing D-RES/D-SHARP/D-COMP is mechanical, not aesthetic.
- 2048² was not attempted: the 1024² scenes were only just finalized, and the
  prereg sets 1024² as the exact minimum with 2048² optional. The pipeline
  supports it (buffer ≈ 12.6 MB < 32 MiB limit); it is untested.
- The architecture scene uses `f64` for beam geometry (deterministic on
  x86-64, but not the integer-only discipline used elsewhere); all texture
  noise remains integer-hash based.
- The alien skyline, while broad-crested, still leans spiky in places; the
  lava veins are subtle at 1024².
- `disc` binary, `.zagd`/`.zag-cache` files, and debug renders are build
  artifacts and are excluded from the commit.
