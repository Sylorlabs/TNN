# Upscale Generation Path — Honest Result (2026-09-27)

## Verdict: GENERATION LOSES to bicubic. Mechanism-level reason documented below.

This is the completion of Micah's 2026-09-26 order: "for upscale continue work" —
replace the drawing-based upscale with a generation path, teach from real photos,
test honestly against held-out ground truth.

## What was built

**`azteach.zag`** (pure Zag, zero RNG): teaches a shared atom vocabulary from 4
real Wikimedia Commons photographs (brick wall, lake water, foliage, stone wall),
768px wide. Selects farthest-point exemplars at S=64/32/16/8 plus S=4 thin atoms
from strong Sobel edges. Every atom records its source image index and pixel
coordinates (provenance). Held out: sky_clouds (test) and the sealed bridge photo
(secondary diagnostic). The held-out bytes never enter training.

**`azgen.zag`** (pure Zag, zero RNG): 2× generation from the shared vocabulary.
- SHAPES: recursive 32→16→8→4 partition fit against shared atoms. A block is
  TAKEN iff its best atom explains ≥9/value AND beats the finer split.
- LINES: measured Sobel strong-edge pixels (no walks, no DDA, no chords) matched
  against shared thin atoms. Taken iff ≥9/value.
- Construction: every pixel = measured region mean + measured atom deviation.
  Even positions are the observed input (KNOWN).
- NO bicubic in the generation result. NO nearest-neighbor. NO procedural
  fallback. Rejected blocks use measured block means (CONSTRUCTED-NO-FIT).
  Leftovers use measured local means (INVENTED). Bicubic survives ONLY as a
  separate baseline for scoring.
- Labels: 0 KNOWN, 2 CONSTRUCTED-LINES, 3 CONSTRUCTED-SHAPES, 4 INVENTED,
  6 CONSTRUCTED-NO-FIT.

## Honest scores (held-out, vs real full-resolution GT)

| Image | Generation PSNR | Bicubic PSNR | Generation SSIM | Bicubic SSIM |
|-------|----------------|--------------|-----------------|--------------|
| Bridge (512×184, secondary) | 18.47 dB | 25.89 dB | 0.4620 | 0.8157 |
| Sky (768×512, held-out) | 22.75 dB | 33.20 dB | 0.5890 | 0.9176 |

Old MIXED TNN (per-image atoms): 25.96 dB / 0.8140 on bridge.
The generation path does NOT beat or match 25.96 dB. It loses by 7.4 dB (bridge)
and 10.5 dB (sky).

## Mechanism-level reason

The shared cross-image atoms hallucinate scene-inappropriate high-frequency
textures. The matching selects atoms by low-resolution key SSD (the 2×2 box
downscale of the atom vs the input block). High gain at input resolution
(SHAPES: 259/value on bridge) does NOT predict high-resolution accuracy.

Concrete failure: a smooth bridge-arch block (32×32 input) matched a BRICK atom
with high gain — the brick key's edge aligned with the arch edge at low res —
but the brick atom's 64×64 high-frequency texture (mortar lines, brick surface)
was stamped onto the smooth arch, producing RMSE 54.5 on SHAPES pixels.

The low-res key is AMBIGUOUS: many different high-res patches downscale to the
same key. Farthest-point selection picks DIVERSE, high-energy, scene-specific
atoms (people, boats, distinctive objects — not generic textures). Cross-image
matching cannot distinguish "this brick pattern continues" from "this smooth
region happens to have similar low-res energy."

Per-image atoms (old MIXED, 25.96 dB) worked because the atoms came from the
same scene: same bricks, same lighting, same scale. The high-frequency details
were correlated. Cross-image atoms are uncorrelated — the hallucination is
wrong more often than right, and MSE punishes sharp-but-wrong far more than
blurry-but-close (bicubic).

This is not a bug. It is a property of the approach: example-based
super-resolution requires examples from the same distribution. The shared
vocabulary is from a different distribution (different scenes), so it cannot
predict the held-out scene's high frequencies.

## What was removed (generate-don't-draw compliance)

- Bresenham/DDA/chord LINES rasterizer: REPLACED with measured Sobel edge
  pixels + thin atoms. No procedural line drawing.
- Bicubic fallback in generation output: REMOVED. Rejected blocks use measured
  means. (Bicubic remains as a separate baseline only.)
- Nearest-observed INVENTED fallback: REMOVED. Leftovers use measured local
  means, labeled INVENTED.
- Fixed 50/50 blend, fixed feathering: already removed in prior work.
- LINES-first order: IMPLEMENTED (was aborting). Both orders work.

## Determinism

Two full runs (teach + both generations) produce byte-identical outputs:
- Bridge gen: 2028ba1dd5cf12e25300c759b72febacab4853a03d1c1302656a7a7a3afa4135
- Sky gen: 842558193c0a56fc73dd86ea160406df8c7cd5023450b687b77043939a8e2408
- Vocab: cbead2f7c13e455fb1598defc34182f7b2517dfaeb6f0fa95925e4f1f0d525b2

Pinned toolchain: ~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1

## Files

- `src/azteach.zag`, `src/azgen.zag`: pure-Zag sources.
- `teach_out/vocab.bin`: shared vocabulary (1,958,448 bytes).
- `teach_out/TEACH_TRACE.txt`: with per-atom provenance.
- `run_bridge_1/`, `run_sky_1/`: sealed fixtures (input, GT, vocab).
- `out_bridge_3/`, `out_sky_3/`: generation outputs, baselines, labelmaps, scores.

## Corpus attribution

All 5 images from Wikimedia Commons (API-verified licenses 2026-09-27):
- brick_wall.jpg: "Red brick wall texture.JPG", CC BY-SA 3.0
- lake_water.jpg: "Dal lake by Ahanger HOBO.jpg", CC BY 4.0
- foliage.jpg: "Thick foliage in the Sinharaja Forest Reserve.jpg", CC BY-SA 4.0
- stone_wall.jpg: "Stone wall texture.JPG", CC BY-SA 4.0
- sky_clouds.jpg: "Cirrus uncinus clouds in the morning sky.jpg", CC BY-SA 4.0
(Held out from training; used only for testing.)

Note: exact author names and source URLs were not recorded at fetch time
(2026-09-27). The titles and licenses above are from the Wikimedia API
responses. Full attribution with URLs should be added before publication.
