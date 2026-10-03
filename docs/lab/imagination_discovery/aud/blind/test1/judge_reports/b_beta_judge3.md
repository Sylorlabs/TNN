# BLIND TEST-1 Ballot — package B-BETA — Judge 3 (native critic)

**Method:** signal-only analysis of the three listed clips via `measure_test1.py`. The synth-smell fingerprint theory and the preregistered scoring rule were the sole basis of identity judgments. No web search, no prior knowledge of the forks, no recognition of any clip.

## 1. Per-clip results

| clip | s1 (periodicity) | s2 (stationarity) | s3 (loops) | s4 (symmetry) | s5 (formant stability) | **S** | key A-NATIVE notes | label | confidence | one-line evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| blind_A.wav | 0.7002 | 0.0000 | 0.0000 | 0.9206 | 0.2892 | **0.3820** | dc≈3.1e-5; no clipping; hiss_ratio 0.055; 1297 clicks; 30 transients (1.0/s) | fork render | LOW | Middle S; s2=0 and s3=0 read real, but s4=0.92 (near-perfect transient symmetry) is the one strongly synthetic fingerprint |
| blind_B.wav | 0.7403 | 0.0000 | 0.0567 | 0.9148 | 0.0000 | **0.3424** | dc≈3.5e-5; no clipping; hiss_ratio 0.064; 2708 clicks (highest); 24 transients (0.8/s) | real recording | LOW | Lowest S; highest flux/rms variability (CV 1.52/1.21 — the most "breathing" texture), s5=0 (formants fully mobile) |
| blind_C.wav | 0.8468 | 0.4622 | 0.0074 | 0.8274 | 0.4018 | **0.5091** | dc≈5.1e-5; no clipping; hiss_ratio 0.035 (lowest); 2397 clicks; only 3 transients (0.1/s) | synth control | LOW | Highest S by a wide gap; leads on s1, s2, s5 — the ONLY clip with stationary texture (s2=0.46 vs 0.00/0.00) and static formants; periodic envelope + ~zero impacts reads as filtered-noise bed + oscillators, not children playing |

**S ranking:** C (0.5091) > A (0.3820) > B (0.3424).
Gaps: C−A = 0.1271; A−B = 0.0396 (< 0.05).

## 2. Forced ranking by most likely to be a real field recording

1. **blind_B.wav** — lowest S; the highest spectral-flux and RMS-envelope variability of the three (real ambience breathes and gusts), fully mobile formants (s5=0), zero stationarity. This is the most real-like bundle.
2. **blind_A.wav** — middle S; real-like variability (s2=0) and zero loop repetition, but its transients are near-perfectly attack/decay-symmetric (s4=0.92), which is the single most synthetic-looking number outside clip C. Consistent with a fork assembled from real captures — real source material carrying an assembly artifact.
3. **blind_C.wav** — highest S; stationary texture, periodic envelope, static formants, and only 3 transients in 30 s — there is almost no discrete impact activity for a "children playing and running" brief. Consistent with a synth control (oscillators + filtered noise) attempting the brief.

## 3. Overrides

**None — baseline stands.**

The top-S clip (C) leads on three of five fingerprints (s1, s2, s5) and by S-gap 0.127 > 0.10 over the next clip; the two dissenting fingerprints (s3 led by B, s4 led by A) do not individually outweigh the s1+s2+s5 bundle, which is exactly the signature the theory predicts for a synth (periodic rhythm, stationary bed, fixed ring). No cited override evidence reverses the baseline labeling.

**Confidence is LOW on all three labels** because (a) the A−B gap (0.0396) is below the 0.05 threshold, and (b) two fingerprints (s3, s4) dissent from the top-S clip's rank. In particular, the real-vs-fork distinction between B and A is thin: B's small loop score (s3=0.057) could be an assembly-repeat artifact of the fork render, while B's variability/formant mobility is the most real-like signal in the set. Under the preregistered rule the baseline mapping (lowest→real, middle→fork) stands, but a B/A swap is the most likely failure mode of this ballot.

## 4. A-NATIVE notes (all three clips)

- DC offset negligible on all three (3–5×10⁻⁵); zero clipping samples on all three; hiss ratios low (0.035–0.064) — no prominent hiss bed, consistent with A-NATIVE expectations across the set.
- Click counts: B 2708 > C 2397 > A 1297. Elevated but not decisive; natural transients (footfalls, stick snaps) or assembly cuts both produce these.
- Transient density: B 0.8/s, A 1.0/s, C 0.1/s. C's near-absence of impacts is anomalous for a playground brief and corroborates the synth read.

## 5. DISCLOSURE

I opened nothing beyond the three listed clip files. I ran only `measure_test1.py` against them. I did not open KEY.sealed.txt, real_calib_30s.wav, or any other file in the directory; I did not browse or search the web; I had no prior knowledge of the B-BETA forks and recognized none of the clips. All numbers above come from the measurement tool; all inferences come from the project's stated fingerprint theory. **My ballot is valid.**
