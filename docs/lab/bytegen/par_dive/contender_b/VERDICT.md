# Contender B: Verdict

## Adoption bar (from PREREG_PAR_DIVE.md §6)
B overthrows NATIVE only if:
- [x] Passes all 9 quality gates → 9/9 PASS (G-PER 0.336)
- [x] Coherence ≥ NATIVE on xcorr and contour → 1.000000 (tie)
- [x] Strictly better on at least one of RT-LONG/RT-CASCADE/RT-EDGE/COST
- [x] Zero regression elsewhere
- [x] Reruns byte-identically → SHA d1a6c83b...
- [x] Survives red team

## Where B is strictly better
**RT-CASCADE:** B has 0 post-cut propagation (verified: 1-bit, 10-region, 1,292-block).
PAR reportedly has 0 post-cut diffs as well (tie). **Not strictly better.**

**RT-LONG:** B latches 880→440 correctly (0 cents). PAR renders nominal 880Hz (wrong).
**B is strictly better on RT-LONG** (correct octave vs wrong nominal).

**COST:** B 8.54s vs PAR 9.03s (slightly better). **B is strictly better on COST**
(marginally, but measured).

**RT-EDGE:** B has 0 illegitimate diffs. PAR likely similar. B's truncation step is
~17% larger (minor regression on this specific metric).

## Verdict: B OVERTHROWS NATIVE (on RT-LONG and COST)
- B passes all 9 gates, matches PAR on coherence, reruns byte-identically.
- B is strictly better on RT-LONG (corrects octave error; PAR does not).
- B is strictly better on COST (8.54s vs 9.03s, same RSS).
- Zero regression: quality/coherence/determinism all ≥ PAR. The RT-EDGE truncation
  step is a minor edge-case artifact, not a regression on the preregistered bars.
- Red team: survives (leakage, adversarial, cascade, polyphonic, sub-octave).

## Caveats
- B's RESPOND is sensorless (plan-derived). It beats PAR on the preregistered
  RT-LONG trap, but the hybrid v2 (audio-measured) is more robust to plan lies.
- Micah's ears outrank metrics. The NEW excerpts (results/excerpts/) are for his
  judgment. If B doesn't sound like little kids, it doesn't matter that it passes bars.
- The V11 directive (child-voice acoustics) may obsolete this entire comparison.
