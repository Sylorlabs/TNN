# VERDICT — W6 ARGUING PAMS

**Date:** 2026-09-24. **Crew:** WILD-A (3rd generation). **Status: SURVIVE**
(all kill bars applied mechanically; no HOLD triggered).

## Battery (frozen spec, PREREG_W6.md §3)

- Input: frozen base tape (2,241 rows, sha `5d4160d1…c611` asserted ✓) +
  14 attack rows, ledger order.
- Binary: `wild/w6/w6` (pure Zag, zero RNG).
- 2 runs byte-identical: sha256 `db18b7fcc4c97adb…` == `db18b7fcc4c97adb…` ✓.
- Evidence: `wild/evidence/w6_run1.txt`, `w6_run2.txt`.
- Per-row ledger: `R|idx|kind|dec|initial_votes|post_persuasion_votes`
  (votes encoded Margin×100+Provenance×10+Confidence).

## Metrics

| Metric | Result | Bar |
|---|---|---|
| Correct-admit (C) | **917/1,102 = 83.21%** (probe predicted 917 exactly) | K3 — PASS |
| False-admit (W) | 0/12 | K1 — PASS |
| Pair installs (P) | 0/9 (0/18 members) | K1 — PASS |
| Attack admits (A) | 0/14 | W6-A1 — PASS |
| Fork installs (FRK) | 0/3 | W6-A2 — PASS |
| B diagnostic | 712/1,109 | diagnostic only |
| K4 | per-row 1808.6→1049.3 µs, ratio 0.58 (3 predicates + ≤3 flip checks) | PASS |
| K5 | one persuasion round; terminated | PASS |

## Kill-bar application (mechanical)

K1 PASS · K2 PASS · K3 PASS (83.21%, highest of the WILD-A survivors) ·
K4 PASS · K5 PASS · W6-A1 PASS · W6-A2 PASS. **No bar fires. SURVIVE.**

## Standing-law cap classification (Micah, 2026-09-24)

| Frozen cap | Class | Evidence |
|---|---|---|
| One bounded persuasion round | **Load-bearing** | Prereg negative result: static 2-of-3 voting (no persuasion) admits 12 W + 11 P → K1. The persuasion round is the difference between that KILL and this SURVIVE. |
| Strength order 3 > 2 > 1 (Margin > Provenance > Confidence) | **Load-bearing** | The W-row worked example requires Margin(3)'s rejection to persuade both weaker arguers; the P-row example requires Provenance(2) to persuade Confidence(1). The order is the mechanism. |
| Majority ≥ 2 of 3 | **Load-bearing (structure)** | With the strength order, majority is what lets Margin keep a lone ADMIT on P rows while still losing the vote — the design's signature behavior. |
| `N=3` | **Unevidenced value, load-bearing shape** | No N≠3 was tested; the odd-N majority shape is structural. Flag N=3's exact value for future variation, not removal. |
| Predicate constants (`3588`, `705`) | **W6's frozen parameters** | Not an M1 adoption (hands-off observed). The values are tuning; the arguers' single-lens structure is the design. |

## Hands-off confirmation

No M1 adoption/recalibration. No fable repairs, no HELD items. K6/K7/K8 not
adopted (no staleness / calibration / classification surface).
