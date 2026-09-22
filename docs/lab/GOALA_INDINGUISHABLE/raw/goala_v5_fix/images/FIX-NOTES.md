# FIX-NOTES — GOAL-A image fix crew (I-T12, I-T13), 2026-09-22

Crew: I-T12/I-T13 subagent of the Goal-A finish coordinator.
Source patched: `~/workspace/tnn-lab/imagination/src/field.zag` (working copy, NOT committed).
Binary rebuilt from scratch: `imagination/src/field_bin`
(`znc field.zag -o field_bin --no-zagd --no-analyze --no-foreground-cache`).
Workdir: `~/workspace/goala_fix_work/` (images, metrics.txt, sha256sums.txt, this file).

## I-T12 — G1 "ember coast": disconnected pale streak left of the fire

**Tell:** `f3_band(ar, 60, 640, 940, 600, 26, 90, 110, 150)` drew a pale
horizontal streak spanning the frame at horizon height. The fire glow covered
its middle, leaving a streak left of the fire that connected to nothing —
read as artifact/UI remnant.

**Per test-both, two variants were implemented, rendered, and measured:**

- **V5a (remove)** — `images/f3g1a.bmp` (+ `f3g1a.png`). The band is deleted.
  Replaced with two shorter, dimmer, slightly tilted haze wisps well clear of
  the fire: `f3_band(ar, 60, 462, 350, 430, 18, 64, 78, 102)` (distant cloud,
  upper left) and `f3_band(ar, 140, 728, 430, 702, 14, 58, 70, 94)` (low mist
  over the water). Note: the first attempt at ~40% dimmer was *invisible*
  after upscale+grain (verified by zoomed crops), so the wisps were
  strengthened to ~30% dimmer / wider until they read as deliberate faint
  cloud — the spec's intent (visible deliberate haze, not a hole) overrode
  the exact dimming number.
- **V5b (connect)** — `images/f3g1b.bmp` (= final `images/f3g1.bmp`). The band
  is broken into two segments with a **gap where the fire glow sits**, so the
  fire reads as breaking through distant lit haze:
  - left: `f3_band(ar, 55, 660, 420, 630, 24, 86, 106, 142)` + taper
    `f3_blotch(ar, 480, 622, 110, 24, 36, 62, 480)` (background-colored fade
    toward the fire),
  - right stub: `f3_band(ar, 840, 604, 980, 590, 18, 92, 110, 140)` + taper
    `f3_blotch(ar, 828, 600, 100, 26, 38, 66, 420)`.
  - The pair has vertical offset (y≈630–660 vs ≈590–604) and asymmetric tilt.
  - Haze is drawn *before* the fire blotches (fire in front). Zoom-verified:
    the left segment reads as atmospheric haze/cloud tapering into the fire
    glow, not a UI remnant.

**Recommendation: ship V5b.** Reasons: (1) it preserves the brief's "low
tilted horizon" compositional element — V5a deletes the only horizon cue,
leaving the left half empty; (2) it answers the stated complaint directly
("connects to nothing" → now connects to the fire); (3) zoom crops confirm
the haze reads as weather. Metrics pass with margin under *both* variants,
so the choice is compositional, not metric-driven. Judges decide finally —
both BMPs are in `images/`.

## I-T13 — G2 "greenhouse at night": perfect radial-gradient lamp glow

**Tell:** the lamp was two concentric centered blotches at (600,320) — a
textbook radial gradient, a generic AI focal marker.

**Fix (in the shipped source, same in both G1 variants):**
- Main glow replaced by **two overlapping offset lobes** (non-circular):
  `f3_blotch(ar, 586, 308, 86, 238, 198, 128, 560)` and
  `f3_blotch(ar, 626, 340, 70, 230, 188, 120, 520)`.
- **Offset secondary scatter blotch** (asymmetric, smaller, lower fall):
  `f3_blotch(ar, 676, 388, 46, 235, 186, 120, 360)`.
- Hot core kept (the lamp bulb): `f3_blotch(ar, 604, 322, 26, 255, 242, 205, 880)`.
- **Foreground occlusion:** a dark mullion bar drawn *after* the glow —
  `f3_rect(ar, 560, 120, 596, 640, 10, 32, 22, 12)` — cuts the glow's left
  edge, so the lamp reads as sitting behind the greenhouse frame. The bar
  extends well beyond the glow vertically, matching the other mullions'
  dark-green palette.

Zoom-verified: the lamp still reads as a warm lamp, but the glow is now
irregular — brighter lobe upper-right, dimmer spill lower-left, dark frame
member crossing it. The perfect-disc signature is gone.

## Verification

- **Bars (binding):** raw H-mirror < 0.60 and gradient-detrended H-mirror
  < 0.30 on all 6 shipped images — 6/6 PASS (see metrics.txt). Detrend =
  subtract per-column vertical linear fit, then correlate with horizontal
  mirror. Note: this harness reproduces the reference unique-color counts
  *exactly* (16,768 / 12,614 / 6,391 / 8,498 / 3,844 / 15,076); symmetry
  magnitudes differ slightly from the canonical table's method but every
  verdict agrees with margin.
- **Byte-identical reruns:** 6/6 identical across two clean runs from the
  from-scratch binary (outputs rm'd between runs); hashes in sha256sums.txt.
- **No RNG:** all new strokes use existing deterministic primitives
  (`f3_band`, `f3_blotch`, `f3_rect`); no new seeds, no randomness.
- **Regression:** all 14 legacy BMP scenes byte-identical under the new
  binary (14/14); g3–g6 byte-identical to the V3/V4 shipped renders
  (g5 hash matches the shipped V4 artifact).
- **Normal-vision law:** night scenes kept ordinary — haze, cloud, mist,
  lamp-behind-frame. No horror-coded elements; no horror language in
  comments.

## Files for the coordinator (do NOT commit per mandate — coordinator decides)

- `~/workspace/goala_fix_work/images/` — `f3g1.bmp`..`f3g6.bmp` (+ `.png`
  presentation copies) final; `f3g1a.bmp`/`.png` (V5a alternate),
  `f3g1b.bmp`/`.png` (V5b = shipped).
- `~/workspace/goala_fix_work/metrics.txt`, `sha256sums.txt`, `FIX-NOTES.md`
  (this file).
- `~/workspace/goala_fix_work/measure_metrics.py` — the metrics harness.
- `~/workspace/goala_fix_work/va/src/field_v5a.zag` — alternate-variant
  source (for the record / in case judges pick V5a); `vb/src/` mirrors the
  shipped source.
- Patched working-copy source: `~/workspace/tnn-lab/imagination/src/field.zag`
  (ships V5b + G2 fix); rebuilt `imagination/src/field_bin`.
