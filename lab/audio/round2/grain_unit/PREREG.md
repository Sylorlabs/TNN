# AUDIO ROUND 2 — FORK 2 PREREG: grain_unit (2026-09-24)

## Design (P1: fossils as units)
Granular synthesis from a REAL vowel fossil (fossil_hi.bin: 122.42–
122.57 s of the Aporee source, F0~788 Hz, F1~2371, F2~4725 — a high
/i/-like vowel). The fossil is the unit; grains are the articulation.

## Engine
- Source: fossil_hi.bin (4816 int16 samples, PF=56).
- 8 notes: F0 523.25, 587.33, 659.25, 783.99, 880.0, 783.99, 659.25,
  587.33 Hz (C5 D5 E5 G5 A5 G5 E5 D5). 0.6 s/note, 0.1 s gaps.
- Granular: 40 ms grains, Hanning window, 50% overlap (20 ms hop).
- Pitch: resample grains by F0_target/788 (PSOLA-ish). Formants shift
  with pitch (documented limitation; the fossil is a single vowel).
- Stressed notes (0, 3, 6): 2× grain density (10 ms hop).
- Deterministic breath (LP'd hash) for HNR.
- 5.5 Hz vibrato ±0.8% (deterministic) for prosody.

## Note on /a i u/
The prereg sketch said "/a i u a i u a i". The fossil is a SINGLE
vowel quality (high /i/-like). True /a i u/ contrast would require
three fossils or formant filtering, which changes the "fossil as
unit" design. The 8 notes use the fossil's vowel throughout; the
/a i u/ labels are not implemented. Documented as a scope limit.

## Kill experiments (TWO)
1. Frozen grain: no time-varying (single grain repeated, no
   resampling). Prosody must COLLAPSE (≤0.1%). Proves the
   time-varying granular articulation is load-bearing.
2. 4× grain size (160 ms): formant smear. F2 must shift ≥200 Hz vs
   the 40 ms version (measured by the analyzer's formant tracker).
   Proves grain size controls spectral resolution.

## Determinism
Zero RNG. hash64 for breath. 3× byte-identical.
