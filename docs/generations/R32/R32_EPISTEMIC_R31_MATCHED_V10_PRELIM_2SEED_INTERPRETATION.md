# R32 V10 preliminary — two fresh seeds (9711–9712)

Status: **REFERENCE_ONLY / PROMISING / THREE-SEED+ CONFIRMATION STILL REQUIRED**

V10 uses the actual R31 evidence/stopping machinery as A, retains persistent hypotheses + provenance + temporal/source-instability state, keeps residual `KEEP_R31 / COMMIT_CURRENT / INSPECT(source) / UNKNOWN` action values, and repairs the decision economics so `UNKNOWN` is a neutral zero-regret fallback rather than being rewarded/punished from an ambiguity classification. Observation actions pay their real cost through next-state Bellman credit.

Across fresh seeds 9711–9712 at 40 evaluations/condition:

- **core hard correctness:** D **0.9792** vs A **0.9854**
- **expanded resolvable correctness:** D **0.9783** vs A **0.9267**
- **genuine-ambiguity UNKNOWN:** D **0.6250** vs A **0.4750**
- **mean wrong commitment:** D **0.0265** vs A **0.0978**
- **cost-too-high abstention:** D **0.3250** vs A **0.2375**
- entity replacement remains strong (D mean **0.9875** vs A **0.7250**)

This is the first fresh-seed pair in the R32 matched lineage where ambiguity recognition is materially above both its matched A control and the historical R31 ~0.5717 boundary while average core-hard correctness remains above ~0.97.

## Causal classification

- V8 fresh-seed failure: active-observation credit assignment (oracle inspection target) — repaired in V9.
- V9 cost-too-high/core regression: incorrect abstention economics — repaired in V10.
- V10 current effect: **decision economics + persistent temporal/provenance uncertainty**, not a new confidence threshold or fixed probe budget.

## Important boundary

Do not yet declare the primary R32 target solved. These are two fresh seeds with 40 evaluations/condition. Seed 9712 D core-hard is 0.9667 individually, just under the ~0.97 target, although the two-seed mean is 0.9792. Run at least one more matched seed and then a harder ambiguity battery. Also, repeated reusable source-7 trials are rare in genuine-ambiguity cases; the current ambiguity gain should not be credited specifically to repeated probing until a battery forces that mechanism to be used.
