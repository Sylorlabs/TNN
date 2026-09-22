# BLIND TEST-1 report — B-β (event-assembler hybrid)

Package: `b_beta/blind/` (sealed; KEY.sealed.txt never opened). Three
30-second clips, blind_A/B/C. Brief: kids playing and laughing. One clip is
a real playground field recording, one is a synth control (oscillators +
filtered noise), one is the B-β fork render (assembled entirely from real
captured playground recordings).

Judges: 3 fresh native critics, signal-only analysis, disjoint from all
other packages. All three ballots valid (no blindness violations disclosed).

## Fingerprint measurements (identical across judges — same deterministic tool)

| clip | s1 (periodicity) | s2 (stationarity) | s3 (repetition) | s4 (symmetry) | s5 (formant) | S |
|---|---|---|---|---|---|---|
| blind_A | 0.700 | 0.000 | 0.000 | 0.921 | 0.289 | 0.382 |
| blind_B | 0.740 | 0.000 | 0.057 | 0.915 | 0.000 | 0.342 |
| blind_C | 0.847 | 0.462 | 0.007 | 0.827 | 0.402 | 0.509 |

A-NATIVE notes: blind_C is the only clip with a stationary texture
(s2=0.462) and has just 3 transients in 30 s (0.1/s vs 1.0/s and 0.8/s);
blind_B has the most mobile formants (s5=0) and highest envelope
variability; blind_A has the densest transient field (30 events) but the
most symmetric transients (s4=0.921).

## Judge × label × confidence × evidence

| judge | blind_A | blind_B | blind_C | ranking (most→least real) |
|---|---|---|---|---|
| 1 | fork render, LOW — middle S; zero loops, breathing flux, dense transients, but s4=0.92 symmetric | real recording, LOW — lowest S, s5=0, highest envelope variability | synth control, LOW — only stationary clip (s2=0.46), most periodic envelope, most static formants, event-sparse | B > A > C |
| 2 | fork render, LOW — s2=0/s5=0.29 real-like, but transient symmetry smells of assembly | real recording, LOW — s5=0, highest variability, dense events | synth control, LOW — decisive s2=0.46 (filtered-noise bed), s1=0.85, 3 transients | B > A > C |
| 3 | fork render, LOW — no overrides; C leads on s1/s2/s5, dissenting s3/s4 don't outweigh | real recording, LOW — highest flux/rms CV, fully mobile formants | synth control, LOW — only stationary texture, most periodic, most static formants | B > A > C |

No judge overrode the preregistered S baseline. All confidences LOW per the
frozen rule: the A−B gap (0.0396) is < 0.05 and two fingerprints (s3, s4)
dissent on blind_C's top rank. The most likely failure mode, flagged by two
judges, is a B↔A (real↔fork) swap.

## Inter-judge agreement

100% — all three judges agree on all three labels and the full ranking.

## Majority verdict

The fork render (blind_A) was labeled **"fork render" by 3/3 judges** and
"synth control" by 0/3. **B-β PASSES machine-blind Test 1.** The fail bar
(≥2 judges labeling the fork render "synth control") was not met. Caveat:
confidence is LOW across the board — the machine track separates the synth
control cleanly but the fork-vs-real discrimination is close.
