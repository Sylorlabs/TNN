# AUDIO ROUND 3 PREREG — no-synth wave manipulation (2026-09-24/25)

## Motivation
Micah's law: NO SYNTHESIZERS, PERIOD. Round 1 (10 synth forks) → 0/10 ears.
Round 2 (LF-model/formant/saw synths) → 3/6 analyzer gates, then the synth
line was outlawed before ears. The only organic material ever produced came
from real recordings (vowel_fossils). This round: audio ONLY via native
wave manipulation and editing of real waveforms.

## The law (absolute)
Every output sample must trace to a recorded sample through a documented
transform. FORBIDDEN: oscillators, formant synths, LF glottal models,
parametric excitation, synthetic noise sources, noise-burst "transient
synthesizers", physical-model oscillators that are synths by another name,
FM/AM synthesis. CONTESTED (allowed only with defense + bound + kill
experiment proving the real source is load-bearing): resampling/interpola-
tion for pitch/time manipulation, crossfades (≤5 ms, disclosed).

## Real source inventory (all 44.1 kHz, SHAs on file)
- `~/workspace/aud_v11/diag/vowel_real.wav` — field anchor, child vowel,
  2.0 s, SHA 8ba3b42708a8bab2…
- `~/workspace/v5work/kida.wav` … `kide.wav` — child utterances, 30 s each,
  kida SHA b8ad8e1a1f4f70b…
- `~/workspace/audio_forks/vowel_fossils/work/fossil_VF1_raw.wav` (+ work/
  protos) — vowel fossils, offsets/SHAs in FOSSIL_LOG.md
- `~/workspace/audio_round2/shared/` — real ambience/breath beds, scripts

## Shared crew laws (every fork)
Pure Zag; zero RNG (deterministic hash-seeding allowed only if documented);
no `as []i32/u32/u16` indexed tables ([]u8 arenas); analyzer-first
(waveform analysis BEFORE any ear claim); SHA-256 every delivered file; NO
output-derived peak normalization; per-event envelopes; 3× byte-identical
reruns; M4A/NEW labels; nothing to Micah's ears without passing gates +
genuinely different measured fingerprint vs all prior clips.

## Shared gates (all forks, analyzer-first)
- frac_static ≥ 0.25
- HNR 3.7 ± 3 dB
- PERIODICITY: autocorr peak at intended F0 period ≥ 0.5
- HF_ROLLOFF: energy above 8 kHz in [-40 dB, -12 dB] rel peak
- PROSODY: F0 std dev over voiced regions in [0.3%, 3%]
- TRANSIENT: onset peak-to-RMS in first 20 ms in [3 dB, 20 dB]; peak < -1 dBFS
- Hum check: 50/60 Hz + harmonics not dominant
- NO-STATIC (hard gate, from Micah's Round-2 verdicts: static is the
  killer, glottal_formant's clarity is the bar): no grain-boundary clicks
  (boundary discontinuity < -40 dB), no sub-period grains in the audio
  path, no uncorrelated noise layering. Analyzer must prove static absent
  before any ear staging.
- Provenance: 100% of output samples mapped to (source SHA, offset);
  interpolated samples listed separately with bound

## Forks (per-fork sections below — kill bars transcribed from debate winners)

### Fork KB-EDIT — conscious-KB-driven editor (MANDATED)
See `~/workspace/audio_round3/KB_FORK_DESIGN.md`. Full autonomous
perceive→deliberate→edit→verify→commit loop over a conscious KB of real
audio units; deliberate install ops; append-only audit; zero human
decisions in the loop. Kill bars KB1-KB5 + self-kill experiment as designed.

### [DEBATE WINNERS — to be filled after judging]
- Fork 1: ...
- Fork 2: ...
- Fork 3: ...

## Verdict recording
Survivors staged as neutral CLIP_A… labels in `~/workspace/audio_round3/clips/`
with CLIP_MAP.md (attribution only after Micah's numbered verdicts).
Measured deltas vs Round 2 clips reported per fork. Commit everything to
tnn-native-lab incrementally (prereg first, then per-fork code, then
evidence). No binaries/`.zagd`.
