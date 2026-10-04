# AUDIO ROUND 2 — FORK 3 PREREG: skeleton_refine (2026-09-24)

## Design (P1: two-stage always)
Coarse pitch/rhythm skeleton (sine-only melody, low-rate structure) →
refinement stage adds harmonics (2nd–20th, 1/k, anti-aliased), breath
noise (formant-region, hash-indexed), and shaped onset transients.
Prosody layer (P3) on both: 5.5 Hz vibrato ±0.8%, hash-seeded
micro-timing (seed 1400200003 — documented below).

## Target
Melodic phrase, 8 notes: C5 D5 E5 G5 A5 G5 E5 D5
(523.25, 587.33, 659.25, 783.99, 880.0, 783.99, 659.25, 587.33 Hz),
0.45 s/note + 0.12 s gaps. Total ~4.6 s.

## Modes
- `full`: skeleton + refinement (the NEW clip)
- `skel`: skeleton only (kill-experiment control)

## Shared-gate plan
- frac_static ≥ 0.25: 3.6 s voiced of 4.6 s.
- HNR 3.7±3 dB: formant-region breath mixed to land HNR in the UPPER
  half of the bar (~5–6.5 dB). NOTE (documented tension): the bar is
  calibrated on a noisy playground anchor; clean synthesis naturally
  sits higher. Targeting the bar's upper edge keeps the letter of the
  prereg while avoiding audible "static" (what Micah rejected in R1).
- PERIODICITY ≥ 0.5: true phase-locked harmonic series.
- HF_ROLLOFF in [-40,-12] dB: harmonics to 20th, anti-aliased; tuned.
- PROSODY in [0.3%,3%]: vibrato ±0.8% → ~0.57% std.
- TRANSIENT crest in [3,20] dB: 3 ms shaped onset bursts, never clipped.
- peak < -1 dBFS: fixed gain staging (fundamental 7000; worst-case peak
  ~26500 = -1.85 dBFS by construction; analyzer verifies).

## Kill experiment (preregistered)
Ship skeleton-only: it MUST fail the HF_ROLLOFF dullness bound
(E>8kHz < -40 dB) — proving the refinement stage is load-bearing.
Support bar: centroid(full) − centroid(skel) ≥ 500 Hz.

## Determinism
Zero RNG. Micro-timing from hash64(note*7919 + SEED), SEED=1400200003. Breath/transient noise from hash64(sample_index ^
0x9E3779B97F4A7C15). 3× byte-identical reruns required.
