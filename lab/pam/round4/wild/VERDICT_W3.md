# VERDICT — W3 VETO-ONLY PAM

**Date:** 2026-09-24. **Crew:** WILD-A (3rd generation). **Status: SURVIVE**
(all kill bars applied mechanically; no HOLD triggered).

## Battery (frozen spec, PREREG_W3.md §3)

- Input: frozen base tape (2,241 rows, sha `5d4160d1…c611` asserted ✓) +
  14 attack rows, ledger order.
- Binary: `wild/w3/w3` (pure Zag, zero RNG).
- 2 runs byte-identical: sha256 `8b1f28967b5f1a34…` == `8b1f28967b5f1a34…` ✓.
- Evidence: `wild/evidence/w3_run1.txt`, `w3_run2.txt`.
- Per-row ledger: `R|idx|kind|dec|bar|veto`.

## Metrics

| Metric | Result | Bar |
|---|---|---|
| Correct-admit (C) | **910/1,102 = 82.58%** (= M1 rate; vetoes fire on 0 C rows) | K3 — PASS |
| False-admit (W) | 0/12 (bar rejects all; mrgF < 3588) | K1 — PASS |
| Pair installs (P) | 0/9 (0/18 members) | K1 — PASS |
| Attack admits (A) | 0/14; **14/14 VETOED** (bar alone would admit all 14) | W3-A1 — PASS |
| Fork installs (FRK) | 0/3 | W3-A2 — PASS |
| B diagnostic | 712/1,109 | diagnostic only |
| K4 | per-row 129.0→213.0 µs, ratio 1.65 | PASS |
| K5 | terminated | PASS |

## Kill-bar application (mechanical)

K1 PASS · K2 PASS · K3 PASS (82.58%) · K4 PASS · K5 PASS ·
W3-A1 PASS (14/14 vetoed) · W3-A2 PASS. **No bar fires. SURVIVE.**

## Standing-law cap classification (Micah, 2026-09-24)

| Frozen cap | Class | Evidence |
|---|---|---|
| M1 bar as the admit path (`705`/`3588`) | **Load-bearing** | It IS the admit path; the 910/1102 rate is exactly the frozen M1 rate. (Used, not adopted — hands-off rule observed.) |
| V2 attack veto | **Load-bearing** | The ledger shows `bar=1, veto=1, dec=0` on all 14 attack rows: the bar alone admits every one. This veto is W3's entire raison d'être and it fires exactly as designed. |
| V1 pair veto | **Load-bearing (live defense-in-depth)** | Fires on 18/18 P rows; critically, 2 P members (tape rows 2233/2235, pairs 5 and 6) PASS the bar and are vetoed only by V1. Without V1, p_member_admit=2. Not decorative. |
| Veto-PAM output alphabet {VETO, ABSTAIN} | **Load-bearing (structural)** | A veto-only PAM cannot cause a false-admit by construction; the evidence (0 wrongs admitted) is consistent, and the structure is what makes W3-A1 a veto-coverage claim rather than a threshold claim. |

## Hands-off confirmation

M1 bar used, not adopted or recalibrated (no strong/agree change).
No fable repairs, no HELD items. K6/K7/K8 not adopted (no staleness /
calibration / classification surface).
