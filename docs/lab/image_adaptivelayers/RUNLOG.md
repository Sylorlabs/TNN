# Adaptive Layers + Adaptive Magnification — Run Log

## 2026-09-26

### Setup
- Base: `image_tnnlayers` (TNN-chosen layers, measured bars, exact closure).
- Fixture: Sealed `original_512.bmp` (SHA-256 `4ee3414bddd289ca7c9544a91ec39b8885f8dcde96fa0ffa0d56aebc38da1b00`).
  - Corrected from wrong `image_zoom_fork/circ_in/original_512.bmp` (SHA `2da0c6c7...`, 286,408 bytes differ).
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (pinned).

### Implementation
- `src/common_az.zag`, `src/azlayers.zag`, `src/azingest.zag`, `src/azemit.zag`, `src/R33_NATIVE_IO_V1.zag`, `src/metrics.py`.
- **SMOOTH**: Replaced fixed midpoint quadtree with `tl_smooth_build_ad` (deterministic CART, `tl_cart_cut`).
- **SHAPES-ZOOM**: `tl_shapeszoom_build` — fixed s×s blocks at coarsest scale, per-block `tl_rect_take`, lazy finer vocabs, zoom iff `gf·cc > gc·c_fine`.
- **Rectangle geometry**: Final records carry `hrw/hrh`; `tl_shapes_render` renders `rw×rh`; knowmap magic bumped to `TNNKTLM3` (17-byte region records: u16 x,y,w,h + u8 s + u16 atom + i16 m[3]).

### Bug found and fixed
- **Negative G in SHAPES-ZOOM**: Initial draft CART-partitioned the SHAPES regions, creating tiny (4×5) rectangles matched against 32×32 atoms → G=-754M (reverted). Root cause: `tl_shapes_render` assumed s×s squares; rectangle w/h was lost. Fixed by carrying w/h through to render and knowmap. Then simplified: SHAPES uses fixed blocks (not CART) — Micah's "adaptive" is the SMOOTH CART, not SHAPES partition. Result: 46.35 dB (was 26.98 dB).

### Official runs
- **Run 1** (`run/`): 2026-09-26 ~19:17 PDT. Ingest ~60s, emit ~7s.
- **Run 2** (`run2/`): 2026-09-26 ~19:18 PDT. Ingest + emit.
- **Byte identity**: knowmap.bin, renderA.bmp, renderB.bmp, render_understanding.bmp, renderB_understanding.bmp, DELIBTRACE.txt, render_layermap.bmp, render_scalemap.bmp, render_splitmap.bmp — all MATCH across run1/run2.
- **Exact closure**: `renderA.bmp` SHA = sealed fixture SHA. Path A == Path B.

### Polish: dimension-derived capacities (2026-09-26 ~20:15 PDT)

All working capacities converted from fixture-derived/round-number
constants to proven dimension-derived bounds (Micah's no-arbitrary-limits
law). Changed in `src/azlayers.zag` + `src/azingest.zag`:
`dcap 16384 -> w*h+1`, `scap 2048 -> s_of(0)^2+1`, `regcap 8192 -> w*h+1`,
SMOOTH `leafcap 8192 -> w*h+1`, LINES `segcap 4096 -> w*h+1`,
walk-record `wcap 4096 -> w*h+1`, walk-pixel `WCAP 16384 -> w*h+1`,
Bresenham `2048 -> w+h+1` (2 sites). Proofs in code comments (partition
argument: every buffer holds pairwise-disjoint >=1-px records).
Rebuilt with the pinned toolchain; two fresh runs (`run3/`, `run4/`):
- knowmap.bin, renderA/B.bmp, DELIBTRACE.txt byte-identical to the
  pre-polish official runs AND across run3/run4 (determinism holds;
  no old capacity ever bound on the fixture).
- Exact closure kept: renderA SHA-256 = sealed fixture SHA.
- Metrics unchanged: 46.35 dB / 0.9955 SSIM, residual 2,591/95,744 px.
Residual fixed constants (not decision machinery): 4MB input-file
staging buffer, 4MB trace text buffer.

## Parent 1 byte-count discrepancy — RESOLVED (2026-09-26)
The verdict's 1,963,911 bytes is CORRECT. Verified: parent 1's own
`run/knowmap.bin` and `run2/knowmap.bin` are both exactly 1,963,911
bytes; its `run/metrics.json` records `"kb": 1963911`; its RUNLOG.md,
VERDICT.md, FREELUNCH.md, and RUNLOG_FL.md all state 1,963,911. The task
text's 1,958,486 figure appears in no artifact on disk and corresponds
to no run — it was an erroneous number in the brief. Comparison stands:
636,451 vs 1,963,911.

## Diagonal staircasing — CLOSED (2026-09-26)
Measured, not prototyped: on the understanding render (46.35 dB),
diagonal-edge neighborhoods (Sobel orientation within 22.5° of 45°/135°,
2px dilation) score PSNR 45.04 dB vs 43.81 dB for axis-aligned-edge
neighborhoods. At matched edge strengths: mag [238,400) -> diagonal
mean|res| 0.066 vs axis 0.143; mag [400,700) -> diagonal 0.000 vs axis
0.196. Only 28 of the 963 worst-1% residual pixels sit in diagonal
neighborhoods (93 in axis neighborhoods). Diagonal edges are the
*better*-handled class — the adaptive zoom refines wherever residual
energy demands it, regardless of orientation. Oriented/non-square atoms
would buy nothing measurable; no prototype warranted. The zoom covers it.

## Metrics (run3, post-polish)
- Understanding: 46.35 dB PSNR, 0.9955 SSIM (via `src/metrics.py`).
- Residual: 2,591 / 95,744 px = 2.7%.
- Knowmap: 636,451 bytes.
- Layers: SMOOTH (46,228 B) → SHAPES-ZOOM (571,565 B, 269 regions, 79 zoomed) → LINES (378 B, 27 segs).

### Gallery
- `~/workspace/your_files/image_adaptivelayers_NEW/index.html` — self-contained (data URIs, zero external loads). Full artifacts + bridge-arch crop + parent comparison table.
