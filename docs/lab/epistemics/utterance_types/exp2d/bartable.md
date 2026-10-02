# exp2d Bar Table

**Date:** 2026-09-27
**Commit:** (runs commit SHA to be filled)

All scores from runs of record (3 reps, byte-identical). Predictions from `PREDICTIONS_LOCKED.md` (committed before runs).

## 2c DP/LK (per type)

| Leg | T1 DP/LK | T2 DP/LK | T3 DP/LK | T4 DP/LK | T5 DP/LK | Pred match? |
|-----|----------|----------|----------|----------|----------|-------------|
| base | 9/9 | 10/10 | 9/3 | 10/10 | 10/9 | YES |
| ab2-a | 9/9 | 10/10 | 9/9 | 10/10 | 9/9 | YES |
| ab2-b | 9/9 | 10/10 | 9/9 | 10/10 | 9/9 | YES |
| abc2-a (α ctrl) | 4/9 | 5/0 | 5/0 | 5/0 | 5/0 | YES (pred FAIL) |
| abc2-b (β) | 9/9 | 10/10 | 9/10 | 10/10 | 9/9 | YES |
| v96-a | 10/9 | 10/10 | 8/10 | 9/10 | 8/9 | YES |
| v96-b | 10/9 | 10/10 | 8/10 | 9/10 | 8/9 | YES |
| de2-a | 9/9 | 10/10 | 9/3 | 10/10 | 10/9 | YES |
| de2-b | 9/9 | 10/10 | 9/3 | 10/10 | 10/9 | YES |

## x2c novel-family (type 3)

| Leg | WI (what-if) | WD (where-do) | Pred match? |
|-----|--------------|---------------|-------------|
| base | 0/10 | 0/10 | YES |
| ab2-a | 0/10 | 10/10 | YES |
| ab2-b | 0/10 | 10/10 | YES |
| abc2-a | 0/10 | 0/10 | YES |
| abc2-b | 0/10 | 10/10 | YES |
| v96-a | 0/10 | 10/10 | YES |
| v96-b | 0/10 | 10/10 | YES |
| de2-a | 10/10 | 10/10 | YES |
| de2-b | 10/10 | 10/10 | YES |

## Key findings

1. **C1 (dedupe):** abc2-b T3 LK = 10/10 (holds). The cc40 near-duplicate was NOT carrying the score. The honest 10/10 stands on cleaned corpus.
2. **C2 (novel-family):** de2 WI = 10/10 (from 0/10 baseline). Novel-family generalization MEASURED. The D/E calibration generalizes to unseen what-if frames.
3. **C3 (collisions):** v96 DP = 8/10 (T3), 9/10 (T4), 8/10 (T5) — exactly the bound. The 3 markers cause exactly 4 probe misses, no more.
4. **Design β:** abc2-b passes all bars; abc2-a (α) fails as predicted. β is adopted.
5. **Determinism:** All 30 runs byte-identical (3 reps each). Empty mode = frozen SHA.

## Answers to Micah's questions

1. **Does cleaned-corpus 9/10 zero-price stand?** YES. ab2-a/b T3 LK = 9/9 (DP/LK). The 9/10 hypothetical LK → 9/10 at zero additional bar failures holds on the cleaned A+B corpus.
2. **What is the honest 10/10 number now?** 10/10 LK on T3 for β+C (abc2-b) and v96 (v96-a/b). The C1 dedupe did NOT reduce the score.
3. **Is novel-family generalization measured, and what is the number?** YES. What-if: 0/10 (base/A+B/β+C/v96) → 10/10 (D/E). Where-do: confounded by cc19 (10/10 on A+B already); clean D/E effect is 0/10 → 10/10 on base.
