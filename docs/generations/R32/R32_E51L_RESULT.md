# R32 E51L — Top-Commit Sign Calibration Result

Date: 2026-08-30
Branch: `r32-agent-sequential-frontier`
Native result: `VALID NEGATIVE — NO_TESTED_TOP_COMMIT_SIGN_CALIBRATION_RESCUE`
Canonical status: R27 unchanged.

## Integrity

- E50 parent integrity: pass.
- 19,440 fresh seeds allocated; zero failures.
- Development: 3,240 episodes / 55,080 states.
- Validation: 5,400 episodes / 91,800 states.
- Confirmation: 10,800 allocated; executed 0.
- Base UNKNOWN target/parameters remain zero.
- Base terminal fit, absolute-scalar fit, and sign-scalar fit are each forward/reverse identical.
- Sign-hinge means/structure/coefficients are forward/reverse identical.
- Sign-hinge calibrator nondegenerate: 4 selected terms.
- Native builds byte-identical: SHA-256 `7be9c1e7dca367459296c7aac628ba117f2ca4bf20e45a4188ea763763832af6`.
- Assembled source SHA-256 `92cd63e2f3ef0ba1312a3a1f7286daa7ff85dce051d3bee63690e73e9fb15978`.
- E51L fragment SHA-256 `575a539d930e0e39131f5ab62a6e3a6179b51bb45ac6a1152969accf2edadb2f`.
- Main injection SHA-256 `f3d56f9cc77641e723b68d5059829007e84178ac9c1d26e138043a61b1e76360`.
- Raw ledger SHA-256 `924efa504e31b0d07549dc1b2ab107b67e0bd3aa64522695430037a7c3b61af7`.
- Runtime 41 seconds; exit code 0.

## State-level decision-side sign accuracy

| Scalar objective | Development positive | Development negative | Validation positive | Validation negative |
|---|---:|---:|---:|---:|
| exact grounded utility | 28,106 / 37,228 = 75.50% | 12,684 / 17,852 = 71.05% | 46,490 / 62,131 = 74.83% | 21,329 / 29,669 = 71.89% |
| top-commit sign | 32,949 / 37,228 = 88.51% | 9,537 / 17,852 = 53.42% | 54,707 / 62,131 = 88.05% | 16,042 / 29,669 = 54.07% |
| sign + 4 learner hinges | 32,646 / 37,228 = 87.69% | 10,564 / 17,852 = 59.18% | 53,968 / 62,131 = 86.86% | 17,914 / 29,669 = 60.38% |

The development and validation figures remain close, again ruling against a primary transfer gap. Sign supervision strongly improves placement of beneficial commits but makes harmful commits too likely to remain on the commit side. Learner-selected hinges recover some negative-side discrimination at a modest cost to positive-side accuracy.

## Validation episode reachability

| Arm | Known reachable | No-unique UNKNOWN reachable |
|---|---:|---:|
| uncalibrated base | 4,192 / 4,200 | 1,148 / 1,200 |
| exact-utility scalar control | 4,154 / 4,200 | 1,177 / 1,200 |
| sign scalar | 4,198 / 4,200 | 1,127 / 1,200 |
| sign scalar + hinges | 4,196 / 4,200 | 1,147 / 1,200 |

Neither sign arm reaches the exact gate or dominates the matched exact-utility scalar control. The sign objective moves the operating point toward commitment; the exact-utility scalar moves it toward abstention. The 4-term hinge arm lies between them.

## Interpretation

E51L rejects the narrow hypothesis that replacing scalar utility magnitude with a simple sign target is sufficient. It does, however, isolate a clearer frontier: the same state contains enough information for a learner to move substantially between commitment and abstention, but the tested low-capacity scalar boundary cannot represent the required heterogeneous decision surface without sacrificing one side.

Because E51K and E51L show the deficit already exists on development worlds and not primarily in validation transfer, the next step is a preregistered training/capacity curve on the same scalar decision problem before any topology rewrite. The immediate question is whether more learner-owned boundary capacity and/or more training worlds moves the positive/negative frontier monotonically toward exact reachability or plateaus.

No topology rewrite or R32 promotion is justified by E51L.
