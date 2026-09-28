# BLIND TEST-1 — judge ballot (judge2, native critic, signal-only)

Package: B-ALPHA · Brief: 30 s children playing/laughing, ≥3 voices, overlapping play, running feet, laughter tumbling.

## Per-clip table

| clip | s1 (regularity) | s2 (stationarity) | s3 (repetition) | s4 (symmetry) | s5 (fixed ring) | S | key A-NATIVE notes | label | confidence | one-line evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| clip_1 | 0.8744 | 0.0000 | 0.0714 | 0.7759 | 0.6261 | 0.4696 | dc≈5.6e-06, clips 0, **click_count 5790**, hiss_ratio 0.32, hf_flatness 0.80, transients/s 0.97 (n=29) | **fork render** | MEDIUM | Low repetition + non-stationary + 29 messy transients + moving formants = real-ish fabric, but s1=0.8744 (most periodic rhythm of the three) smells constructed. |
| clip_2 | 0.6929 | 0.0000 | 0.0000 | 0.7231 | 0.3387 | 0.3509 | dc≈3.9e-07, clips 0, clicks 872, hiss_ratio 0.05, hf_flatness 0.56, transients/s 0.13 (n=4) | **real recording** | HIGH | Lowest on all five fingerprints (no exact repetition, breathing envelope, lowest formant stability, few asymmetric transients); no hiss bed. |
| clip_3 | 0.7084 | 0.7871 | 0.9212 | 0.9868 | 0.9289 | 0.8665 | dc≈3.3e-08, clips 0, clicks 0, **hiss_ratio 1.46, hf_flatness 0.84**, transients/s 0.03 (n=1) | **synth control** | MEDIUM | s3=0.9212 (92% of distant 1 s chunk pairs near-identical = looping), s2=0.7871 stationary flat hiss bed, single near-perfectly symmetric transient (s4=0.9868), frozen formants (s5=0.9289). |

## Forced ranking by realness (most → least likely real field recording)

1. clip_2 (S 0.3509)
2. clip_1 (S 0.4696)
3. clip_3 (S 0.8665)

## Overrides

None. The preregistered baseline (highest S → synth, lowest S → real, middle → fork) stands. Rationale: clip_3's top-S rank is carried by four of five fingerprints (s2/s3/s4/s5 all rank it highest), not by a lone outlier; the only dissent is s1, where clip_1 ranks highest (0.8744 > 0.7084). Per the scoring rule, s1 dissent caps the synth-control confidence at MEDIUM rather than triggering an override: a periodic rhythm envelope in one clip is not enough fingerprint evidence to overrule 92% exact-repetition, stationarity, near-perfect transient symmetry, and fixed formants all pointing at the same clip.

## Disclosure

I opened nothing beyond the three listed WAV files and the measurement script `measure_test1.py` named in the task. I did not open anything under `keys/`, did not recognize any clip (never encountered these files before), performed no web search, and used no non-signal information. Fingerprint numbers were taken verbatim from the tool output. This ballot is not void.

S gaps: clip_3−clip_1 = 0.397; clip_1−clip_2 = 0.119 (both ≥ 0.10; clip_3's all-five agreement fails on s1 → MEDIUM).
