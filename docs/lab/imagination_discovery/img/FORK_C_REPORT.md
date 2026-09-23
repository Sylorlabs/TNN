# Fork C report — mind's-eye elaboration (r8c_alien)

Date: 2026-09-22. Source: `r8c_alien.zag` (pure Zag, zero RNG).
Artifacts: `r8c_alien_1024.bmp` (24-bit, 1024×1024), `r8c_alien_1024.png`
(lossless PIL re-encode of the BMP), `ELABORATION_TRACE.md` (written by the
program as it decided).

## Why Fork C exists

Rounds 1–7 repaired defects inside one rendering family (noise-on-primitives:
fbm terrain + analytic celestial discs + stamped rocks). Round 7 fixed every
mechanical defect the judges named and still scored 0/5 — the family itself
was the wall. Fork C is a fundamentally different family: **the image is the
residue of 269 sequential imaginative decisions in five passes**, the way a
mind's eye comes into focus. The only mark-making primitive is a soft
pigment dab with radial falloff; forms emerge from accumulated dabs, never
from hard analytic edges or placed primitives.

## The five passes

1. **Gist** (5 decisions): one wash of 576 large soft dabs — indigo-teal dusk
   sky, three vague land tiers, an unresolved glow upper-right, dusty air.
2. **Big decisions** (14): the world gets specific — one low sun at the left
   horizon (-880,-260,+390); one left-to-right wind; a breached ancient crater
   rim with a dust glacier pouring through; rust mid-hills; a ventifact field
   of 40 sailstones with downwind dust tails; a wind-carved arch (dark
   silhouette, sunlit left rims, the hazed far rim seen through its opening);
   a banded gas giant with a storm oval; a small cratered moon; wind-drawn
   cirrus; inter-tier haze; a focal anchor at (430,400).
3. **Light logic** (8): the mind imagines a 128×128 relief grid first, derives
   sun-facing normals, marches cast shadows toward the sun azimuth (96 steps),
   softens the shadow map, then applies per-pixel: effective light, warm sun
   tint on lit faces, cool sky fill in shadow, the giant's analytic
   terminator from the same sun, faint teal secondary glow on cloud
   undersides, aerial perspective per tier.
4. **Fixations** (240): the mind's eye looks around. An interest map
   (contrast × novelty × nearness to the focal anchor) is recomputed from the
   canvas every 20 fixations; the max-interest cell is fixated, the variant
   (lift / deepen / texture / edge) is chosen by comparing local luma to the
   tier prior — read from the canvas, not diced — pigment is laid for a stated
   reason, and visited cells fade. Every fixation is traced with coordinates,
   tier, and reason.
5. **Finish** (2): quiet vignette, ±14 hash grain so no gradient is perfectly
   smooth.

## Determinism, and where surprise comes from

Every decision is a pure function of (pass, index, canvas state). No RNG, no
clock, no outside input. Fixation N+1's target is chosen by READING the
canvas after fixation N — the sequence cannot be predicted without running
the elaboration. Surprise comes from feedback, not dice. Verified: 3/3 clean
runs byte-identical (BMP `e4f65557…`, trace `73776d5d…`).

## Iteration diary (diagnosed by eye, fixed in the world model)

- **Murk**: first render read as night, not dusk (light scale 560+464·L2,
  heavy aerial wash). Brightened the gist, raised the light floor to
  700+324·L2, strengthened the warm tint, cut the wash. Deliberate: dusk
  keeps its shadows but the air holds light.
- **The shadow pillar (root-caused)**: a sharp dark column stood right of
  center. Traced to the shadow march: tier heights were uncapped, so the
  escarpment grew thousands of px "tall" and its (physically correct, given
  the height) cast shadow swallowed the scene; the 48-step march truncated it
  into a pillar. Fix: tier heights capped (rim 360 / mid 240 / plain 120 —
  a cliff has a finite height), march extended to 96 steps so the arch's long
  dusk shadow renders whole, shadow map 3×3-softened. The pillar is gone;
  what remains are broad coherent dusk shadows.
- **The arch window**: the opening was a hard per-pixel override — a glowing
  blue rectangle. Reworked as a dark silhouette with sunlit left rims; the
  opening now holds the hazed, dimmed far rim (pass-3 far-tier wash applied
  to opening pixels).

## Mechanical bars (frozen verifier, 2026-09-22)

| Bar | Result |
|---|---|
| D-RES | PASS — 1024×1024, 24-bit |
| D-SHARP | PASS — grad(O)=8.882, grad(B)=2.248, ratio=3.951 ≥ 1.20 |
| D-COMP | PASS for this fork — 0 banned-primitive tokens in `r8c_alien.zag` (comment-stripped audit). NOTE: the repo-wide verifier currently reports hits in the pre-existing `var1_terminus.zag` (`let band:i64`, lines 352/356) from another fork — untouched by this crew. |
| D-DET | PASS — 3/3 clean reruns byte-identical (BMP and trace) |
| D-BLIND | NOT RUN in this crew — separate judging crew follows per the fork plan. |

## What this fork claims

A deterministic program can imagine in the human sense of the word used here:
it invents a world (one sun, one wind, a breached crater rim, a ventifact
field), commits to it, derives consequences (shadows agree with the sun,
tails agree with the wind), and elaborates by attention — 240 fixations whose
targets depend on the evolving canvas. Whether five fresh judges would still
guess AI is for the blind crew to decide; this crew reports only that the
method is new, the bars it can check are green, and the failure mode of
rounds 1–7 (repairing defects inside a dead family) was not repeated.

## Files

- `r8c_alien.zag` — the entire generator (pure Zag, ~1300 lines)
- `r8c_alien_1024.bmp` — canonical output
- `r8c_alien_1024.png` — lossless preview
- `ELABORATION_TRACE.md` — the 269 decisions, written by the program
- `FORK_C_REPORT.md` — this file
