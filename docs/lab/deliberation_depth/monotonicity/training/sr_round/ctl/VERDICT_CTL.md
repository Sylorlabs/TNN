# H5 SR-ROUND — Arm CTL Verdict (Yardstick)

- **prereg SHA256:** `f55d1dbbe1a609f69301ce8f537282a0372880b51fdec6b51d0f588b9fd96d30`
  (PREREG_SR.md FROZEN v1; verified byte-identical against cab05d07)
- **Arm:** CTL — control, NO training. Frozen v2-100× params
  (`training/v2/params/mt2_params_100x.zag`, SHA256
  `8c826a42cdac7ef942742816002a27fcdc6b6d8985ed7cb0eb47553c5643d8ec`)
  re-analyzed on the frozen 37-leg matrix with the frozen analyzer
  (`training/analyze.py`).
- **Method:** pure re-analysis, zero new runs. `analyze_ctl.py` execs the
  def-block of the frozen `training/analyze.py` verbatim (same TSV parsing,
  same `metrics_for_cells`/`g_curve` definitions — never retyped).
- **Reproduction cross-checks vs frozen `training/v2/VERDICT.md`:** ALL MATCH
  (script hard-stops on any mismatch):
  - mech 14 (m14): n10=0, V1=0, V2=44, Gviol=7 ✓
  - mech 4 (M4): n10=0, V1=0, V2=160, Gviol=14 ✓
  - per-family (V2, Gviol): revoke (0,0), logic (0,0), cost (0,0), trap (0,0),
    ceiling/D (0,0), admit (0,1), ceiling/O (0,2), ceiling/P (44,2),
    redteam (0,2) ✓
  - 37/37 m14 A/B leg pairs byte-identical (verified by `cmp` at runtime) ✓
- **Artifacts:** `analysis/ctl_curves.tsv` (per-(family,depth) G/acc/n/conf),
  `analysis/ctl_bars.tsv` (this table, machine-readable),
  `analysis/ctl_buildlog.txt` (input SHAs). Every file opens with the prereg SHA.
- **Status:** yardstick COMPLETE. CTL carries no falsification clause (§9):
  it is the baseline every other arm's delta is measured against.

## Verdict: PARTIAL — as expected (§9)

Genuine non-degenerate calibration on honest families; worst-case residual on
trap/O/redteam plus characterized admit underconfidence. No number disagrees
with the frozen v2 evidence.

## Kill-bar table B1–B13 (prereg §10, applied literally)

| # | Bar | Threshold | Result | Evidence |
|---|-----|-----------|--------|----------|
| B1 | §1 accuracy | n10 = 0 | **PASS** | n10 total = 0 |
| B2 | Theater | V1 = 0, V2 = 0 | **FAIL** | V1=0, **V2=44** (all ceiling/P; frozen v2 §4) |
| B3 | Law (strict) | Gviol = 0 every family | **FAIL** | 7 strict rises: admit=1, ceiling/O=2, ceiling/P=2, redteam=2; revoke/logic/cost/trap/D=0 |
| B4 | Non-degenerate | meanConfCorrect ≥ 0.50 | **PASS** | 0.746680 (n=4005) — matches v2's 0.747 |
| B4b | Honest-family floor | per honest family ≥ 0.50 | **FAIL** | admit 0.217430 (n=1240) FAIL; revoke 1.000000, logic 1.000000, cost 1.000000 PASS |
| B5 | Separation | ≥ 0.20 | **PASS** | 0.746680 − 0.313484 = 0.433196 (n_c=4005, n_w=462) — matches v2's 0.433 |
| B6 | Recall | ≥ 0.95 per family | **PASS** | 1.0000 on all 7 defined families; trap and ceiling/P vacuous (0/0 in both M4 and m14 — zero drift; B9 identity covers) |
| B7 | Abstention volume | ≤ 0.30 | **PASS** | 773/5240 = 0.147519 |
| B8 | G-flatness | defined ≥4/5 (≥5/7 ceiling); not all equal within 1e-3 | **FAIL** | admit/O/P PASS (non-flat); revoke/logic/cost/D FAIL on flatness clause; trap 2/4 defined, redteam 0/4 defined FAIL on count — see prereg-tension note |
| B9 | Answer channel frozen | 100% identity vs M4 | n/a-CTL | 5240/5240 release+correct identical (frozen v2 §8 check 8) |
| B10 | Disconnect real (s9) | — | n/a-CTL | SR-S9 only |
| B10b | Disconnect real (mask) | — | n/a-CTL | SR-S1 only |
| B11 | Post-release only | — | n/a-CTL | SR-S9/SR-S1 only |
| B12 | Refined reading | recorded | **RECORDED** | 4 G>0 crossings: ceiling/O×1 (d2→d4, −0.004→+0.000), ceiling/P×1 (d1→d2, +0.000→+0.996), redteam×2 (d1→d2 −0.333→+0.000, d4→d8 +0.000→+1.000); matches v2 §4 refined reading exactly |
| B13 | Underconfidence floor | G(F,d) ≥ −0.100, n_rel ≥ 8 | **FAIL** | min G = −1.000000; offenders: admit d1 −0.355, d2 −0.834, d4 −0.932, d8 −0.866, d16 −0.926 (n=248 each); ceiling/O d1 −1.000 (n=40) |

## Characterization (the yardstick's shape)

- **Law bars (B1–B3):** strict reading FAILED as preregistered (44 V2 + 7
  strict G-rises, all on adversarial families). Refined reading (B12): 4
  zero-crossings, all on O/P/redteam; honest families fully clean.
- **Non-degeneracy (B4/B5/B7):** comfortably PASS — the head is calibrated,
  not silent (meanConfCorrect 0.747, separation 0.433, abstention 14.8%).
- **Admit underconfidence (B4b/B13):** the head is strongly underconfident on
  admit (acc=1.000 at every depth, conf 0.645→0.066) — law-safe but
  calibration-poor; independently verified from raw TSVs (meanConfCorrect
  0.2174, n=1240). Matches v2 VERDICT.md §9.3.
- **Ceiling/P:** maximal overconfidence on wrong answers (G +0.996→+1.000,
  conf rising with depth → 44 V2) — the frozen residual.
- **Recall (B6):** release+correct identity vs M4 is exact (1.0000 every
  defined family; 0/0 vacuous on trap and ceiling/P with zero drift).

## Prereg-tension note (flagged for coordinator — NOT silently reinterpreted)

B8's vacuity guard, applied literally, FAILS the four perfect-calibration
families: revoke, logic, cost (G≡0.000000, acc=1.0, conf=1.0 at all 5 depths)
and ceiling/D (G≡0.000000 at all 7 depths with acc rising 0.25→1.0 and conf
tracking it exactly — v2's headline "PERFECT"). The guard as written
("defined G values must not be all equal within 1e-3") cannot distinguish
perfect calibration from degenerate flatness; its only example is
abstention-driven vacuity, which does not apply here (all slots defined,
n_rel ≥ 10). Reported per the frozen letter; whether the guard intends
"flat AND degenerate" needs a coordinator ruling / prereg amendment — this
arm does not move the bar itself.

## Delta baseline for other arms

Every arm reports its B1–B13 as deltas vs this table. The bars CTL itself
fails (B2, B3, B4b, B8, B13) are the ones a challenger must clear to move
the yardstick; B12's 4 crossings are the refined-reading residual to beat.
