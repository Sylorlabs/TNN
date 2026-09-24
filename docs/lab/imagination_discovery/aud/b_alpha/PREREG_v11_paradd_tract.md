# PREREG — AUDIO V11 Fork P (PARADD + TRACT)

**Status:** FROZEN. Committed BEFORE any V11 PARADD+TRACT render exists.
**Fork:** P — additive source + architectural vocal tract
**Date:** 2026-09-24
**Author:** fork-P crew (subagent)

## 1. Hypothesis

V10 PARADD was the only render with a measurable voice signature (52 clean
frames) but has **no vocal tract by construction** — additive sines cannot
produce formants (3% formant frames vs 30% in real kids, diagnosis
instrument). The fix is **architectural, not parametric**: keep PARADD's
additive harmonic source, but drive a REAL time-varying vocal-tract filter
with it — a Klatt-style cascade of child-scale resonators whose poles are
set by a 9 cm child tract and morph between child vowel targets — plus
aspiration noise shaped by the SAME tract (parallel cascade). Prediction:
the voice signature moves from V10 PARADD's baseline toward the real-child
anchor on ALL 9 frozen bars, because the spectrum will now carry genuine
resonance structure instead of bare harmonic stacks.

What this prereg rules OUT: parametric-only tweaks (reweighting sine
gains, post-hoc EQ on the finished mix). The resonators must be EXCITED by
the source sample-by-sample — the harmonics drive the poles, the poles
ring — which is a different physical architecture from filtering a
finished waveform, even though both are LTI at any frozen instant.

## 2. Frozen architecture

### 2.1 Source (kept from V10 PARADD, upgraded)

- 3 voice channels, additive harmonic series **k = 1..12, TRUE integer
  harmonics**. (V10 used inharmonic partials 1.0/1.12/1.25/1.40; programmed
  F0 280–520 Hz measured as F0 med 766.6 — the estimator likely locked onto
  a detune artifact. True harmonics should read near programmed F0.)
- Amplitudes `1/k^0.85` (child glottal tilt −6..−9 dB/oct, SOL_IDEAS_V11).
- **Jitter:** ±2% per-cycle F0 perturbation (>1.5% child target, SOL M9),
  **shimmer:** ±4% per-cycle amplitude — both hash-driven at phase wrap,
  deterministic, zero RNG.
- 5.5 Hz vibrato ±1.2% + 0.7 Hz wander ±0.8% (kept from V10, continuous).

### 2.2 Vocal tract (NEW — the architectural addition)

Per voice channel, a cascade of **5 second-order resonators**
(Klatt cascade topology):

```
y[n] = a·x[n] + b·y[n-1] + c·y[n-2]
b = 2·R·cos(2πF/44100), c = −R², R = exp(−πB/44100), a = 1 − b − c
```

Child vowel targets (9 cm tract; SOL_IDEAS_V11 §M4 / Iseli child norms),
frequencies Hz, bandwidths Hz (1.5–2× adult, SOL):

| vowel | F1 | F2 | F3 | F4 | F5 | B1 | B2 | B3 | B4 | B5 |
|-------|----|----|----|----|----|----|----|----|----|----|
| /a/ | 1000 | 2000 | 3400 | 6000 | 7800 | 200 | 320 | 420 | 600 | 750 |
| /e/ | 720 | 2600 | 3700 | 6200 | 7900 | 180 | 330 | 430 | 620 | 770 |
| /i/ | 420 | 3000 | 3900 | 6300 | 8000 | 160 | 340 | 440 | 640 | 790 |
| /o/ | 620 | 1400 | 3300 | 5900 | 7700 | 170 | 290 | 410 | 610 | 760 |
| /u/ | 450 | 1250 | 3200 | 5800 | 7600 | 170 | 290 | 410 | 610 | 760 |

Time-varying, area-function-like control:
- Each utterance carries a vowel pair A→B; F/B morph via `sstep` over the
  utterance (C1 trajectories, no switching).
- Per-child tract-length scale 0.96–1.04 (hash-derived, fixed per channel).
- Resonator coefficients computed at 256-sample control ticks, linearly
  interpolated per sample (same pattern as V10's laugh biquads).
- Resonator states are continuous memory across the whole 30 s (never
  reset) — the tract has a persistent acoustic memory like a real one.

### 2.3 Breathiness (NEW — architectural)

- Aspiration noise (hash stream) through a **parallel identical cascade**
  (same time-varying coefficients, independent states) — breath shaped by
  the same tract, Klatt-style. No unfiltered white-noise path for voices
  (V10's white aspiration is removed).
- Mix level `asp_g` tuned to land **HNR_MED ≈ 3.7 dB** (frozen anchor).
- Giggle segments get 1.6× aspiration (breathy giggle quality, SOL).

### 2.4 Laughter

- **Voiced giggles:** voice-channel events (kind 3) with F0 680–800 Hz,
  /a/→/e/ vowel, continuous 5.0–5.5 Hz syllabic AM with
  `(0.5+0.5·sin)²` shape (C1, always ≥0.45 — no gating), 1.6× aspiration.
- V10's bandpass-noise laugh units kept at 0.5× gain as breathy laugh bed.

### 2.5 Scene (frozen arc, same as V10 PARADD)

One continuous 30 s playground scene:
yard alive (0–6 s) → chase (6–14 s) → trip (14.6 s) → shared laughter
(15–22 s) → wind down (22–30 s). ~75 deterministic hash-chain events:

- Utterances: F0 **560–760 Hz** (V10's 280–520 misread by the estimator;
  true harmonics should measure near programmed), vowel pairs
  hash-weighted toward /a/ and /e/, 40–80 ms attack / 150–400 ms release
  sstep bumps (kept from V10).
- Giggle bursts at ~11 s (chase), 15.5/17.9/20.3 s (laughter), 25.5 s
  (wind-down); 1–2 noise-laugh beds.
- Footsteps and ambience **mechanically identical to V10**
  (damped-sine steps, two-layer noise bed) — they are scene, not voice.

### 2.6 Continuity and determinism

Every output sample is a combination of continuous phase accumulators,
memory-bearing IIR resonator states, and C1 control tracks. No atoms, no
gated on/off triggers, no splicing. Zero RNG in the render path
(h32/h01 hash streams only). **≥2 byte-identical renders**, verified with
`cmp` before submission.

## 3. Instrument and bars (frozen)

Judging ground truth: the frozen `voice_sig` instrument
(`voice_sig_frozen.zag`, SHA-256
`7117ac57b2ad98a2849e4c86ef659164911835f03b50a63c5f6b7b64996e9a65`;
buildable copy `consistency_gate/src/voice_sig.zag` verified
byte-identical; anchor reproduces the frozen §8 numbers exactly).

Anchor A (36 clean frames):
`F0_MED 651.3 | F0_P10 598.0 | F0_P90 772.3 | F1B 794 | F2B 2104 |
F2B_IQR 715 | F3B 2814 | HNR_MED 3.7 | TILT_MED 0.9 | MOD4 0.412`

V10 PARADD baseline R (52 clean frames — the wrong-target reference):
`F0 766.6 | F0DYN 384.3 | F1B 740 | F2B 2329 | F2B_IQR 1247 |
F3B 2968 | HNR 4.0 | TILT 0.0 | MOD4 0.551`

A fork passes a bar iff **(a)** `|F−A| ≤ tol` AND **(b)**
`|F−A| < |R−A| + tol/20` (strictly nearer the anchor than V10 PARADD,
JUDGE_PROTOCOL_V11 §3). Objective PASS = 9/9 + VS_OK 1 (≥25 clean frames).

| bar | anchor A | tol | \|R−A\| | pass window for F |
|-----|----------|-----|--------|-------------------|
| V-F0 | 651.3 Hz | 60 | 115.3 | [591.3, 711.3] |
| V-F0DYN | 174.3 Hz | 69.7 | 210.0 | [104.6, 244.0] |
| V-F1 | 794 Hz | 120 | 54 | (734, 854) |
| V-F2 | 2104 Hz | 180 | 225 | [1924, 2284] |
| V-F3 | 2814 Hz | 200 | 154 | (2650, 2978) |
| V-HNR | 3.7 dB | 4.0 | 0.3 | [3.2, 4.2] |
| V-TILT | 0.9 dB/oct | 3.0 | 0.9 | (−0.15, 1.95) |
| V-F2DYN | 715 Hz | 286 | 532 | [429, 1001] |
| M-MOD | 0.412 | 0.402 | 0.139 | (0.2529, 0.5711) |

Secondary self-checks (diagnosis instrument `v11_diag`, looser gate):
voiced ≥4%, formant frames ≥20% of voiced, HNR ≥3 dB, F0 med 350–700 Hz,
excursion ≥10 st. (Note: under the frozen instrument the anchor itself is
1.8% voiced, so the ≥4% figure is interpreted under the diagnosis
instrument's gate; the frozen instrument is ground truth for judging.)

## 4. Kill rules (frozen)

- **(a) Wrong-target convergence** (JUDGE_PROTOCOL_V11 §4a): z-scored
  Euclidean distance over the 9 bars. If the fork's signature is nearer to
  ANY V10 render than to the anchor → fork DEAD. Report honestly, stop,
  no further iteration.
- **(b)** VS_OK 0 (<25 clean frames) → dead on the objective prong.
- The subjective prong (ears) is out of this crew's scope; the clip is
  submitted with a mandatory steelman against child-likeness regardless
  of the objective score.

## 5. Iteration policy

**Frozen by this prereg:** the architecture — harmonic source exciting a
time-varying 5-resonator child-tract cascade + parallel tract-shaped
aspiration; the scene arc; the bar windows; the kill rules.

**Tunable operating points** (mechanism calibration, not architecture):
vowel target frequencies (±25%), bandwidths, aspiration gain, F0 ranges,
event amplitudes, giggle AM depth/rate, utterance vowel weighting. Any
tuning beyond ±25% of a vowel target is documented in FINDINGS as a
prereg-deviation with justification.

## 6. Deliverables and commit plan

1. **This prereg** → `imagination_discovery/aud/b_alpha/PREREG_v11_paradd_tract.md`,
   committed ALONE on branch `tnn-native-lab` before any render.
2. Final commit (only after self-measurement + iteration):
   - `imagination_discovery/aud/b_alpha/src/render_v11_paradd_tract.zag`
   - `imagination_discovery/aud/b_alpha/clips/b_alpha_kids_1e_k_v11_paradd_tract.wav`
     (44.1 kHz mono 16-bit, 30 s)
   - `imagination_discovery/aud/b_alpha/FINDINGS_v11_paradd_tract.md`
     with: full `voice_sig` output, 9-bar table vs anchor vs V10 PARADD,
     byte-identical proof (`cmp` of 2 renders), and a MANDATORY honest
     steelman arguing why the clip does NOT sound like children.

Never committed: binaries, `.zagd` / `.zag-cache`, anchor WAV/MP3
(CC BY-NC-ND — measurement only, never render source).
