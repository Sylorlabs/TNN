# R32 E51L — Top-Commit Sign Calibration Discriminator

Date frozen: 2026-08-30
Branch: `r32-agent-sequential-frontier`
Canonical status: R27 remains canonical.

## Causal basis

E51I proved that every known validation episode already contains a stopping state where the correct commit action is top-ranked among KEEP/CURRENT/RESTORE, while one global commit shift cannot jointly expose all known decisions and all no-unique UNKNOWN decisions. E51J showed that a state-dependent rank-preserving scalar calibrator has strong causal leverage but trades valid commitment for abstention. E51K then found essentially the same scalar-sign accuracy and episode reachability on the development worlds used for fitting as on fresh validation worlds. The current scalar mechanism is therefore fit/objective-limited rather than primarily generalization-limited.

E51L tests whether the scalar regressor is being distorted by the **magnitude** of grounded negative utilities when the controller only needs the sign of the preferred commitment relative to neutral UNKNOWN.

## Constraints

- Full native Zag v2 only.
- Same primary 32-feature learner-visible terminal state.
- Same frozen absolute-utility linear head supplies KEEP/CURRENT/RESTORE ordering.
- One scalar shift is applied equally to all three commit scores, so commit ordering cannot change.
- UNKNOWN remains exactly score 0 and receives no learned positive target or classifier.
- Evaluator truth, ambiguity membership, seed/stage identity, validation membership, and E51I audit margins are never learner inputs.
- No topology rewrite, graph privilege, ambiguity detector, confidence threshold, or hand-selected feature.
- Development selects nonlinear additions; validation is untouched.
- Confirmation remains sealed unless exact validation succeeds.

## Fresh partitions

- stage 49: development, 3,240 episodes / 55,080 sequential states;
- stage 50: validation, 5,400 episodes / 91,800 sequential states;
- stage 51: confirmation, 10,800 episodes allocated and sealed.

## Shared base learner

Fit the frozen absolute-utility linear terminal head exactly as in E51J/K. At each development state identify the learner-selected top commit among KEEP/CURRENT/RESTORE using this frozen head.

## Arms

### A — absolute-utility scalar calibration control

Target is the exact grounded utility of the frozen learner-selected top commit, reproducing E51J/K's scalar calibration objective. Fit one deterministic linear scalar head. At inference shift all three commit values so the top commit score equals this scalar prediction.

### B — top-commit sign calibration

Convert the same grounded top-commit utility to a neutral-relative scalar target:

- grounded utility > 0 -> +1000;
- grounded utility < 0 -> -1000;
- grounded utility = 0 -> 0.

This is not an ambiguity label. It is consequence-derived supervision for the exact decision the scalar head controls: whether the currently preferred commitment belongs on the commit side (`>= 0`) or UNKNOWN side (`< 0`) of neutral value zero.

Fit the same deterministic linear scalar machinery as arm A.

### C — top-commit sign calibration + learner-selected hinge residual Foundry

Start from B and permit at most four generic data-mean one-sided hinge residual bases. Feature identity, direction, coefficient, and stopping point are selected only by strict development loss improvement. No residual is an UNKNOWN head; the output remains one shared scalar commit calibration.

## Integrity gates

Before interpreting validation require:

1. E50 parent integrity passes;
2. exactly 19,440 fresh seeds allocated with zero failures and confirmation execution = 0;
3. development = 3,240 episodes / 55,080 states;
4. base UNKNOWN targets/parameters remain exactly zero;
5. A and B scalar targets contain both positive and negative support;
6. base terminal fit, A scalar fit, and B scalar fit are independently forward/reverse identical;
7. C data means, selected hinge structure, coefficients, loss, and trace are forward/reverse identical;
8. C is nondegenerate;
9. no evaluator-only audit quantity becomes a learner feature.

Decision-side sign convention is frozen: positive targets are correctly placed when scalar prediction is `>= 0`; negative targets are correctly placed only when prediction is `< 0`, matching terminal tie-breaking.

## Validation gates

Report development and validation sign accuracy for A/B/C, and validation episode reachability for the uncalibrated base plus scalar arms A/B/C.

Exact objective rescue requires one experimental sign arm B or C to reach:

- known reachability = 4,200 / 4,200;
- no-unique UNKNOWN reachability = 1,200 / 1,200;
- all integrity gates pass.

Partial rescue requires B or C to weakly preserve the matched absolute-scalar control's known reachability and strictly improve its no-unique reachability.

Confirmation remains sealed unless exact rescue occurs.

## Frozen outcomes

- `TOP_COMMIT_SIGN_CALIBRATION_RESCUE`: B or C reaches the exact gate.
- `TOP_COMMIT_SIGN_CALIBRATION_PARTIAL_RESCUE`: B or C improves the matched calibration frontier without exact rescue.
- `NO_TESTED_TOP_COMMIT_SIGN_CALIBRATION_RESCUE`: neither B nor C improves the preregistered frontier.
- integrity failure: invalid experiment.

If sign calibration still cannot fit the development decision boundary, the next causal experiment should increase learner-owned scalar boundary capacity or test a local/prototype calibration memory on the same state before adding dose or changing topology. If development becomes strong but fresh validation separates, return to training dose/curriculum diagnosis.

No E51L result can promote R32 or establish AGI.
