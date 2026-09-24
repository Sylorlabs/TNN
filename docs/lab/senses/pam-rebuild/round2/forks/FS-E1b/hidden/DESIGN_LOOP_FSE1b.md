# FS-E1b design-loop log (pre-freeze CP iterations)

Repair: CH-CCN-3 -> CH-CCN-3r (2x2 window with >= 3 pixels of per-pixel
RGB-L1 > 16 between the two d65 G views; DIFFERENT iff such a window
exists). Source: `src/fse1b.zag` (diff vs FS-E1 `fse1.zag` proves only
`cc_chal` + name/comments/audit-string changed). Binary `build/fse1b`.

## Iteration 0 (2026-09-24): repaired rule as preregistered
- Design-loop CP: colorconst, budget 5000 candidates, seeds 20260923
  (untuned) and 20260924 (defect-finding seed; regression).
- Regression check: the 3 known kept fixtures (FS-E1
  `fixtures_cp/cp_colorconst_{0,1,2}.r2fx`) through the new binary.
- Differential validation: `fse1b` outcome vs independent Python reference
  on 30 real CP candidates (2x2-window scan, >=3 rule, CH-CCN-3r name).

(results below)

## Iteration 0 results (2026-09-24)
- Differential validation: 30/30 `fse1b` outcomes match the independent
  Python reference (2x2-window scan, >=3 rule, CH-CCN-3r name). Zag
  implementation correct.
- Regression check: the 3 known kept fixtures now yield
  outcome=DIFFERENT (correct vs truth=DIFFERENT); formation still claims
  SAME_SURFACE -> disposition=WITHHOLD -> not keep-eligible. Defect killed
  at the known points.
- Design-loop CP seed 20260923 (untuned): 5000 candidates, **0 kept**.
- Design-loop CP seed 20260924 (defect-finding seed; regression): 5000
  candidates, **0 kept** (2026-09-24).
- DESIGN-LOOP COMPLETE at iteration 0: zero kept at both seeds, no parameter
  iterations needed. The rule form (coherent minimal-edit count) stands as
  preregistered. REGISTRY FROZEN 2026-09-24 (see `evidence/FREEZE_RECORD.md`:
  source sha256 9089c940169ae0c7ba6bc77d5abe976003e24fb4ad972edbc044140a24d6b2b1,
  binary sha256 ef5bb2dc0df14216008e14d2204b493041d454334460427b186280acade6bb24).
