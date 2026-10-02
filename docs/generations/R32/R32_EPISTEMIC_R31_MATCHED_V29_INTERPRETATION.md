# R32 V29 — Resource-Grounded INSPECT Advantage Integration

Status: **REFERENCE_ONLY / COMPONENT INTEGRATION REJECTED / STATE-ALIASING DIAGNOSED**

V29 applied V28's learned resource shadow price to candidate source-7 INSPECT histories. Advantage targets subtracted actual delayed opportunity loss, not raw cost or a fixed multiplier. The learner received persistent epistemic state, source/provenance, raw experienced cost, observed resource-history features, and the learned shadow cost. Epistemic generator mode, resource regime, future opportunities, ambiguity labels, final answer, and any fixed probe count were excluded.

## Result

The delayed-benefit sign classifier retained useful ranking on the held-out split:

- ROC-AUC: **0.85535**
- average precision: **0.27607** at **0.07245** positive prevalence
- Brier score: **0.05839**

Conditional magnitude components were also directionally sensible:

- predicted positive component on actually beneficial actions: **+0.60687**
- predicted nonpositive component on actually non-beneficial actions: **-0.31754**

But their absolute expected-value composition failed as a runtime gate:

- expected-value ROC-AUC: **0.60849**
- beneficial actions crossing zero: **0.28169**
- non-beneficial actions crossing zero: **0.23781**
- mean predicted value on actually beneficial actions: **-0.12734**
- mean predicted value on non-beneficial actions: **-0.26114**

The failure is especially visible in `costly_stable`, where **0.60476** of actions are predicted positive despite only **0.01786** being actually beneficial.

## Diagnostic

Probability calibration itself is not the primary defect. Across equal-frequency probability deciles, predicted positive probability tracks observed prevalence reasonably; the highest decile predicts **0.28333** and observes **0.30102**. The problem is that the calibrated positive probability on actually beneficial actions averages only **0.18366**, while the conditional-magnitude mixture requires approximately **0.31734** to offset the predicted negative outcome. The top probability decile still has slightly negative mean actual advantage (**-0.01212**).

This means the retained state does not yet identify the subset of trials whose future option value is positive strongly enough for an absolute action-value decision. Ranking evidence exists, but current candidate features alias together:

- a reusable apparatus whose next trial can unlock a resolvable trajectory;
- a stochastic/no-unique trajectory;
- an already-resolved trajectory where another trial is wasteful;
- a costly trajectory whose opportunity loss dominates.

## Causal classification

**Future-dynamics state aliasing / candidate-specific representation loss**, not raw evidence unavailability, undertraining, or probability calibration. V27 established that the evidence action can resolve the constructed cases under a valid cost envelope. V28 established that delayed opportunity cost can be learned accurately. V29 shows that combining those components is insufficient when the action-value learner sees only global epistemic summaries plus source identity/repetition.

## Decision

- Retain V28 learned resource shadow pricing.
- Retain the V29 sign-ranking classifier only as diagnostic evidence; reject the V29 absolute expected-value gate.
- Reject any attempt to fix this with a manually raised/lowered probability threshold.
- Next causal arm: keep the same trajectories, targets, shadow price, and models, but add **candidate-specific ordered raw-history features** for the proposed reusable apparatus: outcome/posterior sequence, run length, switching/return behavior, recent-vs-global divergence, transition entropy, and realized information-gain history. These are computed from retained evidence and contain no condition/mode label.
- Compare base V29 features versus candidate-history features on identical splits. Only if absolute expected advantage improves should the mechanism enter a live controller and forced reusable-probe battery.

R27 remains canonical. Native Zag reproduction remains mandatory before promotion.
