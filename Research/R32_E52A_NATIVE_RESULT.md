# R32 E52A — Native Exact-Coefficient Joint Foundry Result

Date: 2026-08-29  
Status: `EXECUTED_NATIVE DIAGNOSTIC NEGATIVE — TERMINAL GEOMETRY GAIN, NO JOINT RESCUE`  
Canonical: R27 step 60,423

## Repair and data boundary

E52A changed only coefficient fitting: each generic pairwise proposal was refit exactly on the complete development residual before acceptance. E52 development was retained because the repair was caused solely by a development-side fitting defect. The previously untouched E52 confirmation worlds were reclassified before execution as E52A diagnostic validation; they no longer count as confirmation. No new confirmation was allocated.

## Integrity

- parent E50 integrity: PASS
- terminal Foundry forward/reverse determinism: PASS
- terminal interactions selected: 8
- `UNKNOWN` Foundry parameters: 0
- validation: 1,080 episodes
- source SHA-256: `678a75836abb82e64db4636995e4f00b282fd6a7f943a6957434421cc143b04f`
- two byte-identical native binaries: `e6cbf3488565f0124efdd35ff6d59ffc16985d5ce7a48031f28e92a02fce28ef`
- raw ledger SHA-256: `dfd032d5304191781f4ba4b0cf96d3e9c6ac7d9a7253a538de321c8f3e8b9495`
- runtime: 109.32 seconds; expected qualification exit: 1

## Learner-selected terminal interactions

The generic Foundry selected eight bounded pairwise products across the three commit heads. It did not modify `UNKNOWN`.

| Commit head | Selected feature pairs and coefficients |
|---|---|
| keep | `(21×23, -299)`, `(19×21, +42)` |
| current | `(1×23, -175)`, `(0×1, +27)`, `(1×19, +11)` |
| restore | `(1×23, +112)`, `(0×1, -122)`, `(1×19, +64)` |

## Validation

| Arm | Success | UNKNOWN | Wrong | Known success | Known wrong | No-unique UNKNOWN | No-unique wrong | Observations | Net utility |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A frozen terminal | 478 | 572 | 162 | 346 | 54 | 132 | 108 | 0 | 108,400 |
| B frozen + continuation | 485 | 602 | 141 | 337 | 49 | 148 | 92 | 546 | 58,908 |
| C Foundry terminal | 474 | 583 | 156 | 341 | 49 | 133 | 107 | 0 | **114,600** |
| D Foundry + continuation | 481 | 617 | 134 | 329 | 46 | 152 | 88 | 500 | 68,249 |

C improved terminal-only utility by 6,200 and reduced known wrong commits by 5, demonstrating measurable learner-owned terminal geometry value. D improved over B by 9,341 utility, 3 fewer known wrong commits, 4 fewer no-unique wrong commits, 46 fewer observations, and 6,541 less observation cost.

The improvement was not sufficient: terminal reachability did not improve, known successes fell, continuation Foundry growth was zero, net sequential utility remained below terminal-only, and every-cell no-unique safety failed. E52A therefore does not earn confirmation or promotion.
