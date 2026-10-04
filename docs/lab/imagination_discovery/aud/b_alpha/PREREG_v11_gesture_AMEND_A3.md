# PREREG AMENDMENT v11_gesture-A3

**Date:** 2026-09-24 (PDT)
**Amends:** PREREG_v11_gesture.md + AMEND_A1 + AMEND_A2
**Status:** COMMITTED BEFORE USE — no render with A3 parameters exists yet.

## A3.1: Corrected /a/ area LUT (supersedes A2.1 /a/ row)

**Change:** The /a/ row is replaced with a Helmholtz-initialized optimization
result.

New /a/ (row 2):
2.664 3.975 5.22 3.28 0.68 0.6 5.72 6.4 7.72 8.08 8.68 9.6 10.6

**Justification (mechanism repair):**
The A2 /a/ (optimized from a smooth-widening start) achieved the target
CENTROIDS (770/2105/2816) but via a "cheat" solution: actual F1 formant at
1359 Hz (not ~800 Hz). With F0=660 Hz far below F1, the tract attenuated
the fundamental by ~70 dB while boosting H2 (1320 Hz, near F1) — the 2nd
harmonic was 18.7 dB STRONGER than the fundamental, causing voice_sig
octave errors (P10=331.5 Hz = F0/2) and corrupting V-F0DYN.

The A3 /a/ (optimized from a Helmholtz start at the same F0=678 Hz,
same targets) achieves centroids 766/2105/2811 with actual formants
F1=875/F2=2106 Hz. The fundamental (660 Hz) is now 8.0 dB stronger than
H2, restoring correct periodicity detection. This is a repair of the
acoustic mechanism (F1/F0 mismatch), not a change in optimization targets.

The /o/ row from A1 is unchanged.

## A3.2: What is NOT changed

- A1.2 (footstep frequency), A2.2 stand.
- All §8 knob ranges respected.
