# AUDIO ROUND 2 — FORK 5 PREREG: transient_first (2026-09-24)

## Design (P4: transients lead)
Karplus-Strong plucks, burst-led. The attack transient is the
identity of the note; the sustain is the decay.

## Engine
- 8 plucks: C5 D5 E5 G5 A5 G5 E5 D5 (523.25, 587.33, 659.25, 783.99,
  880.0, 783.99, 659.25, 587.33 Hz), 1.0 s apart (amended from 0.5 s:
  the 3 s sustain caused inter-note overlap that broke monophonic F0
  tracking; 1.0 s spacing keeps the texture while allowing clean
  prosody measurement). Total ~8.5 s.
- Karplus-Strong: delay line N = SR/F0, initialized with hash noise
  (seed 1400200005, per-note offset). Loop: d[idx] = damp × 0.5 ×
  (d[idx] + d[(idx+1) % N]). damp tuned for ≥3 s sustain (−60 dB).
- Onset: 3 ms explicit hash-noise burst at 2× KS level, then KS rings.
  Target: crest ≥6 dB in first 20 ms of each note.
- Deterministic breath (two-pole LP hash) at low level for HNR.

## Kill experiments (TWO, preregistered)
1. Burst-removed control: render without the 3 ms transient. The
   onset crest must COLLAPSE (drop ≥3 dB or below the 6 dB bar).
   Proves the burst is load-bearing for the transient gate.
2. 2×-faster decay: damp' = 1 − 2×(1−damp). Sustain must drop BELOW
   3 s. Proves the sustain claim is sensitive to the damping design.

## Gates
All shared gates on the full render. Sustain ≥3 s (measured as time
for note amplitude to decay 60 dB from peak, on the longest note).
Onset crest ≥6 dB (within the [3,20] dB shared gate).

## Determinism
Zero RNG. hash64 for delay-line init and bursts. 3× byte-identical.
