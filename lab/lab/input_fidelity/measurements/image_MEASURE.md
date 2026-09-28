# Input Fidelity — IMAGE modality (measurement worker report)

**Date:** 2026-09-27 ~01:30 PDT · **Prereg:** docs/lab/input_fidelity/PREREG.md (5b661730)
**Method:** committed sources only (origin/tnn-native-lab), pinned toolchain
`znc_linux_x86_64_abed8aa1` (SHA-256 498abcb5…e58ef verified), sealed fixtures
SHA-verified against docs/lab/universal_intake/MANIFEST.sha256 (all 11 image fixtures OK).
Held format: `TNINIMG1` + w,h u64le + w·h·3 RGB bytes. Reference decoder: PIL 10.2.0.

## Bar B1 — lossless PNG/BMP byte-identical: ✅ PASS

| Fixture | Held SHA-256 | Committed claim | Result |
|---|---|---|---|
| img_s16.png (16×16) | 9362aaf6…849f73 | 9362aaf6…849f73 | ✅ MATCH |
| img_m320.png (320×240) | 255682bf…9904508 | 255682bf…9904508 | ✅ MATCH |
| img_odd.png (127×65) | 1c810f47…a6242ad | (no committed SHA) | ✅ byte-identical vs PIL independent decode |
| img_s16.bmp | 9362aaf6…849f73 | == PNG held | ✅ IDENTICAL |
| img_m320.bmp | 255682bf…9904508 | == PNG held | ✅ IDENTICAL |

- BMP held is byte-identical to PNG held on both fixtures (the verdict's identity claim holds).
- img_odd.png (odd dims 127×65) has no committed SHA in VERDICT.md; verified independently: held == PIL decode, 0 diff on all 24,765 pixels.
- Determinism: PNG and JPEG reruns produce byte-identical held files (run 1 == run 2).

## Bar B3 — JPEG honest-lossy: ✅ PASS

| Fixture | Max diff | Mean diff | Bar / committed | Result |
|---|---|---|---|---|
| img_m320_q95_444.jpg (4:4:4) | 3 | 0.2103 | bar ≤3, <0.4 | ✅ PASS |
| img_m320_q90_420.jpg (4:2:0) | 145 | 7.6520 | committed 145 / 7.652; bar = mechanism named+bounded | ✅ PASS |

## Gap mechanisms, ranked by size

### #1 — 4:2:0 chroma upsampling: nearest-neighbor replication (Zag) vs smooth filter (PIL)
**Size:** RGB maxdiff 145 LSB, meandiff 7.65. Dominant error source — the entire gap.
White-box evidence (measured on the artifact, not cited from notes):
- Per-pixel chroma recovered by inverting the fixed-point YCbCr→RGB formula: **held chroma is block-constant within each 2×2 chroma cell** (within-cell std Cb 0.04 / Cr 0.06), while PIL's decode varies smoothly (std 6.58 / 2.94). This is replication, proven from the pixels.
- The maxdiff=145 pixel (288,200): held B=0 vs PIL B=145 with **Y-difference +0.06** — the error is 100% chroma. It sits at a chroma gradient of 469 (vs global mean 31).
- Error decomposition via hybrid rebuilds: rebuild(PIL-Y + held-replicated-chroma) reproduces held to meandiff **0.68** (≈ the Y-channel residual below); rebuild(held-Y + PIL-chroma) leaves meandiff **6.46** (≈ the total gap). The gap rides the chroma channel, not Y.
- Source confirms: jpeg.zag:560–592, "comp 0 = Y … others upsampled by replication", `Cbv = plane[…sy*cw1+sx…]` nearest sampling.
- Honest policy difference, not a decode error: entropy → dequant → IDCT are all correct (see #3).

### #2 — 4:4:4 fixed-point YCbCr→RGB + integer IDCT rounding
**Size:** maxdiff 3, meandiff 0.21. Within bar. Mechanism: scale-2¹⁶ fixed-point coefficients (91881/22554/46802/116130) with round-half-up shifts, plus the 2-pass integer IDCT vs PIL's float IDCT. Unavoidable at ±1–3 LSB; deterministic.

### #3 — Y-plane integer-IDCT rounding (4:2:0)
**Size:** Y meandiff ≈ 0.66 measured (see caveat), ±1–2 LSB at ~24.5% of pixels.
The Y channel is full-resolution in 4:2:0 (no upsampling), so this isolates IDCT: Zag's integer 2-pass IDCT vs PIL's float IDCT. Small, honest, bounded.

## v3 knowledge-path byte-identity re-verification (SHA 4ee3414b…)

**FULLY re-verified from committed sources** (not taken from RUNLOG):
1. Extracted committed `docs/lab/image_exact_work/{common.zag, v3/ingest.zag, v3/emit.zag}` + fixture `docs/lab/image-repro/original_512.bmp`; built with the pinned toolchain.
2. Fixture SHA-256 = **4ee3414bddd289ca7c9544a91ec39b8885f8dcde96fa0ffa0d56aebc38da1b00** — exactly the claimed SHA.
3. Ran the pipeline: ingest reproduced the RUNLOG's exact intermediate counts (1849 quadtree leaves, 3998 edges, 1024 motifs / 1536 blocks, **45,563 residuals** = 47.5% of pixels); emit produced renderB with SHA **4ee3414b… == claim**, and `cmp` confirms renderB **byte-identical** to original_512.bmp. renderA == renderB (same SHA), matching the RUNLOG.

**Taken from RUNLOG, not re-measured:** PSNR inf / SSIM 1.0000 (follows from byte-identity), determinism ×2 of knowmap+render (I ran the pipeline once), the deliverable gallery at ~/workspace/your_files/image_exact_NEW/ (not in the repo).

**Honest caveat on one input:** `common.zag` imports `./R33_NATIVE_IO_V1.zag`, which is *not* committed under `image_exact_work/` (the original crew's local copy never landed in git). I supplied it from the committed repo — byte-identical copies exist at `docs/lab/bytegen/authority_law/R33_NATIVE_IO_V1.zag` and `docs/lab/GROK47_OVERNIGHT/teacher/work/c3s_src/substrate/` (both SHA-256 e6379ddb…e9f61), version V1 matching the import. Everything else is the committed v3 tree.

## Honest caveats
- My Y-meandiff (0.66) exceeds the VERDICT's "Y meandiff 0.3": method difference. They extracted the Y plane from the decoder; I invert from clamped RGB, and RGB clamping destroys invertibility at ~3.4% of pixels (all top-|dY| pixels have clamped 0/255 channels). The decomposition (rebuild tests) bounds the true Y difference independently — chroma dominates either way.
- The VERDICT's JPEG 4:2:0 127×65 row has no sealed fixture in MANIFEST.sha256; not measured.
- Scratch workdir deleted after measurement; total new bytes in this deliverable < 1 MB.

## Gallery assets (full frames, no crops)
- `assets/lossless_m320_sidebyside.png` — input vs held for img_m320.png (320×240): side-by-side + |diff| panel (all black = byte-identical). NEW.
- `assets/jpeg420_sidebyside.png` — PIL reference vs held vs |error| heatmap (×2.2 amplified) for the 4:2:0 fixture. NEW.
- `assets/jpeg444_sidebyside.png` — same for the 4:4:4 fixture (heatmap ×40 amplified; maxdiff 3). NEW.
- No downscaling; all assets plain PNG files (no HTML, no external srcs).
