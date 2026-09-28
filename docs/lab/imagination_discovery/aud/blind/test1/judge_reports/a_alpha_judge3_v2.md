# BLIND TEST-1 ballot — package A-ALPHA — judge 3 (native critic, v2)

Blind signal-only ballot. I have never encountered these clips and did not build them.
Measured 2026-09-22 with `measure_test1.py` (30.0 s per clip).

## 1. Per-clip table

| clip | s1 (period) | s2 (station) | s3 (loop) | s4 (symm) | s5 (formant) | S | key A-NATIVE notes | identity | conf | one-line evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| clip_1.wav | 0.6264 | 0.2975 | 0.0123 | 0.8216 | 0.0000 | 0.3516 | dc≈0; 0 clips; clicks 1978 (≈real anchor 2400); hiss 0.0325 (≈real 0.0354); **hf_flatness 0.1709 ANOMALY** (very peaked HF vs real anchor 0.7854); transients 0.47/s (n=14) | **REAL (forced choice)** | MEDIUM | s3 ≈ real anchor (0.0123 vs 0.0074 — no looping); s4 ≈ real anchor (0.8216 vs 0.8274); s2 nearer real (0.4611) than synth (0.0000) |
| clip_2.wav | 0.5796 | 0.0000 | **0.5025** | 0.7719 | 0.0000 | 0.3708 | dc≈0; **723 clipped samples**; **clicks 10414** (4.3× real anchor — 347/s); hiss 0.0329 natural; hf_flatness 0.8955; transients 1.13/s (n=34, ≈synth control 0.97/s) | **FORK RENDER (forced choice)** | MEDIUM | s3 = 0.5025: half of all distant 1-s chunk pairs near-identical — loop signature, 68× the real anchor (0.0074); s2 = 0.0000 = synth anchor exactly; s4 = 0.7719 ≈ synth 0.7759 |
| calib_real.wav | 0.8468 | 0.4611 | 0.0074 | 0.8274 (n=3) | 0.4020 | 0.5089 | dc≈0; 0 clips; clicks 2400; hiss 0.0354; hf_flatness 0.7854; transients 0.1/s | **LABELED — known genuine playground field recording** | n/a (given) | label + zero loop signature; anchor for S=0.5089 |
| calib_synth.wav | 0.8744 | 0.0000 | 0.0714 | 0.7759 (n=29) | 0.6261 | 0.4696 | **hiss 0.3168 (~9× real — hissy synth bed)**; clicks 5790; 0 clips; hf_flatness 0.7962; transients 0.97/s | **LABELED — known synth control** | n/a (given) | label + most stable formants (s5=0.6261) + stationary-noise bed |

## 2. Forced choice

**clip_1 = the real recording. clip_2 = the fork render.**

### Anchor-margin reasoning (preregistered)

- Anchors: calib_real S = 0.5089; calib_synth S = 0.4696.
- clip_1 S = 0.3516: Δ to real = 0.1573, Δ to synth = **0.1180**.
- clip_2 S = 0.3708: Δ to real = 0.1381, Δ to synth = **0.0988**.
- The mechanical rule ("the unlabeled clip whose S is closer to calib_real's S is real") would name **clip_2** (0.1381 < 0.1573). I invoke the preregistered override: **individual fingerprints tell a different story, decisively:**
  - **s3 (near-exact repetition) is a smoking gun.** clip_2 = 0.5025 vs calib_real = 0.0074 (68×). Theory: "no voice repeats exactly" — a real playground cannot have 50% of its distant 1-second chunk pairs cosine->0.999 identical. That is a loop construct, not children playing and laughing.
  - s2: clip_2 = 0.0000 = calib_synth exactly (calib_real 0.4611). clip_1 = 0.2975, nearer real.
  - s4: clip_2 = 0.7719 ≈ calib_synth 0.7759 (Δ 0.004); clip_1 = 0.8216 ≈ calib_real 0.8274 (Δ 0.006).
  - s5: both unlabeled = 0.0000 — fully variable centroids ("real resonances move, couple, break"), the most real-like end of the theory, beating both anchors.
  - Per-fingerprint mean distance: clip_1→real **0.159** vs clip_1→synth 0.255; clip_2→synth **0.271** vs clip_2→real 0.336.
- **Why S misleads here:** s1 and s4 misfire on playground content. The real anchor itself scores s1 = 0.8468 (rhythmic play — chanting games, running cadences are real rhythms) and s4 = 0.8274 on only n=3 transients (under-sampled). These two components inflate both anchors' S and dominate the mean, burying the s3 discriminator. The fingerprint-level analysis recovers it.
- A-NATIVE corroboration (noted only, not deciding): clip_2 has 723 clipped samples + 10,414 clicks (347/s) + transient density 1.13/s matching the synth control; clip_1 is clean with clicks (1978) ≈ real anchor (2400) and natural hiss. Flagged anomaly: clip_1's hf_flatness = 0.1709 (very peaked HF vs real anchor 0.7854) — possible tonal play sounds (squeaks/whistles); recorded, not identity-bearing.

### Confidence: MEDIUM

Mechanical baseline: the chosen-real clip (clip_1) sits 0.118 from its nearer S anchor (calib_synth), ≥ 0.10 → HIGH baseline. **Dropped one level** because individual fingerprints contradict the S-anchor verdict (per prereg). The s3 loop signature itself is unambiguous for clip_2 = render, but the rule is mechanical, so MEDIUM.

## 3. Forced ranking (most → least likely to be a real field recording)

1. **calib_real.wav** — labeled, verified genuine (known fact, not signal).
2. **clip_1.wav** — forced-choice real; no loop signature, real-side s2/s3/s4.
3. **calib_synth.wav** — labeled synth control; honest stationary bed, no pathologies beyond hiss.
4. **clip_2.wav** — loop signature (s3 = 0.5025), clipping, click storm, synth-side s2/s4.

## 4. DISCLOSURE

I opened ONLY the four listed clips (via `measure_test1.py`, which reads their audio samples). I did not open anything under `test1/keys/`, did not open any other judge reports in `judge_reports/`, did not recognize any clip, and did not use web search or any prior knowledge of the forks. All judgments derive solely from the measurement tool's numbers plus the fingerprint theory stated in the task. **My ballot is valid.**
