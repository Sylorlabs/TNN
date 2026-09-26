# RUNLOG — image_exact_work (2026-09-26)

Micah order ~00:10 PDT: exact replica through the knowledge path (structure + texture).

## v0 — structure (baseline)
- 1,849 quadtree leaves, mean RGB + planar gradients. Threshold 2000 (prior approved).
- 21.95 dB / SSIM 0.5953. renderA == renderB (white-box). Deterministic ×2.

## v1 — + edges
- 3,998 straight segments (Sobel |gx|+|gy| > 96, quantized dir, greedy tracing, mean RGB).
- 23.07 dB / SSIM 0.6617 (+1.12 dB). renderA == renderB.

## v2 — + texture
- Detail = original − structure render; 8×8 blocks; greedy farthest-point motif selection.
- Null-texture motif (index 0) added after 256-motif run WITHOUT null scored 22.54 dB (worse than v1) — smooth blocks were forced onto high-energy motifs. With null: 25.66 dB / 0.7367 (+2.59 dB).
- K_MAX=1024: 30.33 dB / SSIM 0.9177 (+4.67 dB). K_MAX saturated (T_TEX=1728 never triggered) — compute guard, not a knowledge budget.

## v3 — + residual (EXACT)
- 45,563 sparse per-pixel deltas (47.5% of pixels), row-major, (pos, dr,dg,db).
- renderB == original_512.bmp byte-identical. SHA-256 4ee3414bddd289ca7c9544a91ec39b8885f8dcde96fa0ffa0d56aebc38da1b00.
- PSNR inf / SSIM 1.0000. renderA == renderB. Deterministic ×2 (knowmap + render).
- BMP header X/Y ppm set to 3780 to match original container (pixel data was already identical).

## Files
- common.zag: shared machinery (BMP IO, quadtree, edges, texture, residual, kmap).
- v0/, v1/, v2/, v3/: ingest.zag / emit.zag / build.sh per iteration.
- Toolchain: ~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1.
- Deliverable: ~/workspace/your_files/image_exact_NEW/ (self-contained index.html, VERDICT.md, KNOWLEDGE_MAP.md, SHASUMS.txt).
