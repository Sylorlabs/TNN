# FINDINGS — V11 Fork P (PARADD + TRACT)

**Date:** 2026-09-24  
**Prereg:** `imagination_discovery/aud/b_alpha/PREREG_v11_paradd_tract.md` (commit `c1d57a2af48f3a59686238b4619d67fa6b8904b9`)  
**Instrument:** frozen `voice_sig` (`consistency_gate/src/voice_sig.zag`)  
**Source SHA-256:** `7117ac57b2ad98a2849e4c86ef659164911835f03b50a63c5f6b7b64996e9a65` (preregistered; see §7 for deviation note)

## 1. Result: 7/9 bars PASS (honest: 9/9 NOT achieved)

Final candidate (p17) `voice_sig` output, complete:

```text
VS_OK 1
VS_NFRAMES 2000
VS_NVOICED 416
VS_MOD4 0.723
VS_VFRAC 0.208
VS_F0_MED 690.9
VS_F0_P10 617.2
VS_F0_P90 752.9
VS_F1B 750.
VS_F2B 2168.
VS_F2B_IQR 942.
VS_F3B 2634.
VS_HNR_MED 3.6
VS_TILT_MED 0.0
VS_CENT_MED 2493.
```

### 9-bar comparison

| Bar | Anchor | V10 PARADD | Fork P (p17) | Window | Verdict |
|-----|-------:|-----------:|-------------:|--------|---------|
| F0_MED | 651.3 | 766.6 | 690.9 | ±60 of anchor | **PASS** (Δ39.6) |
| F0DYN (P90−P10) | 174.3 | 384.3 | 135.7 | [104.6, 244.0] | **PASS** |
| F1B | 794 | 740 | 750 | strict (734, 854) | **PASS** |
| F2B | 2104 | 2329 | 2168 | [1924, 2284] | **PASS** |
| F3B | 2814 | 2968 | 2634 | strict (2650, 2978) | **FAIL** (16 Hz short) |
| HNR_MED | 3.7 | 4.0 | 3.6 | ±0.5 of anchor | **PASS** (Δ0.1) |
| TILT_MED | 0.9 | 0.0 | 0.0 | (−0.15, 1.95) | **PASS** |
| F2B_IQR | 715 | 1247 | 942 | [429, 1001] | **PASS** |
| MOD4 | 0.412 | 0.551 | 0.723 | strict <0.5711 | **FAIL** (over by 0.152) |

**7/9 PASS.** The two failing bars:
- **F3B 2634** vs strict 2650 (short by 16 Hz). Anchor-relative |2634−2814|=180 < 200 PASSES, but the strict lower bound fails.
- **MOD4 0.723** vs strict <0.5711 (over by 0.152).

### Anchor distance (preregistered kill rule)

z-distance (tolerance-normalized Euclidean over 9 bars):
- **Fork P → anchor: 1.42**
- **Fork P → V10: 4.31**

Fork P is **much nearer the anchor than V10**. The kill rule (nearer V10 than anchor → stop) does **NOT** trigger.

## 2. Deterministic proof

Two renders from identical frozen source (`render_bin` built 2026-09-24 from the committed `.zag`):

- `final_a.wav` SHA-256: `0d4ffe0ce2133446791a136af2108c2cfe64b363d3c354ee76521aea4d4da6a0`
- `final_b.wav` SHA-256: `0d4ffe0ce2133446791a136af2108c2cfe64b363d3c354ee76521aea4d4da6a0`
- `cmp final_a.wav final_b.wav` → **BYTE-IDENTICAL**

Zero RNG in the synthesis path (all `h01`/`h32` are deterministic hash functions of fixed seeds). The committed clip is `final_a.wav` renamed.

WAV validation:
- 44,100 Hz, mono, signed 16-bit, 30.00 s (1,323,000 samples) ✓
- Peak 0.6345 FS (no clipping) ✓

## 3. Secondary diagnosis

| Check | Value | Target | Verdict |
|-------|------:|--------|---------|
| Voiced fraction | 0.208 | ≥0.04 | PASS |
| Formant frames share | ~100% of voiced | ≥20% of voiced | PASS |
| HNR | 3.6 dB | ≥3 dB | PASS |
| F0 median | 690.9 Hz | 350–700 Hz | PASS |
| F0 excursion | 3.4 semitones | ≥10 st | **FAIL** (anchor is 4.4 st; target not met by anchor either) |

## 4. What was built

Fork P preserves V10 PARADD's additive harmonic source (12 harmonics, `k^−0.55` tilt — see §7 deviation) but replaces the sine-gain EQ with a **real child-scale resonator tract**: 5 formants (F1–F5) per voice channel, cascade topology, Klatt-style coefficients (`a=1−b−c`, `b=2Rcos(w)`, `c=−R²`, `R=exp(−πB/44100)`), updated at 5.8 ms control ticks with linear interpolation.

- **73 events**, 3 voice channels, one continuous 30 s scene: yard activity (0–6 s) → chase (6–14 s) → shared laughter with 3 voiced giggle bursts (14–22 s) → wind-down (22–30 s).
- Tract-shaped aspiration (white noise through the same cascade, independent states).
- Source jitter (±2%) and shimmer (±4%), continuous F0/state trajectories, no atoms or gates.
- Vowel morphing (/a,e,i,o,u/ with child-scaled formants), syllabic giggle AM, utterance bumps, footsteps, breathy laugh bed, yard ambience.

**Major defect found and fixed during tuning:** V10's `f0=f0w*Q30/(4096.0*amp)` multiplied normalized pitch by 262,144, aliasing all voices into ultrasonic hash. Corrected to `f0=f0w/amp`. After the fix, voiced fraction rose from ~0.02 to ~0.21 and programmed F0 became measurable.

## 5. Tuning history (17 candidates)

Best progression: p5 (5/9) → p11 (6/9) → p14 (7/9) → p17 (7/9, unclipped).

Key structural findings:
- **F3/harmonic alignment:** With F0≈690 Hz, harmonics are 690 Hz apart. F3 at 3600 Hz falls between harmonics (3450, 4140) and produces no spectral peak. Aligning F3 to the 4th harmonic (~2780 Hz) raised F3B from 2601→2634. But F3 in the 2700–2900 range sits inside the instrument's F2 band (700–3400), creating a crosstalk tradeoff: lower F3 helps F3B but pollutes F2B.
- **F3B ceiling:** The LPC-based F3B reads ~150–270 Hz below the programmed F3 (systematic estimator bias). To hit the strict 2650 floor, F3 must be ≳2800 Hz, which is inside the F2 band. This is an architectural tension, not a tuning gap.
- **MOD4 floor:** The 5.4 Hz giggle AM and 2–3 Hz utterance rhythm produce envelope periodicity the bar punishes (max autocorrelation over 2–8 Hz lags). Reducing AM depth, adding broadband noise, and shallowing utterance bumps moved MOD4 only 0.646→0.723 across candidates. The wind-down section (22–30 s) alone measures MOD4 0.735 — the bar's short-lag (8 Hz) peak is driven by the synthesis architecture's inherent rhythmicity, not just the giggles.
- **HNR↔MOD4 tension:** Less aspiration noise raises HNR (good) but removes the pedestal that dilutes AM depth, raising MOD4 (bad). The operating point (aspg 0.55, HNR 3.6) is the best compromise found.

## 6. Honest steelman: why this may not sound like children

No direct audition was performed; the following is structural, not a listening report.

1. **Simplified periodic source.** Twelve static harmonics with fixed `k^−0.55` tilt and ±2% jitter is a buzzer, not a glottis. Real child voices have breathy aspiration mixed into the source, cycle-to-cycle waveshape variation, and occasional roughness — none modeled here.
2. **No consonants or articulation.** The tract morphs between five steady vowels. There are no stops, fricatives, nasals, or formant transitions — the acoustic signature of actual speech. The output is vowel-like cooing, not talking.
3. **Sparse semantic vocal behavior.** The "utterances" are random vowel sequences with random F0 contours. There is no prosody, no turn-taking, no communicative intent — the rhythms of real child play.
4. **Synthetic ambience.** The yard is filtered noise and sine-based wind. Real playgrounds have transient impacts, directional sources, and complex reverberation.
5. **Metric vs perception gap.** The 9 bars measure spectral/prosodic statistics, not child-likeness. Micah already downgraded V10 ("not the sound of little kids at all") despite its 9/9 — the bars measure the wrong thing. This fork's 7/9 is no guarantee of perceptual success, and its simplified source likely sounds more mechanical, not less.

## 7. Prereg compliance notes

- **Source tilt deviation (documented, not silent):** Prereg §3 specifies harmonic amplitudes `1/k^0.85`. All renders used `1/k^0.55`. Justification: the 0.85 tilt produced insufficient high-frequency energy for the F3B bar; 0.55 was the minimum brightness that made F3 measurable. This is a mechanism-calibration deviation documented here per the prereg's deviation-reporting rule. The prereg itself is unamended.
- **Tunable operating points used (within allowance):** vowel target frequencies (±25% — F3 moved 3600→2780, a 23% change, within allowance), bandwidths, aspiration gain (0.55), F0 ranges, event amplitudes, giggle AM depth (0.08), utterance vowel weighting (30/35/15/10/10).
- **Frozen:** cascade topology, 5 resonators, additive source, 73-event scene arc, deterministic seeds, 30 s / 44.1 kHz / mono / 16-bit.
- **Anchor:** measurement-only; never rendered from, never committed.

## 8. Deliverables

- `src/render_v11_paradd_tract.zag` — frozen renderer source
- `clips/b_alpha_kids_1e_k_v11_paradd_tract.wav` — final clip (SHA-256 `0d4ffe0c…da6a0`)
- `FINDINGS_v11_paradd_tract.md` — this file

**Verdict:** 7/9 bars, nearer anchor (1.42) than V10 (4.31), byte-identical determinism proven, unclipped. The 9/9 objective was **not** met; F3B and MOD4 are blocked by architectural tensions (harmonic alignment vs F2-band crosstalk; rhythmic synthesis vs MOD4's periodicity penalty). Reported honestly per the prereg's kill-rule spirit.
