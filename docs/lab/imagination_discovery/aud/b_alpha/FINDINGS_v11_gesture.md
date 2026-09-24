# FINDINGS — AUDIO V11 Fork G (GESTURE)

**Date:** 2026-09-24 (PDT)
**Verdict:** **KILLED** — signature is nearer V10 than the real-child anchor (see §5).
**Renderer:** `imagination_discovery/aud/b_alpha/src/render_v11_gesture.zag`
**Clip:** `imagination_discovery/aud/b_alpha/clips/b_alpha_kids_1e_k_v11_gesture.wav`

## 1. What was built

A deterministic, pure-Zag renderer using a gesture-driven phonation state
machine (Inhale → Attack → Sustain → Release) and a 13-section Kelly–Lochbaum
child waveguide tract. Three voices produce utterances, shouts, calls,
giggles, and inhalations across a 30 s playground scene (yard activity →
chase → shared laughter → wind-down). Ambience is deterministic hash-stream
noise; footsteps are low thuds (100–145 Hz, below the voice detector floor).

- 44.1 kHz mono 16-bit WAV, 30.00 s (1,323,000 frames)
- Zero RNG in render path; deterministic hash streams only
- Three 256-entry Q24 glottal LUTs; five 13-section vowel LUTs
- Prereg: `efa5f35a2bd3c3af36d8e0cca13a5a3760f683ab`
- Amendment A1 (footstep thuds below detector floor; retuned /a/, /o/):
  `5fd651d5158b3ef0711f765afee01060afdc0885`
- Amendment A2 (refined /a/ LUT at operating F0=678 Hz):
  `74561dd913fbcaec7246efc7172a3d97c6de3bb3`
- Amendment A3 (Helmholtz-initialized /a/) was committed
  (`1d0350e5412e7292e179753f01a0b672d8cb91f2`) but **never used** — it
  scored 3–4/9 in testing and was reverted before the final render. The
  final render uses the A2 /a/ LUT.

## 2. Byte-identity proof

Two renders from the same binary and source:

```
final_a.wav  SHA-256: 4c7c62df6e5fe44896fd20bf40c946c9b58386b00847167a1674aea25aa6abb4
final_b.wav  SHA-256: 4c7c62df6e5fe44896fd20bf40c946c9b58386b00847167a1674aea25aa6abb4
```

`cmp final_a.wav final_b.wav` → identical (no output). Both 2,646,044 bytes.

Note: the frozen judge SHA-256 in the task
(`7117ac57b2ad98a2849e4c86ef659164911835f03b50a63c5f6b7b64996e9a65`)
is the judge binary's hash, not the clip's. The clip hash above is the
deliverable's.

## 3. Full judge output (frozen `voice_sig`, on final_a.wav)

```
VS_OK 1
VS_NFRAMES 2000
VS_NVOICED 139
VS_MOD4 0.474
VS_VFRAC 0.069
VS_F0_MED 657.8
VS_F0_P10 336.6
VS_F0_P90 747.4
VS_F1B 743.
VS_F2B 2107.
VS_F2B_IQR 860.
VS_F3B 3074.
VS_HNR_MED 3.1
VS_TILT_MED 0.5
VS_CENT_MED 3454.
```

Derived: F0DYN = 747.4 − 336.6 = **410.8 Hz**;
excursion = 12·log2(747.4/336.6) ≈ **13.8 semitones**.

## 4. Nine-bar comparison

Frozen references (2026-09-24):

| Bar | Anchor | V10 PARADD | Tolerance | Mine |
|-----|--------|-----------|-----------|------|
| V-F0 | 651.3 | 766.6 | ±60 | 657.8 |
| V-F0DYN | 174.3 | 384.3 | ±69.7 | 410.8 |
| V-F1 | 794 | 740 | ±120 | 743 |
| V-F2 | 2104 | 2329 | ±180 | 2107 |
| V-F3 | 2814 | 2968 | ±200 | 3074 |
| V-HNR | 3.7 | 4.0 | ±4.0 | 3.1 |
| V-TILT | 0.9 | 0.0 | ±3.0 | 0.5 |
| V-F2DYN | 715 | 1247 | ±286 | 860 |
| M-MOD4 | 0.412 | 0.551 | ±0.402 | 0.474 |

Objective (|mine − anchor| ≤ tolerance):

| Bar | \|diff\| | Tolerance | Pass? |
|-----|--------|-----------|-------|
| V-F0 | 6.5 | 60 | ✓ |
| V-F0DYN | 236.5 | 69.7 | ✗ |
| V-F1 | 51 | 120 | ✓ |
| V-F2 | 3 | 180 | ✓ |
| V-F3 | 260 | 200 | ✗ |
| V-HNR | 0.6 | 4.0 | ✓ |
| V-TILT | 0.4 | 3.0 | ✓ |
| V-F2DYN | 145 | 286 | ✓ |
| M-MOD4 | 0.062 | 0.402 | ✓ |

**Objective: 7/9** (fail: V-F0DYN, V-F3).

Beats V10 (|mine − anchor| < |V10 − anchor|):

| Bar | Mine diff | V10 diff | Beat? |
|-----|-----------|----------|-------|
| V-F0 | 6.5 | 115.3 | ✓ |
| V-F0DYN | 236.5 | 210.0 | ✗ (mine farther) |
| V-F1 | 51 | 54 | ✓ |
| V-F2 | 3 | 225 | ✓ |
| V-F3 | 260 | 154 | ✗ |
| V-HNR | 0.6 | 0.3 | ✗ |
| V-TILT | 0.4 | 0.9 | ✓ |
| V-F2DYN | 145 | 532 | ✓ |
| M-MOD4 | 0.062 | 0.139 | ✓ |

**Beats V10: 6/9** (fail: V-F0DYN, V-F3, V-HNR).

## 5. Kill adjudication (geometric distances)

Method: for each bar, z = |value − target| / tolerance (tolerance as
z-scale). Distance = √(Σz²).

Distance from final signature to anchor:
- z: F0 0.108, F0DYN 3.393, F1 0.425, F2 0.017, F3 1.300,
  HNR 0.150, TILT 0.133, F2DYN 0.507, MOD4 0.154
- **D(final, anchor) ≈ 3.70**

Distance from final signature to V10 PARADD:
- z: F0 1.813, F0DYN 0.380, F1 0.025, F2 1.233, F3 0.530,
  HNR 0.225, TILT 0.167, F2DYN 1.353, MOD4 0.192
- **D(final, V10) ≈ 2.68**

**2.68 < 3.70 — the signature is nearer V10 than the real-child anchor.**

Per the standing kill rule ("if signature is nearer V10 than the
real-child anchor, report honestly and stop"), this fork is **KILLED**.
No further tuning was performed after this determination; the A3
experiment above was reverted and is documented only for honesty.

## 6. Self-checks

| Check | Required | Measured | Pass? |
|-------|----------|----------|-------|
| Voiced fraction | ≥4% | 6.9% (139/2000) | ✓ |
| Formant frames | ≥20% of voiced | 39.8% (119/299) | ✓ |
| HNR | ≥3 dB | 3.1 dB | ✓ |
| F0 median | 350–700 Hz | 657.8 Hz | ✓ |
| Excursion | ≥10 semitones | ~13.8 st | ✓* |

\* Excursion uses P10=336.6 Hz, which is likely an octave-halving error
(see §7). The true excursion (P90−P10 over correctly-tracked frames) is
narrower; the 13.8 st figure is inflated by detector error and should not
be read as genuine intonation range.

### 6.1 Formant-frame percentage

Measured with the V11 diagnostic instrument
(`imagination_discovery/aud/b_alpha/v11_diag/diag.zag`, `lpc` mode:
LPC order 24, ≥3 dB prominence, ≥3 peaks, F > 150 Hz) on the final WAV:

```
N frames 2997
N voiced 299
N formant_frames 119
```

**119/299 = 39.8% of voiced frames have measurable formants — passes the
≥20% bar.** (Real-child reference: 30%.)

Caveat (per DIAGNOSIS_V11.md §7): absolute formant frequencies from this
instrument run high at high F0 (F1 med 2512 Hz here vs voice_sig centroid
743 Hz) — likely harmonic fitting or raised playground-speech formants.
The comparative rate (39.8% vs 0%/3% in V10 renders) is the diagnostic
signal.

## 7. Honest steelman: why this does not sound like children

1. **Octave errors corrupt the pitch track.** P10 = 336.6 Hz is ~F0/2
   (true F0s are 615–880 Hz). The /a/ vowel's actual F1 (~1359 Hz) sits
   far above the F0, so the tract attenuates the fundamental ~70 dB while
   boosting H2 (near F1); the 2nd harmonic was measured 18.7 dB stronger
   than the fundamental at F0=680 Hz. The autocorrelation then locks to
   the 2× lag on some frames. This inflates V-F0DYN to 410.8 Hz (anchor
   174.3 Hz) — the single largest z-distance (3.39σ).

2. **F3 is too high.** 3074 Hz vs anchor 2814 Hz (260 Hz over, 1.30σ).
   The 13-section tract's higher modes sit too high; the optimizer
   matched centroids via a solution whose actual F3 (~5 kHz) lies outside
   the measurement band.

3. **HNR is marginal and loses to V10.** 3.1 dB passes the ≥3 dB bar but
   is farther from the anchor (3.7 dB) than V10 PARADD (4.0 dB) is. The
   deterministic hash-stream aspiration and jitter keep it noisy.

4. **Metric improvements ≠ child identity.** Beating V10 on 6/9 bars
   (and 7/9 objective) still leaves the signature geometrically nearer
   V10 than the anchor. The bars measure the wrong thing — as Micah
   ruled on V10, ears outrank metrics. A renderer can move LPC centroids
   without producing the breathy, unstable, overlapping quality of real
   playground speech.

5. **Gestures may sound mechanical.** The Inhale→Attack→Sustain→Release
   state machine loops deterministically; utterances are placed by hash
   streams, not by any model of child intent, turn-taking, or play.
   Deterministic synthesis risks sounding synthetic rather than
   spontaneous.

6. **No auditory verification was available.** This agent had no playback;
   all judgments above are from instruments, not listening. The claim
   "does not sound like children" rests on the kill-rule geometry and
   the diagnosed octave/formant defects, not on audition.

## 8. Files

- Source: `imagination_discovery/aud/b_alpha/src/render_v11_gesture.zag`
- Clip: `imagination_discovery/aud/b_alpha/clips/b_alpha_kids_1e_k_v11_gesture.wav`
  (copied from byte-identical `final_a.wav`)
- This findings file: `imagination_discovery/aud/b_alpha/FINDINGS_v11_gesture.md`

No binaries, no `.zagd`, no debug probes committed. The reference anchor
was measurement-only and was not rendered from or committed.

## 9. Commit SHAs (to be filled after commit)

- Prereg: `efa5f35a2bd3c3af36d8e0cca13a5a3760f683ab`
- A1: `5fd651d5158b3ef0711f765afee01060afdc0885`
- A2: `74561dd913fbcaec7246efc7172a3d97c6de3bb3`
- A3 (committed, unused): `1d0350e5412e7292e179753f01a0b672d8cb91f2`
- Source+findings commit: [PENDING]
- WAV commit: [PENDING]
