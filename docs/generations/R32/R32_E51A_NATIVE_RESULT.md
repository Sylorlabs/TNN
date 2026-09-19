# R32 E51A — Native Sequential Value Mechanism Audit Result

Date: 2026-08-29
Status: `EXECUTED_VALID_NATIVE_DIAGNOSTIC_NEGATIVE — DO NOT PROMOTE`
Canonical: R27 step 60,423
GitHub Actions run: 33277163602

## Result

The preregistered four-arm diagnostic compiled and executed natively in Zag on Linux x86-64. Every arm was compiled twice with the persisted official compiler and produced byte-identical binaries within arm.

The two tested simplifications do **not** rescue R32's historical sequential controller:

1. removing the `learned_credit > 0` gate from continuation training;
2. bypassing the hand-authored continuation value wrapper and using the learned continuation advantage directly.

All four variants still selected UNKNOWN on **0/1000 per-mille** no-unique decisions and made wrong commits on **1000/1000 per-mille** no-unique decisions. All 60 no-unique safety cells failed. The causal completion/regret gate remained zero in every arm. The native core gate remained 4/4.

## Arms

| Arm | Continuation training | Runtime continuation value | Source SHA-256 | Binary SHA-256 | No-unique UNKNOWN | No-unique wrong | Historical gate |
|---|---|---|---|---|---:|---:|---|
| A | gated by learned initiation credit | wrapped | `ba14870e0a359793275b4f5f114bbc358e0c95291ceca4e6d57db9876e90408a` | `4b3fd4dc3b8e8748a132d2b4fa19361d2966ce6946f603a04e76ef92e6e22b9f` | 0/1000 | 1000/1000 | FAIL |
| B | all feasible reachable states | wrapped | `5e145da66101b63b359b6c8cba642b77c6b0cb5600711bbd9784d961b9a21cf0` | `f6f3a08dde89b91d22926e7045cbe5ce901899d78aeef5be6e08898557cd1797` | 0/1000 | 1000/1000 | FAIL |
| C | gated by learned initiation credit | direct learned advantage | `d798fee115f0cea06402f85f8970828d87b2cc7ec79bc4eccab46de4d9206ee8` | `1cde840fa6c2da3e47fbfb905effaf07c9c4fc2e785e513dce3cd0cb603c46fc` | 0/1000 | 1000/1000 | FAIL |
| D | all feasible reachable states | direct learned advantage | `995322612b3e73c39f78826dc049ead2a8b5b88fea9f4810700dc0e35a5adb39` | `87ff8091a3fbb7e264eb759929bf830c848449a757833ac1d75a66be24328565` | 0/1000 | 1000/1000 | FAIL |

## Known-truth effect

Removing the continuation-training gate was harmful in this historical harness. Comparing exact historical control A with treatment B, the preserved subarms' total known-truth successes fell from:

- A-run subarm A: 5,734 -> B-run subarm A: 5,608
- A-run subarm B: 5,801 -> B-run subarm B: 5,661
- A-run subarm C: 5,721 -> B-run subarm C: 5,614
- A-run subarm D: 5,756 -> B-run subarm D: 5,613

Using the direct learned continuation advantage (C versus A, D versus B) did not change the reported safety/known-truth outcome. This indicates that the wrapper is not the active bottleneck under the preserved call geometry.

## Causal interpretation

The preregistered H4 is supported: changing continuation learning alone cannot rescue a controller whose terminal learner never represents a safe no-commit decision in the no-unique cells. This is a mechanism-level negative, not a rejection of sequential continuation value.

The next experiment should therefore combine:

- E50's materially safer batch terminal learner / representation;
- an explicit sequential CONTINUE action or continuation advantage trained in the same delayed utility/regret units;
- actual observation/opportunity cost;
- a matched terminal-only control;
- fresh disjoint development, validation, and sealed confirmation seeds;
- every-cell no-unique safety and known-resolution non-regression gates.

UNKNOWN remains grounded neutral no-commit value. No evaluator ambiguity label, positive UNKNOWN bias, fixed observation count, or tuned confidence threshold is justified by this result.

## Claim boundary

E51A deliberately reused the historical E45 environment and seed structure to diagnose mechanism geometry. It is not promotion-eligible. R27 remains canonical regardless of this diagnostic outcome.
