# PREREG_v11_gesture — AUDIO V11 Fork G (GESTURE)

**Date:** 2026-09-23 (PDT)
**Fork:** G — gesture-driven phonation-state machine driving a child waveguide tract
**Status:** FROZEN at commit (this document). Tuning allowed only inside the
declared knob ranges (§8); everything else is frozen.

## 1. Paradigm (Sol hybrid: swe-1-6-slow + step-3.7-flash)

swe's phonation-state gesture machine (highest-EV behavioral half) DRIVES
step's child waveguide tract (highest-EV anatomical half):

- **Source:** naive sawtooth (phase accumulator) → 256-entry "Glottal
  Shaper" LUT with three frozen curves selected/blended by phonation state:
  - *Pressed* = hard-clip knee: y = clip(3·x) (rich harmonics — shouts,
    attack onsets)
  - *Modal* = soft-clip: y = 1.5x − 0.5x³ (steady child voice)
  - *Breathy* = sigmoid: y = x/(1 + 1.5|x|) (rounded, air leak — releases,
    giggles)
  - Blend by continuous effort e∈[0,1]: e<0.5 → lerp(breathy,modal,2e);
    e≥0.5 → lerp(modal,pressed,2e−1). C1 in time.
- **Instability:** jitter 2–4% of period (hash-stream phase-increment
  noise), 5.5 Hz vibrato ±1.2%, 0.7 Hz wander ±0.8%, shimmer ±5%·effort.
  Deterministic hash streams only — zero RNG in the render path.
- **Gesture state machine** (per utterance, expanded into 256-sample
  control tracks):
  | State   | Duration  | Pitch        | Shaper/effort | Child feature        |
  |---------|-----------|--------------|---------------|----------------------|
  | Inhale  | 60–90 ms  | —            | breath noise  | audible breath intake|
  | Attack  | 30–60 ms  | +20% overshoot (exp. decay) | pressed, e 0.85–1.0 | abrupt energetic onset |
  | Sustain | 150–600 ms| vibrato + jitter | modal, e 0.5–0.7 | wobbly unsteady tone |
  | Release | 50–90 ms  | −10% drop    | breathy, e→0.1| air leak before silence |
  - Giggle syllable = rapid Attack(35 ms)→Release(60 ms) loop at 5–8 Hz,
    effort cycling 0.9→0.15, aspiration burst on every release.
- **Tract (child waveguide):** 13 sections, Δx≈0.78 cm at 44.1 kHz → ≈10 cm
  tract (average 5-year-old scale), Kelly–Lochbaum junctions
  r=(A1−A2)/(A1+A2), per-section damping ×0.9992 (child tissue → wide
  formant bandwidths), glottis reflection rg≈0.92 with source injection,
  lips pl=−0.9·pr, radiation 1-zero HP y=x−0.96·prev. Vowel area-function
  LUTs (relative cm², child scale):
  - /a/: 2.0 2.4 2.8 3.2 3.6 4.2 5.0 6.0 7.0 8.0 9.0 9.5 10.0
  - /i/: 2.0 2.6 3.2 2.4 1.6 1.0 0.6 0.5 0.7 1.2 2.0 3.0 4.0
  - /u/: 2.0 2.6 3.0 3.4 3.0 2.6 2.4 2.2 2.0 1.6 1.2 0.8 0.6
  - /e/: 2.0 2.4 3.0 2.6 2.0 1.6 1.8 2.4 3.2 4.0 4.6 5.0 5.4
  - /o/: 2.0 2.4 3.0 3.4 3.2 3.0 2.8 2.6 2.4 2.2 2.0 1.6 1.2
  - Vowel morph per utterance (sstep blend between two vowels), areas
    interpolated per control tick, reflectances recomputed per tick.
  - The shaper output EXCITES the tract — formants are real resonances.
- **Voices (3 children):** K1 F0 base 620 Hz, K2 700 Hz, K3 540 Hz; per-voice
  hash seeds for jitter/shimmer/vowel morph. Shout segments to 750–800 Hz.
- **Scene (30 s, one continuous playground):** yard activity (0–8 s: 2
  chants + 2 calls, inhales, sparse steps) → chase (8–16 s: 4 shouts +
  calls, faster steps, 2 giggle chains) → shared laughter (16–24 s: 4
  giggle chains + shout-laughs) → wind-down (24–30 s: 2 calls + 1 soft
  giggle, sparse steps). ≈20 utterances, ≈6 laugh bursts, ≈20 footsteps,
  ≈24 low murmur events, 2-layer noise bed (750 Hz body + 2.3 kHz air).
- **Footsteps:** resonant damped sine 130–200 Hz (child thud) + 1-pole-LP
  (≈1 kHz) noise burst, 10 ms raised onset. **Laughter:** giggle-syllable
  state loops; **inhales** audible before loud utterances.
- **Implementation:** pure Zag, 44.1 kHz mono, control tracks at 256-sample
  ticks, i64-Q24 mix arena, wav_write from common_v5.zag (DC removal,
  −1 dB peak, soft clip). Seeds frozen (SEED=20260923 + per-stream salts).
  Byte-identical reruns required (cmp-verified, ≥2 runs).

## 2. What is frozen vs tunable

**Frozen:** architecture (shaper→waveguide), gesture state table (§1),
shaper curve definitions, vowel area LUTs, scene arc, hash-stream scheme,
judging protocol, kill rules.

**Tunable (§8):** mix levels (master, bed, voice, laugh, step), radiation
HP coefficient (0.85–0.97), damping (0.9985–0.9995), F0 bases (±80 Hz),
vowel-morph assignment per utterance, effort ranges (±0.15), breath-mix
gain, giggle loop rate (4–8 Hz), utterance count/density (within ±30%),
vibrato depth (0.8–1.8%), jitter range (1.5–4%).

## 3. Objective bars (from JUDGE_PROTOCOL_V11.md, frozen)

| bar | anchor A | tol | must land (a) | V10 best to beat (b) |
|---|---|---|---|---|
| V-F0 | 651.3 Hz | 60 | [591.3, 711.3] | PARADD 766.6 → \|F−A\| < 118.3 |
| V-F0DYN | 174.3 Hz | 69.7 | [104.6, 244.0] | PARADD 384.3 → < 213.5 |
| V-F1 | 794 Hz | 120 | [674, 914] | PARADD 740 → \|F−A\| < 60 |
| V-F2 | 2104 Hz | 180 | [1924, 2284] | PARADD 2329 → < 234 |
| V-F3 | 2814 Hz | 200 | [2614, 3014] | PARADD 2968 → < 164 |
| V-HNR | 3.7 dB | 4.0 | [−0.3, 7.7] | PARADD 4.0 → \|F−A\| < 0.5 |
| V-TILT | 0.9 dB/oct | 3.0 | [−2.1, 3.9] | PARADD 0.0 → \|F−A\| < 1.05 |
| V-F2DYN | 715 Hz | 286 | [429, 1001] | PARADD 1247 → < 546.3 |
| M-MOD | 0.412 | 0.402 | [0.010, 0.814] | PARADD 0.551 → \|F−A\| < 0.159 |

VS_OK 1 (≥25 clean voice frames) is required — missing voice fails every
voice bar. Self-measure with the frozen instrument (voice_sig_frozen.zag,
SHA-256 7117ac57b2ad98a2849e4c86ef659164911835f03b50a63c5f6b7b64996e9a65)
BEFORE any listening.

## 4. Kill rules

- **(a) Wrong-target convergence** (frozen protocol §4): z-scored Euclidean
  distance over the 9 bars vs anchor must be strictly smaller than the
  distance to PARADD's signature (D_paradd ≈ 4.33). If nearer to PARADD
  than to the anchor → KILLED, reported honestly, work stops.
- **(b) Self-honesty:** if the signature is nearer the V10 renders than
  the anchor, report it and stop — do not tune toward the metric puppet.
- Passing all 9 bars implies D ≤ 3.0 < 4.33, so 9/9 satisfies (a).

## 5. Iteration plan

1. Build instrument, verify frozen SHA, re-measure anchor (expect the
   frozen §8 values).
2. Build renderer; first a 3 s sustained-vowel + giggle test rig to
   validate tract resonances (formant-band centroids) and HNR land near
   anchor before the full 30 s.
3. Full 30 s scene → voice_sig → 9-bar table vs anchor vs V10.
4. Iterate ONLY inside §8 knob ranges. Any change outside §8 requires a
   prereg amendment committed before use.
5. Commit: src/render_v11_gesture.zag + clips/b_alpha_kids_1e_k_v11_gesture.wav
   + FINDINGS_v11_gesture.md (full voice_sig output, 9-bar table,
   byte-identical proof, MANDATORY honest steelman against child-likeness).

## 6. Anti-self-deception

- The frozen instrument is ground truth for the objective prong; the
  diagnosis instrument (v11_diag) is NOT ground truth — do not tune to it.
- The steelman section must argue the clip does NOT sound like children,
  written from the measurements and from critical listening, before any
  verdict of success.
- R1-puppet lesson: metric-matching without prosody is a trap — the
  gesture machine must produce genuine utterance-level prosody (inhale,
  overshoot, leak), not steady tones.

## 7. Commit rules

- Repo sylorlabs/TNN, branch tnn-native-lab ONLY (verify via gh-api after
  every commit). No binaries, no .zagd.
- This prereg is committed ALONE before any render artifact exists.
- Final WAV (2.6 MB) via commit_big_files.py; text via commit_racefree.py;
  TMPDIR=~/workspace/tmp_commit.
