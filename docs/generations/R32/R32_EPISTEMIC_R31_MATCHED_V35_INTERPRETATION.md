# R32 V35 — Exact Future-State Sufficiency Ceiling

Status: **REFERENCE_ONLY / PREDICTION-FIDELITY LIMIT CONFIRMED / EVALUATOR-ONLY FEATURES FORBIDDEN AT RUNTIME**

V35 held V33's action-value learner, delayed resource-grounded advantages, data splits, and base representation fixed. It compared V34's cross-fitted predicted future state against evaluator-only exact future-state summaries. Exact future outcomes never enter a learner-runtime feature; these arms exist only to determine whether V34 failed because its predictions were inaccurate or because the summary itself was irrelevant.

## Ceiling result

The V33 expected-advantage baseline has ROC-AUC **0.6550**, beneficial crossing **0.3638**, false-positive crossing **0.1250**, and selected realized advantage **0.0948**.

Evaluator-only exact summaries produce:

| Future information | Expected AUC | Beneficial > 0 | Non-beneficial > 0 | Selected realized advantage |
|---|---:|---:|---:|---:|
| V34 predicted state | 0.6436* | 0.4437* | 0.1848* | 0.0702* |
| Exact distributions | 0.7444 | 0.5329 | 0.0785 | 0.1736 |
| **Exact scalar dynamics** | **0.8045** | **0.6244** | 0.0779 | 0.1913 |
| Exact all future state | **0.8161** | **0.6338** | **0.0704** | **0.1988** |

`*`The predicted-state arm was refit under a different diagnostic seed and is not used as the authoritative V34 comparison; the persisted V34 matched result remains the prediction baseline.

The all-state sign classifier reaches ROC-AUC **0.9619** and AP **0.6764**, versus V33 **0.8792 / 0.3546**. Exact scalar dynamics alone reach **0.9602 / 0.6722**, while exact distributions reach **0.9228 / 0.5314**.

## Causal classification

**Prediction fidelity on decision-critical future dynamics is the limiting component.** The summary target is sufficient: when supplied exactly, the unchanged action-value learner identifies substantially more beneficial observations, rejects more non-beneficial observations, and selects actions with roughly twice V33's realized advantage.

The most valuable information is not merely the future categorical distribution. Continuous dynamics—future entropy, dominant mass, switching rate, run duration, agreement with the current hypothesis, and return-to-prior behavior—carry most of the causal gain.

This rejects the hypothesis that the action-value architecture is fundamentally unable to use multi-step state. It also rejects generic distribution prediction as the sole target. V34's aggregate R² and cross-entropy gains hide errors concentrated in the rare decision-critical states.

## Decision

- Retain V34's multi-step target family.
- Do not use any exact-future/evaluator-only feature at runtime.
- Next causal audit: isolate exact scalar families across horizons to identify which delayed dynamics carry INSPECT value.
- Then retrain only the important scalar predictors with regret-weighted developmental credit focused on states where scalar prediction error changes the INSPECT decision. Weighting may use delayed realized decision regret, never ambiguity or world-mode labels.

R27 remains canonical. Native Zag reproduction remains mandatory before promotion.
