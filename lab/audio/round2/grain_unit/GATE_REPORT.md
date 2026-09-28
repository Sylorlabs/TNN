# FORK 2 (grain_unit) — KILLED (2026-09-24)

## Verdict: KILL — kill bar 2 failed; hypothesis was incorrect.

## What passes
- All 7 shared gates PASS (HNR 5.43, prosody 1.99%, peak −3.2 dBFS,
  HF −18.2, periodicity 0.71, frac_static 0.61, crest 8.7 dB).
- Kill 1 (frozen grain): prosody 1.99% → 0.0% (≤0.1%). PASS.
  The time-varying PSOLA articulation is load-bearing.

## What fails
- Kill 2 (4× grain size): F2 shift 43 Hz (< 200 Hz). FAIL.

## Root cause (honest negative)
The prereg hypothesized: "larger grains → formant smear → F2 shifts."
The evidence shows the opposite: F2 is stable (1825→1782 Hz, 43Hz)
across 1×, 4×, and 8× grain sizes. 

The hypothesis was BACKWARDS. In PSOLA, larger grains give BETTER
frequency resolution (longer analysis window), not worse. Formants
are spectral features; they don't "smear" with larger grains. The
temporal resolution worsens, but F2 (a frequency) is unaffected.

The kill bar was based on an incorrect mental model of PSOLA.
The fork itself is SOUND (passes all shared gates, kill 1 passes),
but the preregistered kill bar failed as specified.

## Per the task rules
"A failed per-fork kill bar kills the fork; do not ship that clip."
Kill 2 failed. Fork 2 does not survive. No clip shipped.

## Artifacts (committed for the record)
- `gu.zag` (source), `grain_full.wav`, `grain_frozen.wav`,
  `grain_big.wav` + SHAs. The full render passes gates and is
  archived as evidence of a working PSOLA engine, but NOT staged
  for the ear (per the kill rule).
