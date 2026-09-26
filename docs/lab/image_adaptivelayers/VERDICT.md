# Adaptive Layers + Adaptive Magnification — Verdict

## Result: BEATS all three parents

| Metric | Parent 1 (TNN layers) | Parent 2 (no-layers adaptive) | Parent 3 (magnifying glass) | **NEW (this fork)** |
|--------|----------------------|-------------------------------|----------------------------|---------------------|
| Understanding PSNR | 43.43 dB | 30.50 dB | 30.80 dB | **46.35 dB** |
| Understanding SSIM | 0.9937 | 0.9183 | 0.9620 | **0.9955** |
| Residual share | 8.2% | 93.1% | 19.9% | **2.7%** |
| Knowledge bytes | 1,963,911 | 3,682,332 | 1,343,354 | **636,451** |

The NEW fork wins on all four metrics. The win is a free lunch: better quality AND fewer bytes.

## What TNN chose
- **Order**: SMOOTH → SHAPES-ZOOM → LINES (affinities 553 / 372 / 173 ‰ — same order as parent 1, independently chosen)
- **SMOOTH (adaptive CART)**: 1,778 leaves (vs parent 1's 973), G=6,311,802,255, 46,228 bytes. COMMIT.
  - The adaptive CART splits explain MORE energy (+0.77%) with MORE leaves. Content-adaptive positions beat fixed midpoints.
- **SHAPES-ZOOM**: 269 regions, G=57,044,876 (199/value), 571,565 bytes. COMMIT.
  - 96 fixed @32 blocks; 79 zoomed to @16/@8/@4 where measured residual demanded it.
  - Vocabularies: 80 @32, 32 @16, 68 @8, 3 @4 atoms (lazy, from candidates' full blocks).
- **LINES**: 27 segments, G=15,833 (66/value), 378 bytes. COMMIT.
  - Tiny — the residual after SMOOTH+SHAPES is mostly flat. Honest, not padded.

## Integrity
- **Exact closure**: Full render SHA-256 = `4ee3414bddd289ca7c9544a91ec39b8885f8dcde96fa0ffa0d56aebc38da1b00` = sealed fixture SHA. Bit-identical.
- **Path A == Path B**: `renderA.bmp` and `renderB.bmp` byte-identical (knowmap re-render matches ingest render).
- **Two official runs**: `run/` and `run2/` byte-identical across knowmap, renders, trace, and all maps.
- **Pentagon artifact**: ABSENT. Bridge arches are smooth curves (see crop). LINES ran last; curved segments failed the measured bar — same mechanism as parent 1.

## Why it wins
1. **Adaptive SMOOTH**: CART splits follow content boundaries (e.g., the river/bridge edge), not arbitrary midpoints. More leaves, but each leaf is more homogeneous → better fit per byte.
2. **Fixed-block SHAPES + zoom**: The vocabulary matches the block geometry. Zoom refines only where needed (79/96 blocks), avoiding parent 1's uniform 4-scale cost and parent 3's fixed-grid waste.
3. **Honest LINES**: Only 27 segments because the first two layers already explained the structure. Parent 1 needed 48; the better SMOOTH+SHAPES leaves less for LINES.

## Parent 1 byte-count discrepancy (standing note)
Parent 1's verdict reports 1,963,911 bytes; its task text reports 1,958,486 bytes (5,425-byte difference). This fork reports 636,451 bytes (the `knowmap.bin` file size). The comparison uses the verdict's 1,963,911 figure. The discrepancy is noted, not resolved.
