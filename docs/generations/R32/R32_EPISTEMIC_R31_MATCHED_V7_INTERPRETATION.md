# R32 Epistemic Qualification V7 — Temporal Instability Development Result

Status: **REFERENCE_ONLY / PROMISING / INDEPENDENT_SEEDS_REQUIRED**

V7 keeps the V6 residual action-value controller and adds persistent hypothesis-trajectory instability plus within-modality/lineage disagreement. On seed 9710, core hard correctness remains **0.9875** versus A **0.9917**, expanded resolvable correctness improves **0.9092 -> 0.9750**, and genuine-ambiguity UNKNOWN improves **0.5500 -> 0.6500**. Mean wrong commitment falls **0.1243 -> 0.0412**.

The +0.10 ambiguity gain is larger than V6's development gain while keeping hard correctness above the R31 ~0.97 frontier. This is the first evidence that preserving *how the hypothesis population moves over time*, rather than only its current mass, may be the missing epistemic signal.

## Causal classification

**Representation/evidence-instability repair**, with unchanged residual-Q decision formulation. V6 established that decision policy could preserve hard performance but did not robustly improve ambiguity. V7 changes only generic epistemic state features, so any replicated ambiguity improvement is attributable to temporal/source disagreement representation rather than new thresholds or probe budgets.

## Remaining boundary

The cost-too-high condition still under-abstains (D 0.075 vs A 0.150 on this seed). Do not tune that before checking whether V7's ambiguity effect replicates. All quantitative claims remain REFERENCE_ONLY; R27 remains canonical pending native Zag qualification.
