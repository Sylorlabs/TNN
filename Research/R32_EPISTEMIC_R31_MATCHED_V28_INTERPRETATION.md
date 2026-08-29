# R32 V28 — Learned Resource Shadow Price

Status: **REFERENCE_ONLY / RESOURCE-COST COMPONENT RETAINED / EPISTEMIC RUNTIME INTEGRATION NEXT**

V28 replaced the ungrounded fixed conversion from raw observation cost to regret utility with a learned shadow price. Developmental targets were the delayed loss of optimal future opportunities caused by spending resources now. The learner received current budget, experienced action cost, and summaries of recent resource opportunities. Hidden resource regime and the future opportunity list were excluded.

## Component qualification

On 5,200 held-out resource episodes, the adaptive shadow-price model reached:

- **R² 0.9305**
- **MSE 0.0341**
- **MAE 0.1295**

Fixed conversions were materially worse: raw scale 1.0 MSE **0.2354**, fixed audit scale 0.55 MSE **0.2940**, and the best learned global scalar (alpha 0.8241) MSE **0.2202**.

The learned effective multiplier adapts rather than hardcoding V27's envelope:

- generous resources: **0.4142×**
- balanced: **0.7033×**
- scarce: **1.5118×**
- low-value future demand: **0.3150×**
- volatile: **0.9860×**

## Matched epistemic cost application

Using fixed evidence trajectories and actual delayed resource opportunity loss, the learned shadow price selected beneficial observations with **0.9715 precision** and **0.9729 recall**. Mean policy regret fell to **0.001042**, a **94.76%** reduction versus raw scale 1.0 and **94.54%** versus fixed 0.55. False-positive probing was **0.0054**.

The policy adapts in the intended direction: learned inspection rate is **0.2512** when future opportunities are low-value, **0.2179** with generous resources, **0.1333** in balanced conditions, and only **0.0869** under scarcity. A single 0.55 scalar over-probes scarce and volatile conditions and produces negative mean incremental utility under scarcity.

## Causal classification

**Utility/evaluator normalization was a real and repairable component failure.** V27 showed a feasible scalar envelope; V28 establishes that the needed conversion can be learned from delayed grounded resource consequences instead of hardcoded. Fixed global scaling is rejected because the appropriate shadow price changes by resource context.

This remains a component qualification. The epistemic application used fixed evaluator trajectories to isolate cost conversion; it did not yet retrain the full COMMIT / INSPECT / UNKNOWN controller with resource state as a live input.

## Decision

- Retain learned resource shadow pricing.
- Reject raw-cost subtraction and all fixed global multipliers as general policy.
- Keep TNN authority over evidence acquisition; resource cost is learned evidence, not an external probe cap.
- Next run: integrate the learned shadow-price feature and actual delayed opportunity-loss targets into candidate-selected INSPECT action-value training, then run fresh-seed matched epistemic qualification and the forced reusable-probe battery.

R27 remains canonical. Native Zag reproduction remains mandatory before promotion.
