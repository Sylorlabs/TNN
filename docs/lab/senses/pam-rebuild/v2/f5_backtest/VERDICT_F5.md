# VERDICT — F5 counter-corroboration trap backtest

Date: 2026-09-23. Arm: F5. Prereg: `v2/preregs/PREREG_F5_BACKTEST.md`
(prereg commit `f82eab214a393a459a2a67b0616af16162dc9458`, committed alone
before any code).

## Measured result

| Bar | Rule | Measured | Outcome |
|-----|------|----------|---------|
| (a) Block recall | ≥ 8/9 false accepts blocked pre-confirmation | **8/9** | PASS |
| (b) Over-block cost | ≤ 4/34 true accepts within exemplar distance | **0/34** | PASS |

**Verdict: SURVIVE.** No rescue mission was needed; the tests decided.

## Detail (from the frozen predicate, pure Zag, 3 byte-identical runs)

- 43 candidates parsed (`CANDIDATES n=43`), bank = 6 exemplars.
- 8 TMB-5 false accepts (RICH/DARK) → BLOCKED, each within exemplar distance
  (family stem TMB, |Δconf| ≤ 150, |Δmeasure| ≤ 2000; nearest bank entry
  reported as seq 10983, first in bank order — all six exemplars are in
  range for these eight).
- 1 COL-4 false accept (DIFFERENT/SAME) → ALLOWED. It is a colordisc-family
  trial; the bank holds only timbredisc exemplars, so the family rule
  correctly excludes it. This is the designed scope of the trap, not a
  predicate failure.
- 0 of 34 true accepts within exemplar distance → zero would-be-delayed
  correct percepts.

## Determinism

- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- Binary `f5_pred` built from `f5_pred.zag` (+ byte-identical copy of
  `R33_NATIVE_IO_V1.zag`, SHA `e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8`).
- Three runs, stdout SHA-256:
  `8049012b618f6049a8ad1d7415e518cd2e46fa250645166332596efe01f28453`
  (run1.out = run2.out = run3.out, byte-identical). Zero RNG.

## Caveats (frozen in the prereg, not post-hoc)

- `mrgF` is genuinely unavailable for the 43 candidates (sense files and rt4
  fixtures absent from the repo/VM; the ledger format carries only `measure`).
  The frozen predicate substitutes `measure` (documented task-specific raw
  quantity, NOT the margin) on the ±2000 axis. Bar (a) passes at the boundary
  (8/9); a follow-up with true-margin replay is the honest upgrade path.
- The "three deliberate re-inspections from three temporal crops"
  confirmation machinery was NOT exercised — this battery covers the
  pre-confirmation block predicate only, as the kill bars are written.

## Follow-up (conditional clause from the prereg)

300 near-exemplar correct percepts red-team (kill if >25% delayed >50 trials)
was NOT run: it needs fresh fixture generation, not an offline replay of
committed logs. Filed as the documented next step under a separate
preregistered battery.
