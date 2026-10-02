# R32 Epistemic Qualification V8 — Reusable Consequence Probe Development Result

Status: **REFERENCE_ONLY / STRONG_DEVELOPMENT_RESULT / INDEPENDENT_SEEDS_REQUIRED**

V8 changes only active evidence availability relative to V7: one grounded consequence experiment can be repeated as a new costly trial with the same apparatus lineage. Dependence discount remains active and the learner has no fixed probe count.

On seed 9710, D reaches core hard **0.9833** versus A **0.9917**, expanded resolvable **0.9808**, genuine-ambiguity UNKNOWN **0.8500** versus A **0.5500**, and mean wrong commitment **0.0250** versus A **0.1243**.

Crucially, the cost-too-high abstention metric also improves to **0.1625** versus A **0.1500**. This is materially better than V7, where ambiguity was only ~0.65 on this seed and cost-too-high abstention weakened.

## Causal classification

**Poor active observation / finite evidence opportunity** was a real limitation. Persistent temporal/source-instability representation plus residual Q was already sufficient to preserve hard correctness; allowing the policy to acquire another independent consequence trial when its expected value exceeds cost substantially improves no-unique-answer detection without a fixed stopping threshold.

## Boundary

Do not accept the 0.85 ambiguity value from one seed. It is high enough to trigger explicit replication and harder diagnostics. Fresh seeds must preserve ~0.97 hard correctness and show a substantial ambiguity gain; evidence cost and cost-too-high behavior must remain acceptable. Native Zag remains mandatory for promotion and R27 remains canonical.
