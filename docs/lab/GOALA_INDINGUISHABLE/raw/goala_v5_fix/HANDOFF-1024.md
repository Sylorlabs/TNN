# HANDOFF — render pipeline to 1024x1024+ (for the discovery wave)

Date: 2026-09-22. Author: Goal-A finish crew coordinator.
Context: Micah's verdict — the 480x480 G-series reads as blurry (heavy grain
over a 20x bilinear upscale = fuzzy) and template-driven (placed
f3_blotch/f3_band primitives). The new program targets high resolution and
SHARP, no template primitives as the creative ceiling. This note covers only
the PIPELINE mechanics the new renderer must handle. Creative direction belongs
to the discovery wave.

## Current pipeline (what the numbers are)

- Composition arena: 24x24 cells, coords 0..1000 (`f3_vnew`).
- `f3_raster_g`: per-pixel bilinear upscale from the 24x24 arena + per-pixel
  monochromatic grain (persistent + temporal components, amplitude ~14/1000,
  luminance-dependent: `(gp+gt)*(384-luma)/256`).
- Stills: 480x480x3 = 691,200 px bytes; BMP file 691,254 bytes.
- G-video: 480x480, 36 frames, 12fps, 44.1kHz. Whole AVI built as ONE slice:
  ~25.2 MB.

## The hard ceiling: znc 2^25-byte single-slice limit

No single slice larger than 33,554,432 bytes can be indexed — even `a[0]`
panics above it (AGENTS.md). This binds before `nio_alloc`'s i32 range does.

| Artifact | Bytes | Verdict |
|---|---|---|
| 480^2 frame (RGB24) | 691,200 | fine |
| 480^2 x 36f whole AVI | ~25.2 MB | fine but close to ceiling |
| 1024^2 frame (RGB24) | 3,145,728 | fine as one slice |
| 1024^2 x 36f whole AVI | ~113 MB | **FAILS — cannot allocate as one slice** |
| 2048^2 frame (RGB24) | 12,582,912 | fine as one slice |
| 2048^2 x 36f whole AVI | ~453 MB | **FAILS** |

Consequence: the current `f3_emit_avi_g` design (build the entire file in one
`avi` slice, single `f3_write_named` at the end) CANNOT scale to 1024^2 video.
The writer must become streaming:

1. Write the RIFF header + hdrl + strl chunks first (fixed 324 bytes).
2. Per frame: write `00dc` video chunk + `01wb` audio chunk with separate
   `write(2)` calls; record each chunk's file offset and size in small tables
   (the existing `ci/cf/co/cs` tables, NF*8 bytes each — tiny).
3. Write `idx1` LAST from the tables. All chunk offsets are precomputable
   (constant framesz, constant apf), so no seeking is required.
4. Stills need no change: 1024^2 BMP = 3 MB + 54 header, one slice, fine.
   2048^2 stills also fine (12.6 MB).

Per-frame working set at 1024^2 stays small: `far` arena 24,576 B, `px`
3.1 MB, audio pcm 264,600 B (3 s @ 44.1kHz 16-bit mono). No chunking needed
for stills; only the whole-file video slice must go.

Render-time estimate: the per-pixel loop in `f3_raster_g` is 230k px at
480^2; 1024^2 is 1.05M px (~4.5x). Native binary, integer math — expect
seconds per frame, acceptable for 36f. Measure on the first 1024^2 build.

## Why 480^2 reads as blur (and what must change in the grain model)

The fuzz is structural, not a parameter tweak:

1. **Only 576 degrees of freedom.** The 24x24 arena bilinear-upscaled 20x
   means no edge in the image is sharper than ~20 px, and no detail exists
   above the cell Nyquist. The per-pixel grain is the ONLY high-frequency
   content — and it is monochromatic white noise, uncorrelated with image
   structure. The eye reads smooth-gradient-plus-noise as out-of-focus
   photo + film grain: fuzzy.
2. **At 1024^2 with the same 24-cell arena, edges get WORSE** (~43 px wide).
   Raising output resolution without raising generator resolution just makes
   bigger blur.
3. **Grain must become subordinate, not the carrier.** Requirements for the
   new grain model:
   - Real high-frequency IMAGE content first: raise the composition grid
     (24 -> 96/192 cells costs 16-64x in cell loops; measure) and/or add a
     DETAIL PASS at output resolution — structured micro-texture
     (directional strokes, edge-localized detail, material-specific
     drag/pooling behavior per the TELLS.md positive model #7), not white
     noise.
   - Grain amplitude must drop as real detail rises; keep it ~1-2 px
     spatially correlated (not pure white), luminance-weighted as now, and
     strictly below the detail pass in perceptual weight.
   - Sharpness needs genuine 1-3 px edges on focal elements at output
     resolution — the bilinear upscale cannot produce these by construction.
4. **Video:** the frozen-grain fix (V-T5 hardening) stays valid — temporal
   grain must remain subordinate to motion. At 1024^2, per-pixel white shimmer
   is MORE visible, not less.

## Template-primitive ceiling (creative, flagged for the discovery wave)

Micah: no "3 blotches + 2 bands" compositions. The current vocabulary —
`f3_vgrad` / `f3_blotch` / `f3_band` / `f3_rect` on a 24-grid — is the ceiling
he named. The discovery wave needs richer generative marks (open-ended
discovery, e.g. "a high-quality alien planet"). Suggested pipeline shape
(mechanics only): composition field (low-res, layout/mass) -> detail field
(high-res, material marks) -> output-res raster with subordinate grain.
Determinism and byte-identical reruns carry over unchanged (f3_hash2-based
variation, no RNG in any decision path).

## Byte-identical baseline left behind

- `imagination/src/field.zag` (this commit): V5b G1 + G2 lamp fix + V4
  subject videos, all byte-identical verified (see
  `GOALA_INDINGUISHABLE/raw/goala_v5_fix/`).
- Legacy `f3_emit_avi` path untouched and frozen throughout.
