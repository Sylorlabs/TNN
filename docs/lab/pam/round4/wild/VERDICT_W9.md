# VERDICT — W9 RENDER-PAM (reconstruction-fidelity gate)

**Date:** 2026-09-24. **Crew:** WILD-A (3rd generation). **Status: SURVIVE**
(all kill bars applied mechanically; no HOLD triggered).

## Construction audit (PREREG_W9.md §3/§6 — blocked the battery)

`wild/w9/AUDIT_W9.md`: **PASS** before the battery ran. `render_conf` and
`render_mrg` take exactly `(strong, agree)` — no `(conf, mrgF)` parameter,
no arena/global capture of the sensory buffer (zero references in the
function bodies; the single "conf" grep hit is the function's own name),
called only as `render_*(strong, agree)`. Prototypes are six integer
constants — no compressed-copy smuggling. The fidelity comparison runs in
`main`, outside the renderer, matching the prereg's seal definition.

## Battery (frozen spec, PREREG_W9.md §4)

- Input: frozen base tape (2,241 rows, sha `5d4160d1…c611` asserted ✓).
  Attacks out of scope (renderer is content-agnostic, per
  `TAPE_WILDA_ATTACKS.md`).
- Binary: `wild/w9/w9` (pure Zag, zero RNG).
- 2 runs byte-identical: sha256 `eb7934ad72d009a3…` == `eb7934ad72d009a3…` ✓.
- Evidence: `wild/evidence/w9_run1.txt`, `w9_run2.txt`.
- Per-row ledger: `R|idx|kind|dec|lhs` where admit iff `lhs =
  20·|conf−conf′| + |mrgF−mrgF′| ≤ 11000` (integer form of fidelity ≤ 0.55).

## Metrics

| Metric | Result | Bar |
|---|---|---|
| Correct-admit (C) | **829/1,102 = 75.23%** | K3 (HOLD at <66.78%) — PASS |
| Fidelity-pass (W) | 0/12 | K1 — PASS |
| Pair installs (P) | 0/9 (0/18 pass) | K1 — PASS |
| F1: M1-admitted trues admitted | **791/910 = 86.9%** (needs ≥85% = 774) | F1 — PASS, margin 17 rows |
| F2: frozen wrongs passing | **0** (needs ≤2) | F2 — PASS |
| B diagnostic | 679/1,109 pass | diagnostic only |
| K4 | per-row 650.6→973.2 µs, ratio 1.50 (renderer O(1)) | PASS |
| K5 | straight-line; terminated | PASS |

Threshold-margin detail: max admitted-C `lhs` = 10,979 vs threshold 11,000
(21 units of headroom); min rejected-C `lhs` = 11,109; max wrong `lhs` =
17,562 (far above the bar). The threshold sits in a narrow viable band —
see cap classification.

## Kill-bar application (mechanical)

K1 PASS (0 W pass, 0 pair installs) · K2 PASS · K3 PASS (75.23%) ·
K4 PASS · K5 PASS · F1 PASS (791 ≥ 774) · F2 PASS (0 < 3) · F3 PASS
(construction audit, pre-battery). **No bar fires. SURVIVE.**

## Standing-law cap classification (Micah, 2026-09-24)

| Frozen cap | Class | Evidence |
|---|---|---|
| `FIDELITY_THRESHOLD=0.55` | **Load-bearing — and brittle** | F1 clears by only 17 rows (791 vs 774); the prereg's sensitivity note puts 2 wrongs passing at 0.56 (F2 boundary). The threshold sits in a narrow viable band with thin margins on BOTH sides. Load-bearing, flagged as brittle: a small tape-distribution shift could break either F1 or F2. |
| Three prototypes (850,15000)/(750,8000)/(720,2000) | **Load-bearing** | They are the gate's mechanism — trace-conditional constants, audited non-smuggling. |
| Normalizers 1000/20000 | **Arbitrary but harmless (flag)** | Pure scaling; any consistent scaling with a rescaled threshold is equivalent. Not load-bearing, no removal urgency. |

## Hands-off confirmation

No M1 adoption/recalibration. No fable repairs, no HELD items. K6/K7/K8 not
adopted (straight-line renderer; no staleness / calibration /
classification surface).
