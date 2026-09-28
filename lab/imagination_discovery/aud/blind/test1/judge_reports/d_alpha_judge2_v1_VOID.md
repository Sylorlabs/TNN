# BLIND TEST-1 — D-ALPHA — Judge 2 ballot (native signal critic)

Package: `d_alpha` | Brief: 30 s of children playing and laughing (≥3 distinct child voices, overlapping play, running feet, laughter tumbling). One clip = REAL playground field recording, one = SYNTH control, one = FORK RENDER.

## Per-clip measurements and labels

| clip | s1 (env. periodicity) | s2 (stationarity) | s3 (loop reuse) | s4 (transient symmetry) | s5 (formant stability) | S | key A-NATIVE notes | label | confidence | one-line evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| clip_1.wav | 0.048 | **0.895** | **1.000** | 0.500* | **0.951** | **0.679** | dc≈0, 0 clips, **0 clicks**, hiss_ratio 1.47 (hissy), hf_flatness 0.846 (flat white-ish), **0 transients in 30 s** | **SYNTH control** | MEDIUM | every distant 1 s chunk near-identical (s3=1.0), static texture (s2=0.895), frozen formants (s5=0.951); no impact ever lands as a transient |
| clip_2.wav | **0.617** | 0.000 | 0.337 | 0.895 | 0.000 | 0.370 | dc≈1e-5, 0 clips, **7409 clicks**, hiss_ratio 0.50, 43 transients @ 1.43/s, highly symmetric | **FORK render** | MEDIUM | periodic envelope (s1=0.617, strongest of three), ~1/3 of chunk pairs reused (s3=0.337), symmetric transients (s4=0.895) — constructed, but breathing (s2=0) and moving formants (s5=0) |
| clip_3.wav | 0.445 | 0.000 | 0.025 | 0.961 | 0.000 | 0.286 | dc≈2e-6, 0 clips, **9219 clicks**, hiss_ratio 0.019 (dark, little 8–20 kHz), 12 transients @ 0.40/s | **REAL recording** | MEDIUM | least syntheticity overall; almost no exact chunk repeats (s3=0.025), non-stationary (s2=0), formants move (s5=0); caveat: transients it has are the most symmetric (s4=0.961, small sample n=12) |

\* s4 for clip_1 is a 0.500 neutral default — zero transients were detected, so symmetry is unmeasurable. The absence of any transient in a 30 s "children playing" clip is itself evidence (running feet, claps, shouts all produce transients in a real recording).

Ranking gaps: clip_1→clip_2 = **0.309**, clip_2→clip_3 = **0.084**. Per the preregistered rubric: not HIGH (second gap < 0.10), MEDIUM (both gaps ≥ 0.05, and s1 dissents — it ranks clip_1 lowest on envelope periodicity).

## Forced ranking by "most likely to be a real field recording"

1. **clip_3.wav** — lowest S; near-zero loop reuse, non-stationary ambience, unstable centroid. Messy in exactly the ways reality is.
2. **clip_2.wav** — middle S; periodic rhythm and one-third loop reuse mark it as constructed, but it breathes and its resonances move.
3. **clip_1.wav** — highest S; a stationary, looping, formant-frozen texture with zero transients. The opposite of a playground.

## Overrides

**None. Baseline stands** (highest S → synth control, lowest S → real, middle → fork render).

- I considered whether clip_1's top-S rank is legitimate given its low s1 (0.048). It is: the rank is driven by s3=1.000 (literal loop — no real recording has 100% of distant chunk pairs near-identical), s2=0.895, s5=0.951, with zero transients. Envelope periodicity is only one of five fingerprints, and the s3 evidence is dispositive.
- I considered swapping real/fork (clip_2 real, clip_3 fork) because clip_3's s4=0.961 is the most synth-like transient value and clip_3 carries 9219 clicks. Rejected: clip_2's envelope is the most periodic of the three (s1=0.617 — real playground noise does not breathe on a 0.05–3 s metronome) and it reuses chunks three times more (s3=0.337 vs 0.025). On four of five fingerprints clip_3 is the least synth-like. The click anomaly is noted but, per the prereg, identity is decided on the fingerprints; a shared click-detector artifact across clip_2 and clip_3 is more parsimonious than a real recording being rhythmic and looped.
- Note on A-NATIVE: clip_1 violates the spirit of A-NATIVE (hiss_ratio 1.47, flat HF band 0.846 — a prominent white-ish hiss bed) while carrying the highest syntheticity. The anomalies (0 transients in clip_1; thousands of "clicks" in clip_2/clip_3) are recorded above but did not change the labels.

## DISCLOSURE

- I opened **only** the three listed clips, and only through the authorized measurement tool (`measure_test1.py`), which reads the audio files.
- I did **not** open anything under `.../blind/test1/keys/`, did not open any other package, did no web search, and used no prior knowledge of the forks, builders, or clips.
- I recognized **no clip** — none had been encountered before this task.
- I used **only** the tool's numbers and the fingerprint theory from the brief.
- This ballot is **valid** (no blindness violation).
