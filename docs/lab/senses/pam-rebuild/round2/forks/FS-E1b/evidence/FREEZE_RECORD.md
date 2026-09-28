# FS-E1b REGISTRY FREEZE RECORD

Freeze date: 2026-09-24 (UTC)
Prereg: round2/preregs/PREREG_FS-E1b.md (commit 8ed24934ecf018e28a683a7dd89a5a2fd16aa8d0, 2026-09-24)

## Parent
FS-E1 frozen registry: commit 9a8a68e4. FS-E1b changes exactly one quantity
(CH-CCN-3 -> CH-CCN-3r); `diff src/fse1b.zag` vs FS-E1 `src/fse1.zag` proves
only `cc_chal` (body), its comments, the t1 challenge-name string, and the
straw-alternative-audit line changed. All formations, all other challenges,
support rules, ledger, hash-chain, CLI modes: byte-identical logic.

## Frozen source
- src/fse1b.zag: sha256 9089c940169ae0c7ba6bc77d5abe976003e24fb4ad972edbc044140a24d6b2b1
- build/fse1b: sha256 ef5bb2dc0df14216008e14d2204b493041d454334460427b186280acade6bb24
  (binary is a build artifact; never committed)

## Frozen challenges
- colordisc: CH-COL-1 (FS-E1 verbatim)
- colorconst: CH-CCN-3r (FS-E1b REPAIRED: per-pixel RGB-L1 > 16 between the
  two d65 G views; DIFFERENT iff some 2x2 window holds >= 3 marked pixels;
  stat1 = raw marked count, stat2 = best 2x2 window marked count)
- shapetrans: CH-SHP-2 (FS-E1 verbatim)
- pitchdisc: CH-PTC-1 (FS-E1 verbatim)
- timbredisc: CH-TBD-2 (FS-E1 verbatim)
- motiondir: CH-MOT-2 (FS-E1 verbatim)

## Pre-freeze gate status (per frozen prereg)
The prereg freezes the registry when the design-loop CP returns zero kept
families at BOTH seeds (20260923 untuned, 20260924 defect-regression).
Both returned zero:
- colorconst seed 20260923: 5000 candidates, 0 kept
- colorconst seed 20260924: 5000 candidates, 0 kept
- regression: the 3 known kept fixtures now yield outcome=DIFFERENT
  (correct vs truth); formation still claims SAME -> WITHHOLD, not kept.
- differential validation: 30/30 fse1b outcomes match the independent Python
  reference implementation of the repaired rule.
Iteration count: 0 (rule as preregistered; no parameter iterations needed).
REGISTRY FROZEN. No further changes to fse1b.zag challenges.

## Post-freeze plan (per prereg)
1. Fresh post-freeze CP: 5000 colorconst candidates, seed 20260925 (bar c).
2. Formal battery: 10,000 R2A adversarial + 2,000 R2A controls (R2-16 frozen
   lists, same as FS-E1), each run TWICE byte-identically.
3. Score joint bars (a)-(e).
4. Commit evidence + VERDICT_FS-E1b.md (no binaries, no .zagd).
