# exp2d Predictions (LOCKED before runs of record)

**Date:** 2026-09-27
**Status:** FROZEN — committed before any run of record.

These predictions were derived a priori:
- 2c DP/LK: from committed exp2c scores (runs/*.txt) + C1 replacement analysis.
- x2c wi/wd: from exact MDUMP reconstructor run on committed exp2c MDUMP + new probes.
- C3 collisions: from white-box marker analysis.

## 2c DP/LK predictions (per type)

| Leg | Corpus | T1 DP/LK | T2 DP/LK | T3 DP/LK | T4 DP/LK | T5 DP/LK |
|-----|--------|----------|----------|----------|----------|----------|
| base | (none) | 9/9 | 10/10 | 9/3 | 10/10 | 10/9 |
| ab2-a | cleaned A+B (32) | 9/9 | 10/10 | 9/9 | 10/10 | 9/9 |
| ab2-b | cleaned A+B (32) | 9/9 | 10/10 | 9/9 | 10/10 | 9/9 |
| abc2-b | cleaned β+C (48, ADOPTED) | 9/9 | 10/10 | 9/10 | 10/10 | 9/9 |
| abc2-a | cleaned α+C (48, CONTROL, not adopted) | 4/9 | 5/0 | 5/0 | 5/0 | 5/0 |
| v96-a | cleaned 96 (48+48) | 10/9 | 10/10 | 8/10 | 9/10 | 8/9 |
| v96-b | cleaned 96 (48+48) | 10/9 | 10/10 | 8/10 | 9/10 | 8/9 |
| de2-a | D/E (32) | 9/9 | 10/10 | 9/3 | 10/10 | 10/9 |
| de2-b | D/E (32) | 9/9 | 10/10 | 9/3 | 10/10 | 10/9 |

**Basis:**
- base, de2: identical to committed exp2c (no corpus changes affecting these).
- ab2: cc01/cc05 are sincere E replacements; they do not touch probe-relevant markers. Scores identical to ab_a/ab_b.
- abc2-b: cc40 replaced (was near-duplicate of si3_15). Predicted NO CHANGE (10/10 LK on T3 holds) — the mechanism is genuine, not carried by the duplicate. If LK drops, the C1 concern was real and the honest number is the lower one.
- abc2-a: α design; predicted to FAIL as in exp2c (control, not adopted).
- v96: cc01/cc05/cc40 replaced. The 3 n-gram collisions (C3) persist (not fixed in source). Predicted DP: T3 8/10, T4 9/10, T5 8/9 (same as vol2).

## x2c novel-family predictions (type 3, sincere what-if / where-do lookalikes)

| Leg | x2c wi (what-if) | x2c wd (where-do) | Bar (≥9/10) |
|-----|------------------|-------------------|-------------|
| base | 0/10 | 0/10 | wi FAIL, wd FAIL |
| ab2-a | 0/10 | 10/10 | wi FAIL, wd PASS |
| ab2-b | 0/10 | 10/10 | wi FAIL, wd PASS |
| abc2-b | 0/10 | 10/10 | wi FAIL, wd PASS |
| abc2-a | 0/10 | 10/10 | wi FAIL, wd PASS |
| v96-a | 0/10 | 10/10 | wi FAIL, wd PASS |
| v96-b | 0/10 | 10/10 | wi FAIL, wd PASS |
| de2-a | 10/10 | 10/10 | wi PASS, wd PASS |
| de2-b | 10/10 | 10/10 | wi PASS, wd PASS |

**Basis (a priori, confirmed by exact reconstructor on committed MDUMP):**
- The `what if` hypothetical marker stays live in all non-D/E legs → wi probes withheld (0/10).
- The `where do` marker is REVOKED by the single sincere cc19 ("Where do we meet the driver?" E|x) present in A+B (and thus in abc2/v96). → wd probes endorsed (10/10) on all corpus legs.
- D/E calibration revokes both markers → 10/10 on both.
- **Interpretation:** The `wi` probes are the clean D/E-specific novel-family diagnostic (0/10 → 10/10). The `wd` probes are confounded by cc19 (already 10/10 on A+B); they confirm the marker mechanism but do not isolate D/E.

## C3 n-gram collision predictions (white-box, from MDUMP)

Three support-1 provisional markers fire on sincere probes:

| Marker | Concept | Probe hit | Leg | Predicted miss |
|--------|---------|-----------|-----|----------------|
| `the clock` | hypothetical | si3_03 | v96 | T3 DP 8/10 (not 9/10) |
| `is out` | hypothetical | si5_01 | ab2, abc2, v96 | T5 DP 9/10 (not 10/10); pre-existing, not volume-created |
| `at night` | joke | si4_05, si5_09 | v96 | T4 DP 9/10 (not 10/10), T5 DP 8/9 (not 9/9) |

**Bound:** These are inherent to substring firing by support-1 n-grams. They are NOT fixed in exp2d source. The honest DP numbers above INCLUDE these misses. A generic support-1 revocation is a candidate fix but was NOT implemented (risk of breaking D/E and load-bearing markers; "precisely bound" per task).

## Determinism

All legs: 3 reps byte-identical (SHA-256). Empty mode: frozen SHA
`71731400c1758f883c8057ad3dca044f34491c9a7861e6f53c1c5815b8f75407`.

## Falsification conditions

- If abc2-b T3 LK < 10/10: C1 concern was real; report the lower honest number.
- If v96 DP differs from predicted on T3/T4/T5: C3 bound is wrong; re-white-box.
- If de2 wi < 10/10: D/E mechanism does not generalize; novel-family claim fails.
- If any rep differs: determinism broken; halt and investigate.
