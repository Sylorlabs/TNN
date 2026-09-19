# R32 E51K — Calibration Fit vs Generalization Audit Result

Date: 2026-08-30
Branch: `r32-agent-sequential-frontier`
Native result: `VALID DIAGNOSTIC — CALIBRATOR_FIT_LIMITED`
Canonical status: R27 unchanged.

## Integrity

- E50 parent integrity: pass.
- Fresh seed manifest: 19,440 allocated; zero assignment failures.
- Development: 3,240 episodes / 55,080 states.
- Validation: 5,400 episodes / 91,800 states.
- Confirmation: 10,800 allocated; executed 0.
- Base UNKNOWN target nonzero: 0; base UNKNOWN parameters remain zero.
- Base terminal linear fit forward/reverse identity: pass.
- Scalar linear calibrator forward/reverse identity: pass.
- Hinge means/structure/coefficients forward/reverse identity: pass.
- Hinge calibrator nondegenerate: 4 selected terms.
- Native builds byte-identical: SHA-256 `7373318b1cf29babecd7f5a6550fe3d24dd2a74e5d012b24672e2971795870c0`.
- Assembled source SHA-256 `e6c0f82dcee1bfccdd0b80e5a6b5181a209b2080f001e5d2f8abd4bbff761c7e`.
- E51K fragment SHA-256 `646cb6314f81fc95b9e25b477e2e36c78b3f44190e9c28eb5a8f20ffe76fe576`.
- Main injection SHA-256 `bb4854508efc495cec24edc6768944fcae1e796a92cc27cf9d2b7e4d37558df3`.
- Two complete native executions produced byte-identical raw ledgers: SHA-256 `68b9894cec19c984258317adc69c3a01b87f651017ea2a987551683f6af45353`.
- Repeat runtime: 41 seconds; exit code 0.

## Episode reachability: development vs validation

| Arm | Development known | Development no-unique | Validation known | Validation no-unique |
|---|---:|---:|---:|---:|
| A — uncalibrated base | 2,519 / 2,520 | 684 / 720 | 4,197 / 4,200 | 1,129 / 1,200 |
| B — linear scalar calibration | 2,496 / 2,520 | 701 / 720 | 4,155 / 4,200 | 1,166 / 1,200 |
| C — scalar + hinge calibration | 2,481 / 2,520 | 708 / 720 | 4,151 / 4,200 | 1,181 / 1,200 |

The calibrated arms exhibit essentially the same qualitative tradeoff on the worlds they were trained on as on fresh validation: more no-unique abstention is purchased by suppressing valid known commitment.

## State-level decision-side sign accuracy

The frozen sign audit matches controller semantics: positive top-commit utility is correct at predicted scalar `>= 0`; negative utility is correct only at predicted scalar `< 0` because a zero tie remains commit-side.

| Calibrator | Development positive | Development negative | Validation positive | Validation negative |
|---|---:|---:|---:|---:|
| linear | 28,095 / 37,115 = 75.70% | 12,819 / 17,965 = 71.36% | 46,651 / 62,130 = 75.09% | 21,049 / 29,670 = 70.94% |
| hinge | 28,615 / 37,115 = 77.10% | 13,192 / 17,965 = 73.43% | 47,570 / 62,130 = 76.57% | 21,744 / 29,670 = 73.29% |

The development-to-validation gap is tiny: approximately 0.1–0.6 percentage points depending on arm/sign. The dominant error therefore already exists on the development distribution.

## Interpretation

E51K classifies the E51J failure as **fit/objective-limited**, not primarily generalization/support-limited. More training dose on the same scalar absolute-utility regression is not the justified next move: the learner is already misplacing roughly one quarter of positive and negative top-commit states on its own training worlds.

The next causal experiment should change the scalar decision objective or increase learner-owned boundary capacity while preserving the same state, same grounded consequences, same commit ranking, and neutral UNKNOWN. E51L is preregistered to isolate the most conservative objective change: train the shared scalar calibrator directly on the sign of the grounded utility of the learner-selected top commit, rather than its utility magnitude.

No topology rewrite or R32 promotion is justified by E51K.
