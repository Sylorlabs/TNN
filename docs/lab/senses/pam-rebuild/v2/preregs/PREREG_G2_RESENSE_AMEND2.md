# PREREG AMENDMENT 2 — fixed thresholds for color tasks (r2a unusable)

**Date:** 2026-09-24 (before any formal G2 run)
**Reason:** The frozen calibration procedure assumed r2a fixtures supervise
threshold learning. For color tasks they do not:

- Organ 1 (frozen V2-D first organ) scores 51.0% on r2a colordisc and 51.7% on
  r2a colorconst (from sweep.jsonl) — essentially chance. The r2a color
  fixtures are not a usable training signal for ANY organ.
- r2a colorconst has only ONE class (all 680 on-disk fixtures are SAME_SURFACE).
- Calibration consequently degenerated: colordisc T=0 (constant DIFFERENT),
  colorconst T=1145 (unvalidated single-class).

A constant-DIFFERENT organ 2 would be a degenerate second organ (it cannot
exhibit judgment-blindness in Part 4 — it never moves). The hypothesis under
test is a WORKING second organ, so the training set — not the hypothesis —
is at fault.

**Amendment (frozen):** For colordisc and colorconst, replace learned
thresholds with fixed a priori constants (not optimized on the battery set):
- T_col = 20 (RGB euclidean distance on 0..441 scale; <20 = noise/same)
- T_cc = 100 (per-mille chromaticity distance; <100 = same surface)

These are round numbers in the plausible range, chosen WITHOUT searching the
battery trials. The battery (Parts 1–4) adjudicates whether they work.
Timbredisc keeps its calibrated boundaries (B1=2,B2=77,B3=267, 89.2% train).

**Unchanged:** hypothesis, install rule, kill bars, determinism, all procedures.
