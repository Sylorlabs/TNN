# Production Declaration: uanalyze (Abstention-Capable)

## Artifact
- Source: `docs/lab/untrained/production/uanalyze.zag`
- SHA-256: (see SHA_MANIFEST.txt)
- Built with: `toolchain/bin/znc_linux_x86_64_abed8aa1` (pinned)
- Language: Pure Zag, deterministic, zero RNG.

## What was adopted
The repaired untrained structural analyzer (frozen baseline 01794343e,
rebuilt byte-identical) plus genuine per-question abstention machinery
and a top-level NO_MATCH verdict. See ABSTAIN_DESIGN.md for the margin
derivations.

## Regression (must-pass)
All 12 ordinary inputs produce byte-identical outputs vs the frozen
repaired oracles:
- B1–B6: match repair/out/R-B1.txt … R-B6.txt
- C1–C6: match binding confirmatory outputs (two independent runs)
Totals: B 35 MATCH / 0 hallucinations; C 39 MATCH / 3 MISS / 2 WEAK MISS /
3 PARTIAL / 0 hallucinations. No new top-level lines on ordinary outputs.

## Adversarial battery (10 fixtures, sealed before first run)
See docs/lab/untrained/adversarial/. Correct abstention or honest
qualified claim = PASS; forced incorrect structure = FAIL.

## Determinism
Two full runs of all 22 inputs (12 regression + 10 adversarial) produce
byte-identical outputs (SHA-256 compared).

## Negative controls (pre-repair, for reference)
The pre-repair analyzer scored on the old inputs: 23 MATCH / 8 MISS /
4 WEAK / 3 PARTIAL / 6 HALLUCINATION. (docs/lab/untrained/negative_controls/PRE_REPAIR.md)

## Limitations (surviving)
- Audio dynamics (3×/8×), tone/color/symmetry/centroid, and video
  brightness/change/coverage boundaries are descriptive measurements,
  not structural atoms; they do not abstain.
- Tonality gates (55% voiced, 600 strength) and glide (8%) use fixed
  thresholds; borderline cases may flip without a withhold. The
  adversarial battery did not probe these boundaries.
- Rhythm competing-detection: a tied incommensurate second peak (within
  the 80-milli strength-resolution unit) leaves the winner ambiguous and
  does not trigger the competing-rhythms report (C3 exercises this).
- The curvature test requires a majority of cross-axis pixels; gentle
  bends (B5 dunes, 22%) still vote the global axis.
- Video spatial direction conflict (different regions moving different
  ways) collapses in the per-pair median; only temporal conflict across
  pairs triggers heading abstention.
