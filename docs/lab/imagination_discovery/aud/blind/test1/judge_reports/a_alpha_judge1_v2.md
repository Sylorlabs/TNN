# BLIND TEST-1 judge report — package A-ALPHA, judge 1 (v2)

**Method:** signal-only analysis via the project's measurement tool. I cannot hear; no other
information was used. The keys directory exists (`a_alpha_key.json`) but was **never opened**.

## 1. Per-clip fingerprints and A-NATIVE

Higher s1/s2/s3/s4/s5 = more synth-like. S = mean(s1..s5) = syntheticity index.

| clip | s1 (reg.) | s2 (stat.) | s3 (loop) | s4 (sym.) | s5 (ring) | S | key A-NATIVE notes | identity | conf. | one-line evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| clip_1.wav | 0.6264 | 0.2975 | 0.0123 | 0.8216 | 0.0000 | **0.3516** | dc≈0; 0 clips; 1978 clicks; hiss_ratio 0.0325 (like real anchor 0.0354, vs synth 0.3168); 14 transients, 0.47/s | **real recording** (forced choice) | MEDIUM | 4/5 fingerprints match the real anchor; s3 & s4 near-identical to real anchor; no digital damage |
| clip_2.wav | 0.5796 | 0.0000 | 0.5025 | 0.7719 | 0.0000 | **0.3708** | 723 CLIPPED samples (all others 0); 10414 clicks (2.5–5× others); hf_flatness 0.895; 34 transients, 1.13/s (10× real anchor) | **fork render** (forced choice) | MEDIUM | s3=0.5025 (½ of distant chunk pairs near-identical); s2 exact match to synth anchor; s4 near-exact match to synth anchor; clipping/click storm |
| calib_real.wav | 0.8468 | 0.4611 | 0.0074 | 0.8274 | 0.4020 | **0.5089** | LABELED — known genuine playground recording. 0 clips, 2400 clicks, low hiss | labeled real | n/a | anchor |
| calib_synth.wav | 0.8744 | 0.0000 | 0.0714 | 0.7759 | 0.6261 | **0.4696** | LABELED — known synth control. 0 clips, 5790 clicks, hiss_ratio **0.3168** (heavy HF noise bed — the synth control's tell) | labeled synth | n/a | anchor |

## 2. Forced choice — clip_1 is the real recording; clip_2 is the fork render

**Anchor-margin arithmetic (S rule as written):** calib_real S=0.5089, calib_synth S=0.4696.
- |clip_1 − calib_real| = 0.1573; |clip_1 − calib_synth| = 0.1180
- |clip_2 − calib_real| = 0.1381; |clip_2 − calib_synth| = 0.0988

The strict S rule would name clip_2 the real one (0.1381 < 0.1573), but the **margin is only
0.0192** — and the anchors themselves **invert the index**: calib_real's S (0.5089) is
*higher* than calib_synth's (0.4696). Both unlabeled clips score *below* both anchors, so
the S rule is comparing "less unlike an inverted anchor pair" — non-discriminant on this
material. I invoke the preregistered fingerprint override, justified in writing below.

**Fingerprint votes** (which anchor each unlabeled clip is closer to):

| clip_1 | s1 | s2 | s3 | s4 | s5 | net |
|---|---|---|---|---|---|---|
| vs real (0.847/0.461/0.007/0.827/0.402) | weak→real | 0.16→real | **0.005→real (near-exact)** | **0.006→real (near-exact)** | 0.40→real | **5/5 → real** |
| vs synth (0.874/0.000/0.071/0.776/0.626) | | | | | | |

| clip_2 | s1 | s2 | s3 | s4 | s5 | net |
|---|---|---|---|---|---|---|
| vs real | weak→real | 0.46→synth | 0.50→synth-ish (extreme) | 0.06→synth | 0.40→real | **→ synth** |
| vs synth | | **exact match (0.000)** | 0.43→synth | **0.004→synth (near-exact)** | | |

**The decisive signal facts, in order of weight:**
1. **s3 = 0.5025 for clip_2**: over half of distant 1-second chunk pairs are near-identical
   (log-mel cosine > 0.999). A verified-genuine 30 s playground recording does not repeat
   itself verbatim; even the synth control anchor is only 0.0714. This is the footprint of
   an assembled-from-repeated-grains construction, not a field recording. clip_1's s3
   (0.0123) is near-identical to the real anchor's (0.0074).
2. **Digital damage only in clip_2**: 723 clipped samples (all other clips: 0), 10,414
   clicks (2.5–5× every other clip), 34 transients at 1.13/s vs the real anchor's 3 at
   0.1/s — splice-boundary artifacts, not playground ambience.
3. **s2 exact-match**: clip_2's s2 = 0.0000 equals the synth anchor's to four decimals,
   driven by pathological flux_cv/rms_cv (3.55/3.89 — sparse-spike variability, not the
   real anchor's breathing 0.31/0.55). clip_1's s2 (0.2975) sits between the anchors,
   closer to real.
4. **s4 near-exact anchor matches**: clip_1 0.8216 ≈ real 0.8274; clip_2 0.7719 ≈ synth
   0.7759.
5. **A-NATIVE**: clip_1's hiss_ratio (0.0325) matches the real anchor (0.0354) and lacks
   the synth control's 0.3168 noise bed; clip_1 has 0 clipped samples and click counts
   comparable to the real anchor.

**Confidence: MEDIUM.** The fingerprint evidence alone is strong (five independent lines —
repetition, damage, stationarity, symmetry, native-noise profile — all converge). Per the
prereg, because the fingerprints contradict the S-anchor verdict, I drop one confidence
level from HIGH and explain: the S index is not discriminant-valid here (anchors
inverted; S-margin between the two clips' distances to calib_real's S is only 0.0192,
which would score LOW on its own). My verdict rests on the fingerprints, not on S.

## 3. Forced ranking by "most likely to be a real field recording"

1. **calib_real.wav** — labeled known-genuine (certainty by label).
2. **clip_1.wav** — judged the real unlabeled recording (fingerprint convergence, clean A-NATIVE).
3. **calib_synth.wav** — labeled synth control (certain synthetic, but a clean stable one).
4. **clip_2.wav** — judged the fork render; ranks below the synth control because it is
   *more* anomalous than the control itself (s3 0.5025 vs 0.0714; the only clipped clip).

## 4. Disclosure

- I opened **only the four listed files** (via the measurement tool reading them). I listed
  the `keys/` directory to confirm it exists and **opened nothing under it**.
- I have **never encountered any of these clips before** and recognized nothing.
- I used **no web search and no prior knowledge of the forks** — only the numbers from
  `measure_test1.py` and the project's synth-smell fingerprint theory stated in the brief.
- I cannot hear; this ballot is signal-analysis only.

**My ballot is not void.**
