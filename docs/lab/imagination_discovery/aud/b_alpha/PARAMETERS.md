# Fork B-α — Parameters and Mechanisms

**Position:** (b) study-then-invent, pure. Every audible moment originates from a real
captured source; TNN invents only the arrangement.

---

## The anti-additive structural argument

B-α is **not** a synthesizer wearing a costume. The production path (`src/render.zag`)
contains:

- **NO** oscillators (no sine/square/saw generators, no LUT oscillators)
- **NO** resonators or filters (no biquads, no formant synthesis)
- **NO** noise generators (no white/pink noise, no filtered-noise beds)
- **NO** spectral/additive reconstruction (no FFT, no partial stacks, no chirps)
- **NO** synthetic envelopes (no ADSR, no parametric fades — only short edge crossfades)

**What the renderer MAY do** (sample operations only):
- Time-domain traversal via linear interpolation (playback-rate changes)
- DC subtraction, gain staging, summation into a Q24 mix arena
- Short smoothstep edge fades (seam clicks prevention, not sound design)
- Selection and arrangement driven by studied descriptors and grammar

**What the renderer MAY NOT do:**
- Descriptors/grammar affect **selection and arrangement only**, never sample reconstruction.
- No studied atom may be played chromatically or pitched as an instrument (see unplayability inventory).
- Whole studied events only — never grain-level slicing or spectral frames.

The studied descriptors (duration, peak, RMS, ZCR, tilt, attack) and grammar (bigrams,
gap quantiles) are **control signals**, not synthesis parameters. They answer "which event
goes where," never "what does the waveform look like."

---

## Unplayability / anti-rename inventory

| Forbidden construct | B-α status |
|---|---|
| Oscillator (any periodic generator) | ABSENT — no periodic sample generation anywhere |
| Resonator / filter | ABSENT — no feedback, no frequency-domain ops |
| Filtered-noise bed | ABSENT — ambience is crossfaded **recorded** quiet textures |
| Chirp / sweep | ABSENT |
| Decaying-sine drum / boom | ABSENT |
| Grain-level spectral reconstruction | ABSENT — whole events only |
| Chromatic/pitched instrument | ABSENT — atoms are never pitch-quantized; rate changes are continuous and non-musical |
| Renamed equivalents | AUDITED — `place_event` does linear-interp traversal (playback, not synthesis); `bed` does recorded-texture crossfade (editing, not generation) |

The control (`src/control_synth.zag`) deliberately implements the convicted paradigm
(sine LUT oscillators, inharmonic partials, filtered-noise bed, chirp giggles,
decaying-sine footsteps) for blind-test contrast only. It is not part of B-α's claim.

---

## Parameters

| Parameter | Value | Role |
|---|---|---|
| `seed` | 6101 (kids), 6201 (planet), 6301 (alien) | Deterministic stream selector |
| `h32(seed, stream)` | splitmix-like integer hash | ALL "choices" — zero RNG |
| Window | 2 s / 0.5 s hop | No-copy audit granularity |
| No-copy bar | distance ≥ 0.450 | `1 - max(|normalized xcorr|)` vs all studied windows |
| Bed crossfade | 1 s smoothstep | Seamless recorded-texture joins |
| Event edge fades | short smoothstep | Click prevention |
| Mix arena | Q24 (i64) | Headroom before final normalize |
| Final | −1 dB normalize, symmetric soft clip, 30 ms outer fades, DC subtract | A-NATIVE compliance |

---

## Grammar (learned, not designed)

- **Class bigrams (16):** P(class_b | class_a) from studied event sequences.
- **Gap quantiles (12):** p10/p50/p90 inter-event gaps per class.
- Scores consult grammar for fill material between composed beats; beats themselves are
  deliberated scene structure (see `score_kids` comments: Mara/Jo/Pip chasing game).

---

## Determinism

Zero randomness in decision paths. Every choice is `h32(seed, stream)`.
Verified: 3/3 byte-identical SHA-256 for kids, planet, alien, ocean renders.
