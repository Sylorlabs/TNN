# AUDIO ROUND 2 — FORK 4 PREREG: prosody_ab (2026-09-24)

## Design (P3: prosody is a layer)
Take a round-1-style engine (impulse train × frozen 3-formant mask —
the squeal_automaton architectural family) and add ONLY the prosody
layer. Deliver A (no prosody) and B (prosody). The A/B IS the kill
experiment.

## Engine
- Excitation: band-limited impulse train (one unit pulse per period).
- Filter: 3 parallel 2-pole resonators, FROZEN: F1=800/B=100,
  F2=1200/B=140, F3=2800/B=180, gains 1.0/0.7/0.5 (/a/-like mask).
- Phrase: 6 notes 440, 494, 523, 587, 659, 587 Hz; 0.5 s/note,
  0.1 s gaps. Total ~3.9 s.
- Per-note raised-cosine attack 15 ms / release 60 ms.

## Prosody layer (B only)
- 5.5 Hz vibrato, ±0.9% depth (→ F0 std ~0.64%).
- Hash-seeded micro-timing: note onsets ±8 ms, seed 1400200004.
- Breath: hash-indexed noise, two-pole LP, mixed to land HNR in the
  bar's upper half (same documented tension as fork 3).

## A/B expectations
- A: PROSODY ~0% (FAILS the prosody gate by design — the control).
- B: PROSODY in [0.3%,3%]; all other gates pass on B; A/B deltas
  reported on every gate.
- NEW clip = B (the prosody-applied deliverable); A committed as the
  control (SHA'd).

## Determinism
Zero RNG. hash64 for micro-timing/breath. 3× byte-identical reruns.
