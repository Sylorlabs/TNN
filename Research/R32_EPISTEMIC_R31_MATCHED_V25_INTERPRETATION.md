# R32 V25 — Pairwise INSPECT Advantage Diagnostic

Status: **REFERENCE_ONLY / RANKING_SIGNAL_STRONG / UTILITY_CALIBRATION_REJECTED**

V25 changes the target from an absolute INSPECT Q to the delayed grounded advantage of a source-specific INSPECT action over the best available delayed terminal action. The classifier ranks beneficial observations strongly (ROC-AUC **0.8989**), but positive advantage is extremely rare on the inherited random action-transition distribution (**1.70%** of validation rows).

The global class-mean utility conversion therefore fails: even truly positive-advantage rows receive mean predicted expected advantage **-0.891**, and only **0.43%** of actually beneficial rows cross zero. The direct regressor has lower MSE but weak advantage ranking (AUC **0.618**).

## Causal classification

**Developmental action-distribution / credit mismatch**, not epistemic architecture failure. Training contains many random low-value evidence actions, while runtime repeatedly considers a particular reusable consequence action in high-uncertainty states. The rare-positive distribution makes a global positive/nonpositive mean an invalid conditional utility estimate.

## Decision

- Retain pairwise action advantage as the correct comparison target.
- Reject V25's global class-mean expected-advantage conversion.
- Do not harden this runtime formulation.
- Next: build candidate-selected reusable-source development data, then learn a two-part conditional utility model: P(advantage>0 | state/action), E[advantage | positive,state/action], and E[advantage | nonpositive,state/action]. Runtime chooses another reusable observation only when the resulting learned expected advantage over terminal utility is positive. No confidence threshold or fixed probe count.
