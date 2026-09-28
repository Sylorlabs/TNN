# R32 Epistemic Qualification V5 — Development Diagnostic

Status: **REFERENCE_ONLY / DECISION_CALIBRATION_OVERABSTENTION**

The R31-matched control remains strong on this development seed: A core hard correctness is **0.9917** with genuine-ambiguity abstention **0.5500**. B is numerically identical to A by design because persistent hypotheses were added without changing the inherited R31 stopping policy. This is the required causal isolation: the representation alone does not destroy the R31 behavior.

C adds provenance/dependence discounting but keeps the A decision policy. On this seed it changes core hard correctness only from **0.9917** to **0.9917** and ambiguity remains **0.5500**. This small development sample does not justify accepting or rejecting provenance dependence yet.

D materially improves epistemic behavior in some dimensions: ambiguity UNKNOWN rises from **0.5500** to **0.8500** (+0.3000), entity-replacement switch correctness rises from **0.3000** to **0.9875**, and mean wrong commitment falls from **0.1243** to **0.0324**. But core hard correctness collapses from **0.9917** to **0.6937** (-0.2979) and unnecessary abstention rises to **0.1583**.

## Causal classification

**Decision-policy / delayed-regret calibration: excessive abstention.** The persistent/provenance state is not rejected: B proves the state can coexist with inherited R31 behavior. The failure appears when D assigns action utilities to COMMIT / INSPECT / UNKNOWN. The current utility asymmetry penalizes a wrong commit far more strongly than an unnecessary UNKNOWN on a later-resolved case, so the learner can reduce wrong commitments by abstaining too often.

## Decision

- Retain the persistent hypothesis representation.
- Retain provenance and temporal/replacement features as candidates.
- Reject the current D action-value calibration.
- Do not respond with a new arbitrary confidence threshold or fixed probe count. Reweight delayed regret causally: make UNKNOWN on later-resolved experience carry substantial regret, while keeping UNKNOWN rewarded when two delayed grounded windows remain non-resolving. Then rerun the same matched seed before multi-seed confirmation.
- Quantitative claims remain REFERENCE_ONLY until native Zag execution succeeds.
