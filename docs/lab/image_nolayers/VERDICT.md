# VERDICT.md — NO-LAYERS image capture fork

Date: 2026-09-26. Order: Micah ~09:27 PDT ("do layers help or are they needed?"),
plus artifact follow-up ~09:38 PDT (circles-into-pentagons).

Fixture: `~/workspace/your_files/image_repro/original_512.bmp`, 512x187,
SHA-256 `4ee3414bddd289ca7c9544a91ec39b8885f8dcde96fa0ffa0d56aebc38da1b00`
(sealed; verified before any run).

## The fork

ONE deliberative pass, TNN's OWN organization. No structure/edge/texture
stages. One scale-polymorphic shape vocabulary (mean-subtracted exemplar
patches at 64/32/16/8/4, selected by one farthest-point pass per scale,
convergence tau_s = 9*3*s^2 — per-value 9, the v2 never-triggered
precedent). Each region takes its best same-scale atom or splits into
children, decided by gain-per-byte vs the flat-mean baseline (exact integer
cross-multiplication, ties -> take/coarser). Residual is the same honest
error channel both forks share, excluded from understanding metrics.

## Headline results (pre-residual understanding)

| Pipeline | PSNR | SSIM | Residual share | Knowledge bytes |
|---|---:|---:|---:|---:|
| Layered v3 (struct+edges+texture) | 30.33 dB | 0.9177 | 47.5% (45,563 px) | — |
| Layered zoom fork | **30.80 dB** | **0.9620** | 19.9% (19,051 px) | 1,343,354 |
| **NO-LAYERS (this fork)** | **29.27 dB** | **0.9260** | **11.7% (11,262 px)** | 2,505,092 |

## Verdict

**Layers HELP (+1.53 dB / +0.036 SSIM) but are NOT NEEDED.** No-layers
captures the image at 29.27 dB / SSIM 0.9260 on TNN's own organization —
no collapse — and beats layered-v3 on SSIM (0.9260 > 0.9177). But the
layered pipeline is more byte-efficient: no-layers spends ~1.9x the
knowledge bytes for less quality.

**Error character differs**: mean abs error is nearly identical
(2.10 layered vs 2.12 no-layers), but no-layers' errors are CONCENTRATED
in the dense town/building band while layered spreads smaller errors
everywhere. PSNR punishes the concentrated large errors.

**White-box reason for the gap** (mechanical, not vibes): the layered
pipeline's quadtree partition is content-adaptive (splits follow variance),
while no-layers uses a rigid nested grid — a building edge at an arbitrary
grid offset can only match an exemplar whose edge sits at the same offset,
so atoms mismatch at content boundaries. The edge layer's exact-positioned
straight segments also win on long boundaries (rooflines, bridge lines).

## The pentagon artifact (Micah's eyes, white-boxed)

**Mechanism (named): greedy same-direction chord tracing.** The layered
pipeline's edge stage (`deliberate_edges`) quantizes Sobel direction into
4 bins, then greedily walks pixels sharing one direction code. Each walk
is a straight run along one of 4 orientations. A smooth curve's direction
rotates continuously, so the walk breaks at every quantum boundary and the
curve is re-emitted as a polyline of short straight chords (2–15 px,
axis/45° only), Bresenham-drawn. A 28-px-radius bridge arch becomes
~10–15 chords — visibly polygonal. Verified: 46 segments ≥4 px parsed from
the zoom knowmap trace the arch as red chords (gallery overlay); the
structure+edges render shows the polygon BEFORE texture is applied.

The texture layer cannot erase it: arch blocks stayed at zoom-depth 0
(16x16 grid exemplars, never position-aligned to the arch). The residual
hides it only in the exact final render.

**No-layers ELIMINATES the artifact.** Exemplar patches CONTAIN real
curves; stamping them reproduces smooth curves — no polygonization step
exists. Gallery shows original vs zoom (faceted) vs no-layers (smooth) at
10x. The polygon is created by the layered pipeline's edge representation,
not by anything deeper.

**Which layer carries smooth curves? NONE.** No layer in the layered stack
represents smooth curves: the edge layer destroys them (polygonizes), the
structure layer is piecewise-planar, the texture layer is grid-aligned
exemplars. Smooth-curve fidelity in the layered pipeline comes only from
the residual — the exact channel, not understanding.

## Integrity

- Byte-identical reruns x2: knowmap, all renders, deliberation trace.
- White-box path A (per-pixel map) == path B (per-region stamping).
- Full render == sealed fixture (exact closure via residual).
- Zero RNG anywhere. Pure Zag. Pinned toolchain
  `znc_linux_x86_64_abed8aa1`.
- Honest negative where due: no-layers loses on PSNR/SSIM and on
  byte-efficiency. Reported as measured.
