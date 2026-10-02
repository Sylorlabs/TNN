# R32 V31 — Future-Dynamics State-Aliasing Ceiling Audit

Status: **REFERENCE_ONLY / FUTURE-DYNAMICS ALIASING CONFIRMED / EVALUATOR-ONLY ARMS REJECTED FROM COGNITION**

V31 held V30's learner-visible ordered-history representation, delayed opportunity-loss advantage targets, episode splits, and model family fixed. It added forbidden evaluator information in isolated ceiling arms solely to locate the residual:

1. exact delayed resource opportunity loss;
2. hidden dynamics mode/resource/trial identity;
3. both.

The evaluator-only features cannot enter TNN cognition or support promotion.

## Learner-visible baseline

With V30 candidate history alone:

- sign ROC-AUC: **0.87039**
- average precision: **0.32565**
- direct-value ROC-AUC: **0.62215**
- monotonic-utility beneficial-action recall: **0.07277** at false-positive crossing **0.00605**

## Exact opportunity-loss ceiling

Adding the exact future opportunity loss produces almost no sign-ranking gain:

- sign ROC-AUC delta: **+0.00479**
- average-precision delta: **-0.00139**

The direct regressor improves MSE because it receives part of the target itself, but decision separation remains weak and false-positive crossing increases. Therefore residual V28 shadow-price error is not the primary action-selection bottleneck.

## Hidden dynamics ceiling

Adding hidden future-dynamics mode/resource/trial identity changes the result materially:

- sign ROC-AUC: **0.87039 -> 0.94880**
- average precision: **0.32565 -> 0.63496**
- monotonic-utility beneficial-action recall: **0.07277 -> 0.57042**
- monotonic false-positive crossing: **0.00605 -> 0.03227**
- selected actions retain positive realized advantage (**+0.21939**) and positive precision **0.57995**

Adding both hidden dynamics and exact loss gives only a small further gain: sign ROC-AUC **0.95263**, AP **0.65118**. The dominant missing information is dynamics, not cost.

## Causal classification

**Future-dynamics state aliasing is the primary residual.** The learner's current global, epoch, changepoint, candidate-history, provenance, and resource features do not yet express a sufficiently predictive live distribution over what the reusable apparatus will do next. The action-value learner therefore averages together stationary, stochastic, changing, reversing, and already-resolved trajectories whose optimal evidence actions differ.

This is not authorization to expose a mode label. The hidden arm is an evaluator ceiling only.

## Decision

- Retain V28 learned resource shadow pricing.
- Retain V30 candidate-specific ordered raw-history features.
- Reject exact opportunity loss and hidden mode/resource/trial identity from cognition.
- Next mechanism: construct a **generic live predictive-dynamics hypothesis population** over candidate evidence histories. Candidate models include long-window, recent-window, exponential, changepoint, transition, periodic, and return/reversal predictors. Their weights are updated only by prequential next-observation log loss. The action-value learner receives model evidence masses, predictive disagreement, ensemble next-outcome distribution, and candidate-relative predictions; it never receives the evaluator mode.
- Run a matched V30-versus-predictive-dynamics ablation on the same trajectories and delayed opportunity-loss targets. Quantify next-observation prediction as a component and absolute INSPECT value as the decision gate.

R27 remains canonical. Native Zag reproduction remains mandatory before promotion.
