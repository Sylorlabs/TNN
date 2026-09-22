# BLIND TEST-1 ballot — judge 3 (native critic, signal-only) — package B-GAMMA

Brief asked for: 30 s of children playing and laughing — >=3 distinct child voices, overlapping play, running feet, laughter tumbling into each other.

## 1. Per-clip measurements and labels

| clip | s1 (periodicity) | s2 (stationarity) | s3 (repetition) | s4 (symmetry) | s5 (formant stab.) | S | key A-NATIVE notes | label | conf. | one-line evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| judge_A.wav | 0.6495 | 0.0000 | 0.1010 | 0.9344 | 0.0000 | **0.3370** | hiss_ratio 0.485 (high, flat HF band hf_flatness 0.836); clicks 6681 (highest); transients 1.7/s (most, n=51); dc 0.00030; clip_count 0 | **real recording** | LOW | Lowest S; messiest envelope (flux_cv 1.295, rms_cv 1.112) and moving formants (s5=0), but note high s4/s3 |
| judge_B.wav | 0.8468 | 0.4622 | 0.0074 | 0.8274 | 0.4018 | **0.5091** | hiss_ratio 0.035 (very low, dark); clicks 2397; transients 0.1/s (sparse, n=3); dc 0.00005; clip_count 0 | **synth control** | LOW | Highest S; most periodic envelope (s1=0.85), most stationary texture (s2=0.46), most static formants (s5=0.40) |
| judge_C.wav | 0.8169 | 0.0000 | 0.0000 | 0.8512 | 0.3962 | **0.4129** | hiss_ratio 0.164 (moderate, hf_flatness 0.382 — non-flat); clicks 1579 (lowest); transients 0.5/s (n=15); dc 0.00007; clip_count 0 | **fork render** | LOW | Middle S; periodic envelope + static formants like B, but breathing spectral flux (s2=0) and zero repetition |

Score gaps: B−C = 0.0962; C−A = 0.0759. Both gaps ≥ 0.05 and < 0.10.

## 2. Forced ranking — most likely to be a real field recording

1. **judge_A.wav** — lowest syntheticity index; highest envelope variability, moving resonances, hissy HF bed
2. **judge_C.wav** — middle S; breathes like real ambience (s2=0) but envelope periodicity and static formants sit between A and B
3. **judge_B.wav** — highest syntheticity index; periodic envelope, stationary texture, static formants, sparse transients

## 3. Overrides

**None.** The baseline stands, though the fingerprints disagree internally in a way worth flagging to the coordinator: clip B (the top-S pick) ranks first on only 3 of 5 fingerprints (s1, s2, s5); clip A (the low-S pick) ranks first on s3 (0.101 vs B 0.007, C 0.000 — near-exact voice repetition, synth-like) and s4 (0.934 vs B 0.827, C 0.851 — the most symmetric transients, synth-like). No override is justified because the rule's override bar requires *specific* evidence that the baseline misfires (e.g. top-S driven by a single fingerprint, or the middle clip showing stationary high-band hiss with a periodic envelope), and that evidence is absent: B's lead is broad across periodicity, stationarity, and formant stability, not single-fingerprint-driven; C's high band is not flat (hf_flatness 0.382) and its flux breathes (s2=0). The honest read is that A looks real on three fingerprints and synth-like on two — which is exactly why confidence is LOW per the frozen rule.

## 4. Confidence basis

- Both S ranking gaps ≥ 0.05 (0.0962, 0.0759) but neither ≥ 0.10.
- Two of five fingerprints dissent on the top-S clip's rank (s3 and s4 both rank clip A first, not B).
- Frozen rule: "LOW if any gap < 0.05 or >=2 fingerprints dissent." → **LOW for all three labels.**

## 5. DISCLOSURE

- I opened **only** the three listed files (`judge_A.wav`, `judge_B.wav`, `judge_C.wav`) — plus the measurement script named in the task.
- I did **not** open ORDER_SEALED.md, clip_real.wav, clip_synth.wav, or clip_method.wav, or any other file in the package.
- I recognized **no** clip (first encounter; signal-only analysis, no listening).
- I used **no** non-signal information: no web search, no prior knowledge of the forks, only the numbers from `measure_test1.py` and the fingerprint theory in the task.
- **Ballot is valid** (no blindness violations).
