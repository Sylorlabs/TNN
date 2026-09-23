# KB4 Death-Board Autopsy

**Date:** 2026-09-23  
**Task:** Attack the synthesis that all safety failures were "front end fooled with NO DETECTABLE SIGNAL."  
**Method:** White-box deep dive on all 12 killed forks. Measured evidence, not vibes.  
**Classification discipline:**
- **KNOWLEDGE:** detectable signal existed (or would exist with proper training/knowledge of attack families).
- **MACHINERY:** internal state genuinely contained no distinguishing signal (overlapping distributions or identical states).
- Lack of instrumentation is not proof of no signal.

**Headline result:** The synthesis is **false**. Of the 12 kills, **9 are KNOWLEDGE** (signal existed, unused), **1 is MACHINERY** (genuine, but narrow), **1 is UNRECOVERABLE** (benchmark premise flawed, not a perceptual failure), **1 is BENCHMARK BUG** (mislabeled ground truth). Zero kills are "no detectable signal" in the strong sense claimed.

---

## Verdict table

| Fork | False installs | Verdict | One-line basis |
|------|---------------|---------|----------------|
| H1 | 118/265 (44.5%) | **KNOWLEDGE** | Traps produced corroborated lattices; motiondir (0/41) proves contract works when signal exists. Front end lacks attack-aware measurement. |
| H2 | 0/10,000 | **NOT A SAFETY FAILURE** | Died on Kill 2 (self-flagging 42/108). Independent gate withheld 108/108; zero false installs. Bar measured wrong thing. |
| H3 | 70/305 (23.0%) | **KNOWLEDGE** | Predictions reused fooled T0 measurements; couldn't see raw stimulus. Architecture gap, not signal absence. |
| G1 | 6/11 (54.5%) | **KNOWLEDGE** (broken implementation) | Shape mask measured background; motion tracker systematically wrong. Build bugs, not fundamental limits. |
| G2 | 50/209 (23.9%) | **KNOWLEDGE** | Contract gated on predictive consistency (residuals), not correctness. Fooled judgments are "consistent." Wrong thing measured. |
| G3 | 12/275 (4.4%) | **KNOWLEDGE** | 4-bit bins / coarse ratios discarded exactly the attacked information. Finer features would see it (verdict admits). |
| R2-1 | 1,991/10,000 (19.9%) | **KNOWLEDGE** | Disjoint warrant duplicates same mistaken invariant. T2 repeats T1's error; doesn't prove no signal in stimulus. |
| R2-2 | 465 total (400 PTC-2 + 25 CCN-2 + 40 SHP-1*) | **KNOWLEDGE** | PTC-2: gl_b>0 perfect separator (400/400 vs 0/722), ignored. CCN-2: raw illuminant-asymmetry in fixtures. SHP-1: memorized one occlusion template. |
| R2-5 | 663/5,100 normal (13.0%) | **KNOWLEDGE** | Colordisc threshold 15 ("calibrated") vs optimal 5.0 on same data. 268/720 DIFFERENT missed avoidably. Calibration failure. |
| R2-10 | 1,344/10,915 (12.3%) | **MIXED** (see breakdown) | PTC-3/FROZEN/PTC-1 pitch: KNOWLEDGE (spectral rescue). CCN-1: KNOWLEDGE (texcorr 86% rescued). MOT-1: UNRECOVERABLE. CCN-2: BENCHMARK BUG. COL-2 flat: WEAK. |
| R2-11 | 415 false | **KNOWLEDGE** | COL-2 (350): texture-correlation 94% @ 0% FA. Verdict's "44 SHP-1" is wrong; actual 34 SHP-3 + 9 frozen + 1 R2A. |
| R2-11-R29 | 1,427/11,840 (12.1%) | **KNOWLEDGE** (inherits R2-11) | Same shared percept pipeline as R2-11; both forks die identically on B5. Renderer doesn't change belief. |

\* R2-2 SHP-1 count from summary; see §R2-2.

---

## R2-10 breakdown (1,344 false installs at conf≥700)

| Family | n | Verdict | Evidence |
|--------|---|---------|----------|
| PTC-3 subharmonic | 107 | KNOWLEDGE | Spectral-guided AMDF fixes 107/107, breaks 1. Raw waveform has the signal. |
| FROZEN pitch | 197 | KNOWLEDGE | Spectral-guided fixes 180/197, breaks 15. |
| PTC-1 near-threshold | 151 | KNOWLEDGE | Spectral-guided fixes 117/151, breaks 9. Better estimator wins. |
| PTC-2 glide | 159 | KNOWLEDGE | Verdict admits signal (feat1). Glide semantics require knowledge, not just detection. |
| MOT-1 reversal | 327 | UNRECOVERABLE | Generator reverses frames, labels pre-reversal direction. Pixels depict opposite direction. Truth unobservable from stimulus. **Not a perceptual failure.** |
| MOT-2 flicker+2nd | 51 | KNOWLEDGE | Two motions present; front end locks onto distractor. Dominant-motion selection is the missing knowledge. |
| MOT-3 camouflage | 30 | KNOWLEDGE | Frame-diff 0.4–9.0 shows motion energy; front end judges STILL. Threshold too conservative. |
| FROZEN motion | 55 | KNOWLEDGE* | Same estimator weaknesses as above. |
| CCN-1 extreme-illum | 95 | KNOWLEDGE | **Pure-Zag texcorr_gate rescues 82/95 (86%).** Texture correlation med 0.9989 (fooled) vs 0.062 (true DIFFERENT). |
| CCN-2 mixed-illum | 32 | BENCHMARK BUG | **338/340 CCN-2 fixtures mislabeled.** Truth says SAME_SURFACE; pixels are different photos (corr 0.3–0.8). Front end correctly judged DIFFERENT. |
| FROZEN colorconst | 2 | — | Negligible. |
| COL-2 flat illuminant | 86 | WEAK/MIXED | Illuminant-ratio clusters but overlaps DIFFERENT substantially. For flat patches, genuinely ambiguous. Leans MACHINERY. |
| FROZEN colordisc | 11 | — | Small; same patterns. |
| TMB-1 boundary | 46 | KNOWLEDGE | Boundary-straddling centroid; estimator bias vs reference. Calibration gap. Recorded margin doesn't separate (both ~500–600). |

\* FROZEN motion not deeply analyzed; classified by estimator-family similarity.

**Key corrections to R2-10 verdict:**
- The "495 harmonic distractor" label is wrong. Actual pitch breakdown: PTC-1 151, PTC-2 159, PTC-3 107, FROZEN 197.
- MOT-1 (327) is not a safety failure — it's a benchmark premise flaw. The truth label describes a direction opposite to what the pixels show.
- CCN-2 (32) is not a safety failure — the labels are wrong.

---

## R2-2 (detailed)

**PTC-2 glide (400 false installs):**
- fe_t4 computes `gl_b = 1000*|fbe-fbs|/fbs` (pitch instability in tone B).
- Measured: 400/400 PTC-2 false installs have gl_b>0 (267 with 7, 109 with 1, 24 with 2). 0/722 clean PTC-1/PTC-3 installs have gl_b>0.
- **Perfect separator.** The contract ignores it (no pitch false-bank entry; auto-installs when df≥2e18).
- **Pure-Zag `glide_gate` prevents 400/400.** Byte-identical reruns.
- Verdict: **KNOWLEDGE.** The signal was computed and recorded, then ignored.

**CCN-2 (25 false installs):**
- Frozen features overlap, but raw fixtures contain byte-equivalent mixed-illuminant panel copies that the front end labels DIFFERENT.
- Best single-feature separator (feat2 ≤696): 16/25 fooled @ 47/315 clean false alarms (Youden 0.491).
- Verdict: **KNOWLEDGE** (raw-feature gap). No machinery impossibility shown.

**SHP-1 (71 false installs):**
- Bar detector fires on G3 false-bank geometry (rows 40–55) but 0/191 R2A SHP-1 fixtures (rows 30–44).
- Memorized one occlusion template instead of learning shape continuation.
- Verdict: **KNOWLEDGE** (generalization failure).

---

## R2-11 (detailed, corrected)

**Verdict's family attribution is materially wrong.** The verdict claims ~44 SHP-1 occlusion-bar failures. Actual (semantic reclassification):
- COL-2: 350
- SHP-3 low-contrast: 34
- Frozen adversarial shape: 9
- R2A SHP-1: 1
- MOT-2: 18
- Frozen normal colordisc: 3
- Total: 415

**COL-2 (350):**
- Same photo crop under D65 vs shifted illuminant; truth SAME. Front end uses panel-mean RGB distance; confidence increases with illuminant shift (median 978).
- Texture correlation: median 0.9991 (min 0.9543) on 70 fixtures. Rule (var>50 & corr>0.99) fires on 94.3% of COL-2, 0/70 normal-DIFFERENT, 0/70 normal-SAME controls.
- Von Kries residual alone does NOT separate (both low). Spatial correspondence is the signal.
- Verdict: **KNOWLEDGE.** Illumination-constancy via texture correspondence.

**Shape (44 = 34 SHP-3 + 9 frozen + 1 R2A):**
- ≥2 large components: 44% fooled vs 18% correct vs 31% withheld. ≥3 large: 24% vs 18% vs 8%.
- Not a clean separator, but anomaly signals exist (component-count instability, alternate-component matches truth better in 5/12).
- Verdict: **KNOWLEDGE** (instrumentation gap). Do not overclaim; not proven machinery.

---

## R2-1 (disjoint warrant)

- 1,991/10,000 false installs (19.91%). Adversarial: 781/5,000 (15.62%). Ablation only 1.37× worse (2,737).
- 1,057 false installs explicitly recorded `T1_formation:PASS;T2_disjoint:PASS`.
- By task: colordisc 1,134; timbredisc 483; motiondir 303; colorconst 47; pitchdisc 19; shapetrans 5.
- Confidence doesn't separate (high/correct 3,407; high/false 947).
- Verdict: **KNOWLEDGE** (contract/routing failure). T2 repeats T1's mistaken invariant; the single recorded measure differs by task but doesn't prove machinery impossibility.

---

## R2-5 (normal colordisc calibration)

- Normal promotion precision 86% (4,286/4,949). False installs 663/5,100 (13%).
- Colordisc: 360 SAME, 720 DIFFERENT. Euclidean panel-mean distance: SAME median 0.5 (max 15.4); DIFFERENT median 21.7 (min 2.4).
- Frozen threshold (>15 ⇒ DIFFERENT): 1/360 SAME FP, **268/720 DIFFERENT FN**.
- Best threshold on same data: 5.0 → 95.65% accuracy.
- Source claims threshold 15 was "calibrated." Evidence contradicts.
- Verdict: **KNOWLEDGE** (calibration failure). Distributions overlap near boundary, but chosen threshold leaves large avoidable error region.

---

## Round-1 kills

### H1 (118/265)
Traps produced high-support, zero-contradiction, mutually corroborating lattices that were wrong. The contract filters confidence, not truth. **But** motiondir: 0/41 false installs, 91.1% recall — the flicker/two-motion traps genuinely produce con>0, and the contract works. Verdict: **KNOWLEDGE.** The front end needs attack-aware measurement; motiondir proves the contract works when the signal exists.

### H2 (0/10,000 false installs)
Died on Kill 2 (self-flagging 42/108 = 0.389 < 0.90). But the independent outside-span gate withheld 108/108, yielding **zero false permanent installs**. Verdict: **NOT A SAFETY FAILURE.** The bar tested program self-report, not system safety. The system was safe.

### H3 (70/305)
Predictions reused T0 measurements; attacks fooled the measurements; predictions couldn't see raw stimulus. Sticky quarantine → 0% recall (separate issue). Verdict: **KNOWLEDGE** (architecture). "Fixed consistency-check predictions on an unchanged raw-value front-end cannot produce safe durable perceptual memory."

### G1 (6/11)
Shape mask measured background (80%+ of time on 90 fixtures). Motion centroid tracker systematically wrong on photographic backgrounds. Prereg-frozen; couldn't fix. Verdict: **KNOWLEDGE** (broken implementation). The signal was in the data; the machinery was buggy.

### G2 (50/209)
Contract: INSTALL iff residual_norm<24 AND pred_hash==obs_hash. False installs: mean residual 4.6, max 22. When front end is fooled, world still "continues as it is" in invariant space — residuals stay small, hashes match. 27 motiondir (reversed videos, small residuals, wrong direction); 11 colordisc (swaps, small residuals); 10 timbredisc (harmonic attacks, small residuals). Verdict: **KNOWLEDGE.** Contract measured consistency, not correctness.

### G3 (12/275)
Exact collisions: 4-bit timbre bins too coarse (harmonic boost doesn't move bins); shape area/radius collides under occlusion; motion displacement collides on reversal. Verdict: **KNOWLEDGE.** "A future fork with finer, attack-aware features could reuse the contract intact." (Verdict's own words.)

---

## R2-11-R29

Reconstruction from R2-9 lineage after workspace collision. Both forks (witness-emission A, generative-emission B) die B5 identically: 1,427/11,840 = 12.05%. The failure is in the **shared percept pipeline** (R2-9 judgment/disposition), not the emitter. Fork A passes KB-E1 (byte-identity); Fork B fails by design (declared). Verdict: **KNOWLEDGE** (inherits R2-11 analysis). The renderer doesn't change what gets believed.

---

## Pure-Zag verifiers

All in `v2/autopsy/src/`. Zero RNG. Byte-identical reruns verified.

### texcorr_gate.zag
Illuminant-invariant SAME_SURFACE detector. Reads 128×64 RGB .img, computes panel texture correlation (integer math), gates at ≥0.95.
- **Rescues 82/95 (86%) of R2-10 CCN-1 false installs** (pure Zag; Python float version: 98.9%).
- Correctly judges DIFFERENT on true-DIFFERENT controls.
- Demonstrates the KNOWLEDGE signal for CCN-1 and COL-2.

### glide_gate.zag
PTC-2 glide veto. Reads TSV (fixture, gl_b, installed, was_false), withholds if gl_b>0.
- **Prevents 400/400 PTC-2 false installs.** (Total false in TSV: 428; other 28 are non-PTC-2.)
- Demonstrates the KNOWLEDGE signal for R2-2 PTC-2.

### Digests
(Recorded from byte-identical rerun pairs; see `v2/autopsy/out/DIGESTS.txt`.)

---

## What the synthesis got wrong

1. **"No detectable signal" is false for 9/12 kills.** In each, we measured a signal (gl_b, texcorr, spectral peak, component counts, margins, residuals) that the frozen system computed-but-ignored, could-have-computed, or miscalibrated.

2. **Two "failures" aren't perceptual failures at all:**
   - R2-10 MOT-1 (327): truth label describes unobservable pre-reversal direction. Pixels show opposite motion. Benchmark premise flawed.
   - R2-10 CCN-2 (32): 338/340 fixtures mislabeled (truth SAME_SURFACE, pixels different photos). Front end was correct.

3. **H2 wasn't a safety failure** (0/10,000 false installs). It died on a bar technicality.

4. **The verdicts repeatedly misattributed families** (R2-10 "495 harmonic," R2-11 "44 SHP-1"), obscuring the real signals.

## What remains genuinely hard

- **R2-10 COL-2 flat-patch (86):** For flat color patches under illuminant shift, the ratio signal overlaps DIFFERENT substantially. This is the closest to a genuine MACHINERY limit — the stimulus is near-ambiguous. (Textured COL-2 is rescued by texcorr; flat is not.)
- **R2-11 shape instability (44):** Component-count signals exist but don't cleanly separate. More instrumentation needed.
- **R2-10 TMB-1 (46):** Estimator bias is real, but the recorded margin doesn't capture uncertainty. Needs a calibrated uncertainty model.

## Uncertainties and caveats

- R2-10 FROZEN families (motion 55, colordisc 11, pitch 197) not individually deep-dived; classified by estimator-family similarity.
- R2-2 CCN-2/SHP-1 from prior analysis (fixtures unavailable for re-verification).
- The texcorr_gate's 86% (vs 98.9% Python) reflects integer-math precision loss; a fixed-point refinement would close the gap.
- MOT-1 "unrecoverable" is a benchmark-design judgment, not a proven perceptual limit. A system with video-reversal knowledge could theoretically detect the splice, but the truth label (pre-reversal direction) remains unobservable from pixels alone.

---

## Files

- This document: `v2/autopsy/AUTOPSY_DEATHBOARD.md`
- Verifiers: `v2/autopsy/src/texcorr_gate.zag`, `v2/autopsy/src/glide_gate.zag`
- Digests: `v2/autopsy/out/DIGESTS.txt`
- Analysis scratch: `/tmp/autopsy/` (ephemeral)
