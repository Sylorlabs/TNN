# FINDINGS — Fork C / SPECSTAT (V10)

**Date:** 2026-09-23
**Renderer:** `src/render_v10_specstat.zag` (pure Zag, pinned `znc_linux_x86_64_abed8aa1`)
**Clip:** `clips/b_alpha_kids_1e_j_v10_specstat.wav` (30 s, mono, 44.1 kHz, 16-bit)
**SHA-256:** `05988a5ab88fcdeb6b6b5fc2c82a0cae7a5010bd9370bb9f031c9194b4c54c2e`

## Frozen design compliance

SPECSTAT analyzes real playground audio through 12 hand-built time-domain
bandpass resonators (2nd-order constant-skirt biquads, difference equation —
no FFT) and retains **only statistics**: 10 Hz per-band energy trajectories
(488 frames × 12 bands), filter coefficients, per-band noise gains, measured
modulation rates/depths, phase segment picks, and phase amplitude trims.
File: `stats_v10_specstat.txt` (77 KB). **No audio atoms, no waveforms, no
recorded material is retained.** The renderer never opens `study/w2.wav`;
it parses only the statistics file (verified by source audit — the only file
reads are the stats input, the WAV output, and the events log).

Resynthesis: one continuous deterministic noise-excitation stream
(`2*h01(SEED, sample_index)-1`, a pure function of the sample index — never
started, stopped, or reseeded) drives 12 persistent-state resonators for the
full 30 s. Per-band gains are continuous functions of time: lerped 10 Hz
trajectories, 0.5 s boxcar smoothing, 1.25 s frozen-frame crossfades at phase
boundaries, smoothstep/Padé transient bumps. No recorded material, no
splicing, no restarted excitation, no hard gates, no chunk assembly.

## Statistics provenance

- Input: `study/w2.wav` (mono, 44.1 kHz, 48.85 s), analyzed once on
  2026-09-23 by `src/analyze.py`.
- Filter centers: 180 Hz – 8,360 Hz, 12 logarithmic bands.
- Kept: 488 × 12 energy frames, biquad coefficients, per-band noise gains,
  modulation stats, segment picks, trims. Nothing else.

## Scene arc and event strategy

One consistent scene: little kids (ages 3–6), one playground moment.

| Phase | Time | Segment (w2) | Character |
|---|---|---|---|
| Yard alive | 0–6.5 s | 29.0–35.5 s | medium play, voice presence |
| Chase | 6.5–12.5 s | 33.5–39.5 s | high energy, bursty |
| Trip / gasp | 12.5–16.5 s | 36.5–40.5 s | calm, low spectral flux |
| Laughter | 16.5–23 s | 31.5–38.0 s | high energy, mid-band |
| Wind down | 23–30 s | 4.0–11.0 s | quietest, 0.7× attenuation ramp |

Phase means are trimmed to the recording global mean (trims:
1.0257 0.8181 1.5545 0.8252 3.0939); residual dynamics come from the
trajectory shapes, a composed 0.5-depth "held-breath" dip at 13.3–14.9 s
(which hushes event bumps too — a freeze must quiet everything), and the
wind-down ramp. 54 scripted transient bumps (footsteps, laugh pulses, calls,
one thud) with smoothstep attacks and Padé decays — see
`events_v10_specstat.txt` for timestamps. The trip segment was re-picked
during development (frames 80→365) under a spectral-flux guard after the
forensic flux profile showed the original pick spiking G-FLUXm.

## Nine-bar gate (frozen) — PASS, no WARN

| Bar | Value | Limit | Result |
|---|---|---:|---|
| G-PER | 0.255 | 0.350 | PASS |
| G-STA | 2.395 | 3.000 | PASS |
| G-LURCH | 3.962 | 5.000 | PASS |
| G-DRIFT | 272.959 | 800.000 | PASS |
| G-FLUXm | 283.366 | 350.000 | PASS |
| G-SIL1 | 0.000 | 0.020 | PASS |
| G-SIL2 | 0.000 | 0.500 | PASS |
| G-CLIP | 0.679 | 0.950 | PASS |
| G-CREST | 6.398 | 14.000 | PASS |

## CHOP forensic results

- **CHOP-1** (hard discontinuities): **0** — PASS
- **CHOP-2** (silent gaps ≥150 ms): **NONE** — PASS
- **CHOP-3** (flux spikes): **0 total, 0 unexplained**
- **CHOP-4** (structural purity): choppiness is impossible by construction.
  (a) The excitation is a pure function of the sample index — continuous by
  definition; the stream is never interrupted. (b) Every gain is a continuous
  function of time (sstep/Padé envelopes, lerped trajectories, sstep
  crossfades); no parameter ever jumps. (c) All 12 filter states persist
  across the entire render. (d) There is no discrete unit assembly of any
  kind — every mechanism is a continuous function of time. Lexical audit of
  the source confirms no prohibited machinery and no file reads beyond the
  statistics input.

## Determinism proof

Two renders from identical inputs (`stats_v10_specstat.txt`, pinned
compiler, same binary): **byte-identical** (`cmp` silent on both WAV and
events file). SHA-256 above. Both renders pass the gate with identical
scores.

## Honest assessment (for Micah's ears)

Mechanically this clip cannot chop: there are no cuts, no gates, no
restarts — the anti-V9-chop requirement is met structurally, and the
forensics agree (0 discontinuities, 0 unexplained spikes). What it IS is
band-energy-shaped noise: 12 resonant bands breathing with real playground
statistics, plus smooth transient bumps. It will sound like a continuous,
lively, playground-textured wash — not like intelligible individual
children. If the bar is "one consistent imagined scene with no choppiness,"
this clears it. If the bar is "sounds like real kids," that needs your ears;
no metric here can claim it. The honest risk: filtered-noise resynthesis can
sound like playground-shaped mush rather than children at play.
