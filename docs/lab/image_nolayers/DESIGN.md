# DESIGN.md — NO-LAYERS image capture fork

Date: 2026-09-26. Order: Micah ~09:27 PDT.
Question (verbatim in spirit): "I saw the images — it got it after a bunch of
layers, but it should get it without. Try that fork and see what happens:
do layers help or are they needed?"

## What "layers" means here

The layered pipeline (v0→v3, then the zoom fork) captures the sealed Albi
image (512x187, SHA-256 `4ee3414b…`) in four separate stages, each with its
own vocabulary and its own pass:

| stage | vocabulary | mechanism |
|---|---|---|
| structure | 1,849 quadtree leaves | mean + planar gradient per leaf |
| edges | 3,998 straight segments | Sobel → quantized direction → greedy tracing |
| texture (zoom) | 400 motifs (350×16×16 + 49×8×8 + 1×4×4) | farthest-point over detail blocks, zoom where dense |
| residual | 19,051 sparse per-pixel deltas | exact error channel (not understanding) |

Headline (zoom fork): pre-residual **30.80 dB / SSIM 0.9620**, residual
19.9% of pixels.

## The no-layers design

ONE deliberative pass, TNN's OWN organization of the knowledge. No handed
stage boundaries.

**Single knowledge claim** (the only claim type in the system):
> "I looked at region R and saw an instance of the shape I saw at
> exemplar E; its mean color is (r,g,b)."

**Mechanism** (pure Zag, zero RNG, deterministic):

1. **SURVEY.** TNN looks at the image before organizing: per scale
   s ∈ {64,32,16,8,4}, the total energy that would remain if every
   s×s block were flat at its own mean. This is TNN's opening
   observation, recorded in DELIBTRACE.txt.

2. **VOCABULARY.** One pool of *shape atoms*: exemplar patches,
   mean-subtracted, at the five scales. Selected by ONE farthest-point
   deliberation per scale over the union of candidate blocks (full blocks
   only). Atom 0 of every scale is the NULL shape ("flat at its mean").
   Selection converges on marginal explained-energy
   `tau_s = 9 · 3 · s²` (per-value 9 — the precedent of v2's
   never-triggered T_TEX=1728 on 8×8): a precision parameter, never a
   motif-count cap. Caps are data-derived (≤ candidate count per scale),
   never magic constants (no-stupid-limits law).

3. **ASSIGNMENT — the single deliberation.** Nested block grids
   (64→32→16→8→4). Each region either TAKES its best same-scale atom
   (min SSD on mean-subtracted patches; per-region mean is free, so
   atoms match SHAPE and the mean carries color) or SPLITS into four
   children. The decision is **gain-per-byte** against the flat-mean
   baseline, exact integer cross-multiplication, ties → TAKE (coarser
   wins). Floor at 4×4 (must take). Region records are 10 bytes
   (x, y, s, atom, r, g, b). The scale map this produces —
   render_scalemap.bmp — is where TNN itself chose to look closely:
   TNN's own organization of the image.

4. **RENDER.** pixel = clamp(atom_shape + region_mean). Two white-box
   paths: A (ingest, per-pixel via region-id map) and B (emit,
   per-region stamping from the knowledge map alone). They must agree
   byte-identically.

5. **RESIDUAL.** The honest error channel (same contract as the layered
   pipeline): sparse per-pixel deltas to exact closure, EXCLUDED from
   all understanding metrics. Keeping it is not a layer — it is the
   exactness mechanism both forks share, so the comparison is apples
   to apples.

**Knowledge map** "TNNKNLM1": magic, w/h, 5 scales × (B, na, na
shape-atoms as i16, na exemplar ids), region list, residual list.

## Why this is a fair test of the question

- Same fixture (sealed SHA verified before any run).
- Same understanding metric: PRE-residual PSNR/SSIM via the same
  metrics.py.
- Same residual honesty rule: residual share reported, never counted
  as understanding.
- Same determinism bar: byte-identical reruns ×2 (knowmap, renders,
  deliberation trace).
- The no-layers fork is allowed to use as much knowledge as its
  convergence criterion selects — the question is whether TNN's own
  organization matches the hand-layered one, not who uses fewer bytes.
  Knowledge bytes are reported honestly for both.

## White-box prediction (to be tested, not assumed)

The layered pipeline's stages have DIFFERENT cost structures for
different content: smooth regions cost ~bytes/leaf, long straight
boundaries cost ~bytes/segment, repeating texture costs ~bytes/motif.
The no-layers vocabulary has a UNIFORM cost structure (atoms cost
3·s² bytes regardless of content). The predicted failure mode, if any:
long straight/diagonal boundaries (rooflines, bridge cables, building
edges) — the edge stage draws EXACT segments, while a block vocabulary
must staircase them with small atoms. The error map will show whether
this is where the dB go. If TNN's atom adoption order re-derives
coarse-smooth → boundary → fine-detail sequencing on its own, the
layers were TNN-natural organization, not scaffolding.

## Standing rules honored

- Pure Zag mechanism; zero RNG; byte-identical reruns ×2.
- No arbitrary limits: scales from image dims (powers of 2, floor 4),
  taus from the per-value-9 precedent, caps from candidate counts.
- Honesty: if no-layers loses, the loss is reported with the
  mechanical reason. A clean negative is a valid result.
