# BLIND TEST-1 — Blind Native Critic Report (D-ALPHA, Judge 1)

**Role:** blind native critic. I built none of these clips and had never encountered them before this task. I cannot hear; this ballot is signal-only.

## 1. Per-clip measurements and labels

| clip | s1 (periodicity) | s2 (stationarity) | s3 (repetition) | s4 (transient symmetry) | s5 (formant stability) | **S** | key A-NATIVE notes | label | confidence | one-line evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| clip_1.wav | 0.6171 | 0.0000 | **0.3374** | 0.8945 | 0.0000 | 0.3698 | click_count 7409; hiss_ratio 0.4955 (strong); hf_flatness 0.8815 (flat/white-ish highs); 1.43 transients/s; no clipping; dc ≈ 9.5e-6 | **fork render** | MEDIUM | Highest envelope periodicity + near-exact 1 s-loop repetition (s3 = 0.3374) = constructed/looped render; hiss-heavy. |
| clip_2.wav | 0.4454 | 0.0000 | 0.0246 | **0.9606** | 0.0000 | 0.2861 | click_count 9219 (highest); hiss_ratio 0.0194 (very clean highs); hf_flatness 0.7877; only 0.4 transients/s (n=12); dc ≈ 2.2e-6 | **real recording** | MEDIUM | Lowest S; near-zero repetition (s3=0.0246), no stationarity, no fixed formants, least periodic — the messy/reality profile. |
| clip_3.wav | 0.5012 | **0.4399** | 0.1232 | 0.8794 | **0.5868** | 0.5061 | click_count 551 (smooth); hiss_ratio 0.0673; hf_flatness 0.5332; dc ≈ 1e-7; cleanest A-NATIVE profile | **synth control** | LOW | ONLY clip with stationary texture (s2>0) AND static formants (s5>0): the filtered-noise-bed + fixed-resonator synth signature. |

### Fingerprint rank-check (per frozen confidence rule)

- s1 top: clip_1 (0.6171) — dissents from top-S clip_3 (0.5012)
- s2 top: clip_3 (0.4399) — agrees (only nonzero)
- s3 top: clip_1 (0.3374) — dissents
- s4 top: clip_2 (0.9606) — dissents
- s5 top: clip_3 (0.5868) — agrees (only nonzero)

S gaps: clip_3−clip_1 = 0.1363; clip_1−clip_2 = 0.0837.

## 2. Forced ranking by "most likely to be a real field recording"

1. **clip_2.wav** — lowest S (0.2861), no stationarity, no fixed formants, near-zero repetition.
2. **clip_1.wav** — middle S; strong repetition/periodicity looks constructed, but shows none of the stationary fixed-formant bed of a synth.
3. **clip_3.wav** — highest S; the stationary, fixed-formant texture is the textbook synth profile.

## 3. Overrides

**No override of the preregistered baseline.** I considered re-labeling clip_1 (top on s1 and s3) as the synth control, but the fingerprint-pair that most directly diagnoses an oscillator/resonator/filtered-noise synth — **s2 (stationarity) + s5 (fixed ring)** — is nonzero ONLY in clip_3, and the theory says "higher = more synth-like." clip_1's s1/s3 excess (periodicity + looping) reads more like a granular/event-assembled constructed render than a resonator synth, which is consistent with the fork-render label rather than the synth-control label. The dissent is real (3 of 5 fingerprints rank another clip first), so per the frozen rule the synth-control label is assigned **LOW** confidence; the real and fork labels get **MEDIUM** (single neighboring gap 0.0837 ≥ 0.05, and clip_2's profile matches the reality signature on 4 of 5 fingerprints, with only s4 dissenting on a small n=12 transient set).

## 4. DISCLOSURE

I opened only the three listed clip files and the measurement tool I was explicitly instructed to run (`measure_test1.py`). I did not open anything under `.../blind/test1/keys/`, did not use the web, did not recognize any clip, and used no non-signal information. **My ballot is valid (not void).**
