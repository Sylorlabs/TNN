# VERDICT — image zoom fork (deliberative variable-scale zoom)

Date: 2026-09-26. Order: Micah ~01:11 PDT — give the sealed Albi image knowledge
path a magnifying glass: deliberate variable-scale zoom, pre-residual
understanding vs v2b's 30.33 dB / 0.9177, residual closure kept explicitly separate.

## Verdict: ZOOM WINS — genuine understanding curve pushed past v2b

| Iteration | Vocabulary | PSNR (dB) | SSIM | Motifs |
|---|---|---|---|---|
| v0 | Structure: 1,849 quadtree leaves | 22.06 | 0.5953 | — |
| v1 | + Edges: 3,998 segments | 23.21 | 0.6617 | — |
| v2b (baseline) | + Texture: fixed 8×8 codebook, K=1024 cap | 30.40 | 0.9177 | 1024 |
| **zoom (this fork)** | **+ Zoom: 16×16 coarse + deliberative 8×8/4×4 zoom-in** | **30.80** | **0.9620** | **400** |
| zoom, coarse-only (ablation) | 16×16 motifs, zoom-in disabled | 30.33 | 0.9484 | 350 |
| v3 / zoom+residual | + Residual (honest error channel) | inf | 1.0000 | — |

PSNR = mean of per-channel dB; SSIM = Gaussian-window, per-channel mean.
All rows recomputed with one script (metrics.py) against the sealed fixture.
(v2b's frozen log reads 30.33/0.9177; same script on v2's render gives 30.40/0.9177 —
the +0.07 dB is metric-script drift, identical for all rows.)

**The zoom fork beats v2b by +0.40 dB / +0.0443 SSIM with 2.5× fewer motifs
(400 vs 1024).** The ablation splits the win cleanly:
- **Scale effect:** 16×16 coarse motifs alone (350) match v2b's PSNR (30.33 vs 30.40)
  with a third of the motifs and already beat its SSIM (0.9484 vs 0.9177).
- **Zoom-in effect:** the deliberative zoom-in adds +0.47 dB / +0.0136 on top
  (74 of 1,536 blocks, 4.8%, 49 fine motifs).

## White-box: why variable scale wins

1. **Coarser scale = denser patch space = convergence instead of saturation.**
   v2b's fixed 8×8 codebook hit its 1,024-motif guard and stopped on a compute-time
   bound, not on evidence. At 16×16, fine idiosyncrasies average out, so greedy
   farthest-point **converges on the data**: 350 motifs, last marginal gain 6,812
   < 6,912 threshold, zero cap hits. Each coarse motif application explains 4× the
   pixels of an 8×8 one.
2. **Zoom-in spends fine motifs only where the coarse description provably fails.**
   After L0, detail energy fell 119.3M → 3.43M (97.1% explained). TNN zoomed to 8×8
   only where block residual energy exceeded 8,192 — the bottom river strip with its
   ripple/reflection detail (y 176–186) — 74 blocks, 49 motifs, energy → 0.999M.
   The other 95.2% of blocks needed no finer look. v2b's uniform grid instead burns
   motifs on high-energy-but-unrepeatable fine detail.
3. **L2 honesty:** TNN reached for 4×4 on 49 blocks, but all were partial edge-row
   blocks (the image is 187 = 46×4+3 tall), so no full 4×4 block could serve as an
   exemplar. Recorded in the ledger, contributed nothing. The magnifier tried,
   the data said no, the ledger shows it.

## What was kept honest

- **Residual is the error channel, never understanding.** Zoom closes to byte-exact
  through 19,051 delta pixels (19.9% of 95,744) vs v3's 45,563 (47.5%) — the
  understanding render is genuinely closer, so the honest error channel is smaller.
  It is scored and reported separately, never headlined as zoom.
- **Structure/edges reproduce v0/v1 exactly** (same code path, same counts:
  1,849 leaves / 3,998 edges; 22.06/0.5953 and 23.21/0.6617 match within
  metric-script drift).
- **No arbitrary limits.** Motif counts are convergence outcomes (marginal-gain
  thresholds), never a K budget. Capacity arrays are sized from natural block
  counts (nb+1), not a 4096 cap.
- **Two independent render paths agree byte-identically** (ingest per-pixel lookup
  vs emit per-block stamping): renderA == renderB, understanding_A ==
  understanding_B.
- **Determinism ×2:** two full runs byte-identical — knowmap.bin, renderA/B,
  understanding renders, ZOOMLEDGER.txt (SHAs below).
- **Pure Zag, zero RNG** anywhere in the TNN paths. Farthest-point uses null-motif
  seed and lowest-index tie-breaking.

## Evidence SHAs (this fork, run/ = run2 = byte-identical)

- knowmap.bin: `966aa8e5dd9deb6f48bcf2215ee28b87ffe66ff4748f64e6ba1fc47eaf3aa7b8`
- render_understanding.bmp (= renderB_understanding.bmp):
  `27eb9d32c1714004f5704bc476b71c13a2b5ef6ace83d5b708bfdac201fc1404`
- renderA.bmp (= renderB.bmp = original fixture):
  `4ee3414bddd289ca7c9544a91ec39b8885f8dcde96fa0ffa0d56aebc38da1b00`
- ZOOMLEDGER.txt: `28147132cd208552857e09a1d46b278682e86676d318e33bbd3ac58ac22111e0`

Fixture integrity: original_512.bmp matches the sealed SHASUMS.txt
(`4ee3414b…b00`).

## Delivered

- Gallery: `index.html` in this directory — self-contained (10 images as data
  URIs, zero external loads), full renders + zoom-depth map + water/brick crops.
- Sources committed to `tnn-native-lab` branch at `docs/lab/image_zoom_fork/`:
  `common.zag`, `R33_NATIVE_IO_V1.zag`, `zoom.zag`, `ingest.zag`, `emit.zag`,
  `build.sh`, `metrics.py`, `RUNLOG.md`, `VERDICT.md` (this file),
  `evidence/ZOOMLEDGER.txt`.
- Workdir (not committed): `~/workspace/image_zoom_fork/`
  (sources, run/, run2/, run_coarse/, binaries, gallery builder).

## Boundary note

Zoom was not tuned past the first principled configuration (marginal-gain
thresholds matched to v2's never-triggered per-value ~= 9; zoom thresholds at
per-value ~= 32). The clean negative to watch: if zoom thresholds drop so low
that most blocks zoom, the mechanism degrades to a uniform fine grid and the
advantage over v2b should collapse — the deliberation (zoom only where coarse
provably fails) is the load-bearing part, not the multi-scale vocabulary alone.
That boundary was not mapped; the win stands at the tested configuration.
