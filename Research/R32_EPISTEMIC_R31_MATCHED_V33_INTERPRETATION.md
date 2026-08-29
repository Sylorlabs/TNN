# R32 V33 — Learned Predictive-Dynamics Credit

Status: **REFERENCE_ONLY / ONE-STEP WEIGHTING REPAIR RETAINED / LONG-HORIZON INSPECT VALUE STILL OPEN**

V33 held the V32 predictive-model inventory, V30 trajectories, delayed resource-grounded advantages, train/calibration/test splits, and action-value model family fixed. It replaced the fixed prequential `exp(-cumulative loss)` mixture with an episode-disjoint learned gate. Gate inputs were only persistent learner state, each generic model's current prediction, and accumulated prequential evidence. Targets were each model's delayed loss on the next experienced grounded observation. World mode, ambiguity, resource-regime identity, trial index, and future opportunities were not inputs.

Three episode-disjoint cross-fitting folds generated gate features for the action-value training rows. A final gate trained on splits 0–5 generated calibration/test features. Mixture temperature and the fixed-model control were selected only on splits 6–7; splits 8–9 remained held out.

## One-step predictive result

The calibration-selected fixed model was `recent5`. Held-out next-outcome performance was:

| Predictor | Top-1 | NLL | Brier |
|---|---:|---:|---:|
| V32 prequential mixture | 0.6520 | 1.1114 | 0.5605 |
| Fixed `recent5` | 0.6512 | 1.0606 | 0.5386 |
| **Learned hard selector** | **0.6665** | **0.9744** | **0.4873** |
| Learned soft mixture | 0.6716 | 1.0018 | 0.5002 |
| Per-row oracle, evaluator only | 0.8078 | 0.6891 | 0.3264 |

The learned next-loss gate therefore repairs the V32 weighting failure. Its predicted loss surface has variance-weighted R² **0.4270**. The hard selector matches the evaluator-only per-row oracle only **27.81%** of the time, leaving a substantial model-selection ceiling, but its excess NLL over oracle drops to **0.2853**, versus **0.4224** for V32's mixture.

## INSPECT action-value result

Adding learned gate state to V32 raises the sign classifier from ROC-AUC **0.8693** / AP **0.3320** to **0.8792** / **0.3546**. Expected-advantage ROC-AUC rises **0.6482 -> 0.6550**. Non-beneficial observations crossing zero fall **0.1764 -> 0.1250**, and selected actions have mean realized advantage **+0.0948**.

However, truly beneficial observations crossing zero remain essentially unchanged: **0.3662 -> 0.3638**. Mean predicted value on actually beneficial observations remains negative (**-0.0958**). The alternative representation that replaces V32's old mixture features shows the same boundary: sign AUC **0.8783**, but beneficial crossing only **0.3756**.

## Causal classification

Two causes are now separated:

1. **Predictive-hypothesis weighting / credit assignment was genuinely faulty and is repaired.** Learned episode-disjoint loss prediction materially beats both the fixed recent-history control and the V32 mixture.
2. **The remaining INSPECT failure is long-horizon option-state insufficiency.** Better one-step prediction reduces false probes but does not identify most observations whose value emerges only after multiple future trials, stabilization, replacement, reversal, or persistent non-convergence.

This is not evidence for adding a confidence threshold or fixed probe count. Nor is it evidence that the raw observation is uninformative: V27 showed a feasible zero-cost information route. The missing state is the expected multi-step path from another observation to eventual grounded resolution under cost.

## Decision

- Retain learned predictive gating and episode-disjoint delayed-loss credit.
- Reject V32's fixed prequential mixture as authority.
- Do not promote V33 expected advantage as the live INSPECT gate.
- Next matched mechanism: add generic duration/hazard and multi-step convergence hypotheses over retained raw evidence. Train them only from delayed observed stabilization, change, return, and non-convergence. The action-value learner should receive predicted probability/time-to-resolution and expected cumulative future observation cost, not evaluator mode labels.
- Compare one-step learned gating against multi-step convergence state on unchanged trajectories before any new architecture expansion.

R27 remains canonical. Native Zag reproduction remains mandatory before promotion.
