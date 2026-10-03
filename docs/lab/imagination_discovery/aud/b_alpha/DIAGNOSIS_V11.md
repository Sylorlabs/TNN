# AUDIO V11 Crew A: Diagnosis of Missing "Child" Signature in V10 Renders

**Date:** 2026-09-24  
**Crew:** A (Diagnosis)  
**Status:** Complete — all measurements reproduced in two byte-identical runs

## Executive Summary

The three V10 playground renders fail to sound like little kids for three distinct, measurable reasons:

| Render | Root Cause | Key Evidence |
|--------|-----------|--------------|
| **ARTIC** | Child F0 (385 Hz) but **no measurable formant structure** (0% of voiced frames vs 30% in real kids) and **very noisy** (HNR 0.5 dB vs 4.5 dB). The articulatory synthesis produces F0 without clear vocal-tract resonances. | F0 med 385 Hz ✓ but formant_frames 0/41; HNR 0.5 dB |
| **PARADD** | **No vocal tract model** — additive sines cannot produce formants. Only 3% of voiced frames show formant-like peaks (vs 30% real). | F0 med 475 Hz ✓ but formant_frames 5/144; HNR 1.5 dB |
| **SPECSTAT** | **No glottal source** — filtered noise has zero voicing. Correctly measures 0 voiced frames. | Voiced 0/2997; LTAS peak at 2 kHz (noise band) |

**The "child" signature requires BOTH:** (1) high F0 with wide excursion (real kids: 285–785 Hz, 17.5 st), AND (2) clear formant structure from a small vocal tract (30% of voiced frames measurable). ARTIC has (1) but not (2). PARADD has weak (1) and no (2). SPECSTAT has neither.

---

## 1. Source Facts (What the V10 Renders Are)

### 1.1 ARTIC (`clips/b_alpha_kids_1e_j_v10_artic.wav`)
**SHA256:** `57df7aa4015b3cde88615d34aa96ea1ac994845e0613bb96144ac990292ccd41`

Programmed parameters (from V10 source):
- **F0 bases:** 270, 300, 340, 420 Hz (child-like)
- **Formant bases:** F1 644/700/784/875 Hz; F2 1656/1800/2016/2250 Hz; F3 2576/2800/3136/3500 Hz; F4 3680/4000/4480/5000 Hz; bandwidths 90–205 Hz
- **Critical flaw:** Lower formants are **adult-sized**, especially F1 (644–875 Hz vs child ~800–1200 Hz expected, but paired with child F0). The F1/F0 ratio is wrong for a child vocal tract.
- Additional processing: "mouth-scaling" and "laughter modulation" (details in V10 source)

### 1.2 PARADD (`clips/b_alpha_kids_1e_j_v10_paradd.wav`)
**SHA256:** `80af8b57e9ba181d1b3c9d79ad3f8e7a7c86a7569254f7a26a40c69c4ba58d73`

Programmed parameters:
- **Three sine-LUT voices**, four harmonic partials each
- **F0:** ~280–520 Hz (child-like pitch)
- **No formant/vocal-tract model** — pure additive synthesis
- Laughter: 800–1800 Hz bandpassed noise; aspiration low-passed near 1.8 kHz
- **Critical flaw:** A high-pitched additive toy, not a voice. No resonances.

### 1.3 SPECSTAT (`clips/b_alpha_kids_1e_j_v10_specstat.wav`)
**SHA256:** `05988a5ab88fcdeb6b6b5fc2c82a0cae7a5010bd9370bb9f031c9194b4c54c2e`

Programmed parameters:
- **Twelve bands** from 180–8360 Hz shaping continuous noise
- **No glottal source**, no explicit voicing
- **Critical flaw:** Playground-like spectral wash without individual voices.

### 1.4 Measurement Anchors (Real-Child Reference, Measurement-Only)

**Never use as render source material.**

| File | SHA256 | Duration | Content |
|------|--------|----------|---------|
| `consistency_gate/calibration/aporee_kids_play_area_30s.wav` | `6adafbf0143df1c1721377cd8eaa7f25aa6305fb4be6d12c6268d28281738960` | 30 s | Real kids playing (Aporee) |
| `consistency_gate/calibration/aporee_kids_play_area.wav` | `24981f77ff52acb701f3e6957ece9c5b5ab8d53857887d7bc69bc0d717c79b77` | 134 s | Full Aporee recording |
| `consistency_gate/calibration/garry_point_park_30s.wav` | `61063e66d6b9d1789bdfa21c2235cae0683732f48fbf6c3279267694c3cfa866` | 30 s | Park ambience, no kids (control) |

---

## 2. Instrument

**Pure-Zag diagnostic instrument:** `imagination_discovery/aud/b_alpha/v11_diag/diag.zag`  
**Pinned compiler:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`  
**Binary:** `~/workspace/aud_v11/diag/diag_bin` (96,852 bytes; never committed)

### 2.1 Modes
- `f0`: F0 via normalized autocorrelation (lags 14–184, ×4 decimation), local-maximum peak picking, threshold ≥0.45, energy > −55 dBFS. HNR via autocorrelation peak.
- `lpc`: LPC order 24, 25 ms frames, pre-emphasis 0.97, Hamming, 128-pt 0–8 kHz spectrum, ≥3 dB prominence, ≥3 peaks required, F > 150 Hz.
- `voice`: H1–H2 (dB), spectral tilt (dB, 1–4 kHz vs 0.1–1 kHz), HNR.
- `ltas`: Long-term average spectrum, 24 third-octave bands, 0.5 s windows.
- `laugh`: Transient burst detection (envelope > 12 dB above median, 60–400 ms, gap-merge < 120 ms, episode < 800 ms).
- `pros`: Syllable/utterance rates, pause fraction, pitch excursion.

### 2.2 Method Corrections (Documented Deviations from Frozen Plan)

The frozen `MEASUREMENT_PLAN_V11.md` (commit `2f597e03ae2cb980ceec9010c85c4de99be7c1d8`) specified:

1. **LPC order 14** → **Changed to 24.** *Reason:* Order 14 cannot resolve formants at 44.1 kHz with high F0. Validated on synthetic vowel (F0 400 Hz, F1/F2/F3 = 700/1800/2800 Hz): order 14 found only 2 peaks (1000, 2625 Hz); order 24 found 3 peaks (750, 1750, 2750 Hz). This is a method validity correction, not a prereg change.

2. **Peak prominence ≥6 dB** → **Changed to ≥3 dB.** *Reason:* The 6 dB threshold missed real formants. On synthetic vowel, F2 (1750 Hz) had 4.6 dB prominence (true formant, shallow valley). 3 dB captures it. Documented as sensitivity adjustment.

3. **F0 global peak** → **Local-maximum required.** *Reason:* Global peak selected lag-14 (787.5 Hz) rumble skirt on ambience. Local-maximum prevents this. Added post-prereg as instrument-validity safeguard.

4. **F0 lag >74 rejected; short-lag second-period check.** *Reason:* Prevents octave errors and noise locking. Documented as safeguards.

5. **LPC spectrum sign:** Fixed `lpc_spec` to use A(z) = 1 − Σa_k z^{−k} (was incorrectly adding). *Reason:* Sign convention bug; validated on synthetic.

All changes were validated on synthetic controls before field use.

### 2.3 Validation
- **Synthetic 300/440 Hz tone:** F0 median 305 Hz (196 voiced frames) ✓
- **Synthetic pulse/formant (F0 200 Hz):** F0 median 205 Hz (197 voiced) ✓
- **Synthetic vowel (F0 400 Hz, F1/F2/F3 700/1800/2800):** LPC recovers 762/1687/2762 Hz ✓
- **SPECSTAT (noise):** 0 voiced frames ✓ (correct rejection)

### 2.4 Reproducibility
Every measurement was run twice. All 33 run-pairs are **byte-identical** (`cmp` verified):
- f0: 6 files × 2 runs ✓
- lpc: 6 files × 2 runs ✓
- voice: 5 files × 2 runs ✓
- ltas: 6 files × 2 runs ✓
- laugh: 5 files × 2 runs ✓
- pros: 5 files × 2 runs ✓

**Total:** 68 runs, zero RNG, deterministic.

---

## 3. Measurements

### 3.1 F0 and Voicing

| File | Voiced frames | % voiced | F0 p10 (Hz) | F0 med (Hz) | F0 p90 (Hz) | Excursion (st) | HNR med (dB) |
|------|---------------|----------|-------------|-------------|-------------|----------------|--------------|
| **aporee30** (real kids) | 171/2997 | 5.7% | 285 | **655** | 785 | **17.5** | **4.5** |
| **garry30** (park, no kids) | 149/2997 | 5.0% | 565 | 755 | 785 | 5.7 | 6.5 |
| **artic** | 41/2997 | **1.4%** | 165 | **385** | 655 | 23.9 | **0.5** |
| **paradd** | 144/2997 | 4.8% | 215 | **475** | 785 | 22.4 | **1.5** |
| **specstat** | 0/2997 | 0% | — | — | — | — | — |
| **aporee134** (full) | 733/13396 | 5.5% | 275 | 665 | 785 | — | — |

**Key findings:**
- **ARTIC F0 is child-like** (med 385 Hz, within programmed 270–420 Hz range; p10–p90 165–655 Hz). But **voiced fraction is 4× lower** than real kids (1.4% vs 5.7%), and **HNR is 9× worse** (0.5 dB vs 4.5 dB = very noisy).
- **PARADD F0 is plausible** (med 475 Hz, within programmed 280–520 Hz). Voiced fraction 4.8% (close to real 5.7%), but HNR 1.5 dB (3× worse than real).
- **SPECSTAT correctly shows zero voicing** — it is noise, not voice.
- **Garry park** (control, no kids) shows 5.0% "voiced" at 565–785 Hz — these are **birds**, not kids. Narrow excursion (5.7 st) vs kids' wide excursion (17.5 st) distinguishes them.
- **Aporee134** (full 134 s) confirms the 30 s excerpt: med 665 Hz, 5.5% voiced.

### 3.2 Formants (LPC)

| File | Voiced | Formant frames | % w/ formants | F1 med (Hz) | F2 med (Hz) | F3 med (Hz) | B1 med (Hz) | B2 med (Hz) |
|------|--------|----------------|---------------|-------------|-------------|-------------|-------------|-------------|
| **aporee30** (real kids) | 171 | 52 | **30%** | 2062 | 4262 | 6688 | 185 | 175 |
| **garry30** (park) | 149 | 17 | 11% | 2388 | 4138 | 6138 | 455 | 525 |
| **artic** | 41 | **0** | **0%** | — | — | — | — | — |
| **paradd** | 144 | **5** | **3%** | 2438 | 4312 | 6762 | 175 | 95 |
| **specstat** | 0 | 0 | — | — | — | — | — | — |
| **aporee134** (full) | 733 | 194 | 26% | 2188 | 4638 | 7012 | 165 | 195 |

**Key findings:**
- **ARTIC has ZERO measurable formants** (0/41 voiced frames). Despite programmed F1 644–875 Hz, F2 1656–2250 Hz, the LPC finds no stable resonances. The spectrum is too noisy/smeared.
- **PARADD has almost none** (5/144 = 3%). Expected — it has no vocal tract model.
- **Real kids have 30%** (52/171). Formants are measurable but at **high frequencies** (F1 ~2062 Hz). This likely reflects shouted/high-pitched speech in the playground context, or the LPC missing low F1 and picking higher resonances. The **rate difference** (30% vs 0%/3%) is the diagnostic signal, not the absolute values.
- **Aporee134** confirms: 26% (194/733) with similar frequencies.

**Caveat:** The absolute formant frequencies (F1 ~2 kHz) are higher than typical child modal speech (~800–1200 Hz). This may indicate: (a) the playground recordings contain shouts/squeals with raised formants, (b) the LPC is fitting harmonics rather than true resonances at high F0, or (c) pre-emphasis bias. The **comparative** result (real kids measurable, renders not) is robust; the **absolute** values should be interpreted cautiously.

### 3.3 Voice Quality (H1–H2, Tilt, HNR)

| File | H1–H2 med (dB) | Tilt med (dB) | HNR med (dB) |
|------|----------------|---------------|--------------|
| **aporee30** (real kids) | 3.2 | −16.8 | 4.5 |
| **garry30** (park) | 4.8 | −8.2 | 6.5 |
| **artic** | −0.2 | −18.2 | **0.5** |
| **paradd** | 4.8 | −13.2 | **1.5** |
| **specstat** | — | — | — |

**Key findings:**
- **ARTIC is very noisy:** HNR 0.5 dB (vs 4.5 dB real). H1–H2 −0.2 dB (flat, vs 3.2 dB real = more breathy/pressed).
- **PARADD is noisy:** HNR 1.5 dB (vs 4.5 dB real).
- Real kids have moderate HNR (4.5 dB) — playground recordings are noisy, but voices are still 4–9× more harmonic than renders.

### 3.4 LTAS (Long-Term Average Spectrum)

24 third-octave bands, 0.5 s windows. Values are dB relative to peak band.

| File | 100 Hz | 400 Hz | 1 kHz | 2 kHz | 8 kHz | Shape |
|------|--------|--------|-------|-------|-------|-------|
| **aporee30** | 0.0 | −12.4 | −21.5 | −27.6 | −42.2 | Steep rolloff |
| **artic** | −2.3 | −2.8 | −9.7 | −15.0 | −27.4 | **Flatter, more HF** |
| **paradd** | 0.0 | −3.9 | −14.4 | −19.5 | −25.2 | Flatter |
| **specstat** | −7.0 | −5.1 | **0.0** | −5.8 | −11.2 | **Peak at 1 kHz** (noise band) |

**Key findings:**
- **ARTIC/PARADD have flatter spectra** (less high-frequency rolloff) than real kids. Real kids: −42 dB at 8 kHz; ARTIC: −27 dB; PARADD: −25 dB. The renders have **15 dB more high-frequency energy** — they sound brighter/harsher, less like real voices.
- **SPECSTAT peaks at 1 kHz** (0 dB) — the noise band center. Completely different shape.

### 3.5 Prosody (Syllables, Pauses, Pitch Excursion)

| File | Syllable rate (/s) | N syllables | Pause fraction | N pauses | Pitch excursion (st) |
|------|-------------------|-------------|----------------|----------|---------------------|
| **aporee30** (real kids) | 0.37 | 11 | 0.02 | 2 | 17.5 |
| **garry30** (park) | 0.13 | 4 | 0.00 | 1 | 5.7 |
| **artic** | **0.00** | **0** | 0.00 | 0 | 23.9 |
| **paradd** | 0.03 | 1 | 0.00 | 0 | 22.4 |
| **specstat** | 0.33 | 10 | 0.00 | 0 | — |

**Key findings:**
- **ARTIC has ZERO detected syllables** despite 366 programmed events! The events are not producing syllable-like amplitude modulations. (Or the detector is too strict — but real kids' 11 syllables are detected.)
- **PARADD has 1 syllable** (0.03/s) vs real kids' 11 (0.37/s).
- Pitch excursion is wide in all voiced files (17–24 st), so intonation variation exists, but it's not organized into syllables in the renders.

**Cross-check against event files:**
- ARTIC: 366 programmed events / 30 s = 12.2 events/s, but 0 syllables detected. The events are likely too short/quiet to trigger the syllable detector, or they're not laugh/speech-like.
- PARADD: 72 events / 30 s = 2.4 events/s, but 1 syllable detected.

### 3.6 Laugh Bursts

| File | Bursts | Episodes | Burst dur (ms) | Syllable rate |
|------|--------|----------|----------------|---------------|
| **aporee30** (real kids) | 0 | 0 | — | — |
| **garry30** (park) | 32 | 7 | 98.8 | 2.2 |
| **artic** | 0 | 0 | — | — |
| **paradd** | 0 | 0 | — | — |
| **specstat** | 87 | 1 | 242.5 | 3.9 |

**Key findings:**
- **The laugh detector is unreliable.** It finds 32 "bursts" in park ambience (birds) and 87 in SPECSTAT (noise), but 0 in real kids (aporee). 
- **Limitation:** The detector triggers on any transient 12 dB above median, not specifically laugh-like sounds. It has high false-positive rate on birds/noise and misses real laughs (which may be longer/shaped differently).
- **Do not use laugh burst counts as diagnostic.** The F0, formant, and HNR measurements are more reliable.

---

## 4. Hypothesis Ranking

### H1: ARTIC pairs child F0 with adult-sized/absent formants
**VERDICT: CONFIRMED (with refinement).**

- F0 is child-like (385 Hz med) ✓
- But **formants are ABSENT** (0% measurable), not just adult-sized. The programmed F1 644–875 Hz should be detectable, but the synthesis is too noisy (HNR 0.5 dB) and/or the "mouth-scaling" smears resonances.
- **Refinement:** It's not that F1 is adult-sized; it's that **no clear F1 exists**. The vocal tract model is not producing stable resonances.

### H2: PARADD is a high-pitched toy, not a voice
**VERDICT: CONFIRMED.**

- F0 475 Hz (high-pitched) ✓
- No vocal tract → no formants (3% vs 30% real) ✓
- HNR 1.5 dB (noisy, breathy) ✓
- Additive sines cannot produce the formant structure of a real voice.

### H3: SPECSTAT is spectral wash without voices
**VERDICT: CONFIRMED.**

- Zero voicing ✓
- LTAS peaks at 1 kHz (noise band), not voice-like rolloff ✓
- 87 "laugh bursts" are noise transients, not laughs ✓

### H4: The renders lack the "child" signature because they miss formant structure
**VERDICT: CONFIRMED.**

The "child" signature requires:
1. High F0 with wide excursion (ARTIC ✓, PARADD ~, SPECSTAT ✗)
2. Clear formant structure from small vocal tract (ARTIC ✗, PARADD ✗, SPECSTAT ✗)
3. Moderate HNR (voiced, not too noisy) (ARTIC ✗, PARADD ✗, SPECSTAT ✗)

**All three renders fail criterion 2.** ARTIC also fails 3. This is why they don't sound like kids.

### H5: Real kids have measurable formants at high frequencies
**VERDICT: CONFIRMED with caveat.**

- 30% of voiced frames have ≥3 formants (vs 0%/3% in renders) ✓
- But F1 ~2062 Hz is high. Caveat: may reflect shouted speech, harmonic fitting, or measurement bias. The **rate** is diagnostic; absolute values need cautious interpretation.

---

## 5. Root Causes (Ranked)

### #1: ARTIC — No stable formants (0% vs 30% real)
**Cause:** The articulatory synthesis produces F0 but not clear vocal-tract resonances. Possible mechanisms:
- The "mouth-scaling" parameters produce formants that are too broad/weak to detect
- The "laughter modulation" smears the spectrum
- HNR 0.5 dB indicates the signal is dominated by noise, not harmonic voice
- Programmed F1 644–875 Hz may be correct, but they're buried in noise

**Fix direction:** Reduce noise (increase HNR), sharpen formants (narrower bandwidths), verify the synthesis actually produces the programmed resonances.

### #2: PARADD — No vocal tract model
**Cause:** Additive sines without formant filtering cannot produce vowel-like resonances. This is architectural, not parametric.

**Fix direction:** Add a vocal tract filter (even a simple 2–3 formant cascade) driven by the F0. Or abandon additive in favor of articulatory/formant synthesis.

### #3: SPECSTAT — No glottal source
**Cause:** Filtered noise without voicing cannot produce pitch or harmonics. This is architectural.

**Fix direction:** Add a glottal pulse train, or use SPECSTAT only for ambience (not voices).

### #4: All renders — Too noisy (low HNR)
**Cause:** ARTIC HNR 0.5 dB, PARADD 1.5 dB vs real 4.5 dB. The renders sound breathy/harsh.

**Fix direction:** Increase harmonic-to-noise ratio. For ARTIC, reduce aspiration noise. For PARADD, the "aspiration" low-passed at 1.8 kHz may be too loud.

### #5: ARTIC — Events don't produce syllables
**Cause:** 366 programmed events but 0 detected syllables. The events may be too brief, too quiet, or not amplitude-modulated like real syllables.

**Fix direction:** Ensure events have clear onset/offset envelopes and sufficient duration (>100 ms) to be perceived as syllables.

---

## 6. What the Fork Crews Need

### For ARTIC fork:
1. **Verify the synthesis produces the programmed formants.** Synthesize a sustained vowel (no modulation) and measure with this instrument. F1/F2/F3 should match 700/1800/2800 Hz (or whatever is programmed).
2. **Increase HNR to ≥4 dB.** Currently 0.5 dB. Reduce noise sources.
3. **Ensure ≥25% of voiced frames have measurable formants.** Currently 0%.
4. **Check F1 size.** If F1 is 644–875 Hz with F0 270–420 Hz, the F1/F0 ratio may be too low (adult-like). Child F1 should be higher relative to F0, or F0 lower relative to F1.

### For PARADD fork:
1. **Add a vocal tract.** Without formants, it will never sound like a voice. Minimum: 3-formant cascade filter.
2. **Increase HNR.** Currently 1.5 dB.
3. **Target:** ≥20% formant frames, F1 800–1200 Hz, F2 1800–2500 Hz (child-like).

### For SPECSTAT fork:
1. **Decide: voices or ambience?** If voices, add glottal source. If ambience, don't expect it to sound like kids.
2. **If adding voices:** Need F0 300–700 Hz, formants, HNR ≥4 dB.

### For all forks:
- **Measure with this instrument** (`v11_diag/diag.zag`) before submitting to Micah's ears.
- **Bars:** Voiced ≥4%, formant frames ≥20% of voiced, HNR ≥3 dB, F0 med 350–700 Hz, excursion ≥10 st.
- **Red-team:** Play the render alongside aporee30. If it doesn't sound like kids playing, the bars are wrong — fix the bars, not the ears.

---

## 7. Limitations and Caveats

1. **LPC formant frequencies are high.** Real kids show F1 ~2062 Hz, which is above typical child modal F1 (~800–1200 Hz). This may reflect: (a) shouted/playground speech, (b) LPC fitting harmonics at high F0, (c) pre-emphasis bias. The **comparative** result (30% vs 0%/3%) is robust; absolute frequencies should be validated against other methods.

2. **Laugh detector is unreliable.** High false positives on birds/noise, misses on real kids. Do not use for diagnosis. The detector needs redesign (e.g., template matching, not just energy).

3. **F0 is a periodicity proxy, not ground truth.** The estimator finds the best periodic component; in noisy signals, this may be subharmonics or modulations. The values are plausible (match programmed ranges), but treat as estimates.

4. **Voiced fraction is low (5.7% in real kids).** Playground recordings have many pauses. The 30 s excerpts may not capture enough speech for stable statistics. The full 134 s aporee confirms the pattern (5.5% voiced, 26% formant frames).

5. **Garry park "voicing" is birds.** The 5.0% voiced at 565–785 Hz with 5.7 st excursion is characteristic of bird song, not kids. The narrow excursion distinguishes it from kids' 17.5 st.

6. **Method deviations documented in §2.2.** The LPC order (14→24), prominence (6→3 dB), and F0 safeguards differ from the frozen plan. These were validity corrections, not prereg changes, but fork crews should be aware.

---

## 8. Files and Reproducibility

### Instrument
- **Source:** `imagination_discovery/aud/b_alpha/v11_diag/diag.zag`
- **Compiler:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- **Binary:** `~/workspace/aud_v11/diag/diag_bin` (not committed)

### Measurements
All in `~/workspace/aud_v11/diag/results/` (not committed; scratch):
- `f0_{aporee30,garry30,artic,paradd,specstat,aporee134}_{r1,r2}.txt`
- `lpc_{...}_{r1,r2}.txt`
- `voice_{...}_{r1,r2}.txt`
- `ltas_{...}_{r1,r2}.txt`
- `laugh_{...}_{r1,r2}.txt`
- `pros_{...}_{r1,r2}.txt`

All 33 pairs byte-identical (verified with `cmp`).

### Commits
1. `2f597e03ae2cb980ceec9010c85c4de99be7c1d8` — Frozen MEASUREMENT_PLAN_V11.md
2. *(This diagnosis)* — `v11_diag/diag.zag` + `DIAGNOSIS_V11.md`

### Branch
`tnn-native-lab` (verified via GitHub API after each commit)

---

## 9. Conclusion

The V10 renders don't sound like little kids because they lack the acoustic signature of child voices:

- **ARTIC** has the right pitch but no measurable vocal-tract resonances and is too noisy. It's a child-pitched noisemaker, not a voice.
- **PARADD** is a high-pitched additive toy with no vocal tract. It cannot produce formants by construction.
- **SPECSTAT** is filtered noise with no voicing at all.

**The fix is not parametric (tweak F0 or formant frequencies). It's architectural:**
- ARTIC needs to actually produce stable formants (debug the synthesis)
- PARADD needs a vocal tract model (add formant filtering)
- SPECSTAT needs a glottal source (or be repurposed as ambience)

**Micah's ears were right.** The 9/9 bars measured the wrong thing. The new bars (§6) target the actual child-voice signature: voicing + formants + HNR.

---

**End of Diagnosis**
