# AUDIO ROUND 2 — FORK 1 PREREG: glottal_formant (2026-09-24)

## Design (P2: glottal flow + vocal tract)
LF-model glottal flow derivative (abrupt closure → rich harmonics)
driving 6 series formant resonators (200–6000 Hz). The source-filter
model: glottis creates the buzz, tract shapes the vowels.

## Engine
- LF-model: simplified. Pulse with Tp=0.6*T (open), Te=0.9*T
  (excitation peak), Ta=0.05*T (closure). Derivative has sharp
  negative spike at closure → −12 dB/octave tilt (vs sine's −∞).
- 6 formants (series): F1 800, F2 1200, F3 2800, F4 3500, F5 4500,
  F6 6000 Hz. Bandwidths 80, 100, 120, 150, 200, 300 Hz.
- Phrase: /ba/ (196 Hz), /da/ (247 Hz), /ga/ (294 Hz). 0.5 s each,
  0.1 s gaps. Consonant burst (5ms noise) at each onset.
- Deterministic breath for HNR. 5.5 Hz vibrato ±0.8%.

## Kill experiment
LF→sine excitation swap. Replace the LF pulse with a pure sine at
F0 (same formants, same phrase). The spectral tilt (H1-H2 or
HF rolloff) must flip by ≥6 dB. Proves the LF glottal model (not
just the formants) is load-bearing for the voice quality.

## Determinism
Zero RNG. hash64 for breath/bursts. 3× byte-identical.
