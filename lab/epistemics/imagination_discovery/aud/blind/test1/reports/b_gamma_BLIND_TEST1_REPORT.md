# BLIND TEST-1 report — B-γ (monster fork)

Package: `b_gamma/blind/` (sealed; ORDER_SEALED.md never opened;
clip_real/clip_synth/clip_method.wav never opened). Three 30-second clips,
judge_A/B/C. Brief: kids playing and laughing. One clip is a real
playground field recording; the other two are machine-made by different
methods attempting the same brief (one a synth control, one the B-γ fork
render).

Judges: 3 fresh native critics, signal-only analysis, disjoint from all
other packages. All three ballots valid (no blindness violations disclosed).

## Fingerprint measurements (identical across judges — same deterministic tool)

| clip | s1 (periodicity) | s2 (stationarity) | s3 (repetition) | s4 (symmetry) | s5 (formant) | S |
|---|---|---|---|---|---|---|
| judge_A | 0.650 | 0.000 | 0.101 | 0.934 | 0.000 | 0.337 |
| judge_B | 0.847 | 0.462 | 0.007 | 0.827 | 0.402 | 0.509 |
| judge_C | 0.817 | 0.000 | 0.000 | 0.851 | 0.396 | 0.413 |

A-NATIVE notes: judge_B is the only stationary clip (s2=0.462) with 3
transients in 30 s; judge_A carries the most high-band hiss (0.485) and the
most transients (51); judge_C has the most shaped high end (hf_flatness
0.382) and 15 transients. Honest tension flagged by two judges: judge_A
looks real on three fingerprints but carries the highest repetition
(s3=0.101) and most symmetric transients (s4=0.934) — genuine strikes
against its "real" label.

## Judge × label × confidence × evidence

| judge | judge_A | judge_B | judge_C | ranking (most→least real) |
|---|---|---|---|---|
| 1 | real recording, LOW — lowest S; breathing flux, moving formants | synth control, LOW — highest S; periodic envelope, stationary texture, static formants | fork render, LOW — middle S; periodic envelope like B but breathing flux, zero repetition | A > C > B |
| 2 | real recording, LOW — messiest envelope, s5=0 | synth control, LOW — s1/s2/s5 all rank it first; poverty of impacts (3 transients) | fork render, LOW — periodic + static formants like B, but non-stationary, non-flat HF | A > C > B |
| 3 | real recording, LOW — lowest S, hissy HF bed | synth control, LOW — most periodic, only stationary, most static formants, sparse transients | fork render, LOW — middle S; periodic envelope + static formants like B, but breathing flux, zero loops | A > C > B |

No judge overrode the preregistered S baseline. All confidences LOW per the
frozen rule: both S gaps (0.0962, 0.0759) are ≥0.05 but <0.10, and two
fingerprints (s3, s4) dissent on judge_B's top rank.

## Inter-judge agreement

100% — all three judges agree on all three labels and the full ranking.

## Majority verdict

The fork render (judge_C) was labeled **"fork render" by 3/3 judges** and
"synth control" by 0/3. **B-γ PASSES machine-blind Test 1.** The fail bar
(≥2 judges labeling the fork render "synth control") was not met. Caveat:
confidence is LOW — the machine track separates the synth control but the
fork-vs-real discrimination is close, and judge_A's repetition/symmetry
marks mean the "real" label itself is not clean.
