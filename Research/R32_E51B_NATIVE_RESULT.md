# R32 E51B — Native Batch-Terminal + Sequential Continuation Result

Date: 2026-08-29
Status: `EXECUTED_VALID_NATIVE_NEGATIVE — NO VALIDATED SEQUENTIAL RESCUE`
Canonical: R27 step 60,423
GitHub Actions run: `33277879372`

## Integrity

- E50 parent seed preflight: PASS
- E50 batch statistics: PASS
- E50 forward/reverse batch parameters: byte-identical / PASS
- E50 convergence: PASS
- E50 frozen auxiliary state: PASS
- E51B parent integrity gate: PASS
- fresh E51B effective seeds emitted: 19,440
- E51B seed-assignment failures: 0
- development episodes: 3,240
- validation episodes: 5,400
- sealed confirmation allocated: 10,800
- sealed confirmation executed: 0
- continuation target has positive and negative interior support in both models
- E51B batch statistics: PASS
- E51B forward/reverse fitted continuation parameters: identical / PASS
- native candidate source SHA-256: `4be62ff732142c8f9fb4dfd6c0298b7cf2939cf794393ead65e7ea34a294d764`
- frozen core SHA-256: `6812efb4c2cb990a59bd0f33f0a44469950201cac6633099fa4f4b2c7ae276e0`
- two native binaries were byte-identical at SHA-256 `5d04f8f4ef08246f67d28072ad8d78261d1a5e7c1cc3b4fc85eab6021e76d710`

## Learned target support

| Model | positive continuation targets | negative | zero |
|---|---:|---:|---:|
| M0 safer E50 control | 6,797 | 45,159 | 3,124 |
| M1 E50 provenance/temporal treatment | 6,828 | 45,119 | 3,133 |

The continuation question is therefore not degenerate. Both signs occur in the development trajectories and the learned policy continues only on a subset of validation episodes.

## Validation

### M0 — preregistered primary safety authority

| Metric | frozen terminal control | + learned CONTINUE | Delta |
|---|---:|---:|---:|
| episodes | 5,400 | 5,400 | 0 |
| known success | 1,720 | 1,644 | -76 |
| known wrong commits | 293 | 271 | -22 |
| no-unique UNKNOWN | 619 | 687 | **+68** |
| no-unique wrong commits | 581 | 513 | **-68** |
| episodes continuing at least once | 0 | 619 | +619 |
| total observations | 0 | 2,832 | +2,832 |
| observation/opportunity loss | 0 | 333,412 | +333,412 |
| grounded net utility | 436,800 | 152,988 | **-283,812** |
| every-cell no-unique safety | FAIL | FAIL | no rescue |

### M1 — E50 provenance/temporal terminal representation

| Metric | frozen terminal control | + learned CONTINUE | Delta |
|---|---:|---:|---:|
| episodes | 5,400 | 5,400 | 0 |
| known success | 1,537 | 1,479 | -58 |
| known wrong commits | 46 | 46 | 0 |
| no-unique UNKNOWN | 599 | 671 | **+72** |
| no-unique wrong commits | 601 | 529 | **-72** |
| episodes continuing at least once | 0 | 541 | +541 |
| total observations | 0 | 2,478 | +2,478 |
| observation/opportunity loss | 0 | 289,783 | +289,783 |
| grounded net utility | 723,800 | 462,417 | **-261,383** |
| every-cell no-unique safety | FAIL | FAIL | no rescue |

## Interpretation

This is stronger evidence than E51A. A learned sequential continuation action has **causal leverage**: under both frozen E50 terminal representations it converts dozens of otherwise wrong no-unique commitments into grounded UNKNOWN outcomes. It is not always-stop or always-continue collapse.

However the single linear continuation head is not selective enough. It spends too much observation cost and trades away known-resolution success. The preregistered net-utility and non-inferiority gates therefore fail, as does every-cell no-unique safety. Confirmation remains sealed.

The result rejects the tested **linear continuation approximation**, not continuation-versus-termination value itself.

## Next causal question

Do not tune a confidence threshold and do not manually add another ambiguity feature. The highest-value next test is a generic learner-owned continuation-head Foundry: expose only generic feature-composition primitives, let development delayed utility/regret select sparse nonlinear candidate structures, freeze the selected structure before fresh validation, and compare against this exact E51B linear head and terminal-only control. This tests whether the problem is approximation capacity/selectivity while moving architecture choice from the researcher into TNN.

Any Foundry candidate remains subject to evaluator blindness, deterministic native reproduction, resource accounting, fresh validation, regression non-inferiority, and sealed confirmation.
