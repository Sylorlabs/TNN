# BLIND TEST-1 ballot — judge 2 (native critic), package B-GAMMA

Package: `b_gamma` · brief: 30 s of children playing and laughing (>=3 distinct child voices, overlapping play, running feet, laughter tumbling into each other). One real field recording, one synth control, one fork render. Signal-only analysis; I cannot hear.

## 1. Per-clip measurements and labels

| clip | s1 (envelope periodicity) | s2 (stationarity) | s3 (loop/repetition) | s4 (transient symmetry) | s5 (formant stability) | S (syntheticity) | key A-NATIVE notes | label | confidence | one-line evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|
| judge_A.wav | 0.6495 | 0.0000 | 0.1010 | 0.9344 | 0.0000 | **0.3370** | dc 3.0e-4 (highest); hiss_ratio 0.485 (highest), hf_flatness 0.836; clicks 6681 (highest); 51 transients (1.7/s) | **real recording** | LOW | Lowest S; messy envelope (flux CV 1.30), non-stationary (s2=0), moving formants (s5=0), most impacts — but s4=0.93 (symmetric) and s3=0.101 are strikes against. |
| judge_B.wav | 0.8468 | 0.4622 | 0.0074 | 0.8274 | 0.4018 | **0.5091** | dc 5.1e-5; hiss_ratio 0.035 (lowest); clicks 2397; only 3 transients in 30 s (0.1/s) | **synth control** | LOW | Highest S; most periodic envelope (s1=0.85), only stationary clip (s2=0.46), most static formants (s5=0.40), and a poverty of impacts for a running-play scene. |
| judge_C.wav | 0.8169 | 0.0000 | 0.0000 | 0.8512 | 0.3962 | **0.4129** | dc 7.2e-5; hiss_ratio 0.164; hf_flatness 0.382 (most shaped HF); clicks 1579; 15 transients (0.5/s) | **fork render** | LOW | Middle S; periodic envelope and static formants like B, but no looping (s3=0), non-stationary (s2=0). |

S computed as mean(s1..s5): A = (0.6495+0+0.101+0.9344+0)/5 = 0.3370; B = (0.8468+0.4622+0.0074+0.8274+0.4018)/5 = 0.5091; C = (0.8169+0+0+0.8512+0.3962)/5 = 0.4129. Matches the tool output.

All three: 30.0 s, clip_count 0, no clipping anywhere.

## 2. Forced ranking by realness (most likely a real field recording)

1. **judge_A.wav** — lowest S (0.3370); messy envelope, non-stationary, moving formants, 51 impacts/30 s.
2. **judge_C.wav** — middle S (0.4129); mixture of static formants/periodic envelope with non-stationarity and no loops.
3. **judge_B.wav** — highest S (0.5091); only stationary clip, most periodic envelope, most static formants, only 3 transients in 30 s (a running-feet scene with 3 impacts is implausible for a field recording).

## 3. Overrides

**No override — the baseline stands.** Highest S (B) is not driven by a single fingerprint: s1, s2, and s5 all rank B first (envelope periodicity 0.85, the only non-zero stationarity at 0.46, formant stability 0.40 — all the regularity/stationarity/fixed-ring signatures). The dissenting fingerprints do not isolate B as an outlier in a way that relocates it.

Honest caveat (why confidence is LOW rather than higher): two fingerprints dissent on B's top-S rank. s3 ranks A first (0.101 near-exact repetition vs ~0 for B and C) and s4 ranks A first (0.934 transient symmetry vs 0.851/0.827 — though the s4 spread is narrow across all three). A's near-exact repetition and symmetric transients are genuine strikes against A's "real" label, and the B−C S gap (0.0962) is under one fingerprint-weight of flipping. Additionally, A's high hiss_ratio (0.485) with flat high band (hf_flatness 0.836) and 6681 clicks are quality anomalies — but per the prereg I decided identity on the fingerprints, not A-NATIVE, and hiss was added-to-pass-bars before, so it does not move the identity call.

Confidence accounting (per frozen rules): S gaps are B−C = 0.0962 and C−A = 0.0759 — both >= 0.05 but not both >= 0.10, so HIGH is out; fingerprints s3 and s4 dissent on the top-S clip's rank (two dissents), so the rule's LOW condition (>=2 dissents) applies to all three labels.

## 4. DISCLOSURE

I opened nothing beyond the three listed clips: judge_A.wav, judge_B.wav, judge_C.wav. I did not open ORDER_SEALED.md, clip_real.wav, clip_synth.wav, or clip_method.wav, and I did not inspect any directory contents for the package beyond what this ballot required. I did not recognize any clip — I cannot hear, and no non-signal information (no web search, no memory of the forks) entered this analysis; the only inputs were the numbers returned by `measure_test1.py` plus the fingerprint theory in my task. My ballot is not void.
