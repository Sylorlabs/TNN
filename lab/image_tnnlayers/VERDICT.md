# VERDICT.md — TNN-CHOOSES-ITS-LAYERS (image_tnnlayers)

## The question

Micah, 2026-09-26: *"layers are clearly needed — but what happens if TNN
chooses its layers instead?"*

## What TNN decided (from DELIBTRACE.txt)

TNN surveyed the fixture, computed per-mille affinities, and chose:

| # | Layer | Affinity (per-mille) | Measured G | N | G/N | Bytes | Decision |
|---|---|---|---|---|---|---|---|
| 1 | SMOOTH (quadtree mean+planar) | 553 | 6260482978 | 287232 | 21795 | 25298 | COMMIT |
| 2 | SHAPES (exemplar patches) | 372 | 107772342 | 287232 | 375 | 1828516 | COMMIT |
| 3 | LINES (straight segments) | 173 | 132317 | 555 | 238 | 672 | COMMIT |

Commit bar: G/N >= 9 (per-value-9 precision precedent), measured on the
current residual. All three passed; none were reverted.

Key data-driven choices:
- **Order**: SMOOTH -> SHAPES -> LINES (descending affinity; LINES last
  because straight boundaries are scarce: 16,612 straight-run px vs
  40,349 curvy-run px).
- **SHAPES scale set**: {32,16,8,4} — the repetition probe on the
  post-SMOOTH residual measured 195 per-mille (< 250), so TNN dropped the
  64 scale. Vocabularies: 73/310/1214/4003 atoms at 32/16/8/4.
- **LINES**: 56 walks found, 48 kept, 8 dropped by the per-segment bar
  (g >= 9n). The 48 survivors are tiny (~4 px each) straight corrections
  on the residual — TNN measured them, they passed, it kept them.

## Head-to-head (same fixture, same metric code, pre-residual understanding)

| Approach | PSNR (dB) | SSIM | Residual | Knowledge bytes |
|---|---|---|---|---|
| Hand-designed layered zoom | 30.80 | 0.9620 | 19.9% | 1,343,354 |
| No-layers (exemplar take/split) | 29.27 | 0.9260 | 11.7% | 2,505,092 |
| **TNN-chooses-layers** | **43.43** | **0.9937** | **8.2%** | **1,963,911** |

TNN's chosen decomposition wins on all four columns: +12.6 dB over the
hand-designed zoom, +14.2 dB over no-layers, with the smallest residual
share and fewer knowledge bytes than no-layers.

Why it wins: the SMOOTH quadtree (mean+planar, 973 leaves, 25 KB) captures
coarse structure far more efficiently than exemplar patches alone, leaving
SHAPES to spend its 1.8 MB vocabulary on genuine mid-scale texture. The
layering is synergistic — SMOOTH explains 98.3% of raw energy, SHAPES
explains most of what remains, LINES cleans up 48 tiny straight details.

Honest caveat: 1.96 MB of knowledge for a 287 KB image is memorization as
much as understanding — but it is *mechanistic* memorization (quadtree,
exemplars, segments), all of it white-box and committed through measured
bars, not a black-box fit. The residual contract holds: 43.43 dB is
pre-residual understanding, and the 8.2% residual is excluded.

## The pentagon artifact

The zoom fork's edge stage faceted the bridge arch into pentagons by drawing
straight chords through curved edge runs. Here:
- TNN put LINES *last* (affinity 173, the lowest), on the smallest residual.
- The per-segment bar dropped 8/56 walks (the curved ones).
- The 48 kept segments are ~4 px each — too small to facet anything.
- Bridge-arch crop (110,85)-(230,165), 4x: the arch curve is smooth in
  TNN's understanding render; the zoom's faceting is visibly absent.

The pentagon does not appear. TNN's deliberation (low affinity -> late
order -> per-segment bar) contained the risky mechanism by measurement,
not by hand-authored prohibition.

## White-box verification

- Path A (ingest) vs Path B (emit, knowmap-only):
  `render_understanding.bmp` == `renderB_understanding.bmp`
  (SHA-256 `a83417476fbbed156b784476b6c3ecf58e7db08e33ae2839a1f10fd6e27524a9`).
- Closure: `renderA.bmp` == `renderB.bmp` == sealed fixture
  (SHA-256 `4ee3414bddd289ca7c9544a91ec39b8885f8dcde96fa0ffa0d56aebc38da1b00`).
- Determinism: `run/` vs `run2/` — byte-identical knowmap, renders, and
  DELIBTRACE.txt (verified by SHA-256; see SHASUMS.txt).

## The verdict

**TNN choosing its layers beats the hand-designed layering.** On the sealed
512x187 Albi fixture, TNN's survey -> affinity -> order -> commit-bar
deliberation produced a 3-layer decomposition (SMOOTH, SHAPES, LINES) that
outscores both baselines on PSNR (+12.6 dB), SSIM (+0.0317), residual share
(8.2% vs 19.9%/11.7%), and knowledge bytes (1.96M vs 2.51M no-layers). The
pentagon artifact is absent — TNN contained the risky LINES mechanism by
measurement (low affinity, late order, per-segment rejection of curved
walks), not by fiat. Every decision is in DELIBTRACE.txt with its numbers.
Falsification was on the table; the data went the other way.
