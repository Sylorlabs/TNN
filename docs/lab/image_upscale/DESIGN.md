# HONEST UPSCALE — design

Micah order 2026-09-26 ~12:52 PDT: "since TNN is good at reproducing the same
image byte-for-byte, can it upscale it? ... another step towards image gen
with imagination."

This is the first imagination-grade image test: TNN must construct pixels it
was never given, from its own understanding — not a generic interpolator.

## Phase 1 — honest 2x upscale

**Protocol (frozen before running).**
1. Crop the sealed 512x187 fixture to 512x184 (drop bottom rows 184-186, the
   darkest foreground-water rows; top anchor preserved).
2. Downscale the crop to 256x92 with a documented 2x2 box filter,
   round-half-up: `(a+b+c+d+2)/4`. This is ALL TNN sees.
3. TNN re-runs the full adaptive-layers deliberation (survey, affinity order,
   commit/revert bar G >= 9N) on the 256x92 observation.
4. TNN constructs 512x184 from its COMMITTED layers:
   - SHAPES: each region's atom exemplar drawn at 2x as 2x2 blocks
     (nearest — the exemplar's content preserved exactly, no invented
     sub-atom detail). Region pixel (ix,iy) -> value = mean + atom(iy*s+ix),
     drawn as a 2x2 block.
   - LINES: segments re-rasterized at doubled endpoints (same Bresenham
     arithmetic), segment mean values.
   - SMOOTH: planar leaves re-sampled at half-pixel offsets
     (v = m + (ax*du2+ay*dv2)/512) — IF committed.
   - Even positions (2x,2y) are OBSERVED: the residual channel covers them,
     so they reproduce the input exactly.
   - Odd pixels no committed layer covers are INVENTED: TNN repeats the
     nearest observed pixel (top-left even neighbor) — the most conservative
     invention, one step from an observation.
5. Bicubic baseline (Catmull-Rom, exact integer arithmetic, t=0.5 weights
   [-1,9,9,-1]/16, separable, edge-clamped) implemented in the same Zag
   binary, from the same input.
6. Both compared against the HELD 512x184 ground truth (integer-exact SSE
   per channel; PSNR via the parent experiment's metrics.py convention:
   mean of per-channel dB; SSIM via metrics.py).

**Epistemic labeling** (every output pixel):
- 0 KNOWN: observed / residual-covered (even positions).
- 1 CONSTRUCTED-SMOOTH: planar model.
- 2 CONSTRUCTED-LINES: segment model.
- 3 CONSTRUCTED-SHAPES: atom exemplar.
- 4 INVENTED: no layer model (nearest-observed fill).
- 5 CONSTRUCTED-SHAPES-EXTRAP: outpaint strip only.

A label map is rendered. TNN's deliberation trace (order, gains, commit/
revert decisions, per-region construction notes) is written as
UPSCALE_TRACE.txt.

**What actually happened (deviation from the plan, recorded honestly).**
The plan assumed SMOOTH would commit (as at full res). On the 256x92
observation TNN's deliberation chose order SHAPES -> LINES -> SMOOTH and
REVERTED SMOOTH (G=12558, N=70656, 0.18/value vs the 9 bar). The
construction follows TNN's deliberation, not the plan's assumption:
no SMOOTH render, no planar fallback. Odd pixels with no committed-layer
coverage are INVENTED (in the event: zero — SHAPES+LINES cover the frame).

## Phase 2 — outpaint (imagination)

Extend 64px on the RIGHT. Why the right: the right edge carries the river,
the far bank, and open sky — horizontally-continuous scene elements. The
left edge is the brick building wall, an occluder whose continuation is
unconstrained.

Construction: the right border is covered by 3 committed SHAPES regions.
SMOOTH was reverted, so there is no committed planar model — recorded, not
worked around. Each strip pixel takes its row's border region's edge column
(value = region.mean + region.atom[rightmost column][iy]); the edge texture
continues horizontally. No atom structure is invented past the edge column.
LINES segments are NOT extended (recorded decision: they describe observed
structures). All 11,776 strip pixels labeled CONSTRUCTED-SHAPES-EXTRAP (5) —
never observed.

## Standing constraints honored

- Pure Zag, zero RNG, pinned toolchain
  (~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1).
- Two byte-identical reruns (run/, run2/); all deterministic outputs
  compared by SHA-256.
- Never present constructed pixels as observed; the label map marks every
  pixel's epistemic status.
- Micah's eyes are the primary judge; numbers are secondary.
- Gallery is self-contained (data URIs, zero external loads).
- Repo gets code + docs + verdict evidence only (no binaries, no .zagd,
  no caches, no regenerable renders).
