# J1 Verdict — Fixed-k Competing Tilings (STRUCT)

**Date:** 2026-09-21
**Scale:** 1x (r1)
**Status:** DEAD — Kill criterion 1 fired (binding)

## Verdict

**J1 is DEAD.** Kill criterion 1 fired on both M1 corpora:

> Best-of-k ≤ best single tiling + 2 points at equal total budget on
> adversarial-cut corpus.

### Evidence

**m1-1x-prose** (prose.bin, 5.4MB, 963,478 words):
- Best-of-3 arbitration coverage: **96.2%**
- Best single tiling (T2, 64-byte grid): **94.4%**
- Difference: **1.8 points** (≤ 2.0)
- `J1_ADV prose.bin words=963478 arb=96.2 t0adv=3.9 t1adv=58.4 t2=94.4 gridB=11.4 kill_i=1`

**m1-1x-code** (code.bin, 9.5MB, 1,223,384 words):
- Best-of-3 arbitration coverage: **93.9%**
- Best single tiling (T2, 64-byte grid): **92.2%**
- Difference: **1.7 points** (≤ 2.0)
- `J1_ADV code.bin words=1223384 arb=93.9 t0adv=8.1 t1adv=55.9 t2=92.2 gridB=29.1 kill_i=1`

The three-tiling arbitration does not beat the best single fixed tiling
(T2) by more than 2 percentage points. The complexity of maintaining three
competing tilings with α/β/γ arbitration is not justified.

### Literal reading

Implemented per the assignment:
- "Best-of-k" = arbitration coverage (best covering tiling per word, T0>T1>T2
  priority as value proxy)
- "Best single tiling" = max(T0, T1, T2, equal-budget grid) coverage
- "Equal total budget" = grid with B=n0+n1+n2 chunks (same total as 3 tilings)
- "Adversarial-cut corpus" = the M1 corpora (prose.bin, code.bin), testing
  word coverage (words are adversarial to fixed cuts)
- Threshold: ≤ 2.0 percentage points (20 tenths)

Both corpora fire. The arm is dead. No reinterpretation.

## M1–M9 1x Row (partial — arm dead)

| Mode | Metric | Value | Bar | Status |
|------|--------|-------|-----|--------|
| M1 prose | recall | 100.0 | — | PASS |
| M1 prose | boundary | 100.0 | — | PASS |
| M1 prose | ID probe | PASS (PROVISIONAL-PENDING-FREEZE) | — | PASS |
| M1 prose | kill_i | 1 | must be 0 | **FAIL (KILL)** |
| M1 code | recall | 100.0 | — | PASS |
| M1 code | boundary | 100.0 | — | PASS |
| M1 code | ID probe | PASS (PROVISIONAL-PENDING-FREEZE) | — | PASS |
| M1 code | kill_i | 1 | must be 0 | **FAIL (KILL)** |
| M2–M9 | — | — | — | NOT RUN (arm dead) |

## 10x Status

**ATTEMPTED — FAILED** (not attempted; arm dead by binding kill criterion)

## Kill Criteria Evaluation

### Kill (i): Best-of-k ≤ best single + 2pts — FIRED

See above. Binding. Arm dead.

### Kill (ii): Non-covering or >5% suboptimal — PASS (M1 only)

- m1-1x-prose: cov_viol=0, subopt_viol=0/2011734 (0%)
- m1-1x-code: cov_viol=0, subopt_viol=0/2595446 (0%)

Arbitration never chose a non-covering tiling, and never chose a
lower-scoring-by->γ-margin tiling when a better one was available.

### Kill (iii): Turnover fails to settle — NOT EVALUATED (arm dead)

M1 win shares (prose): T0 44%, T1 39%, T2 16% (886171, 797550, 328013).
M1 win shares (code): (pending full output).

Settling not evaluated because the arm is already dead by criterion (i).

## Ambiguities and Provisional Choices

See ARM_SPEC.md §7. Key items:

1. **α/β/γ = 2/1/1, T0/T1/T2 values = 20/16/8, recency = seq mod 64, death share = 5%**
   — Judgment-set, NOT prereg-frozen.

2. **A15 schedule PROVISIONAL-PENDING-FREEZE** — Probe PASS on both corpora
   (prose: 47 pass, 0 side, 16 loud; code: 30 pass, 0 side, 33 loud).
   Loud failures are the literal sparse-table behavior; logged, not reinterpreted.

3. **Kill (i) "equal total budget"** — Implemented as: best single includes
   the equal-budget grid (B chunks) as a comparator, but the max is taken over
   all (T0, T1, T2 at natural budgets, plus grid at equal budget). The T2
   natural tiling beats the grid, so the "best single" is T2. This is the
   literal reading; if the prereg intended a different normalization, the
   implementation must be updated.

## Commit Hashes

PENDING
