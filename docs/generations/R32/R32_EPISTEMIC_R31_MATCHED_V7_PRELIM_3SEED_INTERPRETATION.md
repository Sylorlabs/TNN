# R32 V7 Preliminary Multi-Seed Read

Status: **REFERENCE_ONLY / TEMPORAL_STATE_RETAINED / PRIMARY_AMBIGUITY_TARGET_ONLY_MODESTLY_IMPROVED**

Across seeds 9710-9712, V7 D averages core hard correctness **0.9881** versus A **0.9833**, expanded resolvable **0.9768** versus A **0.9168**, wrong commitment **0.0465** versus A **0.1075**, and entity-replacement correctness **0.9817** versus A **0.5900**.

Genuine-ambiguity UNKNOWN rises from A **0.5433** to D **0.5833** (+0.0400). That is directionally better and slightly above the historical R31 ~0.5717 boundary, but not yet a substantial enough gain to declare the primary R32 target solved.

## Causal classification

The temporal/source-instability representation is **retained** because it adds ambiguity signal without sacrificing the ~0.97 hard frontier, and V6 showed less ambiguity improvement with the same residual-Q controller. The residual error is now primarily **poor active observation / insufficient persistent evidence sampling**: genuine ambiguity has only three one-shot physical sources in this harness. When the finite samples happen to agree by chance, the state cannot infer non-uniqueness reliably even though later held-out consequences remain unstable.

## Next experiment

Do not add a confidence threshold. Give the policy a reusable physical-consequence observation action whose repeated trials have explicit provenance/dependence and cost, allowing it to decide from expected value whether another independent trial is worth acquiring. Track realized information gain and source-outcome instability. Compare one-shot physical sources versus reusable consequence probes on the same delayed-regret objective. This directly tests whether the remaining ~0.58 ambiguity ceiling is active-observation-limited rather than representational.

Cost-too-high abstention also remains weak and should be evaluated jointly, because reusable probes must stop when expected information gain is below cost.
