# VERDICT — M1 Bar Calibration (PAM Round 3, Crew 7)

**Date:** 2026-09-24. **Prereg:** `e0d96b7f78de7d485f8ed2fb6134d3e011a89f2d`
(committed alone). **Method:** pure-Zag exact grid search (prereg §6),
zero RNG, 3 byte-identical runs
(`9c8df89a…e980c` ×3), all 18 reported numbers independently reproduced by
`score_m1.py`.

## Verdict: SURVIVE (kill bar not triggered) — with load-bearing residuals

KB-M1 (frozen, fable audit Q6): KILL iff optimized RK-3 < 82%.
**Optimized bar (ST=0, AT=0, CT=705, MT=3588) yields RK-3 = 910/1,102 =
82.58% ≥ 82% (bar: 904).** Zero false-PASS on the 12 TMB-5 wrongs, zero
false installs on the 9 CC1 wrong-pairs — both constraints verified at
exactly 0 by instrument and scorer independently. The recalibration survives
mechanically.

## What the search proved

1. **The current bar is miscalibrated, as the audit charged.** Baseline
   (CT=700, MT=0, ST=1, AT=1): 12/12 TMB-5 wrongs false-PASS, 9/9 CC1 pairs
   false-install, at 826/1102 = 74.95% true-PASS. The bar the audit says
   admits trial 1145 admits the entire frozen wrong battery.
2. **The exact optimum is (0,0,705,3588): 910/1102 = 82.58%.** CT=705 blocks
   every CC1 pair through the conf arm (weakest wrong conf = 704); MT=3588
   blocks all 12 TMB-5 wrongs through the margin arm (max wrong mrgF = 2373)
   with the prereg's defense-first tie-break (largest MT among the five
   equal-throughput optima). Exactness is proven, not sampled (prereg §6).
3. **Trial 1145 still PASSES the optimized bar** (conf 874 ≥ 705, margin
   10410 ≥ 3588, strong/agree arms disabled). The motivating evidence is NOT
   fixed by recalibration: pointwise adjudication of confidently-wrong
   corroborated pairs remains impossible — consistent with the program's
   ceiling (2) ("Pointwise adjudication impossible"). M1 blocks the frozen
   wrong *sets*; it does not block the 1145 *class*.

## Residuals (reported per prereg §9; adoption needs Micah's word)

- **R1 — the optimizer disabled the load-bearing arms.** The optimum sets
  ST=AT=0, switching off the strong/agree (disjoint-span (g)-check) arms that
  the O1 prereg calls load-bearing for RK-2. Broad-wrong false-PASS explodes
  **7 → 712/1,109**. The specified objective Goodharts the narrow constraint
  set: it buys 84 true passes by abandoning the machinery that keeps 705
  wrongs out. The safety-constrained variant (ST=AT=1, arms frozen ON) scores
  671/1102 = 60.89% → would KILL under KB-M1.
- **R2 — six trials of headroom.** 910 vs the 904 kill line: the 3pp
  frozen-data overfitting tolerance the audit granted is nearly exhausted by
  the point estimate itself. Any deployment must re-measure on held-out
  wrongs before trusting 82.58%.
- **R3 — scope.** The W/P fixtures carry no strong/agree (prereg's worst-case
  convention treats them as 1); the bar was therefore tuned against
  conf/margin only. Real wrongs with strong/agree = 0 would be blocked by
  arms the optimum discards.

## Recommendation

M1 SURVIVES its frozen kill bar, so the recalibration is not killed — but it
must not ship as-is: adopting (0,0,705,3588) trades the (g)-check's 705-wrong
protection for 84 true passes, which reverses the program's defense-first
posture. Recommend: (a) hold the thresholds as a *measurement* (the bar's
ceiling under the frozen constraints is 82.58%, and the current bar's
12/12 + 9/9 failure is now quantified); (b) put to Micah whether the
strong/agree arms are free parameters or frozen safety machinery — if
frozen, M1's answer is 60.89% and the hypothesis dies by its own kill bar.

## Artifacts

`gen_m1.py`, `m1_cases.txt` (sha
`5d4160d1…c611`), `m1_grid.zag`, `R33_NATIVE_IO_V1.zag` (pinned
`e6379ddb…f61d8`), `score_m1.py`, `evidence/` (run1/2/3.txt, DIGESTS.txt),
`RUNLOG_M1.md`. No binaries, no `.zagd` committed.
