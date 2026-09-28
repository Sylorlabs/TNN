# R32 V36 — Exact Scalar-Family Causal Ablation

Status: **REFERENCE_ONLY / CANDIDATE-SUPPORT TARGET IDENTIFIED / EVALUATOR-ONLY VALUES FORBIDDEN AT RUNTIME**

V36 held the V33 action-value learner, trajectories, delayed advantages, and data splits fixed. It appended one exact future scalar family at a time across horizons 1, 2, 3, 5, 8, and 12. These exact values are evaluator-only and cannot enter TNN cognition; the purpose is to identify which delayed dynamics are worth learning accurately.

## Ranking

| Exact future family | Expected AUC | Beneficial > 0 | Non-beneficial > 0 | Selected realized advantage |
|---|---:|---:|---:|---:|
| All scalar dynamics | 0.8119 | 0.6408 | 0.0992 | 0.1656 |
| Dominant mass + current-hypothesis support | 0.7951 | 0.6009 | 0.0711 | 0.2014 |
| **Current-hypothesis support alone** | **0.7847** | **0.6033** | **0.0589** | **0.2104** |
| Instability + return | 0.7351 | 0.5164 | 0.1316 | 0.1152 |
| Entropy + switching + run duration | 0.7332 | 0.4953 | 0.0675 | 0.1795 |
| Transition rate | 0.7303 | 0.5000 | 0.1122 | 0.1243 |
| Longest run | 0.7258 | 0.4883 | 0.1144 | 0.1276 |
| Dominant mass | 0.7189 | 0.4883 | 0.1883 | 0.0809 |
| Return-to-prior | 0.7118 | 0.4648 | 0.1401 | 0.0985 |
| Entropy | 0.7032 | 0.4507 | 0.1304 | 0.1061 |

## Causal interpretation

The central missing quantity is **candidate-specific future support**, not generic uncertainty. The learner needs to estimate how strongly future grounded outcomes will continue to support the currently leading hypothesis across multiple horizons. Generic entropy, transition rate, and duration help, but they do not encode whether the expected future evidence favors the candidate whose commitment is under consideration.

Future dominant mass is useful primarily when paired with candidate support. Dominant mass alone can describe a future that becomes confident around the *wrong* or replacement hypothesis and therefore generates more false-positive INSPECT values.

This explains V34's pattern: its future distribution and instability statistics were accurate in aggregate, while its `fraction_equal_current_top` prediction had much larger error (~0.25 MAE). Aggregate predictive quality concealed poor fidelity on the scalar with the strongest causal value.

## Decision

- Retain multi-step future-state prediction, but prioritize the candidate-support target.
- Next matched run: train specialized predictors for future current-hypothesis support and dominant mass across all horizons.
- Compare ordinary delayed-outcome training against regret-weighted training, where sample weight depends only on later realized decision regret/advantage magnitude—not ambiguity, mode, or evaluator state.
- Append only cross-fitted predictions to the unchanged V33 action-value learner and test whether the exact-family ceiling begins to close.

R27 remains canonical. Native Zag reproduction remains mandatory before promotion.
