# R32 E51J — Learner-Owned State-Dependent Commit Calibration

Date frozen: 2026-08-30
Branch: `r32-agent-sequential-frontier`
Canonical status: R27 remains canonical.

## Causal basis

E51I found zero known-episode commit-ranking failures: every one of 4,200 known validation episodes had at least one state where the correct commit action was already the highest-scoring commit. The residual known failures were therefore caused only by neutral UNKNOWN outranking those commit scores. E51I also proved that one global commit shift cannot satisfy both sides: all-known reachability required a uniform integer shift of at least +57, while all-no-unique UNKNOWN reachability required at most -631.

E51J therefore tests the narrow next mechanism: a **learner-owned state-dependent scalar calibration value** applied equally to KEEP, CURRENT, and RESTORE, preserving their ordering exactly while learning whether the currently preferred commit is worth more or less than neutral UNKNOWN.

## Constraints

- Full native Zag v2 only.
- Primary E51E/E51G 32-feature learner-visible state only.
- Frozen base terminal commit ranking comes from the existing absolute-utility linear head.
- UNKNOWN remains exactly neutral at score 0 and is never given a positive target/classifier.
- The calibrator cannot change the ordering of KEEP/CURRENT/RESTORE: one scalar shift is applied equally to all three commit scores at each state.
- Evaluator truth, ambiguity membership, seed/stage identity, hidden labels, and validation membership are not learner inputs.
- No topology rewrite, graph privilege, confidence threshold, ambiguity detector, or hand-selected calibration feature.
- Development selects all nonlinear residual additions; validation is untouched.
- Confirmation remains sealed unless exact validation succeeds.

## Fresh partitions

- stage 43: development, 3,240 episodes / 55,080 states;
- stage 44: validation, 5,400 episodes / 91,800 states;
- stage 45: confirmation, 10,800 episodes allocated and not executed unless the exact gate passes.

## Training sequence

1. Fit the frozen absolute-utility linear terminal head on development states exactly as in E51G/E51I.
2. For each development state, identify the highest-scoring commit among KEEP/CURRENT/RESTORE using only the frozen learner scores.
3. Use the grounded terminal utility of that learner-selected top commit as a scalar calibration target. This target can be positive or negative; it is consequence supervision, not an ambiguity label.
4. Train a scalar calibrator from the same 32 learner-visible features to predict that top-commit grounded value.
5. At inference, let `b(x)` be the original top-commit score and `g(x)` the learned scalar calibrated value. Apply the same shift `g(x)-b(x)` to KEEP/CURRENT/RESTORE. Their ordering is therefore unchanged and the top commit's calibrated score is exactly `g(x)`. UNKNOWN remains 0.

## Arms

### A — frozen base terminal head

No calibration. Matched control.

### B — linear state-dependent scalar calibrator

Use the existing deterministic order-invariant integer linear batch machinery for one scalar auxiliary value head. The auxiliary head is not an action head; only its scalar output is used.

### C — scalar calibrator + learner-selected hinge residual Foundry

Start from B and permit at most four generic data-mean hinge residual bases. Feature, direction, coefficient, and stopping point are selected only by strict development loss improvement. This changes calibration capacity but still cannot alter commit ordering.

## Integrity gates

Before interpreting validation require:

- E50 parent integrity passes;
- exactly 19,440 fresh seeds allocated with zero failures; confirmation execution remains 0;
- development = 3,240 episodes / 55,080 states;
- base UNKNOWN targets/parameters remain exactly zero;
- scalar calibration targets contain both positive and negative grounded support;
- base linear head and scalar linear calibrator are each forward/reverse identical;
- scalar hinge means/structure/coefficients/loss trace are forward/reverse identical;
- hinge calibrator is nondegenerate;
- no evaluator-only audit quantity from E51I is a learner feature.

## Validation gates

Report episode reachability for A/B/C.

Exact calibration rescue requires one calibrated arm to reach:

- known: 4,200 / 4,200;
- no-unique UNKNOWN: 1,200 / 1,200;
- all integrity gates pass.

Partial rescue requires a calibrated arm to weakly preserve matched-control known reachability and strictly improve matched-control no-unique reachability, while beating the historical E51E no-unique 1,125/1,200 result.

Confirmation remains sealed unless exact rescue occurs.

## Frozen outcomes

- `STATE_DEPENDENT_CALIBRATION_RESCUE`: B or C reaches the exact gate.
- `STATE_DEPENDENT_CALIBRATION_PARTIAL_RESCUE`: B or C improves the preregistered frontier without exact rescue.
- `NO_TESTED_STATE_DEPENDENT_CALIBRATION_RESCUE`: neither calibrated arm improves the frontier.
- integrity failure: invalid experiment.

If exact terminal reachability is rescued, the next experiment is eligible to test direct five-way KEEP/CURRENT/RESTORE/CONTINUE/UNKNOWN sequential control with the frozen winning terminal system. If not, the next experiment must characterize calibration support/generalization before any topology rewrite.

No E51J result alone can promote R32 or establish AGI.
