# BAR RESULTS: Experiment 1, Wave wave-20260926-2321pdt

Run date: 2026-09-27.
Toolchain SHA-256: 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef.
Output SHA-256 (two runs, byte-identical):
ba4677cc8a786a0d52f0ec89a891c6d9b7e16436c484d61ff388d16a88521ebf.

## Medians (12 variants each)

| Arm | Median ticks |
|---|---:|
| P (taught WARD) | 600 |
| Z (fixed-seed random) | 89 |
| R (recall-only) | 600 |
| I-survive | 574 |
| I-invent | 574 |

## Calibration gates

C1: median P at least 480. Result: 600. PASS.
C2: median Z below 150. Result: 89. PASS.
C3: three qualitatively distinct strategies reaching at least 360 ticks.
  forage median 600, ward-turtle median 600, lamp-farm median 600. PASS.

## Kill bars

K1: if median I-survive is at most median R, KILL H1.
  I-survive 574, R 600. 574 is at most 600. KILL H1.
  The invention claim is killed. The I arm did not beat recall-only R.

K2: if median I-survive is at most median Z, KILL H1 and investigate simulation.
  I-survive 574, Z 89. 574 exceeds 89. PASS.
  (H1 already killed by K1.)

K3: if median P is below 480, VOID.
  P median 600. Not below 480. PASS (not void).

K4: novelty. See novelty audit. The I arm's strategy is judged below.

K5: blind cuing audit. See blind cuing audit. Incomplete: no independent auditor.

K6: ablation. The runner's ablation section was empty (no novel composition
  was identified for replacement, since H1 was killed at K1).

## A1/A2

A1: strategy extraction wherever either I arm beats R by at least 60 ticks.
  I-survive 574 vs R 600: does not beat R. A1 does not trigger.

A2: deterministic replacement. Not triggered (A1 did not trigger).

## A3: comparison with Task 1 (8/58)

Task 1 reported 8/58. This experiment's I-survive median is 574/600 ticks,
which is not directly comparable (different task, different metric).
The 8/58 figure is noted here for the record; no claim of improvement
or regression is made.

## Verdict

H1 (invention beats recall) is KILLED by K1.
The experiment itself is not void (C1, C2, C3 pass; K3 pass).

## CORRECTION (2026-09-27, independent red-team review, wave-20260927-0221pdt)

The wave-20260926-2321pdt reimplementation of the world (commit 74565859f,
whose code produced the medians and SHA-256 ba4677cc reported above)
contained a physics bug: the hi-side mote reflection was algebraically the
identity (hi - (hi - pos) = pos), so moving motes escaped to infinity on
first hi-side contact. Only the stationary mote (at P's home, velocity 0,
never touching the bounce code) remained edible. The published world was
degenerate: a single stationary food source.

The original EXP1 commit (19f97c6cb) had correct bounce; the bug was
introduced in the 2321-wave reimplementation. K1's KILL verdict
(I-survive 574 <= R 600) is arithmetically valid within the degenerate
world and its direction is unchanged. But the world did not implement its
specified physics (PREREG section 3: "Motes: M=6 energy packets with
fixed velocities, bouncing at the ends"), R's 600 is "camp the single
stationary mote" (an artifact: with correct bounce the earlier iteration
had R at only 160), and C3's three distinct strategies are not credible
when all reduce to camping one stationary mote.

EXP1 remains DISCARDED (per PREREG_EXP1b). This note stands as the
correction to its published record.
