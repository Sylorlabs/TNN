# DOUBLE_COUNT_NOTE.md — `killed_rightimp` metric defect and repair

Date: 2026-09-20. Status: **APPLIED (REPAIR).** Found by the trial closer
during evidence review, before the checker ran on the full cell set.

## The defect

In `felt_trial_v3.zag`, `record_kill()` (line 278) increments
`killed_rightimp` once for every class-1 (right-important) kill — and then
three of its four call sites increment it **a second time**:

- line 408 → 409 (Gate-1 evidence-gated kill path)
- line 449 → 450 (F-arm deliberate sacrifice path)
- line 504 → 505 (N-arm deliberate sacrifice path)

The fourth call site (line 722, mandatory-revision kill path) does not
re-increment. So the emitted `FELT_METRIC,killed_rightimp` equals
2×(Gate-1 + sacrifice class-1 kills) + 1×(revision class-1 kills) — an
inconsistent double count, not the prereg's F_wbs numerator. In F v0 it
reads 284 where the true class-1 kill count is 142.

## Why it matters

K1 and K4 both consume F_wbs = killed_rightimp / admitted_right_imp.
Doubling (inconsistently) the numerator inflates |F_wbs(F)−F_wbs(N)| and can
flip kill criteria. The metric as emitted does not implement the prereg
definition (V3 §10: right-important wrongly killed / right-important
admitted).

## The repair (implementer-residue bug, not a prereg change)

`kill_c1` is incremented exactly once per class-1 kill, inside
`record_kill()` alone (line 282) — it is the clean, correct numerator and
is present in every already-emitted cell output. No cell is re-run; the
ledgers are intact and the evidence supports the correct computation.

- `check_felt_v3.py` `metrics_of()`: F_wbs now uses `kill_c1` instead of
  `killed_rightimp`, with a code comment citing this note. The checker
  implements the prereg definition; the driver bug is not propagated.
- The raw `killed_rightimp` lines remain in the cell outputs, unedited, as
  evidence of the defect.

No frozen bar, formula, threshold, schedule, or kill criterion was touched —
only which emitted counter implements the prereg's F_wbs definition.
