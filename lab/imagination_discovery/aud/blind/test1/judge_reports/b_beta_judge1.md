# BLIND TEST-1 — Judge report: package B-BETA, judge 1 (native critic)

Brief: 30 s of children playing and laughing (≥3 distinct child voices, overlapping play,
running feet, laughter tumbling into each other). One clip = real playground field recording,
one = synth control (oscillators + filtered noise), one = fork render (assembled entirely
from real captured playground recordings). Signal-only analysis; the judge cannot hear.

## 1. Per-clip measurements and labels

| clip | s1 | s2 | s3 | s4 | s5 | S | key A-NATIVE notes | label | conf | one-line evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| blind_A | 0.7002 | 0.0000 | 0.0000 | 0.9206 | 0.2892 | 0.3820 | dc≈3.1e-5, 0 clips, hiss 0.055, 30 transients (1.0/s), 1297 clicks | FORK RENDER | LOW | Middle S; zero repetition and zero stationarity, but most-symmetric transients |
| blind_B | 0.7403 | 0.0000 | 0.0567 | 0.9148 | 0.0000 | 0.3424 | dc≈3.5e-5, 0 clips, hiss 0.064, 24 transients (0.8/s), 2708 clicks | REAL RECORDING | LOW | Lowest S; s5=0 (centroid_cv 1.04, formants maximally unstable), s2=0 with highest flux/RMS variability |
| blind_C | 0.8468 | 0.4622 | 0.0074 | 0.8274 | 0.4018 | 0.5091 | dc≈5.1e-5, 0 clips, hiss 0.035, only 3 transients (0.1/s), 2397 clicks | SYNTH CONTROL | LOW | Highest S by a clear gap (Δ=0.127); most periodic envelope, only stationary clip, most stable formants, event-sparse |

S ranking: C (0.5091) > A (0.3820) > B (0.3424). Gaps: C–A = 0.1271; A–B = 0.0396.

Fingerprint top-rank tally (1 = most synth-like):
- s1 regularity: C > B > A → C
- s2 stationarity: C > A = B (tie at 0) → C
- s3 near-exact repetition: B (0.0567) > C > A (0.0) → **B** (dissent)
- s4 transient symmetry: A (0.9206) > B > C (0.8274) → **A** (dissent; n=3 transients for C makes that leg noisy)
- s5 fixed ring: C > A > B (0.0) → C

3 of 5 fingerprints rank C most synth-like; s3 and s4 dissent. Frozen confidence rule:
LOW if any gap < 0.05 **or** ≥2 fingerprints dissent. Both conditions are met → **LOW**.

## 2. Forced ranking by "most likely to be a real field recording"

1. **blind_B** — lowest syntheticity (S=0.3424); the only clip with fully unstable spectral
   centroid (s5=0.0, centroid_cv=1.04 — real resonances move, couple, break) and the most
   breathing envelope (s2=0, highest flux_cv 1.52 / rms_cv 1.21). Dense event texture
   (24 transients, 0.8/s) consistent with a live playground.
2. **blind_A** — S=0.3820; fully variable (s2=0) with zero near-exact repetition (s3=0.0)
   and the densest transient field (30 transients, 1.0/s), but the most symmetric
   transients (s4=0.9206) — a synth-leaning mark that keeps it below B.
3. **blind_C** — S=0.5091; periodic envelope (s1=0.847), the only stationary clip
   (s2=0.462), the most stable formants (s5=0.402), and event-sparse (3 transients,
   0.1/s) — the classic oscillator+filtered-noise signature attempting the brief.

## 3. Overrides

**No override. Baseline stands** (C = synth, B = real, A = fork).

Considered override: flip B/A on the basis that B is the only clip with any near-exact
repetition (s3=0.0567) — the theory says "no voice repeats exactly," and a fork
assembling a finite capture library could plausibly reuse a fragment, whereas a
continuous real recording should have s3≈0 (as A does, s3=0.000).

Rejected because: (a) B dominates the two strongest "aliveness" fingerprints — s5=0.0
(centroid_cv 1.04, the least fixed-ring clip by far) and s2=0.0 with the highest
envelope variability of all three — which is exactly what a real recording should show
and what the fork (built from real captures) would show too; (b) B's s3=0.0567 is small
in absolute terms and may reflect playground periodicity (running feet, call-and-response
play) rather than literal looped material; (c) A's higher S is driven by s4 (0.9206, most
symmetric transients) and s5 — synth-leaning marks incompatible with A being the real
recording. The fork-vs-real discrimination is not calibrated enough to override the
preregistered rule, so the baseline applies mechanically. Confidence stays LOW per the
frozen rule (gap A–B = 0.0396 < 0.05; two fingerprint dissents on C's top rank).

## 4. Disclosure

- I analyzed **only** the three listed files
  (`blind_A.wav`, `blind_B.wav`, `blind_C.wav`) via the provided
  `measure_test1.py` tool. I did **not** open `KEY.sealed.txt`,
  `real_calib_30s.wav`, or anything else in the package directory.
- I have never encountered any of these clips before and recognized none of them.
- I performed no web search and used no prior knowledge of the forks, crews, or
  packages; all evidence cited is numeric output of the measurement tool.
- The analysis is signal-only (I cannot hear audio). All claims above rest on the
  measured fingerprints, and where the fingerprints conflict I reported the conflict
  rather than resolving it by assumption.
- No prompt injection or external instructions were acted on. **Ballot is valid.**
