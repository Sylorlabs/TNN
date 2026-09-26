# VERDICT.md — image_nolayers_adaptive (rigid grid gone)

## The order

Micah (2026-09-26 ~09:54 PDT): "yes I want the rigid grid gone for no
layers, for a real result."

## The result

| Pipeline | PSNR | SSIM | Residual share | Knowledge bytes |
|---|---|---|---|---|
| Layered zoom fork | 30.80 dB | 0.9620 | 19.9% | 1,343,354 |
| No-layers, rigid grid | 29.27 dB | 0.9260 | 11.7% | 2,505,092 |
| **No-layers, adaptive splits** | **30.50 dB** | **0.9183** | **93.1%** | **3,682,332** |

- **Gap closed: 1.23 dB of the 1.53 dB (80%).** Remaining gap to zoom: 0.30 dB.
- SSIM slipped 0.0077 (0.9260 → 0.9183) — the price of many small tiles
  (50.9% of pixels sit on tile boundaries; SSIM penalizes the blocking
  more than PSNR does).
- Residual share jumped (11.7% → 93.1%) and knowledge bytes grew
  (2.51MB → 3.68MB): the error is now many small errors (~8 avg) rather
  than few large ones. The understanding itself is 30.50 dB; the residual
  is the exact-reconstruction contract, not a quality crutch.

## How much of the gap was the rigid grid?

**~80% (1.23 dB of 1.53 dB).** The rigid grid's dyadic boundaries
misaligned with content in the town band, forcing coarse 64×64 takes
where the content needed fine subdivision. Content-aligned CART cuts
recover most of it.

## The failure in the middle (honest)

The first adaptive run scored **21.42 dB** — worse than rigid. White-box
diagnosis: the inherited gain-per-byte take-vs-split, applied to a large
rect whose take tiles N atoms, aggregates N tiles into one greedy
decision. The root (512×187) TOOK at 64-scale for the whole image
(ea=137M); the town child (512×109) TOOK at 64 (ea=300M). Smooth tiles'
gains dragged complex tiles into coarse takes; the myopic recursion never
went deep. The rigid fork avoids this only because it decides per 64×64
block — no aggregation.

Fix (DESIGN.md amendment, structural not tuned): a take matches ONE
vocabulary atom. A rect bigger than its fit-scale atom (bw > s or bh > s)
MUST subdivide via the CART rule; only an atom-sized rect may deliberate
take-vs-split by the inherited gain-per-byte. Floor (no valid or no
energy-reducing cut) falls back to tiled take. One mechanism, one pass;
CART still chooses every position.

## Pentagon re-verification

The bridge arch at 10×: smooth curves in adaptive, rigid, and original.
The layered zoom's faceting is absent. The pentagon artifact stays
eliminated — exemplar patches contain real curves, and the CART cuts do
not reintroduce chord tracing. (Crops in gallery.)

## Remainder analysis (white-box)

The remaining 0.30 dB gap to the zoom fork points at:

1. **Square axis-aligned atoms.** The vocabulary's atoms are s×s squares.
   Diagonal boundaries (rooflines, bridge cables) still staircase. The
   error map shows the residual error concentrated along diagonals in the
   town band (y 70–116 holds 38.5% of the adaptive error vs 0% for rigid
   — the rigid's error was at the bottom, y 140–187, 93.1%).

2. **Axis-aligned CART cuts.** Cuts are vertical/horizontal only. A
   diagonal content boundary needs many staircase cuts to approximate.

3. **Tile-boundary discontinuities.** 50.9% of pixels are on boundaries;
   boundary mean abs err (4.279) ≈ interior (4.563) — no severe blocking,
   but SSIM sees it.

The zoom fork's edge stage traces curves explicitly, which is why it
keeps the 0.30 dB. Closing it would need non-square or oriented atoms —
a vocabulary change, not a deliberation change.

## Determinism

Pure Zag, zero RNG. Two independent runs byte-identical (knowmap,
understanding renders, full renders, scale map, trace; SHA-256 in
SHASUMS.txt). Path A (ingest) == Path B (emit) understanding; full
render == sealed fixture.

## What was committed

`tnn-native-lab`, `docs/lab/image_nolayers_adaptive/`: code (nolayers_ad.zag,
nlingest_ad.zag, nlemit_ad.zag, build_ad.sh, analyze.py, build_gallery.py),
docs (DESIGN.md + amendment, PROVENANCE.md, RUNLOG.md, VERDICT.md,
SHASUMS.txt), evidence (trace excerpts, metrics). No binaries, no renders,
no .zagd. Gallery: `~/workspace/your_files/image_nolayers_adaptive_NEW/index.html`
(self-contained, data URIs, zero external loads).
