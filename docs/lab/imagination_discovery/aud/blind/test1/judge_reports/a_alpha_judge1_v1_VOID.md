# BLIND TEST-1 ballot — package A-ALPHA — native critic judge 1

Blinded. I built none of these clips, have never encountered them, and cannot hear. Verdict below is signal-only, from `measure_test1.py` plus the preregistered synth-smell fingerprint theory. I did not open the sealed `keys/` directory, any other judge's report, or any other file. The two calibration clips are analyzed exactly as labeled.

## 1. Per-clip measurements

| clip | s1 | s2 | s3 | s4 | s5 | **S** | key A-NATIVE notes | identity | confidence | one-line evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| clip_1.wav | 0.6264 | 0.2975 | 0.0123 | 0.8216 | 0.0000 | **0.3516** | dc≈0; clips 0; clicks 1978; hiss_ratio 0.033 (clean); transients 0.47/s (14); hf_flatness 0.171 | FORK RENDER (forced choice) | LOW | S nearest-anchor distance is to calib_synth (0.1180) vs calib_real (0.3301); no near-exact chunk repetition (s3≈0.01) |
| clip_2.wav | 0.5796 | 0.0000 | 0.5025 | 0.7719 | 0.0000 | **0.3708** | dc≈0; **clips 723**; **clicks 10414**; hiss_ratio 0.033 (clean); transients 1.13/s (34); hf_flatness 0.896 | REAL RECORDING (forced choice) | LOW | S is marginally nearer calib_real (0.3109) than clip_1 is (0.3301); margin 0.0192 — razor thin |
| calib_real.wav | 0.0584 | 0.8960 | 1.0000 | 0.5000 | 0.9543 | **0.6817** | labeled real; dc≈0; clips 0; clicks 0; hiss_ratio 1.484 (hissy wash); transients 0.00/s (none detected) | LABELED REAL (anchor) | n/a (labeled) | known playground field recording per label |
| calib_synth.wav | 0.8744 | 0.0000 | 0.0714 | 0.7759 | 0.6261 | **0.4696** | labeled synth; dc≈0; clips 0; clicks 5790; hiss_ratio 0.317; transients 0.97/s (29) | LABELED SYNTH (anchor) | n/a (labeled) | known synth control per label |

s1 = envelope periodicity · s2 = stationarity · s3 = near-exact repetition · s4 = transient symmetry · s5 = centroid/formant stability · S = mean(s1..s5), higher = more synth-like.

## 2. Forced choice with anchor-margin reasoning

- **Real recording: clip_2** — **Fork render: clip_1.**
- Anchor S values: calib_real S = 0.6817, calib_synth S = 0.4696. Both unlabeled clips fall *below* both anchors (clip_1: 0.3516, clip_2: 0.3708), so the anchor pair does not bracket the field the way the design expects. Applying the frozen rule anyway: |clip_2 − calib_real| = 0.3109 vs |clip_1 − calib_real| = 0.3301. clip_2 is nearer the real anchor by **0.0192** < 0.05 → **LOW confidence**.
- Per-fingerprint cross-check vs the anchors: clip_2 is nearer calib_real on s1 (0.521 vs 0.568 gap) and s3 (0.498 vs 0.988 gap); it matches calib_synth exactly on s2 (0.0 = 0.0); both clips tie far below both anchors on s5 (0.0 vs real 0.9543 / synth 0.6261 — i.e., both clips have far more *moving* resonances than either anchor); both clips match the synth anchor on s4 (≈0.77–0.82 vs synth 0.7759 / real 0.5000).

## 3. Forced ranking, most likely to be a real field recording

1. **calib_real.wav** — labeled real; wins by definition.
2. **clip_2.wav** — forced-choice real per the anchor rule (S margin 0.0192).
3. **clip_1.wav** — forced-choice fork render; the less-synth-smelling clip on s3 but farther from the real anchor on S.
4. **calib_synth.wav** — labeled synth; wins last by definition.

## 4. Caveats (why this ballot is weak)

- **The anchors invert the theory's expected ordering.** calib_real scores S = 0.6817, *more* "synthetic" than the labeled synth control (S = 0.4696). The real anchor is a hyper-stationary wash: s2 = 0.896, s3 = 1.000 (every distant 1 s chunk near-identical — a homogeneous wash correlates that way), s5 = 0.9543, and zero detected transients. Against the theory's own sketch of a real playground (messy rhythm, breathing ambience, moving resonances), the real anchor looks like a distant, steady crowd wash, and both unlabeled clips look *more* real-like than it on the S index.
- **Individual fingerprints contradict the anchor verdict.** The verdict's strongest counter-evidence is s3 in clip_2 = 0.5025 — half of all distant 1 s chunk pairs are near-exact repeats, which per the theory ("no voice repeats exactly") is the classic event-assembler signature (reused material). clip_2 also carries 723 clipped samples and 10,414 clicks (heavy digital artifacts). Per the instructions I drop one confidence level for the contradiction — confidence is already LOW, so it stays LOW with this written justification. If forced to bet beyond the frozen rule, the s3 repetition signature alone would flip my call to clip_1 = real / clip_2 = fork.
- Both clips are far cleaner than the real anchor on hiss (0.033 vs 1.484) and far livelier (0.47–1.13 transients/s vs 0.00/s), so the A-NATIVE profile of the real anchor does not match the unlabeled field well either.

## 5. DISCLOSURE

I opened only the four listed clips via the prescribed measurement tool: clip_1.wav, clip_2.wav, calib_real.wav, calib_synth.wav in `/home/hatch/workspace/tnn-lab/imagination_discovery/aud/blind/test1/packages/a_alpha/`. I did **not** open anything under `.../test1/keys/`, did not read any other judge's report, recognized no clip, used no web search and no non-signal information. My ballot is **not void**.
