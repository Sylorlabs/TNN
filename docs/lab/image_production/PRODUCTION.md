# TNN Production Image Pipeline — Adaptive Layers + Adaptive Magnification

**Status: PRODUCTION.** Adopted by Micah order 2026-09-26 ~12:52 PDT ("adopt it — it wins every category").
This directory is THE live image path for TNN. Retired pipelines are documented in
`NEGATIVE_CONTROLS.md`; they stay in the repo as evidence but are never callable from here.

## What it is

A pure-Zag (zero RNG) fork combining three parent ideas, promoted from
`docs/lab/image_adaptivelayers/`:

1. **TNN-chosen layers** — Survey → per-mille affinities → TNN selects its own layer
   order (SMOOTH → SHAPES-ZOOM → LINES). Measured commit/revert bars (gain ≥ 9/value).
2. **Content-adaptive CART splits** in the structural layer — the SMOOTH layer uses
   deterministic content-adaptive CART binary splits (energy-minimizing cut positions,
   4px minimum, strict-improvement for deterministic ties) instead of a fixed midpoint
   quadtree.
3. **Per-region adaptive magnification** — the SHAPES layer assigns fixed s×s blocks at
   the coarsest scale chosen by the repetition probe, then zooms individual blocks to
   finer scales only when measured residual energy demands it (`post-atom residual > 27·w·h`)
   AND the finer assignment wins on measured gain-per-byte (`gf·cc > gc·c_fine`).
   Finer vocabularies are built lazily, from candidate regions' full blocks.

Knowmap format: magic `TNNKTLM3`; 17-byte region records (u16 x,y,w,h + u8 s + u16 atom + i16 m[3]).

## The numbers (sealed fixture, byte-identical reruns)

| Metric | Production value |
|---|---|
| Understanding PSNR | 46.35 dB |
| Understanding SSIM | 0.9955 |
| Residual share | 2591/95744 px = 2.7% |
| Knowledge (knowmap.bin) | 636,451 bytes |
| Layer order | SMOOTH → SHAPES-ZOOM → LINES |
| SMOOTH | 1,778 CART leaves, G=6,311,802,255, 46,228 B |
| SHAPES-ZOOM | 269 regions (79 zoomed), 571,565 B |
| LINES | 27 segments, 378 B |
| Pentagon artifact | ABSENT (bridge arches render as smooth curves) |

## Closure contract (load-bearing)

1. **Exact closure**: full render SHA-256 == sealed fixture SHA
   (`4ee3414bddd289ca7c9544a91ec39b8885f8dcde96fa0ffa0d56aebc38da1b00`).
2. **Path A == Path B**: ingest's `renderA.bmp` byte-identical to emit's `renderB.bmp`
   (emit re-renders from `knowmap.bin` only, with the same shared render functions).
3. **Determinism**: two ingest+emit runs byte-identical on knowmap, all renders,
   DELIBTRACE.txt, and layer/scale/split maps. Zero RNG anywhere.

A future change that breaks any of these three does not ship. Regression evidence:
`REGRESSION.md`.

## Build and run

Pinned toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
(Building on another toolchain requires a full byte-identical reproduction first.)

```bash
cd src && ./build.sh                      # -> azingest_bin + azemit_bin
azingest_bin <indir> <outdir> knowmap.bin renderA.bmp    # indir holds original_512.bmp
azemit_bin <outdir> knowmap.bin renderB.bmp
python3 src/metrics.py <indir>/original_512.bmp <outdir>/render_understanding.bmp
```

Ingest ≈15s, emit ≈2s. Self-contained: all `@import`s resolve inside `src/`.
Mentions of retired pipeline names in source comments are provenance notes only —
nothing here imports, calls, or reads from any retired directory.

## Sources

SHA-256 manifest: `MANIFEST.sha256`. Seven files, nothing else:
`R33_NATIVE_IO_V1.zag`, `common_az.zag`, `azlayers.zag`, `azingest.zag`,
`azemit.zag`, `build.sh`, `metrics.py`.
