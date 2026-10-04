# PREREG AMENDMENT 1 (pre-run correction, no scores seen)

Date: 2026-09-27. Status: committed before any baseline or variant run.

## What was wrong in PREREG_LIGHT.md Section 5

Section 5 states the skycrop battery image is "fully supported by the
committed binary" at 512x256 (input 256x128). This is factually wrong:
azupscale.zag hardcodes input dimension guards (`need w=256`,
`need h=92`; source lines ~554-555). A 256x128 input would be refused.
No runs have happened; no scores have been seen; this amendment corrects
the protocol before any evidence exists.

## Corrected Section 5 (replaces the skycrop paragraph)

- skycrop: rows 0..183 of
  docs/lab/image_upscale/generation/run_sky_1/gt.bmp (a real photo),
  i.e. a 512x184 crop, prepared by azcrop.zag (crop, then the documented
  2x2 box downscale to input_256x92.bmp). The top 184 rows are the
  gradient-dominant sky part of the frame, which is where the
  mechanism's claim applies. The crop rows are frozen here, before any
  run. The 512x184 / 256x92 dimensions exactly match the committed
  binary's hardcoded protocol, so the baseline and variant run
  unmodified; the 8x4 tile scoring grid is exactly valid.
- Rationale for the change (recorded, not tuned): the committed binary
  cannot be modified for the battery without weakening the
  no-regression comparison, so the battery image is sized to the
  binary's frozen protocol instead.

## What is unchanged

Sections 1, 2, 3, 4, 6, 7, 8 stand as frozen. The mechanism, estimator,
construction change, bars, void conditions, and judge rule are
untouched. The battery is still {sealed, skycrop}; only skycrop's
dimensions changed (512x256 -> 512x184, rows 0..255 -> rows 0..183).
azcrop.zag is updated to match (crop 512x184, downscale to 256x92);
its box filter is unchanged.
