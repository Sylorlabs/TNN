# PREREG_v11_repair — AUDIO V11 Fork R (REPAIRED ARTIC)

**Frozen:** 2026-09-23, BEFORE any repair render or probe render.
**Crew:** Fork R (repair, not rebuild, of V10's articulatory renderer).
**Status:** preregistered; no render work has been done under this prereg.

## 1. Question

Was V10 ARTIC's failure a wrong paradigm or a wrong execution?
V10 ARTIC passed 9/9 V10 bars yet measured 0 clean voice frames under the
frozen voice-sig instrument (max autocorr peak 0.398 < 0.60 gate), HNR
0.5 dB, zero measurable formants. Hypothesis under test: the
source→parallel-resonator architecture is sound; the failure is
parametric — the programmed formants exist but are drowned by an
aspiration-noise source ~5.6× the glottal amplitude, pitched too low for
the instrument's ZCR screen, and sized for an adult tract. Repair, don't
rebuild: keep continuous state, no atoms/gates, the 4-kid scene structure.

## 2. Frozen references

- Judging ground truth: JUDGE_PROTOCOL_V11.md (9 bars, tolerances, kill
  rules). Frozen anchor signature: F0 651.3 | F0DYN 174.3 | F1B 794 |
  F2B 2104 | F3B 2814 | HNR 3.7 | TILT 0.9 | MOD4 0.412 | 36 clean frames.
- Instrument source: voice_sig_frozen.zag,
  SHA-256 7117ac57b2ad98a2849e4c86ef659164911835f03b50a63c5f6b7b64996e9a65
  (verified identical in consistency_gate/src/voice_sig.zag; anchor values
  reproduced exactly on 2026-09-23 before this prereg: 36 frames, all 9
  values byte-match §8).
- V10 wrong-target baselines: ARTIC VS_OK 0 (0 clean frames), SPECSTAT
  VS_OK 0, PARADD 52 frames (F0 766.6/F0DYN 384.3/F1B 740/F2B 2329/
  F3B 2968/HNR 4.0/TILT 0.0/MOD4 0.551).

## 3. White-box probes (before repair)

Built as one probe renderer writing test WAVs, all measured with the
frozen instrument:

- P1: single resonator (F1 950 Hz, BW 200) impulse response → verify
  ring frequency, decay rate, peak gain vs theory.
- P2: swept sine through the parallel 4-resonator bank → verify the 4
  programmed peaks are present and measurable in the summation.
- P3: glottal pulse train (F0 650 Hz) through the bank, zero noise →
  expect clean frames, high HNR, formant-band centroids near anchor.
- P4: P3 + V10-level aspiration gain → demonstrate the HNR collapse
  (the predicted formant killer).
- P5: V10 ARTIC clip re-measured → reproduce VS_OK 0 (done: 0 frames).

Expected finding: resonators are correct (P1/P2/P3 pass); aspiration
noise is the killer (P4 collapses to V10-like); P5 reproduces V10.

## 4. Repair hypotheses (each with a kill bar)

- H-noise: V10 aspiration `asp = af*(0.15+0.85*sw)*breath*burst*(1+3uv)`
  with breath 0.35–1.30 and burst ≤2.4 puts noise ~5.6× over the glottal
  pulse (peak 0.55) → HNR 0.5 dB → no clean frames. Fix: scale aspiration
  so clean-frame HNR lands in [3.2, 4.2] dB (the V-HNR bar window).
- H-f0: V10 F0 bases 270–420 Hz fail the instrument's ZCR screen
  (≥20 crossings/1000 samples needs F0 ≳ 440 Hz for tone-like voices)
  and sit below the V-F0 bar (591–711 Hz). Fix: bases ~600–740 Hz
  (playground shout register; matches anchor med 651).
- H-formant: V10 formants are adult-sized. Fix: child-scaled
  F1 900–1100, F2 2400–3000, F3 3700–4400, F4 5500–6500 Hz,
  bandwidths 1.5–2× wider (B1 150–250, B2 250–400, B3 350–500,
  B4 500–700 Hz). Targets: F1B 734–854, F2B 1924–2284, F3B 2650–2978.
- H-tilt: V10 glottal tilt too steep. Fix: reshape glottal pulse toward
  −6..−9 dB/oct and add lip-radiation compensation so radiated TILT
  lands in (−0.15, 1.95) dB/oct (nearer anchor than PARADD's 0.0).
- H-mod: V10 has no syllabic AM on modal voices (0 detected syllables).
  Fix: 4–6 Hz syllable-rate AM on all voices → MOD4 in (0.253, 0.571).
- H-jitter: add ~1.5–2% cycle-to-cycle F0 jitter (child motor
  immaturity); BACK OFF if the V-HNR bar breaks (jitter trades against
  autocorr peak). Not one of the 9 bars; documented as a trade-off.
- H-excursion: 4 voices at distinct bases + wander → F0 P90−P10 in
  [105, 244] Hz.
- H-f2dyn: wide vowel glides (mouth openness) across clean frames →
  F2B_IQR in [429, 1001] Hz.

## 5. What is kept from V10

Continuous state everywhere (no atoms, no splicing, no gated on/off);
C1/C2 control trajectories; phase-integrated glottal pulses; parallel
2-pole formant resonators; the 4-kid scene (yard → chase → shared
laughter → wind-down); damped contact-oscillator footsteps; wind,
distant-play, reflections, swing creak. 44.1 kHz mono 16-bit, 30 s,
pure Zag, zero RNG, ≥2 byte-identical renders.

## 6. Bars (frozen judge protocol §3; all 9 must pass for objective PASS)

| bar | anchor A | tol | pass range | beat-V10 bound |
|---|---|---|---|---|
| V-F0 | 651.3 | 60 | 591.3–711.3 | \|F−651.3\| < 118.3 |
| V-F0DYN | 174.3 | 69.7 | 104.6–244.0 | \|F−174.3\| < 213.5 |
| V-F1 | 794 | 120 | 674–914 | \|F−794\| < 60 → 734–854 |
| V-F2 | 2104 | 180 | 1924–2284 | \|F−2104\| < 234 → 1924–2284 |
| V-F3 | 2814 | 200 | 2614–3014 | \|F−2814\| < 164 → 2650–2978 |
| V-HNR | 3.7 | 4.0 | −0.3–7.7 | \|F−3.7\| < 0.5 → 3.2–4.2 |
| V-TILT | 0.9 | 3.0 | −2.1–3.9 | \|F−0.9\| < 1.05 → −0.15–1.95 |
| V-F2DYN | 715 | 286 | 429–1001 | \|F−715\| < 546.3 → 429–1001 |
| M-MOD | 0.412 | 0.402 | 0.010–0.814 | \|F−0.412\| < 0.159 → 0.253–0.571 |

Self-check bars (task): voiced ≥4% (diag terms), formant frames ≥20% of
voiced, HNR ≥3 dB, F0 med 350–700 Hz, excursion ≥10 st; beat V10 on all 9.

## 7. Kill rules (frozen; this prereg adds none)

- (a) Wrong-target convergence: if the final signature's z-scored
  Euclidean distance is nearer ANY V10 render than the anchor → KILLED.
  Report honestly and stop.
- (b) Architecture ceiling: if probes P1–P3 show the parallel-resonator
  architecture cannot produce measurable formants at child scale after
  noise is tamed → document the mechanism ceiling, report, stop.

## 8. Deliverables

- src/render_v11_repair.zag (pure Zag renderer)
- clips/b_alpha_kids_1e_k_v11_repair.wav (30 s, 44.1 kHz, 16-bit mono)
- FINDINGS_v11_repair.md: white-box root cause with probe measurements,
  full voice_sig output, 9-bar table vs anchor vs V10, byte-identical
  proof (2 renders, cmp), mandatory honest steelman against child-likeness.

## 9. Commit plan (branch tnn-native-lab ONLY, never main)

1. This file ALONE (now).
2. Final: renderer + clip + findings (clip via big-file path).
Never committed: binaries, .zagd, anchor audio (CC BY-NC-ND,
measurement only), probe scratch in ~/workspace/aud_v11/fork_r/.
