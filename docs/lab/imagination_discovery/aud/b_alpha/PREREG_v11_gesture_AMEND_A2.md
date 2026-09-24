# PREREG AMENDMENT v11_gesture-A2

**Date:** 2026-09-24 (PDT)
**Amends:** PREREG_v11_gesture.md + AMEND_A1 (commit 5fd651d5158b3ef0711f765afee01060afdc0885)
**Status:** COMMITTED BEFORE USE — no render with A2 parameters exists yet.

## A2.1: Refined /a/ area LUT (supersedes A1.1 /a/ row)

**Change:** The /a/ row is re-optimized at F0=678 Hz (the scene's measured
median F0) instead of F0=650 Hz.

New /a/ (row 2):
0.78 1.18 3.12 3.46 2.7 3.66 3.7 6.131 7.98 9.62 10.38 9.4 11.3

**Justification:** The formant-band centroids are F0-dependent (measured:
F0=650→2104/2817, F0=750→2358/3597, F0=575→2630/3478 for F2B/F3B).
Optimizing at the scene's median F0 (678 Hz) yields F1B=770/F2B=2105/
F3B=2816 on the replica — matching the anchor at the operating point.
The /o/ row from A1 is unchanged.

## A2.2: What is NOT changed

- A1.2 (footstep frequency) stands.
- All other A1 provisions stand.
