# Upscale Round 4 — VERDICT: KILLED (honest loss)

Date: 2026-09-27. Frozen prereg: `PREREG_R4.md` (this directory).
Battery: `BATTERY_R4.md` + `RAW_TABLE.csv` (158 rows, 21 images × configs, 2× byte-identical).
Red team: `REDTEAM_R4.md` (independent, 5 attacks).
Gallery (for Micah's eyes): `~/workspace/upscale_r4/GALLERY_R4.html` (self-contained, not in repo — re-renders from committed sources).

## The one-paragraph verdict

Round 4 is **KILLED**. Four new arms were built to answer round 3's open
questions on a fresh 10-image sealed battery with a frozen bicubic column.
The learned vocabulary is **retired** (binding abandonment bar fired:
planes beat atoms by −0.633 dB mean on identical take geometry). The
chooser/deliberation is **decorative or harmful** (PLANE-forcing arm P1
within +0.08 dB of C3 on sealed). Of the six sealed candidates, only
P2plane — measured planes rendered on the lineage-restricted take
geometry — passed BAR 1 (+0.539 dB mean, 10/10 wins, no image below
−0.50). The independent red team then **killed P2plane**: on
category-shift traps it renders false ramps across sharp edges
(−11.57/−8.34/−11.96 dB vs bicubic — worse than the round-3 deficits
that killed C3), and ±1–2 LSB input perturbations amplify 44–88× in
output through silent take flips. Per the frozen prereg, an arm that
wins BAR 1 but fails the red team is KILLED, not shipped. No arm ships.

## Bar readings (frozen)

| item | result |
|---|---|
| BAR 0 (baseline reproduction) | PASS — bridge/sky SHAs byte-identical, all 11 dev PSNRs ±0.02 |
| BAR 1 (sealed broad win) | C3 FAIL (floor −0.99), P1 FAIL (floor −0.99), P2 FAIL (mean −0.094), **P2plane PASS** (+0.539, 10/10, floor +0.00), P3 FAIL (floor −0.99), P4 FAIL (floor −0.57, texture group −0.29) |
| BAR 2 (bridge/sky ≥ baseline−0.10) | PASS — all arms |
| BAR 3 (vocabulary abandonment, binding) | **FIRES** — mean Δ(P2−P2plane) = −0.633 ≤ 0 over 10 sealed images |
| P1 deliberation reading (±0.10 dB vs C3) | +0.080 on sealed → deliberation decorative or harmful |
| Red-team gate (P2plane) | **KILL** — traps + close-call amplification |
| Eyes gate | gallery built and load-verified; Micah's eyes are the final judge |

## What each arm proved

- **P1 (force PLANE everywhere):** +0.872 sealed mean vs C3's +0.789 —
  within the ±0.10 band. The round-3 "chooser" adds nothing over
  always-plane. Decorative or harmful, per the preregistered reading.
- **P2 (lineage-vouched cascade, real VOC3):** dry-run passed (240-atom
  mapping unambiguous; stone_wall contributed 0 atoms). Sealed mean
  −0.094 — the lineage restriction neither helps nor (much) hurts. The
  analysis mode (identical geometry, planes instead of atoms) beats it
  by 0.633 dB. Vocabulary retired as a renderer.
- **P3 (inverted architecture — atoms only as licensed residuals):** the
  honest-improvement check rejected **every** licensed atom on real
  pixels (0 residual takes on bridge/sky; battery: P3 ≡ C3 on most
  images). No atom earned its place on observed pixels.
- **P4 (C1's license gate + PLANE fallback):** byte-identical to C1 on
  10/11 dev images; the fallback never engaged on bridge/sky. Sealed:
  fails BAR 1 on the floor (−0.57) and the texture group (−0.29). The
  license gate, not the fallback, is the problem.
- **P2plane (analysis mode, not a candidate arm):** the only BAR-1
  passer — then red-team-killed. Its take geometry is still
  vocabulary-decided (fixed-grid planes score −0.333 vs its +0.539),
  so the vocabulary's last remaining value is as a *partition
  decider*, not a renderer. The kill mechanism: the atom-match gain
  does not penalize edge-straddling blocks, so the least-squares plane
  renders false ramps across sharp edges.

## Standing facts (unchanged, re-confirmed)

- Every arm and baseline sits 0.5–3.3 dB below PIL bicubic on every
  real image; 8–12 dB below on the traps. The binaries' own Zag
  bicubic is worse than PIL's — the published column is PIL 10.2.0.
- Determinism: 158/158 jobs byte-identical across 2× runs; 30/30
  allocator perturbations identical. Zero RNG anywhere.
- Post-hoc protocol note (§5b of BATTERY_R4.md): sealed_04 panicked
  the frozen LINES code (hardcoded 16384-row take buffer; the image
  needs 16,847). Capacity repair (`w*h*7*8`, identical in 6 sources,
  C1 untouched) was proven decision-neutral — 77/77 dev output SHAs
  byte-identical vs unrepaired — before the full rerun. Not tuning.

## Mechanism lessons for the next round

1. Atoms-as-rendering is dead; planes win on identical geometry.
2. The chooser is decoration — always-plane matches the "deliberated"
   choice.
3. The remaining hard problem is **edges**: any block partitioner +
   smooth renderer that doesn't detect and respect strong edges will
   die on the traps. The match gain must penalize edge-straddling, or
   an edge-aware operator must own those blocks.
4. Vocabulary-as-partitioner still beats a fixed grid (+0.87 dB) —
   don't throw out the geometry signal with the rendering.

## Line status

Round 4 closed as killed. No code ships. The honest-loss record above
is the deliverable, plus the sealed 10-image battery (now a dev set
for round 5 — it must be replaced, not reused, for generalization
claims) and the retired-vocabulary finding, which constrains all
future arms to measured-only construction.
