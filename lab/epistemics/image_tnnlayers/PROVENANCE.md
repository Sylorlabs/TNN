# PROVENANCE.md — TNN-CHOOSES-ITS-LAYERS (image_tnnlayers)

## Sealed fixture

- `~/workspace/your_files/image_repro/original_512.bmp`
- 512x187, 24-bit BMP (uncompressed).
- SHA-256: `4ee3414bddd289ca7c9544a91ec39b8885f8dcde96fa0ffa0d56aebc38da1b00`
- Verified before the run (2026-09-26); the working copies in `run/` and
  `run2/` are byte-identical copies (checked by sha256sum).

## Toolchain (pinned)

- `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- Both binaries (`tlingest_bin`, `tlemit_bin`) built 2026-09-26 from the
  sources in this directory. Build log: `tlingest_build.log`,
  `tlemit_build.log` (workdir only, not committed).

## What TNN chose (from DELIBTRACE.txt)

TNN surveyed the fixture, computed per-mille affinities, chose its own
layer order, chose the SHAPES scale set from a repetition probe, and
committed each candidate only after it measured G/N >= 9 on the current
residual. See VERDICT.md for the layer list and reasons.

## Comparison baselines (prior forks, same fixture, same metric code)

| Approach | PSNR (dB) | SSIM | Residual | Knowledge bytes |
|---|---|---|---|---|
| Hand-designed layered zoom | 30.80 | 0.9620 | 19.9% | 1,343,354 |
| No-layers (exemplar take/split) | 29.27 | 0.9260 | 11.7% | 2,505,092 |
| **TNN-chooses-layers (this fork)** | **see VERDICT.md** | | | |

Metrics: PSNR = mean of per-channel dB; SSIM = Gaussian window,
per-channel mean (same `metrics.py` as the zoom fork). Pre-residual
understanding renders only; residual is the excluded error channel.

## Reproducibility

- `run/` and `run2/` are independent runs from the same sealed fixture.
- Required: byte-identical `knowmap.bin`, `renderA.bmp`,
  `render_understanding.bmp`, and `DELIBTRACE.txt` across both runs.
- `tlemit_bin` (path B) reads only `knowmap.bin` and must reproduce
  `render_understanding.bmp` exactly (`renderB_understanding.bmp`) and
  close the fixture exactly (`renderB.bmp` == `original_512.bmp`).

## Gallery

`~/workspace/your_files/image_tnnlayers_NEW/index.html` — self-contained
(all images data URIs, zero external loads): full renders, bridge-arch
crops (original | zoom | no-layers | tnn-layers), layer map, error maps,
pentagon analysis, deliberation trace head.
