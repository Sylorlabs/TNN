# Fable consultation — fusion's sticker problem (2026-09-26)

Opinion only, not evidence. One streaming round via
`~/workspace/skills/unorouter/bin/fable_stream.py` (claude-fable-5.1),
max_tokens 16000. Full transcript: `transcript_round1.md` (raw SSE output saved as .txt at stream time; content identical).

## Q1 — Why it keeps collapsing to stickers

Fable's diagnosis: the missing representation is **articulated part pose**.
A mask says WHERE head-pixels are; a warp remaps pixels into that region. Neither
carries: the head's viewing angle relative to the body, the neck as a 3D hinge,
or how head-surface geometry deforms under rotation (visible surface is
generated AND destroyed when a head turns — no 2D warp can synthesize the
newly-visible side). The pipeline is solving a 3D visibility problem with a 2D
lookup table. No refinement of masks, tracking, or photometry can cross that
gap, because all of those are per-pixel operations on a 2D canvas, while a head
swap is a structural substitution of a 3D part onto a different skeleton.
Fable's verdict: a flat texture stretched onto a mask shape looks like a sticker
*because it is one*.

## Q2 — The genuinely logical architecture (Fable's sketch)

- **Parts**: a minimal 2.5D articulated skeleton — torso bone (bunny, neck→spine)
  plus head bone (neck→snout). Carries a 3D quantity: viewing yaw/pitch estimated
  from 2D landmark configuration by closed-form geometry, e.g.
  `tan(yaw) = snout_offset / half_width` (frontal: snout centered, width max;
  turned: width foreshortens, snout shifts). A head is a reference image +
  fixed landmark set + landmark-parameterized warp + 3D offsets of landmarks on
  a half-ellipsoid estimated from the frontal frame — so landmark constellation
  can be rotated by a real rotation matrix and the pixel warp follows.
- **Attachment**: the neck as an interface with four checkable constraints —
  positional continuity (jawline center = neckline center), orientation continuity
  (tangents match), scale continuity (widths match), and C1 silhouette continuity
  at the seam. Cross-fade is *subordinate* to geometric attachment: without it,
  blending just blurs a sticker's edge.
- **Pose transfer (side-view pig → front-view bunny)**: estimate target yaw from
  the bunny; then (preferred) SELECT the pig frame at matching yaw from tracked
  pig footage — choosing the right source material by geometric reasoning, Fable
  calls this "the foundational operation of imagination in this context" —
  falling back to projection-driven landmark warp only within ~15° of available
  footage; then apply pitch/roll from the bunny's neck→snout vector as three
  3×3 rotations + projection.
- **Lighting**: estimate scene light direction from the bunny body's shading
  gradient; apply a spatially-varying gain ramp that *rotates the pig head's
  shading* to match (`B_target(φ)/B_source(φ)`), plus per-channel white-point
  gain; interpolate the gain map across the seam. Fable's caveat: this is shading
  rotation, not true relighting — sufficient for BBB's soft cartoon light.
- **Coherence criterion (system-checkable, no human)**: five automated checks —
  (1) silhouette C1 (curvature spike at seam), (2) light-direction agreement
  head vs body < 15°, (3) color-histogram distance, (4) texture-frequency
  continuity across the seam (within 30%), (5) attachment-constraint residuals
  (position < 3px, angle < 5°, scale 0.85–1.15). Failures are localized to *which*
  aspect broke.

## Q3 — Minimal next step (Fable's recommendation)

Build `pose_pig_head_to_bunny` (~150 lines, days of work):
1. Compute target yaw from bunny landmarks (`atan2(snout_offset, half_width)`).
2. Scan tracked pig frames; use the frame whose yaw matches — a LOOKUP, not a warp.
3. Neck-anchored placement: align jawline center→neckline center, tangents, widths.
4. Lighting gain remap; 10px seam cross-fade.
5. Run the five coherence checks and report.

The smoking gun: the system must use a DIFFERENT pig frame for a 0°-yaw bunny
vs a 45°-yaw bunny. If both composites use the same pig image, it's still pasting.
Most diagnostic test: side-by-side 0° vs 45° bunny frames must show different,
correctly-posed pig heads.

Fable's confidence: diagnosis, yaw geometry, attachment constraints, coherence
checks, and the minimal-step direction — confident. Lighting gain remap adequate
for cartoon — mildly speculative. Ceiling acknowledged: 2.5D, not full 3D —
extreme pose mismatches and big pitch differences exceed it; full 3D morphable
models would be the eventual answer but this gets "sticker → structural
compositing" with minimal code.
