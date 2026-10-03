# BLIND TEST-1 — B-ALPHA package — Judge 3 ballot (blind native critic)

Blindness: I analyzed ONLY the three WAV files named in the task. I did not open the `keys/` directory or any other file, I recognized none of the clips, and I used only the measurement numbers plus the fingerprint theory. No web search, no prior knowledge of the forks.

## Per-clip results

| clip | s1 | s2 | s3 | s4 | s5 | S | key A-NATIVE notes | label | confidence | one-line evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| clip_1 | 0.8744 | 0.0000 | 0.0714 | 0.7759 | 0.6261 | 0.4696 | dc≈5.6e-06; clicks=5790 (high — note as anomaly, likely dense digital transients); transients 0.97/s (29 total); hiss_ratio 0.32, hf_flatness 0.80 | fork render | MEDIUM | Middle S (0.47): strongly periodic envelope (s1=0.87) but almost no near-exact repetition (s3=0.07), flux/rms CVs healthy — rhythmic but not looped |
| clip_2 | 0.6929 | 0.0000 | 0.0000 | 0.7231 | 0.3387 | 0.3509 | dc≈3.9e-07; clicks=872; transients 0.13/s (4 total); hiss_ratio 0.05, hf_flatness 0.56 (high band present but not flat/noise-like) | real recording | MEDIUM | Lowest S (0.35): zero loop score, zero stationarity, lowest formant stability (s5=0.34) and most transient asymmetry among the three |
| clip_3 | 0.7084 | 0.7871 | 0.9212 | 0.9868 | 0.9289 | 0.8665 | dc≈3.3e-08; clicks=0; transients 0.03/s (1 total); hiss_ratio 1.46, hf_flatness 0.84 (dominant, flat high-band bed) | synth control | MEDIUM | Top S by a wide margin (0.87): near-perfect repetition (s3=0.92), stationary texture (s2=0.79), near-symmetric single transient (s4=0.99), static formants (s5=0.93) — filtered-noise-loop textbook |

All three: 30.0 s, clip_count=0, no DC offset issues.

## Forced ranking (most → least likely a real field recording)

1. **clip_2** — lowest syntheticity on every dimension that separates loops/stationarity; organic variability in flux, rms, and spectral centroid.
2. **clip_1** — midway: its high s1 (envelope periodicity 0.87) reads like genuinely rhythmic play (running feet, clapping games) rather than a loop, since s3 confirms nothing repeats exactly; the 5790 clicks are an A-NATIVE anomaly noted but not identity-decisive per the brief.
3. **clip_3** — near-certainly the synth: s2/s3/s4/s5 all ≥0.79, one detected transient in 30 s, and a flat high-band hiss bed.

## Overrides

**None.** The baseline (highest S = synth, lowest S = real, middle = fork) stands. Clip_3's synth identity is driven by four independent fingerprints (s2, s3, s4, s5 all rank it top with wide gaps); its s1 is only 3rd-ranked, so the sole dissenting fingerprint is immaterial to the verdict.

## Confidence rationale (per frozen rules)

- S gaps: 0.8665 − 0.4696 = 0.397; 0.4696 − 0.3509 = 0.119 — both ≥ 0.10.
- Fingerprint agreement on the top-S clip: s2, s3, s4, s5 rank clip_3 top; **s1 ranks clip_1 top** → exactly one dissenting fingerprint.
- Gaps ≥ 0.10 + one dissent → **MEDIUM** per rule ("both gaps ≥ 0.05 but ≥1 fingerprint dissents" → MEDIUM; note s1's dissent is consistent with rhythmic-but-not-looped real or rendered play, and clip_3 still holds S by a 0.40 margin).

## DISCLOSURE

- I opened nothing beyond the three listed clip files (the measurement script and its output only).
- I recognized none of the clips; I have never encountered them and did not build any fork.
- I used no non-signal information. **This ballot is not void.**
