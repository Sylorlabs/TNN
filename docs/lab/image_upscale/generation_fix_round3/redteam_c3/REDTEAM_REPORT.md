# Red Team Report: C3 Upscale Repair (Round 3)

**Candidate:** `docs/lab/image_upscale/generation_fix_round3/src/azgen_c3.zag`
**Commit:** `28cedd2d5c398c635472690992c264fdd29016dc` (sylorlabs/TNN, tnn-native-lab)
**Date:** 2026-09-27
**Verdict:** **KILLED**

## Summary

C3 is killed by preregistered category-shift traps. The plane gate — the mechanism
behind 85.7% of C3's operator choices — confidently misclassifies sharp edges as
"smooth planes," losing 5-6 dB to bicubic on diagonal and curved boundaries while
the trace claims `reason=plane_resid_le_e_half`. Supporting attacks confirm the
deliberation is discontinuously unstable at gate boundaries and that the ATOM
operator is functionally marginal.

## Reproduction (kill-grade gate)

| Check | Result |
|---|---|
| Pristine azgen.zag baseline, 11/11 images | All within ±0.005 dB of claimed (bar: ±0.05) — PASS |
| C3 battery, 11/11 images | All match claimed to 0.01 dB — PASS |
| Operator census (2,996 regions) | PLANE 85.75%, MEAN 10.65%, ATOM 3.60% — matches verdict |

Baseline scores reproduced: bridge 18.47, sky 22.75, fabric 21.47, woodgrain 18.37,
treebark 18.94, calmwaters 19.46, portrait 21.19, car 22.92, building 14.96,
cat 16.60, market 18.36 (all deltas < 0.005 dB).

C3 scores reproduced: bridge 19.74, sky 23.89, fabric 21.47, woodgrain 20.05,
treebark 20.51, calmwaters 20.08, portrait 22.32, car 24.43, building 15.24,
cat 17.19, market 19.07 (all exact to displayed precision).

## Attack 2 — Category-shift traps (KILL)

Protocol: analytical 256×256 RGB ground truths, frozen 2×2 box-average downscale,
C3 and its own bicubic comparator scored against exact GT. Zero RNG.

| Trap | C3 dB | Bicubic dB | C3−bicubic | Trace |
|---|---|---|---|---|
| Vertical binary step | 31.83 | 30.07 | +1.76 | none |
| **Diagonal binary step** | **21.51** | **26.97** | **−5.46** | **8/8 PLANE, `plane_resid_le_e_half`** |
| **Binary circle** | **19.46** | **26.00** | **−6.54** | **20 PLANE, 3 MEAN, 2 ATOM** |
| 4-pixel checkerboard | 9.61 | 9.67 | −0.06 | none |
| Gradient + sharp step | 34.42 | 41.47 | −7.04 | none (SHAPES reverted) |
| Sine grid | 15.79 | 17.52 | −1.73 | none |

The preregistered kill criterion (≥2 dB loss vs bicubic with confident trace) is met
by the diagonal step (−5.46 dB) and the circle (−6.54 dB).

**Mechanism:** The plane gate passes when the fitted plane explains ≥50% of block
variance (`2*residual ≤ e`). An 8×8 block straddling a sharp diagonal edge has
`2*residual/e = 0.667` — the gate passes, and C3 renders a false ramp across the
discontinuity. The trace records `edge=289` (28.9% strong-edge pixels) for these
blocks — the evidence that would distinguish a step from a gradient is measured
and ignored by the frozen rule. The trace confidently claims the plane is the
honest model (`reason=plane_resid_le_e_half`, `pok=1`) while the output loses
5.46 dB to bicubic.

The circle trap shows the same failure on curved boundaries: 20/25 regions choose
PLANE around the curve, losing 6.54 dB.

The gradient+step trap (−7.04 dB) is a further generalization failure, but SHAPES
reverted there (no confident PLANE trace), so it is supporting evidence only.

## Attack 1 — Close-call perturbation (SUPPORTING)

An exact integer oracle replicated the plane gate for all 2,888 non-ATOM regions.
40 regions (1.4%) sit within 10% of the plane boundary; 24 within 1%.

Key methodological finding: the deliberation evidence (e, f, m, plane) is
mean-centered and ratio-based, hence **invariant to uniform brightness shifts and
global contrast scaling**. The meaningful stability probe is a texture change.

Targeted ±1–2 LSB checkerboard perturbations (below the LINES Sobel threshold,
so no LINES confound) on the 12 closest plane-gate calls:

| Target | margin_p | Result | Input Δ | Output Δ |
|---|---|---|---|---|
| woodgrain (272,316,4×4) | 0.9999 | PLANE→MEAN | ±1 | **95** |
| cat (356,84,4×4) | 0.9981 | PLANE→MEAN (amp=2) | ±2 | 91 |
| building (364,88,4×4) | 0.9970 | PLANE→MEAN (amp=2) | ±2 | 101 |
| woodgrain (220,340,4×4) | 0.9988 | PLANE→GONE (amp=2) | ±2 | 138 |
| treebark (192,224,32×32) | 1.0035 | MEAN→GONE (amp=6) | ±6 | 195 |

8/12 flipped (including "GONE" = partition restructuring via the operator-honest
recursion). Output jumps of 91–195 gray levels from ±1–2 LSB input changes —
a 50–95× amplification. The trace records no margin, so it gives no warning that
a decision was a coin flip.

This does not independently kill (hard thresholds are inherently discontinuous),
but it shows the plane boundary is both densely populated and structurally
consequential.

## Attack 3 — Operator neutering (SUPPORTING)

Topology-preserving variants (only the render changes; gret, splits, and commit
identical):

**ATOM→MEAN** (retain atom gret):

| image | C3 | neutered | Δ |
|---|---|---|---|
| bridge | 19.74 | 19.73 | −0.01 |
| sky | 23.89 | 23.89 | 0.00 |
| fabric | 21.47 | 21.47 | 0.00 |
| woodgrain | 20.05 | 20.02 | −0.03 |
| treebark | 20.51 | 20.48 | −0.03 |
| calmwaters | 20.08 | 20.07 | −0.01 |
| portrait | 22.32 | 22.30 | −0.02 |
| car | 24.43 | 24.41 | −0.02 |
| building | 15.24 | 15.23 | −0.01 |
| cat | 17.19 | 17.18 | −0.01 |
| market | 19.07 | 19.07 | 0.00 |

Max |Δ| = 0.03 dB. ATOM (3.6% of regions) is **functionally marginal**:
neutering changes outputs on 8/11 images, but its total quality contribution is
≤0.03 dB per image — below the kill-grade threshold itself. The verdict's "stamp
path barely earns its keep" is confirmed; "barely" is ≈0.015 dB mean.

**PLANE→MEAN** (retain plane gret; slopes zeroed so construction renders flat):

| image | C3 | neutered | Δ |
|---|---|---|---|
| bridge | 19.74 | 18.28 | −1.46 |
| sky | 23.89 | 22.93 | −0.96 |
| fabric | 21.47 | 21.47 | 0.00 |
| woodgrain | 20.05 | 18.27 | −1.78 |
| treebark | 20.51 | 18.97 | −1.54 |
| calmwaters | 20.08 | 19.25 | −0.83 |
| portrait | 22.32 | 21.38 | −0.94 |
| car | 24.43 | 22.96 | −1.47 |
| building | 15.24 | 15.00 | −0.24 |
| cat | 17.19 | 16.52 | −0.67 |
| market | 19.07 | 18.49 | −0.58 |

PLANE's render contributes 0.24–1.78 dB (mean ≈1.04 dB). PLANE is load-bearing:
removing its render (keeping all gains/splits/commit identical) costs ≈1 dB on
average. Topology fully preserved (e.g., woodgrain 1,042→1,042 takes).

**MEAN→PLANE** (retain gret=0):

| image | C3 | neutered | Δ |
|---|---|---|---|
| bridge | 19.74 | 19.86 | +0.12 |
| woodgrain | 20.05 | 20.11 | +0.06 |
| treebark | 20.51 | 20.63 | +0.12 |
| calmwaters | 20.08 | 20.10 | +0.02 |
| car | 24.43 | 24.48 | +0.05 |
| others | — | — | 0.00 |

Forcing MEAN regions to render as PLANE (using the computed-but-rejected plane
coefficients) **improves** 5/11 images. The plane gate is conservative: planes it
rejects would have helped. Topology fully preserved (1,042→1,042 takes on
woodgrain).

## Verdict

**KILLED.** The diagonal-step (−5.46 dB) and circle (−6.54 dB) traps meet the
preregistered kill bar: C3's plane gate confidently misclassifies sharp
discontinuities as smooth planes, with the trace claiming `plane_resid_le_e_half`
while losing 5+ dB to bicubic. The 85.7%-dominant operator is structurally blind
to the difference between a gradient and a step edge.

Supporting: gate-boundary instability (50–95× output amplification from ±1 LSB),
ATOM functional marginality (≤0.03 dB), conservative plane gate (rejected planes
would help by up to +0.12 dB).

## Artifacts

All analysis scripts in `~/workspace/upscale_r3/redteam_c3/`:
`battery.py`, `parse_traces.py`, `plane_oracle.py`, `attack1b.py`, `attack1c.py`,
`attack2.py`, `attack3.py`, `gen_neutered.py`, `baseline.py`.
Binaries, BMPs, and /tmp scratch deleted per disk-hygiene requirement.
