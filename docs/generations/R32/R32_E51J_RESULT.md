# R32 E51J — State-Dependent Commit Calibration Result

Date: 2026-08-30
Branch: `r32-agent-sequential-frontier`
Native result: `VALID NEGATIVE — NO_TESTED_STATE_DEPENDENT_CALIBRATION_RESCUE`
Canonical status: R27 unchanged.

## Integrity

- E50 parent integrity: pass.
- 19,440 E51J seeds allocated; zero failures.
- Development: 3,240 episodes / 55,080 states.
- Validation: 5,400 episodes / 91,800 states.
- Confirmation: 10,800 allocated; executed 0.
- Base UNKNOWN target nonzero: 0; base UNKNOWN parameters remain zero.
- Base terminal linear fit forward/reverse identity: pass.
- Scalar calibration targets: 37,331 positive, 17,749 negative, zero neutral.
- Scalar linear calibrator forward/reverse identity: pass.
- Unused auxiliary scalar heads remain zero: pass.
- Learner-selected hinge calibrator forward/reverse identity: pass.
- Hinge terms selected: 4.
- Native builds byte-identical: SHA-256 `7c2ce33f4cccd1a2a576fde58381ec7f7fc51c8570e31f69f389485e44af5d3c`.
- Raw ledger SHA-256 `e767f432af7bef4d2298110fd13d08159be21499c6f75a0e553e1bdbf9971da5`.
- Native exit code 0; runtime 39 seconds.

## Validation reachability

| Arm | Known reachable | No-unique UNKNOWN reachable |
|---|---:|---:|
| A — uncalibrated base | 4,196 / 4,200 | 1,108 / 1,200 |
| B — linear state-dependent scalar calibration | 4,160 / 4,200 | 1,160 / 1,200 |
| C — scalar calibration + learner hinge residuals | 4,141 / 4,200 | 1,178 / 1,200 |

Neither calibrated arm satisfies the exact gate or the preregistered partial gate because improvements in no-unique abstention are purchased with substantial loss of known reachability.

## Interpretation

E51J confirms that state-dependent calibration has strong causal leverage: the nonlinear scalar calibrator eliminates 70 of the matched control's 92 no-unique vetoes. But the same learned calibration suppresses valid commitment on 55 additional known episodes.

Because the scalar shift cannot change KEEP/CURRENT/RESTORE ordering, this regression is specifically a **calibration generalization/support problem**, not a commit-ranking problem. The learner does not yet predict the sign/value of its preferred commitment reliably enough across fresh worlds.

Per preregistration, the next experiment must characterize calibration support/generalization before any topology rewrite. Candidate questions include whether the failure is caused by sparse coverage of the relevant state regions, excessive smoothness of the scalar calibrator, or instability of the target because the learner-selected top commit changes across nearby states.

No topology rewrite or R32 promotion is justified by E51J.
