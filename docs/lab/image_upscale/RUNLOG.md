# HONEST UPSCALE — run log

All times PDT, 2026-09-26. Toolchain pinned:
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1.

## Build

- src/ copied the four verified support files from the adaptive-layers
  parent (R33_NATIVE_IO_V1.zag, common_az.zag, azlayers.zag, metrics.py).
- Wrote src/azprep.zag, src/azupscale.zag, src/azoutpaint.zag, src/build.sh.
- Build: 3 binaries, warnings only (same analyzer style as the parent).
  Two bugs found and fixed before the official runs:
  1. Bicubic 4-tap reads indexed BEFORE edge clamping (negative index panic
     at frame borders) — fixed by clamping coordinates first.
  2. No fallback for odd pixels with no committed-layer coverage — fixed
     with the INVENTED nearest-observed fill (top-left even neighbor).

## Prep (once)

- ./azprep_bin indir stage: validated the sealed fixture
  (512x187, SHA-256 4ee3414b...b00 — matches the sealed value).
- Wrote stage/gt_512x184.bmp (HELD; rows 0..183) and
  stage/input_256x92.bmp (2x2 box, round-half-up; ALL TNN sees).

## Phase 1 — upscale (run/, run2/)

- ./azupscale_bin stage run — EXIT=0. TNN's deliberation on 256x92:
  order SHAPES(3) -> LINES(2) -> SMOOTH(1);
  SHAPES COMMIT (G=1548951066, N=70656),
  LINES COMMIT (G=6046240, N=5415),
  SMOOTH REVERT (G=12558, N=70656; 0.18/value vs bar 9).
  Residuals 7452/23552 (31.6% — the downscaled fit is much looser than the
  parent's full-res 2.7%, as expected).
- 36 SHAPES regions, 472 LINES segments committed.
- Outputs: upscale_tnn.bmp, upscale_bicubic.bmp, labelmap.bmp,
  labels_raw.bin, knowmap_256.bin, UPSCALE_TRACE.txt, SCORES.txt,
  TILES.txt, LABELS.txt.
- Rerun into run2/: all 9 deterministic outputs byte-identical
  (SHA-256 compared; stdout excluded — contains wall-clock timing).

## Scoring

- Integer-exact SSE vs held gt_512x184.bmp, computed in Zag.
- PSNR (metrics.py convention, mean of per-channel dB):
  TNN 21.96 dB, bicubic 25.89 dB (delta -3.92 dB).
  Odd (constructed) pixels only: TNN 21.12 dB, bicubic 25.87 dB (-4.74).
- SSIM (metrics.py): TNN 0.7039, bicubic 0.8157.
- Per-tile (64x46): TNN wins 16, bicubic wins 15, tie 1 — but TNN's losses
  are catastrophic (up to -17.5 dB) while its wins are small (+0.2..+2.2).
- Per-label (odd px): SHAPES n=45786: TNN 21.19 vs bic 25.89 (-4.71);
  LINES n=1318: TNN 19.38 vs bic 25.09 (-5.70); INVENTED n=0.

## White-box diagnosis (the honest loss)

- Where TNN's atoms self-match (regions 0,1,3: m+atom reproduces the
  observed pixels BIT-EXACTLY, RMSE 0.00), its construction beats bicubic
  (+2.2 dB tiles) — the exemplar IS the texture.
- Region 2 (native (128,0) 64x64) was FORCED by the SHAPES-ZOOM design to
  take an atom ("assign @64: 8 fixed blocks (take 8)" — no reject option at
  the top level). Its best atom fits with RMSE 44.15. At native res the
  residual channel hides this; at 2x the odd pixels carry the raw model
  error -> visible checkerboard (even-vs-odd differ ~18.6 levels) ->
  tiles (4,0),(5,0) lose by -14/-17.5 dB.
- Finding: the forced-take means TNN commits to models that don't fit, and
  the residual hides it. Imagination exposes it. This is architecture, not
  a bug in the upscale.

## Phase 2 — outpaint (run/, run2/)

- ./azoutpaint_bin run run — EXIT=0. 64px right strip from the 3 committed
  border SHAPES regions' edge columns; 11,776 px all labeled
  CONSTRUCTED-SHAPES-EXTRAP (5). LINES not extended (recorded).
- Rerun on run2 inputs: outpaint.bmp, outpaint_labelmap.bmp,
  OUTPAINT_TRACE.txt all byte-identical.

## Artifacts

- run/SHASUMS.txt: SHA-256 of every input, output, and source.
- Gallery: ~/workspace/your_files/image_upscale_NEW/index.html
  (self-contained, data URIs, NEW-badged; full-frame TNN vs bicubic,
  label maps, trace excerpts, scoreboard).
