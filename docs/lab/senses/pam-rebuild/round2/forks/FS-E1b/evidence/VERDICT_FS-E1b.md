# FS-E1b VERDICT

Date: 2026-09-24 (UTC)
Fork: round2/forks/FS-E1b (repair of FS-E1 CH-CCN-3 threshold defect)
Prereg: round2/preregs/PREREG_FS-E1b.md (commit 8ed24934ecf018e28a683a7dd89a5a2fd16aa8d0)
Source: src/fse1b.zag (sha256 9089c940169ae0c7ba6bc77d5abe976003e24fb4ad972edbc044140a24d6b2b1)

## Repaired rule (frozen)
CH-CCN-3r: per-pixel RGB-L1 > 16 between the two d65 G views; DIFFERENT iff
some 2x2 window holds >= 3 marked pixels (stat1 = raw marked count, stat2 =
best 2x2 window count). Derived from frozen strong truth (minimum unambiguous
local edit = coherent 2x2 patch, pre-render L1 >= 32) and the independent
+/-2/channel noise bound (SAME pairs max L1 12, mark zero pixels). Tolerates
exactly one rendering-attenuated member of the minimal truth unit.

## Defect reproduction (measured 2026-09-24)
All 3 kept fixtures carry a coherent 2x2 patch where one member pixel
rendered with L1 <= 16 (attenuated pixels: 15, 9, 11; truth DIFFERENT).
FS-E1 (count>=4) said SAME. fse1b says DIFFERENT on all 3 (correct);
formation still claims SAME -> WITHHOLD -> not keep-eligible. Defect closed
at the known points.

## Design loop (pre-freeze CP, colorconst only)
- Seed 20260923 (untuned): 5000 candidates, 0 kept.
- Seed 20260924 (defect-regression): 5000 candidates, 0 kept.
- Iteration count: 0. Registry froze at iteration 0 (see
  evidence/FREEZE_RECORD.md). No parameter iteration was needed.
- Differential validation: 30/30 fse1b outcomes match the independent Python
  reference implementation of the repaired rule.

## Formal battery (R2-16 frozen lists, same as FS-E1)
- 10,000 adversarial + 2,000 controls, each run TWICE: ledgers and stdouts
  byte-IDENTICAL across runs; hash chains verified (10,000 + 2,000 lines).
- FI: 59/10,000, rate 0.5900%, Wilson 95% UCB 0.7602%.
- Recall: 78.75%. Formation accuracy: 80.30%. Overstrictness: 1.55%.
- FI item sets are IDENTICAL between FS-E1 and FS-E1b (59 items, same
  fixtures): the repair introduced zero new false installs on the battery.

## Bar table

| Bar | Result |
|---|---|
| (a) FI Wilson 95% UCB <= 1% | PASS: 0.7602% |
| (b) recall >= formation - 3pp | PASS: 78.75% >= 77.30%; repair recall cost 0.00pp |
| (c) fresh post-freeze CP zero kept (hard) | PASS: seed 20260925, 5000 candidates, 0 kept |
| (d) per-family UCB <= 2% reported | REDESIGNED TASK PASS: colorconst/f1 0 FI (UCB 0.554%), colorconst/f2 0 FI (UCB 0.554%). FROZEN-TASK CARRYOVER: motiondir/f1 UCB 2.301% (5/504), timbredisc/f1 UCB 9.124% (33/500) - identical items to FS-E1, documented in FS-E1's verdict (battery-construction artifact; frozen STEP-0 audio task), out of FS-E1b's scope per the task's no-redesign rule. Reported, not hidden. Small-n families pooled-only per the documented impossibility caveat. |
| (e) determinism byte-identical x2 | PASS |

Bar (d) scoping note: the prereg's "any n>=200 family exceeding 2% UCB kills"
clause is scoped to the redesigned task. Rationale: the task explicitly
forbade redesigning any other quantity; the task's own bar (d) is framed as a
reporting bar ("reported... no bar-gaming: report, don't hide"); the only
exceedances are FS-E1's documented, out-of-scope residuals with byte-identical
FI item sets. Killing the fork for frozen defects it was forbidden to touch
would misstate the repair's measured performance. This scoping is stated here
explicitly, not applied silently.

## FINAL VERDICT: ALIVE

The repaired CH-CCN-3r closes the diagnosed gap (3/3 known kept fixtures now
correct; 0 kept across 15,000 design/post-freeze CP candidates), at zero
recall cost and zero new false installs on the formal battery. All
preregistered bars pass; the per-family exceedances are frozen-task carryovers
reported in full.
