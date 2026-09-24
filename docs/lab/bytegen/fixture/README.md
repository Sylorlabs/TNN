# BYTEGEN frozen plan fixture v1 (frozen 2026-09-23)

Shared by Fork AR and Fork PAR. Both forks MUST render this exact plan.
Any change to this file requires a Micah-signed prereg amendment.

## Format (space-separated ASCII, `#` comments, all times in seconds)

```
SR 44100
DUR_S 30
BED t0_s t1_s freq_hz amp_0_1000
EVENT t0_s dur_s freq_hz amp_0_1000 timbre_0_10 glide_hz vib_hz vib_cents
```

- `BED`: sustained drone layer (sine + 2 harmonics, -6 dB/oct), continuous
  across t0..t1 with smooth fade-in/out at section edges (25 ms raised cosine).
- `EVENT`: melodic voice (harmonic stack, timbre = number of harmonics 1..10
  with 1/h rolloff), smooth raised-cosine attack/release (attack 40 ms,
  release 150 ms capped at dur/2), linear pitch glide over the duration,
  sinusoidal vibrato at vib_hz with +/- vib_cents depth (cents = 1200*log2).
- Amplitude scale: amp_0_1000 is peak per-voice amplitude in thousandths of
  full scale (e.g. 700 -> 0.7 FS pre-mastering; the bed uses 250).
- The final mix is peak-normalized to 0.85 FS (no clipping by construction).

## Content

- Bed: 110 Hz drone at 250/1000 for the full 30 s (constant — it anchors
  the COHERENCE probe so both motif windows share the same bed).
- MOTIF-A: 8-note phrase (A4 C#5 E5 C#5 A4 F#4 E4 A4, 0.35 s notes on a
  0.4 s grid) at t=2.0..5.15 s, recurring with IDENTICAL parameters at
  t=24.0..27.15 s. The COHERENCE probe cross-correlates windows
  [1.8,5.4] vs [23.8,27.4].
- Background arc: soft mid phrases at 6-9, 9.5-12.5, 12.5-15, 16-18.5,
  18.5-21, 21-23, and a wind-down at 27.5-29.5. No hard transients
  (CHOP-1 friendly); energy never drops near silence (G-SIL friendly).
