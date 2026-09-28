# SENSES_UNLIMITED — human-limit audit (2026-09-22)

Micah's law: human sensory drawbacks must not be part of TNN. Every hardcoded
human-range assumption below is either REMOVED by the u4f/ufreq work or
explicitly documented with a reason. "Silent" = data lost with no flag.

## Audio / signal limits

| ID | Location | Assumption | Effect | Status |
|---|---|---|---|---|
| A1 | `imagination/src/field.zag:6-7,348-350` | Audio field = 48 semitone bins, bin b → 110·2^(b/12) Hz → max ≈ 1.66 kHz | Nothing above ~1.66 kHz imaginable. `f3_tone` SILENTLY drops out-of-range bins (`if (fbin<0\|\|fbin>47) return rc`) | Documented; superseded by ufreq atoms (unbounded) |
| A2 | `field.zag:1070,949,1089` | Max 8 harmonics; Nyquist max-harmonic at 22050 (SR-derived) | Harmonic content capped by sample rate | Documented; ufreq has no harmonic cap |
| A3 | `field.zag:913,1064,1444`, `imagine.zag:3115`, `emit.zag:1070` | Fixed 8000 / 44100 Hz sample rates | Nothing above Nyquist representable in emitted audio | KEPT with reason: emission to human-audible WAV is a *rendering* choice, not a representational limit. ufreq atoms are SR-free; the WAV writer is one declared mapping |
| A4 | `imagination/src/sin_lut.zag` | 256-entry sine LUT is the only oscillator | Fixed waveform ceiling (already flagged 2026-09-22) | Open — non-fixed-waveform replacement is a separate track |
| A5 | `field.zag:918-935,1063,1075` | Frames clamped 1..48, total samples 8000..200000 | Duration silently clamped | Documented; ufreq time is i64 µs (±292k yr), no clamp |
| A6 | `senses/rebuild/a_raw/sense.zag:443,600` | f0 estimator supports 50..2000 Hz only | Human voice range; returns -1 outside | Documented; estimator is a *measurement* tool, not imagination. Widening it is future work |
| A7 | `senses/rebuild/b_percept/sense.zag:90,112` | Rejects audio with sr < 8000 | Cannot ingest low-SR audio | Documented; input-validation, not a representation limit |

## Visual / image limits

| ID | Location | Assumption | Effect | Status |
|---|---|---|---|---|
| V1 | `field.zag:5,143-145,224-331` | Visual = 24-bit RGB, 0..255/channel, `f3_clamp255` | SILENT saturation at 255; no UV/IR/X-ray channels | REMOVED in u4f: i64 channels, no 255 ceiling, SATFLAG instead of silent clamp |
| V2 | `field.zag:1443` | AVI writer: uncompressed 24-bit RGB | Video emission is RGB-only | KEPT with reason: emission mapping, declared. u4f false-color renderer records its mapping |
| V3 | `field.zag:5` | 4th channel "rough 0..1000" — only non-RGB channel, arbitrary 1000 cap | Hidden-layer precedent exists but capped | REMOVED in u4f: roughness is channel 8, i64, uncapped |

## Structural limits (kept, documented with reason)

| ID | Location | Assumption | Reason kept |
|---|---|---|---|
| S1 | `field.zag:11` | Max 64 strokes/scene | Deliberate construction budget, not a sensory limit — Micah's "as capable as me" targets content quality, not stroke count. Recorded, not a human-sense limit |
| S2 | i64/u64 widths in ufreq | freq_hz: u64 (max 1.8e19 Hz), time: i64 µs | Covers EM spectrum through gamma rays; documented as the explicit representational boundary, flagged never wrapped |

## What "unlimited" means here (binding)

1. Representation (u4f image field, ufreq signal atoms) has no human-band ceiling.
2. No silent saturation/wrapping anywhere: overflow sets SATFLAG / returns status.
3. Emission to human-perceivable form (BMP/WAV) is always a DECLARED mapping
   (false-color id, pitch-shift octaves) recorded with the artifact — the map is
   never presented as the territory.
4. Fidelity of each mapping is MEASURED (ratio preservation, rank correlation),
   not vibe-checked.
