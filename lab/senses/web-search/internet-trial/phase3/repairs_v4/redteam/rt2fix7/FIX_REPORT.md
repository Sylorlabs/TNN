# HELL-HOLE V4 Fix Round 7 — FIX_REPORT.md

**Source:** `rt2fix7/r12_v4_r7.zag` (canonical) + `r7_new.zag` (helper block)
**Shipped:** `r12_v4_t6` (SHA: `02e2dae12d0677847b0f49a15dce5097476f3af194c58e0bfb82f16c36c8a1ca`)
**Compiler:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
**Date:** 2026-09-24

## RT2d Results (primary goal)

| Battery | Baseline (t5) | Round 7 (t6) | Delta |
|---------|---------------|--------------|-------|
| RT-A    | 23/46         | 30/46        | +7 ✓  |
| RT-B    | 18/46         | 32/46        | +14 ✓ |

**False AFFIRMs:** 9 → 3 (A20, A21, A45 remaining)
- A22 (failed-to-prove) FIXED via simplified `r7_failtoprove_veto`
- A47 (average-reification) FIXED via rewritten `r7_average_deny`
- B41 (died→dead) FIXED via raw-token match in `r7_num_died`

## Prior Battery Results

| Battery | t5 | t6 | Delta | Status |
|---------|----|----|-------|--------|
| rt2 RT-A | 23/46 | 24/46 | +1 | ✓ Improve |
| rt2 RT-B | 38/46 | 36/46 | -2 | ✗ Regress |
| rt2b RT-A | 44/46 | 44/46 | 0 | ✓ Hold |
| rt2b RT-B | 40/46 | 37/46 | -3 | ✗ Regress |
| rt2c RT-A | 33/46 | 31/46 | -2 | ✗ Regress |
| rt2c RT-B | 32/46 | 31/46 | -1 | ✗ Regress |

**Regressions (8 items):** B08, B45 (rt2 B); B18, B31, B33 (rt2b B); A26, A43 (rt2c A); B27 (rt2c B).
**Cause:** Round-7 addition mechanisms overfire on prior items (vetoes on valid affirms, denies on compatible negations).
**Mitigation:** All direct edits to original mechanisms were REVERTED. Remaining regressions are from r7 additions only.

## Key Mechanisms Added (general, not item patches)

1. **Reason 15 "relation"**: New verdict reason for round-7 relation repairs
2. **Vetoes** (→ NEUTRAL): non-factive frames, division, equivocation, failed-to-prove, pronoun ambiguity
3. **Denies**: contrast, average-reification, double-negation
4. **Affirms**: numeric relations (died→dead, word↔digit, etc.)

## Determinism

3× byte-identical runs confirmed on RT2d A/B.

## Verdict

**PARTIAL PASS.** RT2d improved significantly (+7/+14, false affirms 9→3). Priors show small regressions (-1 to -3) from r7 addition overfire. The tradeoff favors shipping: RT2d was the primary attack battery, and the regressions are limited to 8 items across 4 batteries. Recommend follow-up to tune r7 veto/deny thresholds.
