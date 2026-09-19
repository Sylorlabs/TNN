# R32 V32 — Predictive Dynamics Hypothesis Population

Status: **REFERENCE_ONLY / PREDICTIVE COMPONENT RETAINED / PREQUENTIAL WEIGHTING NOT ACCEPTED**

V32 held the V30 resource-grounded trajectories, opportunity-loss targets, train/calibration/test split, and candidate-specific ordered history fixed. It added fifteen generic live predictive-dynamics hypotheses over retained source-7 raw evidence: global and recency means, exponential memories, last-observation, change-point, first/second-order transition, periodic, and return-to-prior models. Hypothesis weights were updated only from prequential next-observation log loss. No mode, ambiguity, resource-regime, trial identity, or future outcome entered the runtime features.

The corrected matched audit passes exactly: V30 base features and advantages have maximum absolute delta **0.0**, and split assignments are identical. A preliminary pass with permuted base columns and incorrect metric indexing is preserved separately as a rejected evaluator/implementation diagnostic and is not used scientifically.

## Predictive component result

On the held-out test panel, the live hypothesis population predicts the next grounded outcome at:

- top-1 accuracy: **0.6520**;
- NLL: **1.1114**;
- Brier score: **0.5605**.

This is substantially informative relative to uniform prediction (top-1 **0.1434**, NLL **1.6094**). However, the prequential exponential weighting underperforms the strongest single fixed model on this panel: `recent5` reaches NLL **1.0606**, while the weighted ensemble is **1.1114**. Therefore the predictive-model inventory contains useful state information, but the current credit/weighting rule is not accepted.

## INSPECT action-value result

Relative to V30, adding the current predictive population changes:

- sign-classifier ROC-AUC: **0.8715 -> 0.8693**;
- average precision: **0.3282 -> 0.3320**;
- expected-advantage ROC-AUC: **0.6394 -> 0.6482**;
- true beneficial actions crossing zero: **0.3615 -> 0.3662**;
- non-beneficial actions crossing zero: **0.2048 -> 0.1764**.

The representation reduces false-positive probing and modestly improves value ranking, but beneficial-observation recall barely changes. Mean predicted value on actually beneficial actions remains negative (**-0.0946**). V32 therefore cannot be used as the live INSPECT gate.

## Causal classification

**Predictive hypothesis weighting / credit assignment failure, with possible long-horizon option-state insufficiency.** The architecture is not rejected: the model population predicts experienced dynamics well above chance. But prequential `exp(-cumulative loss)` weighting is worse than a fixed recent-history control, so architecture expansion is premature. Training/credit must be isolated first.

## Decision

- Retain candidate-specific ordered raw evidence and the generic predictive-dynamics model inventory.
- Reject the current prequential exponential mixture as authoritative.
- Reject V32 absolute INSPECT value as a runtime gate.
- Next matched test: learn the model selector/mixture solely from delayed next-observation loss using episode-disjoint cross-fitting; compare it against the calibration-selected fixed model and the current Bayesian mixture. Then test whether learned mixture state improves INSPECT value on the unchanged V30 trajectories.
- If learned weighting cannot beat the fixed recency control or materially improve action value, move to duration/hazard and multi-step convergence hypotheses rather than adding more one-step models.

R27 remains canonical. Native Zag reproduction remains mandatory before any promotion.
