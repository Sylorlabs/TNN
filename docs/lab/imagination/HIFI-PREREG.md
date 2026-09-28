# HIFI-PREREG (MOOD-2 revision, supersedes MOOD-1 method, keeps its questions)

Frozen: 2026-09-22, before any hi-fi code is written.
Micah's correction: the 8 kHz renders sound DISTORTED ("like a dollar tree mic") and the
horror quality is probably CAUSED by the distortion, not the composition. Agreed the confound
is real. Phase 1 fixes fidelity first; Phase 2 re-runs the mood probe on the clean synth.

## Distortion diagnosis (from code inspection of f3_synth, frozen here)

1. **8000 Hz sample rate** — telephone bandwidth, Nyquist 4000 Hz. Everything above 4 kHz
   is simply absent; transients smear. "Dollar tree mic" starts here.
2. **62.5 ms constant-energy frames (the likely "horror" source)** — each cell renders its
   whole 500-sample frame at one fixed energy, then steps to the next frame's value.
   That is 16 Hz amplitude stair-stepping: zipper noise / tremolo-like roughness in the
   10–20 Hz roughness band, which human hearing reads as harshness, unease, dread.
   Envelopes (attack/decay) are also applied at frame granularity, so even "soft" swells
   step. A horror-movie drone + 16 Hz roughness = creepy regardless of notes chosen.
3. **Hot peak normalization (28000/32767 = 0.85 FS)** — no headroom; dense stacks sit near
   the rail. No integer overflow (i32 mix), but no safety margin either.
4. **Sine-LUT: NOT the distortion source (stated explicitly).** 256-entry i16 sine,
   quantization noise ~−90 dB per partial — inaudible. Harmonics capped at Nyquist
   (mh = 4000/hz), so no aliasing. Integer truncation in `ew` is sub-LSB. The LUT stays;
   polishing it would not fix anything. If Micah's "no hardcoding sines" objection is
   about oscillator *choice* (fixed waveform vocabulary) rather than *fidelity*, that is a
   separate Phase-3 question (non-fixed-waveform oscillator), not a distortion fix.

## Phase 1 design (pure Zag, no new generators; legacy 8 kHz path untouched for AVI)

- `f3_synth_hifi`: SR = 44100 Hz, 16-bit mono. SPF = 2756 samples/frame (62.494 ms;
  field grid unchanged, documented).
- **Per-sample envelope interpolation**: energy linearly interpolated between frame t and
  t+1 values per sample — kills the 16 Hz zipper at the source.
- **Fine phase increments**: sub-unit fixed-point phase (idx = (pha>>24)&255,
  inc = f_fp16·h·256/SR) — detune < 0.5 cent (was ~5 cents at 8 kHz).
- **Nyquist cap raised**: mh = min(8, 22050/hz).
- **Gain staging**: per-voice ew unchanged (e·28·w/1000); global peak normalize to
  24000/32767 (0.73 FS) — headroom, zero clipping by construction (clamp kept as
  dead-code safety, must never trigger; harness asserts zero clamped samples).
- **Release tail**: final segment gets +5512 samples (0.125 s) so last notes decay to
  true zero instead of ending mid-frame.
- `f3_emit_wav_hifi` + `f3_wav_header_sr` (sample-rate-parameterized header).
- New outputs: which=11 → `f3song_hifi.wav`; moods reuse which 8/9/10 filenames
  (`f3mood_happy/scary/calm.wav`) — hi-fi renders supersede the 8 kHz ones.
- New command `f3hifi <dir>`: song + 3 moods via the hi-fi path.

## Phase 1 verification bars (all must pass)

- H1: two clean runs byte-identical (SHA-256) for all 4 files.
- H2: WAV headers parse: 44100 Hz, 16-bit, mono, exact sample counts.
- H3: zero samples at ±32767 rail; peak ≤ 24000+1 (rounding) — i.e. no clipping, headroom kept.
- H4: spectrum check — harmonic peaks at expected bin frequencies (±2 Hz), noise floor
  ≥ 40 dB below voice peaks in voice bands, no 16 Hz frame-rate sideband energy
  (compare 8 kHz render: sideband present there).
- H5: determinism of interpolated envelopes (implied by H1).

## Phase 2 (only after H1–H5 pass)

- Same three compositions (f3_gen_mood, intent labels frozen in MOOD-PREREG.md) rendered
  through the hi-fi path; shipped to ~/workspace/your_files/imagination_audio/.
- Blind rating by Micah: which is HAPPY / SCARY / CALM?
- Report must answer: (a) did the hi-fi re-render change the perceived mood of f3song?
  (b) can TNN hit intended moods through a clean synth?
- Kill bars: 3/3 correct = PASS; 2/3 = PARTIAL; ≤1/3 = FAIL (mood-aiming not demonstrated).

## ADDENDUM — bugs found during Phase 1 implementation (2026-09-22, before ship)

Three real defects were found by measurement while building the hi-fi path. All are fixed
in `f3_synth_hifi` / `f3_emit_wav_hifi` only; the legacy 8 kHz path is byte-identical.

**B1 — half-wave rectification (the "dollar tree mic", CONFIRMED by measurement).**
`f3_get32` returns mix words as UNSIGNED (0..2^32-1, no sign extension). The emitters used
it for peak/abs/scale, so every negative sample read as a huge positive: the true
negative half of each sine mapped to near-full-scale positive, the true positive half
crushed to ~0. Measured: legacy f3song.wav min=0/max=28000/zero-crossings=0, DC mean
0.42. Half-wave-rectified sines sound harsh, buzzy, and "cheap" — this is very likely
the dominant distortion Micah heard. Fix: `f3_get32s` (sign-extending read) in the hi-fi
emitter. Legacy `f3_emit_wav` and `f3_emit_avi` carry the same bug — all shipped 8 kHz
WAVs and AVI soundtracks are rectified; flagged for a follow-up re-render, not silently
changed here.

**B2 — mistuned semitone constant (CONFIRMED).** Bin march used 1117040/1048576 =
1.0652921 instead of 2^(1/12) = 1.0594631: +9.5 cents per semitone, COMPOUNDING
(bin 12 rendered 235 Hz, not 220; a fifth rendered 66 cents sharp). Stretched intervals
sound eerie/detuned — plausibly part of the "horror" quality. The file header documents
"bin b -> 110*2^(b/12) Hz", so the constant contradicted the contract. Fix: 1110928
in the hi-fi path (error 0.0005 cents). Verified: rendered peaks at exact 12-TET
frequencies (C3 130.8, C4 261.6, F4 349.2, G4 392.0, C5 523.3, E5 659.3, G5 784.0).

**B3 — phase-shift typo in the new code (caught before ship).** First hifi build used
`(pha>>24)&255` with inc scaled for >>16: rendered every pitch ÷256 (measured 1–6 Hz
dominance). Fixed to `(pha>>16)&255`; verified by spectrum.

**On the sine-LUT question (explicit):** the LUT is NOT a distortion source — 256-entry
i16, correct values (verified 0/32767/0/−32767 at 0/64/128/192), quantization −90 dB,
harmonics capped at Nyquist. No non-fixed-waveform replacement is needed for fidelity.
Micah's "no hardcoding sines" remains a separate *vocabulary* question (oscillator
choice), not a fidelity defect.

H4c note: the 16 Hz zipper sideband metric could not clearly separate legacy (0.39)
from hi-fi (0.06–0.89) — inconclusive as a measurement. The per-sample envelope
interpolation is kept (it is strictly smoother by construction), but the audibility
claim for the zipper rests on code inspection, not on this metric.
