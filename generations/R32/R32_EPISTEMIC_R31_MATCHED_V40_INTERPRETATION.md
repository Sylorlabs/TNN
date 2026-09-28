# R32 V40 — Horizon-Conditioned Persistence / Change Hazard Population

Status: **REFERENCE_ONLY / TEMPORAL HAZARD STATE RETAINED / LIVE QUALIFICATION NEXT**

V40 replaced the rejected opaque recurrent state with an explicit non-graph population of delayed temporal hypotheses. Separate learned surfaces predict, at horizons 1, 2, 3, 5, 8, and 12:

- support retained by the current leading hypothesis;
- future dominant-state mass;
- leave/change increments;
- return-to-prior increments;
- cumulative persistence/change/return quantities.

All quantities are learned from delayed observed outcomes over retained ordered evidence. Horizon is learner-visible. Generator mode, ambiguity status, resource-regime identity, and evaluator answer are excluded. No fixed probe count or confidence threshold is used.

## Prediction result

Relative to V38's repeated-continuation ExtraTrees mean predictor:

- overall MAE: **0.147459 → 0.142996**
- R²: **0.449229 → 0.466176**
- high-regret-quartile MAE: **0.172690 → 0.170127**
- decision-positive MAE: **0.232893 → 0.231408**

The small decision-positive MAE gain confirms that horizon decomposition does not fully recover the latent future state. It does, however, provide action-relevant structure not captured by one aggregate continuation mean.

## Action-value result

The best arm is `horizon_hazard_variance`, compared with V38 predicted repeated mean + variance:

- expected-advantage ROC-AUC: **0.658849 → 0.693649**
- average precision: **0.370269 → 0.421136**
- beneficial observations crossing zero: **0.354460 → 0.436620**
- non-beneficial observations crossing zero: **0.074624 → 0.079941**
- selected realized advantage: **0.147189 → 0.152146**

The pair-only arm raises beneficial selection further to **0.455399**, but false selection rises to **0.125779** and selected value falls to **0.117086**. The hybrid arm likewise broadens the action region and lowers selected value. They are rejected.

## Causal classification

**Explicit temporal-state representation gain.** V39 showed that generic recurrent capacity converged without improving positive-state support. V40 holds the evidence, target, split, resource shadow price, and downstream action learner fixed, but decomposes future dynamics by horizon and by persistence/change/return. The resulting improvement therefore comes from interpretable temporal state structure, not extra stopping thresholds, probe budgets, or cost tuning.

## Decision

- Retain the `horizon_hazard_variance` state for the next R32 candidate.
- Reject horizon-pair-only and hybrid broadening because their additional recall is purchased with excessive false evidence acquisition and lower realized value.
- Retain V38 repeated-continuation variance for no-unique safety.
- Do not claim the primary R32 ambiguity target solved from this offline action-value validation.
- Next: run a live sequential reusable-consequence battery with fresh episode streams and resource contexts. Compare V38 and V40 acquisition policies using the same retained terminal COMMIT / UNKNOWN controller. Measure ambiguity UNKNOWN, resolvable success, wrong commitment, trial cost, runaway acquisition, replacement/reversal recovery, and cost-sensitive stopping.

R27 remains canonical. Native Zag reproduction remains mandatory before promotion.
