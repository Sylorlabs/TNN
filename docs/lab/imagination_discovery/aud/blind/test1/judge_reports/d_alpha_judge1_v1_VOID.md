# BLIND TEST-1 — D-ALPHA ballot (native critic judge 1)

Judge role: blind native critic. Signal-only analysis; no listening, no web search, no prior exposure to the forks.

## Method
Ran `measure_test1.py` on the three clips (30.0 s each). Identity decided on the five synth-smell fingerprints (S = mean of s1..s5); A-NATIVE numbers used only for anomaly notes.

## 1. Per-clip results

| clip | s1 | s2 | s3 | s4 | s5 | S | key A-NATIVE notes | label | conf | one-line evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| clip_1 | 0.0478 | 0.8947 | 1.0000 | 0.5000 | 0.9514 | 0.6788 | dc≈0, 0 clips, 0 clicks, hiss_ratio 1.47 (elevated HF energy), hf_flatness 0.85, **0.00 transients/s (zero transients in 30 s)** | **synth control** | LOW | s3=1.0: every distant 1 s chunk pair is near-identical — a looped bed; stationary (s2=0.895), static formants (s5=0.951), zero impacts in purported playground |
| clip_2 | 0.6171 | 0.0000 | 0.3374 | 0.8945 | 0.0000 | 0.3698 | dc≈1e-5, 0 clips, 7409 clicks, hiss_ratio 0.50, 1.43 transients/s (43 transients) | **fork render** | LOW | Non-stationary, moving formants (real-like), but highest envelope periodicity (s1=0.617) and high transient symmetry (s4=0.8945) — rhythmic regularity reads as construction |
| clip_3 | 0.4454 | 0.0000 | 0.0246 | 0.9606 | 0.0000 | 0.2861 | dc≈2e-6, 0 clips, 9219 clicks, hiss_ratio 0.019 (very low HF energy), 0.40 transients/s (12 transients) | **real recording** | LOW | Lowest S; s3=0.0246 (no voice ever repeats — the reality signature), s2=0 (breathes), s5=0 (resonances move) |

## 2. Forced ranking — most likely real field recording
1. **clip_3** — lowest S; near-zero repetition score (s3=0.0246) is the strongest reality marker in the fingerprint set
2. **clip_2** — messy spectra and moving formants argue real, but its envelope periodicity (s1=0.617, highest of the three) is the single most synth-like value outside clip_1's bed fingerprints
3. **clip_1** — stationary looped texture with static formants and zero transients across 30 s; incompatible with a live playground

## 3. Overrides
**None.** Baseline stands: highest S → synth (clip_1), middle S → fork (clip_2), lowest S → real (clip_3).

Considered and rejected:
- Override clip_2 as the synth? Its s1=0.617 (periodic envelope) and s4=0.8945 (symmetric transients) are real synth-smells. But its s2=0, s5=0, s3=0.337 and 43 transients show the spectral messiness the synth control (clip_1) entirely lacks; periodicity alone can come from rhythmic play (running, clapping games), so the evidence does not outweigh the baseline ordering.
- Override clip_3 as the fork? clip_3 has the highest s4 (0.9606) — but only 12 transients, and its s3 is the lowest measured of the package (0.0246), the fingerprint the theory explicitly ties to reality ("no voice repeats exactly"). Nothing supports elevating it above clip_2 on the synth scale.

## 4. Confidence rationale (preregistered rule)
S ranking: clip_1 (0.6788) > clip_2 (0.3698) > clip_3 (0.2861). Gaps: 0.309 and 0.0837 — both ≥0.05, second gap <0.10.
Fingerprint agreement on the top-S clip: s2, s3, s5 rank clip_1 first; **s1 and s4 rank it last** (s1: clip_2 > clip_3 > clip_1; s4: clip_3 > clip_2 > clip_1). Two fingerprints dissent → **LOW** confidence per the frozen rule ("LOW if any gap < 0.05 or ≥2 fingerprints dissent").
Caveat on s4: clip_1's s4=0.5 is a no-transient default (n_transients=0), not a measured symmetry — the dissent is partly an artifact of clip_1 containing no transients at all, which is itself evidence of a synthetic bed rather than against it. This caveat does not meet the bar for an override (no evidence favoring a different identity assignment), so the baseline stands at LOW confidence.

## DISCLOSURE
- I opened ONLY the three listed clip WAV files and ran the supplied `measure_test1.py` on them. I did not open anything under `.../blind/test1/keys/` (sealed mappings) or any other file in the test directory.
- I recognized none of the clips; I have never encountered these recordings or the forks that may have produced them.
- No non-signal information was used: no web search, no prior knowledge of the forks, no external references. Identity decisions rest solely on the measurement-tool numbers and the project's stated fingerprint theory.
- On that basis, my ballot is **valid** (not void).
