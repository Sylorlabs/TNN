# DESIGN.md — TNN-CHOOSES-ITS-LAYERS (image_tnnlayers)

## The order

Micah, 2026-09-26 ~09:54 PDT: *"layers are clearly needed — but what happens if
TNN chooses its layers instead? Let's try that."*

The layered zoom fork (30.80 dB / 0.9620 SSIM) beat no-layers (29.27 dB /
0.9260 SSIM), but its layer decomposition was hand-designed. This fork asks:
can TNN itself survey the image, choose how many layers it needs, pick the
mechanisms and vocabularies, order them, and commit each one only if it earns
its place? The deliberation is part of the artifact: `DELIBTRACE.txt` records
the survey, the affinities, the chosen order, every gain measurement, and
every commit/revert decision with reasons — in TNN's voice.

## The mechanism menu (fixed; the *selection* is TNN's)

TNN does not invent mechanisms from nothing — it chooses from a menu of three
candidates, each a real image mechanism implemented in pure Zag:

1. **SMOOTH** — content-adaptive quadtree; each leaf stores its mean plus
   least-squares planar gradients (dx, dy per channel). A node splits iff the
   split's measured SSD gain is >= 9 per value (the per-value-9 precision
   precedent from the zoom fork), down to 4x4 leaves. 26 bytes/leaf.
2. **LINES** — Sobel strong-edge pixels (|sobel| >= 27 on luminance),
   direction quantized to 4 bins, deterministic greedy walks, one straight
   Bresenham chord per walk. Each candidate segment must pass a per-segment
   bar (gain >= 9 per claimed value) or it is dropped — curved walks whose
   chord mismatches the real curve fail this bar. 14 bytes/segment.
3. **SHAPES** — multi-scale mean-subtracted exemplar patches: one
   farthest-point vocabulary per scale (atom 0 = flat NULL), then the
   take-or-split deliberation from no-layers (gain-per-byte, ties -> take,
   floor at the finest chosen scale). The *scale set* is TNN's choice (see
   below), not the hand-picked {64,32,16,8,4}. 13 bytes/region + atoms.

LINES is included deliberately as the pentagon-risk candidate: the zoom fork's
edge stage polygonized the bridge arch because it drew straight chords through
curved edge runs. TNN gets to try it, measure it, and reject it if the numbers
don't work. If it commits LINES and the pentagon comes back, that failure is
visible in the trace and the verdict — falsification is a valid result.

## What TNN decides (nothing hand-authored)

- **Survey.** Before choosing, TNN measures: flat-block SSD energies at
  64/32/16/8/4 vs the global mean; Sobel edge/run analysis separating
  straight boundary pixels (runs >= 16) from curvy ones (runs 2..15).
- **Affinities (per-mille, data-derived):**
  - SMOOTH = 1000 * (Etot - E64) / Etot (coarse-smooth share)
  - LINES  = 1000 * straight_px / npix (straight-boundary density)
  - SHAPES  = 1000 * (E64 - E4) / Etot (mid-scale structure share)
- **Order** = descending affinity; ties break SMOOTH, LINES, SHAPES.
- **SHAPES scale set** from a repetition probe on the current residual:
  8x8 mean-subtracted blocks, each block's best match among blocks with
  index%4==0; rep = per-mille of blocks matching under SSD 1728
  (= 9*3*64, the per-value-9 precedent at 8x8).
  rep >= 250 -> {64,32,16,8,4}; rep >= 100 -> {32,16,8,4};
  else -> {64,32,16}.
- **Commit bar.** Each candidate runs on the *current residual* (i64 space).
  COMMIT iff measured G/N >= 9, where G is the SSD the layer explains and N
  the values it covers. Otherwise REVERT: records discarded, residual
  restored, rejection written to the trace with the measured shortfall.

The residual image is maintained in i64 throughout; understanding is the sum
of committed layer reconstructions, clamped once at the end (path A). The
residual channel (per-pixel deltas where |error| >= 9) is the honest error
channel, excluded from understanding metrics, exactly as in the prior forks.

## White-box verification

Same contract as the prior forks: `tlemit` reads ONLY `knowmap.bin`
(`TNNKTLM1` magic), re-renders each committed layer with the *same* shared
render functions ingest used, clamps to `renderB_understanding.bmp`, applies
residual deltas to `renderB.bmp`. Understanding metrics (PSNR/SSIM) are
computed pre-residual; `renderA.bmp` must equal the sealed fixture exactly.

## Determinism

Zero RNG in any decision path. Farthest-point selection, walk order, quadtree
recursion, affinity ties — all deterministic, lowest-index/canonical
tie-breaking. Two runs must produce byte-identical knowmap, renders, and
deliberation trace.

## Files

- `tnnlayers.zag` — mechanisms, survey, renderers, knowmap writer (imports
  `common_tl.zag` plumbing + `R33_NATIVE_IO_V1.zag`)
- `tlingest.zag` — the deliberation orchestrator: survey -> affinities ->
  order -> cascade with commit/revert -> renders + knowmap + trace
- `tlemit.zag` — independent knowmap-only re-render (path B)
- `build.sh`, `metrics.py` (copied from the zoom fork's metric definition)
- `run/`, `run2/` — the two official runs (byte-identical)

## Result

(See VERDICT.md for the measured outcome, the layer list TNN chose with
reasons, the pentagon finding, and the head-to-head table.)
