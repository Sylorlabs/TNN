# R32 E51K — Calibration Fit vs Generalization Audit

Date frozen: 2026-08-30
Branch: `r32-agent-sequential-frontier`
Canonical status: R27 remains canonical.

## Question

E51J showed that a state-dependent scalar calibrator can move many no-unique episodes toward safe UNKNOWN while losing too many known episodes. Because the scalar cannot alter commit ranking, the remaining question is whether this is primarily:

1. **fit/capacity failure** — the calibrator cannot even learn the required commit-vs-neutral mapping on development worlds; or
2. **generalization/support failure** — development fit is strong but the learned calibration sign/value does not transfer to fresh validation worlds.

This audit is required before changing topology or adding a larger calibrator.

## Frozen mechanism

Reproduce E51J exactly on fresh domains:

- frozen absolute-utility linear terminal head;
- scalar target = grounded utility of the learner-selected top commit;
- arm B linear scalar calibrator;
- arm C linear + up to four learner-selected data-mean hinge residual terms;
- one state-dependent scalar shift applied equally to KEEP/CURRENT/RESTORE;
- UNKNOWN fixed at zero.

No audit result is fed back into the learner.

## Partitions

- stage 46: development, 3,240 episodes / 55,080 states;
- stage 47: fresh validation, 5,400 episodes / 91,800 states;
- stage 48: confirmation, 10,800 allocated and sealed.

## Required measurements

For arms A/B/C, measure episode reachability on both:

- the development worlds used for fitting;
- the untouched validation worlds.

For scalar calibrators B/C also measure state-level sign agreement with the grounded utility of the learner-selected top commit:

- target positive and predicted scalar > 0;
- target negative and predicted scalar < 0;
- score 0 is counted as commit-side because terminal tie-breaking keeps a commit at zero.

Report separate positive-target and negative-target accuracy on development and validation. Evaluator mode/resource breakdowns may be reported as audit-only diagnostics but are never learner inputs.

## Integrity

Require:

- E50 parent integrity;
- fresh seed allocation with zero failures;
- confirmation execution 0;
- exact development/validation counts;
- base UNKNOWN target/parameters zero;
- base and calibrator forward/reverse fit identity;
- hinge structure forward/reverse identity and nondegeneracy;
- no evaluator labels or E51I margins in learner features.

## Interpretation

- `CALIBRATOR_FIT_LIMITED`: development negative-target safety or known reachability is materially poor; next step should improve the learner objective/capacity before adding dose.
- `CALIBRATOR_GENERALIZATION_LIMITED`: development is substantially stronger than fresh validation, especially on negative-target/UNKNOWN safety; next step should run a training dose/curriculum curve with the same mechanism before architecture change.
- `CALIBRATOR_BOTH_LIMITED`: meaningful deficits exist both on development and in the development-to-validation gap.

No E51K result can promote R32 or justify topology change by itself.
