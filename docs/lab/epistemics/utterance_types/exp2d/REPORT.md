# exp2d Final Report: Sincere-Hypotheticals Follow-up

**Date:** 2026-09-27
**Branch:** tnn-native-lab
**Commits:**
- Pre-run: `f71ff91f66bc672d01f8b0a9544cf1067e465d90` (amendments, predictions, source, items)
- Runs: (to be filled)

## Executive Summary

exp2d retests the sincere-hypotheticals design-β with all three exp2c caveats addressed:

1. **C1 (dedupe):** FIXED. cc01/cc05/cc40 replaced per preregistered rule. Scanner confirms 0 flags.
2. **C2 (novel-family):** MEASURED. Extended probes (10 what-if + 10 where-do lookalikes). D/E calibration: 0/10 → 10/10 on what-if.
3. **C3 (collisions):** BOUNDED. Three support-1 markers cause exactly 4 probe misses. Bound is precise.

**All predictions confirmed.** No surprises.

## Answers

### 1. Does cleaned-corpus 9/10 zero-price stand?

**YES.**

A+B (cleaned, 32 items): T3 LK = 9/9 (DP/LK) on both designs. The hypothetical LK 3/10 → 9/10 at zero additional bar failures holds after removing the near-duplicates (cc01, cc05). The C1 concern did not materialize.

### 2. What is the honest 10/10 number now?

**10/10 LK on T3 for β+C (48 items) and v96 (96 items).**

- abc2-b (cleaned β+C): T3 LK = 10/10.
- v96-a/b (cleaned 96-item): T3 LK = 10/10.

The cc40 near-duplicate (of si3_15) was NOT carrying the score. Removing it did not reduce LK. The honest 10/10 stands.

### 3. Is novel-family generalization measured, and what is the number?

**YES. What-if: 0/10 → 10/10.**

- Baseline (base, A+B, β+C, v96): 0/10 on sincere what-if lookalikes. The `what if` hypothetical marker stays live; probes withheld.
- D/E calibration: 10/10. The marker is revoked; probes endorsed.
- The D/E mechanism generalizes to novel what-if frames (nominalized: "the what ifs", "each what if", etc.) that were NOT in the training items.

**Where-do:** Confounded. The A+B corpus already contains a sincere "where do" (cc19), so wd probes are 10/10 on A+B/β+C/v96. The clean D/E effect (base 0/10 → D/E 10/10) is present but not isolated.

## Design β Adoption

**ADOPTED** (Micah sign-off 2026-09-27).

- abc2-b (β): All bars pass. T3 LK 10/10.
- abc2-a (α control): Fails as predicted (T3 LK 0/10). Not adopted.

## C3 Collision Bound (Precise)

Three support-1 n-gram markers fire on sincere probes:

| Marker | Hits | Effect |
|--------|------|--------|
| `the clock` (hypothetical) | si3_03 | v96 T3 DP 8/10 |
| `is out` (hypothetical) | si5_01 | ab2/abc2/v96 T5 DP 9/10 (pre-existing) |
| `at night` (joke) | si4_05, si5_09 | v96 T4 DP 9/10, T5 DP 8/10 |

**Bound:** Exactly 4 probe misses, all accounted for. No other effects. Not fixed in source (generic support-1 revocation deemed too risky for D/E markers).

## Determinism

- 30 runs (9 modes × 3 + empty × 3): all byte-identical per mode.
- Empty mode: frozen SHA `71731400c1758f883c8057ad3dca044f34491c9a7861e6f53c1c5815b8f75407`.

## Files

- `docs/lab/epistemics/utterance_types/exp2d/`
  - Amendments, predictions, source, items, analysis, runs, reports.

## Red Team

**Status:** PENDING. A fresh independent red team must be dispatched by the parent (this coordinator cannot spawn subagents).

**Scope for red team:**
1. Re-derive all scores from raw outputs (runs/*.txt).
2. Audit source for hardcodes (HARD0: 11 hits, all pre-existing).
3. Verify C1: re-run scanner, attack thresholds, try to find remaining near-duplicates.
4. Verify C2: test novel what-if/where-do frames not in the probe set.
5. Verify C3: try to construct new n-gram collisions.
6. Check determinism (all 30 SHAs).
7. Attack the wd confounding (is cc19 really the cause?).

**Red-team brief:** (to be provided by parent)
