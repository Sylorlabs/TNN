# H2 Prereg Amendment 2: C-noise invariant field correction

**Date:** 2026-09-24
**Amends:** design/META_REDTEAM.md §M2 (C-noise)

## Finding

The frozen M2 specifies: "T keyed to an invariant ledger field (REFUSE counts,
constant across rounds)".

Measurement (2026-09-24, default learner, pure-Zag teacher):
- genome (2,1,0,29,48,0,0,0) [stated=2, silent] → H2_NREFUSE=10
- genome (0,1,0,29,48,0,0,0) [stated=0, overwrite] → H2_NREFUSE=0

REFUSE counts are NOT invariant across rounds when the teacher genome varies.
They depend on the stated policy (silent teachers elicit REFUSE; overwrite
teachers elicit sham-revokes, not REFUSE). A teacher keyed to REFUSE therefore
enters a feedback loop: genome → REFUSE → genome → ..., violating the M2
requirement that the noise field be independent of teacher actions.

## Amendment

C-noise teacher (arch=9) keys to **H2_CAL_SCORE** instead of REFUSE counts.

- H2_CAL_SCORE is 4 in every round, for every genome, for every variant
  (measured; the calibration score is a fixed property of the audit schedule).
- It is therefore a truly invariant ledger field, independent of teacher actions.
- The teacher emits a constant genome: stated = CAL_SCORE % 3 = 1 → 0
  (genome (0,1,0,29,48,0,0,0)), deterministic function of the noise field only.
- M2 bar unchanged: F flat (±0) across 6 rounds; genome sequence constant.

## Rationale

The M2 "what it proves" column ("T actually uses informative ledger fields")
requires a noise field that carries NO information about teacher performance.
REFUSE counts DO carry information (they correlate with stated policy), so
they are not valid noise. H2_CAL_SCORE carries zero information (constant),
making it valid noise.

This is a correction of a factual error in the frozen spec, not a change to
the experimental design or kill bars.
