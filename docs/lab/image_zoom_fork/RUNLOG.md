# RUNLOG — image zoom fork (deliberative variable-scale zoom)

Date: 2026-09-26. Order: Micah ~01:11 PDT.
Task: give the sealed Albi image knowledge path deliberative variable-scale
zoom; compare genuine pre-residual understanding against v2b (30.33 dB /
0.9177); keep residual closure explicitly separate; deliver code/evidence/
gallery; commit to `tnn-native-lab`.

## Fixture

- `~/workspace/your_files/image_repro/original_512.bmp` (512x187, 24-bit)
- SHA-256 `4ee3414bddd289ca7c9544a91ec39b8885f8dcde96fa0ffa0d56aebc38da1b00`
  matches sealed `~/workspace/your_files/image_exact_NEW/SHASUMS.txt`.

## Workdir

`~/workspace/image_zoom_fork/` — sources `common.zag` (copied from
`~/workspace/image_exact_work/`, the v0–v3 reference), `R33_NATIVE_IO_V1.zag`,
`zoom.zag`, `ingest.zag`, `emit.zag`, `build.sh`, `metrics.py`,
`build_gallery.py`; run dirs `run/` (primary), `run2/` (determinism rerun),
`run_coarse/` (ablation).

## Method

`zoom.zag` — deterministic hierarchical texture reconstruction over
`original − structure`:
1. 16×16 coarse motifs (farthest-point, null seed, lowest-index ties, zero RNG),
   converging on marginal explained-energy (tau0=6912 ~= per-value 9, matching
   v2's never-triggered T_TEX=1728 on 8×8).
2. Compute unexplained residual energy per 8×8 block; zoom where > tauz1=8192.
3. 8×8 fine motifs over zoomed blocks only (tau1=1728).
4. Zoom to 4×4 where remaining energy > tauz2=2048 (tau2=432).
5. Two render paths: ingest per-pixel lookup (path A) and emit per-block
   stamping (path B). `TNNKZMAP` knowledge-map format + optional exact residual.

Thresholds are argv-overridable (args 5–9); znc passes argc=0 so they are read
unconditionally via `_zag_arg`.

## Builds

```
./build.sh   # znc ingest.zag -> ingest_bin ; emit.zag -> emit_bin (both clean, first try)
```

Two bugs fixed during bring-up (both in my new code, not the mechanism):
- `emit.zag` file_read_all cap 60,000,000 > nio_alloc's 33,554,432 limit returned
  empty → "kmap too short". Set to 20,000,000 (v3's value).
- Gallery placeholder `__ORIG__` vs key-generated `__ORIGINAL__`.

## Runs

```
mkdir -p indir && cp <fixture> indir/
./ingest_bin indir run knowmap.bin renderA.bmp
./emit_bin run knowmap.bin renderB.bmp
./ingest_bin indir run2 knowmap.bin renderA.bmp && ./emit_bin run2 knowmap.bin renderB.bmp
./ingest_bin indir run_coarse knowmap.bin renderA.bmp 6912 1728 432 999999999999 999999999999
```

Primary run output (run/):
```
ingested 512x187
leaves 1849
edges 3998
zoom motifs L0/L1/L2: 350 / 49 / 1
zoomed blocks L1/L2: 74 / 49
residuals 19051 / 95744 px (198 per-mille)
```

## Metrics (metrics.py — PSNR = mean of per-channel dB; SSIM = Gaussian window,
per-channel mean; all rows same script, same fixture)

| render | PSNR dB | SSIM |
|---|---|---|
| run/render_struct.bmp | 22.06 | 0.5953 |
| run/render_edges.bmp | 23.21 | 0.6617 |
| run/render_understanding.bmp (zoom) | **30.80** | **0.9620** |
| run_coarse/render_understanding.bmp (16×16 only) | 30.33 | 0.9484 |
| v2/run/renderA.bmp (v2b baseline) | 30.40 | 0.9177 |
| run/renderA.bmp (zoom + residual) | inf | 1.0000 |

## White-box checks (all pass)

- `cmp run/renderA.bmp run/renderB.bmp` → identical (machinery lossless)
- `cmp run/render_understanding.bmp run/renderB_understanding.bmp` → identical
  (path A == path B on the zoom render)
- `cmp run/renderA.bmp <fixture>` → identical (exact closure via residual)
- Determinism ×2: run/ vs run2/ — knowmap.bin, renderA/B.bmp, both
  understanding renders, ZOOMLEDGER.txt all byte-identical.
- Structure/edges reproduce v0/v1 exactly (same code path: 1849 leaves,
  3998 edges).

## Ledger (run/ZOOMLEDGER.txt, byte-identical across runs)

```
thresholds: tau0=6912 tau1=1728 tau2=432 tauz1=8192 tauz2=2048
L0 16x16: motifs=350 caphit=0 first_gain=1682483 last_gain=6812 applied=384
L1 8x8: motifs=49 caphit=0 last_gain=0 zoomed_blocks=74 of 1536
L2 4x4: motifs=1 caphit=0 last_gain=0 zoomed_blocks=49 of 6016
energy: E_detail=119291319 E_after_L0=3426420 E_after_L1=999009
leaves=1849 edges=3998 residuals=19051 (error channel, not understanding)
```

Zoomed L1 blocks are all in the bottom river strip (y 176–186); L2's 49 flags
are all partial edge-row blocks (187 = 46×4+3) with no full-block exemplar —
recorded, contributed nothing.

## Gallery

`~/workspace/your_files/image_zoom_fork/index.html` — self-contained
(10 images as data URIs; verified zero non-data src, no <link>, no <script>),
full renders + zoom-depth map + 3× water-strip and 2× brick-building crops
(original | v2b | zoom). Plus VERDICT.md in the same directory.

## Commit

Committed to `tnn-native-lab` at `docs/lab/image_zoom_fork/`:
`common.zag`, `R33_NATIVE_IO_V1.zag`, `zoom.zag`, `ingest.zag`, `emit.zag`,
`build.sh`, `metrics.py`, `RUNLOG.md` (this file), `VERDICT.md`,
`evidence/ZOOMLEDGER.txt`. No binaries, no caches, no renders.
