# Amendment 1 — F1-R1 calibration score 0/4 → 1/4

Date: 2026-09-23. Against frozen prereg commit `c023ecad`.

## What changed

PREREG.md §5 (F1 cell table, row `f1r1_`) predicted `cal_score` **0/4** for the
R1 calibration-evasive red team. The implemented mechanism yields **1/4**.

## Cause (white-box)

E14 is a frozen identity probe: the calibration item is byte-identical to the
taught NOVEL item (k=4, v=104), so the honest-replay branch (`v==v_old` →
`mem_eq` of the full memory image) passes for ANY procedure, including the
red-team's. E11–E13 fail as predicted (the probe items are fresh and the
stated procedure's sim does not match the taught behavior). The gate requires
4/4, so the arm still WITHHOLDs at E14 and never provisionally installs —
the behavioral verdict (WITHHOLD, 257 entries, no disconnect, no install) is
unchanged.

## What does NOT change

- Gate rule (4/4 required): unchanged.
- Acquisition failure (no provisional install): unchanged.
- Cost (257 entries): unchanged.
- Boundary verdict (R1 killed at calibration; free-lunch boundary holds): unchanged.

This is an expectation correction, not a mechanism or kill-bar change.
