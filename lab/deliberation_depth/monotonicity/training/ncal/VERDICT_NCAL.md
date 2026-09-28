# VERDICT — Native Epistemic Calibration (NEC)

- **Date:** 2026-09-25
- **Arm:** NEC (Native Epistemic Calibration), non-scaffold
- **Status:** PARTIAL — B2 passes, B3/B13 fail, but OUTPERFORMS both scaffold arms

## Head-to-head (frozen analyzer, 37-leg matrix)

| Bar | NEC (m9) | SR-S9 (m15) | SR-S1 (m16) | Threshold |
|-----|----------|-------------|-------------|-----------|
| B1 (1→0) | 0 ✓ | 0 ✓ | 0 ✓ | =0 |
| B2 (V1, V2) | 0, 0 ✓ | 0, 160 ✗ | 0, 85 ✗ | =0, =0 |
| B3 (Gviol, strict) | 6 ✗ | 14 ✗ | 18 ✗ | =0 |
| B4 (meanConfCorrect) | 0.972 ✓ | — | — | ≥0.50 |
| B4b (honest floors) | ≥0.984 ✓ | — | — | ≥0.50 |
| B5 (separation) | 0.668 ✓ | — | — | ≥0.20 |
| B6 (recall) | 1.00 ✓ | — | — | ≥0.95 |
| B7 (abstention) | 0.148 ✓ | — | — | ≤0.30 |
| B9 (identity vs M4) | 100% ✓ | — | — | 100% |
| B13 (underconf) | 6 ✗ | 46 ✗ | 19 ✗ | =0 |

**NEC is the BEST of the three on B2, B3, and B13.** It is the ONLY arm
with V1=0 and V2=0. It has the fewest G-violations (6 vs 14 vs 18) and
the fewest B13 violations (6 vs 46 vs 19).

## What passed

- **B2 (Theater): V1=0, V2=0.** The per-item deliberation ceiling
  (conf nonincreasing along depth path) WORKS. This is the first arm
  in the H5 round to achieve zero theater violations. The scaffold arms
  (SR-S9: V2=160, SR-S1: V2=85) do NOT.
- **B1, B4, B4b, B5, B6, B7, B9:** all pass. Non-degenerate (B4=0.972),
  well-separated (B5=0.668), M4-identical.

## What failed

- **B3 (strict): 6 G-violations.** ceiling/D:2, ceiling/O:2, redteam:2.
  The violations are:
  - ceiling/O and D: selection effects from M4 abstention. As low-conf
    items abstain at deeper depths, the released-set mean confidence
    rises, causing family G to rise even though per-item confidence is
    nonincreasing.
  - redteam: tiny-n noise (n=3,2,1). G values are unstable with so few
    cells; strict monotonicity is unsatisfiable.
- **B13: 6 violations, all ceiling/O.** G≈-0.43 (severe underconfidence).
  The O items are released and correct (acc=1.0) but receive conf≈0.57.
  They occupy low-(margin, evidence) reference classes pooled with
  trap/wrong items; the ledger cannot distinguish them without family
  labels (which are barred).

## Interpretation

1. **NEC falsifies H-SR as a REQUIREMENT? NO.** H-SR necessity requires
   a non-scaffold arm to "achieve non-degenerate non-overconfident
   depth" (clear B1–B9+B13). NEC fails B3 and B13, so necessity SURVIVES.

2. **H-SR SUFFICIENCY is KILLED.** Neither SR-S9 (Gviol=14, V2=160,
   B13=46) nor SR-S1 (Gviol=18, V2=85, B13=19) clears the bars. Per
   PREREG_SR.md §1: "if NEITHER scaffold arm achieves non-degenerate
   non-overconfident depth post-release, the sufficiency claim is
   KILLED."

3. **NEC is the best-calibrated arm tested.** It dominates the scaffold
   arms on B2 (theater), B3 (law), and B13 (underconfidence). The
   per-item ceiling is the ONLY mechanism to achieve V2=0.

4. **B3 (strict) may be unsatisfiable.** All three arms fail. The
   violations stem from (a) M4 selection effects (family G rises when
   low-conf items abstain), and (b) tiny-n noise (redteam). A strict
   per-family G monotonicity with no n-filter may be incompatible with
   M4's abstention dynamics.

## Honest limitations (from prereg)

- The ledger uses online GT feedback (past judgments' correctness).
  This is disclosed, not hidden. A truly zero-GT stateless architecture
  was tested and FAILED (b3=3, b13=19).
- Parameters (K=2, p0=0.95, mbw=150, cbw=250) were tuned via pre-prereg
  grid search. Disclosed in PREREG_NCAL.md §3.
- The per-item ceiling uses deliberation continuity (the machine's own
  past confidence). Authorized in PREREG_NCAL.md §2.3.

## Artifacts

- Prereg: `ncal/PREREG_NCAL.md` (DRAFT v0)
- Design note: `ncal/DESIGN_DECISION.md`
- Implementation: `ncal/src/nec.zag` (pure Zag, zero RNG)
- Binary: `ncal/src/nec_bin` (NOT committed)
- Input: `ncal/necc_input.tsv` (5,240 rows, frozen leg order)
- Output A/B: `ncal/necc_out_A2.tsv`, `ncal/necc_out_B2.tsv`
  (SHA256: 10b7a1f7ffac3006666943de074e306e899dd91e0d44be6613255e69f7cd471e,
   byte-identical)
- Analyzer inputs: `ncal/results_nec2/` (37 files, m9)
- This verdict: `ncal/VERDICT_NCAL.md`

## Recommendation

NEC demonstrates that a non-scaffold architecture CAN outperform
scaffold-and-release on calibration bars. The per-item ceiling is a
novel contribution (first V2=0 in H5). However, B3/B13 failures mean
NEC does not "achieve" the full bar set.

**For Micah:** The strict B3 bar fails for ALL arms (scaffold and
non-scaffold). Consider whether the refined reading (G>0 crossings)
should be the operative bar, or whether B3 needs an n-filter. NEC's
B2 success (zero theater) is the standout result.
