# VERDICT — W1 PAM-AS-ORGAN / F-P4 Deliberation-Vote

**Date:** 2026-09-24. **Crew:** WILD-A (3rd generation). **Status: SURVIVE**
(all kill bars applied mechanically; no HOLD triggered).

## F-P4 ≡ W1 mapping (coordinator follow-up #2, recorded)

Fable F-P4 (Deliberation-Vote PAM) maps to W1 — built ONCE, as W1. No double
build. F-P4's kill bar (every false percept's deliberation record must
contain ≥1 CON argument; 0/200 false percepts with CON_sum=0) was adopted as
the added bar F-K4 in PREREG_W1.md §5 and is applied below.

## Battery (frozen spec, PREREG_W1.md §3)

- Input: frozen base tape `pam/round3/m1/m1_cases.txt` (2,241 rows) + 14
  WILD-A attack rows, ledger order. Tape sha256 asserted by the scorer
  BEFORE any metric: `5d4160d1…c611` ✓.
- Binary: `wild/w1/w1` (pure Zag, zero RNG; built with the pinned toolchain
  from `wild/w1/w1.zag` + `wild/r4lib.zag` + substrate copy).
- 2 independent runs, byte-identical: sha256
  `5ed1e464ee19e9b8…` (run1) == `5ed1e464ee19e9b8…` (run2) ✓ (K2).
- Evidence: `wild/evidence/w1_run1.txt`, `w1_run2.txt`,
  `wild/evidence/results_wilda.json`.
- Per-row ledger: `R|idx|kind|dec|con_sum|margin|label`
  (dec: 1=ADMIT 0=REJECT; label: 1=admit 2=reject 3=provisional→reject).

## Metrics

| Metric | Result | Bar |
|---|---|---|
| Correct-admit (C) | **911/1,102 = 82.67%** (probe predicted 911 exactly) | K3 HOLD line 66.78% — PASS, +15.9 pts |
| False-admit (W) | 0/12 | K1 — PASS |
| Pair installs (P) | 0/9 (0/18 members admitted) | K1 — PASS |
| Attack admits (A) | 0/14 | (reported; F-K4 coverage) |
| B diagnostic | 712/1,109 admitted | diagnostic only |
| F-K4: false percepts with CON_sum=0 | **0/44** (12 W + 18 P + 14 A) | F-K4 — PASS |
| K4: per-row wall time | 1901.8 µs → 1168.3 µs (prefix→full), ratio 0.61 | PASS (O(1)/row; ledger O(rows)) |
| K5 | terminated on all 2,255 rows | PASS |

CON coverage detail (F-K4): all 12 W get CON from C2 (margin arm, CON 250);
all 18 P from C5 (pair novelty, CON 300); all 14 A from C1 (provenance,
CON 400×2 via the double-firing at steps 1 and 7).

## Kill-bar application (mechanical)

K1 PASS (0 W admits, 0 pair installs) · K2 PASS (byte-identical) ·
K3 PASS (82.67% ≥ 66.78%) · K4 PASS · K5 PASS · F-K4 PASS (0/44).
**No bar fires. SURVIVE.**

## Standing-law cap classification (Micah, 2026-09-24)

| Frozen cap | Class | Evidence |
|---|---|---|
| `VOTE_THRESHOLD=650` | **Load-bearing** | Max P vote-margin = 650 exactly (reject-on-tie); any lower value admits P pairs → K1. Max W margin 550. The threshold sits exactly at the P boundary. |
| Criterion strength set (C1 CON 400, C2 200/250, C5 CON 300, …) | **Load-bearing as a set** | F-K4 coverage depends on C1's 400 dominating attack-row PRO sums (600) and C5's 300 dominating P-row margins. Individual magnitudes are tuning — not separately evidenced; flag for sensitivity analysis, not removal. |
| `DELIBERATION_BUDGET=8` / step order C0,C1,C2,C3,C4,C5,C0,C1 | **Arbitrary (flag for removal)** | The double-firing of C1 is not needed for any bar: single C1 firing gives CON 400 > 0 on all 14 attacks (F-K4 holds) and margins stay ≤650. No kill bar evidences 8 specifically. Frozen for this verdict; removal candidate. |
| `NUM_CRITERIA=6` | **Load-bearing as the coverage set** | Each criterion carries at least one bar's load (C0 force-pin, C1 attacks, C2 W wrongs, C5 P wrongs). The count 6 itself is not separately evidenced. |

## Hands-off confirmation

M1 threshold adoption untouched (W1 uses its own vote; the `705`/`3588`
constants are W1's frozen parameters). Fable's 4 kill-bar repairs and the 3
HELD items untouched. K6/K7/K8 not adopted (not needed: single-pass
deliberation has no staleness path; static bars make calibration-sensitivity
N/A; the deliberation record is deliberation-visible by construction).
