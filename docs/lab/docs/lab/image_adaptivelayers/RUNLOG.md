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

### Metrics (run1)
- Understanding: 46.35 dB PSNR, 0.9955 SSIM (via `src/metrics.py`).
- Residual: 2,591 / 95,744 px = 2.7%.
- Knowmap: 636,451 bytes.
- Layers: SMOOTH (46,228 B) → SHAPES-ZOOM (571,565 B, 269 regions, 79 zoomed) → LINES (378 B, 27 segs).

### Gallery
- `~/workspace/your_files/image_adaptivelayers_NEW/index.html` — self-contained (data URIs, zero external loads). Full artifacts + bridge-arch crop + parent comparison table.
