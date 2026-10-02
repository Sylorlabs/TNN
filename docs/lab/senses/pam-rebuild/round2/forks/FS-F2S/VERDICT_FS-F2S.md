# VERDICT_FS-F2S — shapetrans formation improvement — 2026-09-24

## FINAL: ALIVE

Applied mechanically from the frozen prereg
(PREREG_FS-F2S.md, commit `1259d595c29c5daf532b4193f4c6a9dbd1698c5e`;
amendment PREREG_FS-F2S_AMENDMENT.md, commit
`2ffba7a05b4c3a88eb700f15552ac0c1b3c22912`).

## Phase-0 diagnosis (white-box, pre-freeze)

FS-E2's `f_shapetrans` classified via thresholded foreground bounding-box
fill ratio (CIRCLE >= 700, SQUARE 550-699, TRIANGLE < 550 on a /1000
scale). Measured fill ranges: CIRCLE 750-825, TRIANGLE 461-548,
SQUARE 499-1000 (median 588) — rotation-variant for squares, so rotated
squares crossed both the circle and triangle bins. Truth-to-prediction
breakdown on the 1296 Phase-0 controls: CIRCLE 432/432, TRIANGLE 432/432,
SQUARE 180/432 (113 -> CIRCLE, 139 -> TRIANGLE); total 1044/1296 = 80.56%.

## Improved rule (frozen, integer-exact)

Normalized second central moment `phi1 = (mu20 + mu02) / mu00^2` over
pixels > 180, computed as `t5 = floor((m00*q - sx^2 - sy^2) * 100000 /
m00^3)`; `m00 < 200` -> SQUARE; `t5 < 16218` -> CIRCLE;
`16218 <= t5 < 17798` -> SQUARE; else TRIANGLE. Pure Zag; the other five
formation functions are FS-E2's logic unchanged.

## Results

- Bar (a) shapetrans, fresh deterministic draw (n=1296, R2-7 generator,
  indices 5000-6295, 432/432/432): **1296/1296 = 100.00%** (0 errors)
  >= 85% -> PASS
- Bar (b) no regression: colordisc 1004/1080 = 92.96% (>= 91.96%),
  pitchdisc 705/720 = 97.92% (>= 96.92%), motiondir 545/564 = 96.63%
  (>= 95.63%) — all exactly FS-E2's Phase-0 levels -> PASS
- Bar (c) two complete runs byte-identical (all 5 TSV pairs `cmp`-equal)
  -> PASS

FINAL: **ALIVE** — the improved shapetrans formation rule earns FS-E2 scope.

## Evidence committed

- `src/fsf2s_form.zag` (improved formation, pure Zag),
  `src/R33_NATIVE_IO_V1.zag` (substrate),
  `src/gen_fresh_shapetrans.py`, `src/run_eval.py`, `src/score_f2s.py` (glue)
- `lists/`: the five eval fixture lists
- `evidence/eval/`: ten run TSVs (r1/r2 x 5 sets), `EVAL_REPORT.md`,
  `fresh_shapetrans_MANIFEST.sha256` (2592 fixture + truth hashes)
- Binary and `.zag-cache/` excluded per lab policy. The 2592 fresh-draw
  fixture files are not committed: they regenerate byte-identically from
  `src/gen_fresh_shapetrans.py` + the frozen R2-7 generator (proven by
  independent regeneration + byte-compare of indices 5000/6295) and are
  covered by the committed manifest.
