# QUARANTINE PROPOSAL: R2A-CCN-2 (mixed-illuminant color constancy) fixtures

**Date:** 2026-09-23. **Crew:** PAMs v2 gap crew D (calibration claim + benchmark integrity).
**Status:** PROPOSAL ONLY. No fixture, truth file, verdict, or manifest has been
modified. Fixture changes require Micah's prereg amendment; this document is the
evidence package for that decision.

## Claim under test

The autopsy death-board (v2/autopsy/AUTOPSY_DEATHBOARD.md) claims: "338/340
CCN-2 fixtures mislabeled. Truth says SAME_SURFACE; the pixels are different
photos (corr 0.3–0.8). Front end correctly judged DIFFERENT."

## Finding: CONFIRMED — 340/340 mislabeled

All 340 fixtures of family R2A-CCN-2 (`r2a_colorconst_0340.img` …
`r2a_colorconst_0679.img`, listed in `round2/fixtures/FAMILIES.tsv`) carry
`truth=SAME_SURFACE`. Measurement shows **none of them depict the same
surface**:

1. **Panel correlation (340/340):** Pearson correlation between the left and
   right 64×64 panels (all RGB samples). 323/340 have corr < 0.9 (min −0.48,
   p5 0.03, median 0.48) — the range the death-board reported (0.3–0.8) for
   different photos. For reference, the generator's *intended* design ("same
   crop, same spatial illuminant gradient on both panels") would produce
   near-byte-identical panels (corr ≈ 1.0).
2. **Shift-alignment test (17/17 high-corr fixtures):** for the 17 fixtures
   with corr ≥ 0.9, a ±32px shift search found NO alignment: the best shift
   is at the search boundary for all 17, and rmse at (0,0) is 4.3–38.2.
   Control: 10 known same-crop fixtures (r2n_colorconst even idx) align
   exactly at (0,0) in 9/10 cases; 10 known different-photo fixtures align
   nowhere (best at boundary, rmse 42–84). The 17 behave like the
   different-photo controls.
3. **Affine-fit residual:** per-channel affine fit p2 = a·p1 + b (the correct
   model for same-crop under a different global illuminant) leaves mean RMSE
   1.1–14.6 on the 17 — overlapping the known-same-crop control range, so
   not decisive alone; the shift test is decisive.

The death-board's "338/340" vs this measurement's "340/340": the 2-fixture
gap is a threshold artifact (their correlation cutoff vs mine). No fixture
survives the same-crop test. Substance fully confirmed.

## Root cause (generator)

`round2/fixtures/gen_r2a.py`, `gen_colorconst_adv`, R2A-CCN-2 branch
(idx ≥ 340): the committed fixtures were generated with
`truth=SAME_SURFACE` for all 340 while the two panels were rendered from
**different photos** (the `_colorconst_panels` DIFFERENT path: two distinct
photo/crop selections), or at minimum different crops — in no case the same
surface region. Note the current `gen_r2a.py` on disk cannot even reproduce
these fixtures (CCN-2 calls `_colorconst_panels` with a single illuminant,
which would loop forever on `while i2 == i1`, and would alternate truth by
idx parity) — the committed fixtures predate the current generator.

## Impact

- R2-10's 32 CCN-2 "false installs" are not safety failures: the front end
  judged DIFFERENT on stimuli that ARE different. (Death-board §R2-10.)
- R2-2's 25 CCN-2 false installs are likewise suspect (death-board notes the
  raw illuminant-asymmetry signal was in the fixtures).
- Any bar, verdict, or gate-discipline count that includes CCN-2 fixtures is
  computed against wrong ground truth.

## Proposed quarantine list

**Quarantine all 340 fixtures:** `r2a_colorconst_0340.img` through
`r2a_colorconst_0679.img` (inclusive), i.e. every row of FAMILIES.tsv with
family `R2A-CCN-2`, plus their `.truth` files. Do not delete; mark
quarantined in the manifest and exclude from all future batteries until
Micah approves a relabel-or-regenerate amendment.

Fixture-level evidence table: `ccn2_evidence_table.csv` (340 rows: fixture,
truth, panel correlation, per-channel mean illuminant differences, finding).

## What this proposal does NOT do

- Does not modify any fixture, truth file, verdict, or manifest (frozen).
- Does not relabel anything (relabeling requires Micah's prereg amendment).
- Does not claim anything about CCN-1 (extreme-illuminant) fixtures — those
  were separately verified as correctly labeled (death-board §R2-10:
  texcorr median 0.9989 on fooled fixtures).
