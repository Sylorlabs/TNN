# R32 V34 — Multi-Step Convergence and Duration State

Status: **REFERENCE_ONLY / FUTURE-STATE PREDICTOR RETAINED / INSPECT-VALUE EFFECT NOT ESTABLISHED**

V34 held V33's persistent state, learned one-step gating, resource-grounded advantage target, episode-disjoint splits, and action-value model family fixed. It added a generic multi-step state predictor trained only from delayed experienced outcome sequences. For horizons 1, 2, 3, 5, 8, and 12, the predictor estimates future outcome distributions, entropy, dominant mass, transition rate, longest-run duration, agreement with the current hypothesis, and lag-2 return behavior, plus the final future outcome. World mode, ambiguity, resource-regime identity, trial identity, and future targets are not runtime inputs.

## Component qualification

The cross-fitted multi-step state reaches variance-weighted R² **0.4956**, MSE **0.0543**, and MAE **0.1448** on held-out episodes. It is materially more informative than repeating the learned one-step distribution:

- horizon-1 distribution cross-entropy: **0.6950** versus **1.0018**;
- horizon-5: **0.7163** versus **1.0421**;
- horizon-12: **0.7222** versus **1.0618**;
- final-outcome top-1: **0.6889** versus **0.6245**;
- final-outcome NLL: **0.7243** versus **1.0744**.

The gain spans stable, replacement, reversal, and no-unique evaluator conditions. The predictor is therefore retained as a real generic representation of expected future evidence dynamics.

## INSPECT action-value result

Appending the predicted multi-step state to V33 changes:

- sign-classifier ROC-AUC: **0.8792 -> 0.8818**;
- average precision: **0.3546 -> 0.3575**;
- expected-advantage ROC-AUC: **0.65504 -> 0.65500**;
- beneficial actions crossing zero: **0.3638 -> 0.3732**;
- non-beneficial actions crossing zero: **0.1250 -> 0.1454**;
- mean realized advantage of selected actions: **0.0948 -> 0.0882**.

Thus the future-state representation predicts delayed dynamics well but does not improve net INSPECT option-value discrimination. Its small beneficial-recall gain is offset by more false-positive probing and lower realized selected utility.

## Causal classification

The result narrows the remaining failure but does not yet distinguish two possibilities:

1. **prediction fidelity remains insufficient** for the rare positive INSPECT states, despite strong aggregate future-sequence metrics; or
2. **the chosen future-state summaries are not sufficient statistics for option value**. Generic future entropy/duration can be predictable without encoding how one additional observation changes the candidate-specific terminal decision under resource cost.

No architecture conclusion is drawn from this ambiguity. The next run is an evaluator-only ceiling audit that appends the exact future-state targets to the unchanged action-value model. If exact future state materially improves value discrimination, prediction quality is limiting. If it does not, the summary target itself is insufficient and the next learner must predict candidate-specific resolution/decision value rather than generic sequence statistics.

## Decision

- Retain the cross-fitted multi-step predictor as a component.
- Do not use V34 as the live INSPECT gate.
- Run the exact-future-state ceiling audit before adding duration/hazard mechanisms or changing the action-value learner.

R27 remains canonical. Native Zag reproduction remains mandatory before promotion.
