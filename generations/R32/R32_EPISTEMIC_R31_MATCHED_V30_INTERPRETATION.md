# R32 V30 — Candidate-Specific Ordered Evidence History

Status: **REFERENCE_ONLY / REPRESENTATION COMPONENT RETAINED / ABSOLUTE INSPECT GATE STILL REJECTED**

V30 is a strict matched representation ablation against V29. It regenerated exactly the same 29,400 action states, delayed opportunity-loss advantages, resource shadow prices, and episode splits. Maximum absolute delta in the V29 base feature matrix and advantage targets was **0.0** and split identity was exact. The sole change was adding 89 candidate-specific features computed from retained ordered raw evidence for the proposed reusable consequence apparatus: source outcome/posterior trajectories, run/switch/return behavior, transition entropy, recent-versus-global divergence, current-epoch relation, and realized margin/entropy/information movement.

No epistemic mode, resource regime, ambiguity label, future opportunity list, final answer, or fixed runtime probe count entered learner features.

## Result

Candidate history improves delayed-benefit ranking:

- sign ROC-AUC: **0.85535 -> 0.87151**
- average precision: **0.27607 -> 0.32823**
- Brier score: **0.05839 -> 0.05607**

It also improves the composed absolute expected advantage:

- expected-value ROC-AUC: **0.60849 -> 0.63937**
- beneficial actions crossing zero: **0.28169 -> 0.36150**
- non-beneficial actions crossing zero: **0.23781 -> 0.20480**
- mean predicted value on actually beneficial actions: **-0.12734 -> -0.10679**

A direct advantage regressor remains weaker for ranking (ROC-AUC **0.62109**) and still predicts negative mean value on truly beneficial actions (**-0.11653**).

## Causal classification

**Candidate-specific temporal representation loss was causal but not sufficient.** Ordered raw apparatus history adds real signal without changing trajectories, credit, cost semantics, or model class. It is therefore retained.

The absolute INSPECT action gate remains unqualified. Only 36.15% of beneficial actions cross zero, while 20.48% of non-beneficial actions do. `costly_stable` remains pathological: 42.62% of actions are selected despite only 1.79% being beneficial. Scarce-resource false-positive selection remains 36.41%.

A monotonic delayed-utility calibration over the V30 sign score confirms that a small high-value subset can be selected rationally: selected actions have mean realized advantage **+0.18199** and positive precision **0.46552**, with false-positive crossing **0.01137**. But it captures only **0.12676** of beneficial actions. This is useful as an evaluator diagnostic, not an acceptable controller; it would be another over-conservative policy and would fail the dynamic resolvable cases.

## Decision

- Retain candidate-specific ordered raw-history features.
- Retain the learned resource shadow price.
- Reject V30 two-stage and direct absolute INSPECT gates for live qualification.
- Do not repair by choosing a manual score/probability threshold.
- Next causal audit holds V30 features and targets fixed while adding evaluator-only information in separate ceiling arms:
  1. exact delayed opportunity loss;
  2. hidden future-dynamics mode/resource/trial identity;
  3. both.
  This determines whether the residual is resource-state estimation, future-dynamics aliasing, or model/training capacity. The evaluator-only arms cannot enter cognition.

R27 remains canonical. Native Zag reproduction remains mandatory before promotion.
