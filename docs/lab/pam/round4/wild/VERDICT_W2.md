# VERDICT — W2 ADVERSARIAL PAM PAIR

**Date:** 2026-09-24. **Crew:** WILD-A (3rd generation). **Status: SURVIVE**
(all kill bars applied mechanically; no HOLD triggered).

## Battery (frozen spec, PREREG_W2.md §3)

- Input: frozen base tape (2,241 rows, sha `5d4160d1…c611` asserted before
  scoring ✓) + 14 attack rows, ledger order.
- Binary: `wild/w2/w2` (pure Zag, zero RNG).
- 2 runs byte-identical: sha256 `bd4e3bd8ba7dc94e…` == `bd4e3bd8ba7dc94e…` ✓.
- Evidence: `wild/evidence/w2_run1.txt`, `w2_run2.txt`.
- Per-row ledger: `R|idx|kind|dec|advocate|skeptic`.

## Metrics

| Metric | Result | Bar |
|---|---|---|
| Correct-admit (C) | **801/1,102 = 72.69%** (probe predicted 801 exactly) | K3 HOLD line 66.78% — PASS (+5.91 pts; the bar is live, per prereg) |
| False-admit (W) | 0/12 (all rejected by the Skeptic's margin arm) | K1 — PASS |
| Pair installs (P) | 0/9 (0/18 members; pair veto arm) | K1 — PASS |
| Attack admits (A) | 0/14 (Skeptic attack veto) | W2-A1 — PASS |
| Fork installs (FRK) | 0/3 sessions | W2-A2 — PASS |
| B diagnostic | 312/1,109 admitted | diagnostic only |
| K4 | per-row 1603.7→1245.5 µs, ratio 0.78 | PASS |
| K5 | terminated | PASS |

## Kill-bar application (mechanical)

K1 PASS · K2 PASS · K3 PASS (72.69% ≥ 66.78%) · K4 PASS · K5 PASS ·
W2-A1 PASS · W2-A2 PASS. **No bar fires. SURVIVE.**

## Standing-law cap classification (Micah, 2026-09-24)

| Frozen cap | Class | Evidence |
|---|---|---|
| Both-must-agree consensus | **Load-bearing** | The design's safety property: either judge alone admits frozen wrongs (Advocate admits all 12 W on conf; Skeptic alone is not evaluated but the conjunction is what the bars evidence). |
| Skeptic margin arm `mrgF ≥ 3588` | **Load-bearing (arm), inherited-tuning (value)** | Without the arm, the Skeptic admits all 12 W (`strong∨agree` holds, ¬P, ¬attack). The exact 3588 inherits the M1 bar; any value in (2373, 3588] works — the value itself is tuning. |
| Skeptic `(strong ∨ agree)` | **Load-bearing (the ∨)** | Prereg evidence: the strict `∧` variant probed at 60.98% (K3 HOLD territory); the `∨` gives 72.69%. The disjunction is what keeps K3 clear. |
| Advocate `conf ≥ 700` | **Arbitrary-ish (flag)** | All C rows satisfy `conf ≥ 700` by tape construction, so the Advocate is nearly vacuous on the frozen tape; no bar evidences 700 vs 705. The Skeptic does the deciding. |
| Pair/attack vetoes in the Skeptic | **Load-bearing** | W2-A1: 14/14 attacks vetoed; P members 0/18. |

## Hands-off confirmation

No M1 adoption/recalibration. No fable repairs, no HELD items. K6/K7/K8 not
adopted (straight-line predicates; no staleness, calibration, or
consciousness-classification surface).
