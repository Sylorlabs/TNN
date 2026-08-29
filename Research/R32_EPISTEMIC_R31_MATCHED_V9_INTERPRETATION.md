# R32 Epistemic Qualification V9 — Bellman Credit Repair, Fresh Seed 9711

Status: **REFERENCE_ONLY / RUNAWAY_FIXED / ECONOMIC-REGRET OBJECTIVE STILL WRONG**

V9 replaces V8's oracle-best inspection target with a one-step fitted/Bellman target from the observed next evidence state minus full observation cost. This fixes the reusable-source runaway: seed 9711 completed without the evaluator safety guard firing.

At 40 evaluation episodes per condition on fresh seed 9711:

- A core hard correctness: **1.0000**
- D core hard correctness: **0.9542**
- A expanded resolvable correctness: **0.9117**
- D expanded resolvable correctness: **0.9700**
- A genuine-ambiguity UNKNOWN: **0.4500**
- D genuine-ambiguity UNKNOWN: **0.6500**
- A mean wrong commitment: **0.1191**
- D mean wrong commitment: **0.0441**
- A cost-too-high abstention: **0.2000**
- D cost-too-high abstention: **0.0250**
- D entity-replacement correctness: **0.9750** vs A **0.4500**

## Causal classification

1. **V8 runaway:** confirmed active-observation credit-assignment bug; V9 repairs it.
2. **Remaining cost-too-high failure:** regret/economic objective bug. Current `UNKNOWN` utility is negative whenever delayed future evidence eventually forms a unique consensus. That incorrectly treats eventual resolvability as proof that another observation was worth its current cost. In `cost_too_high`, the decisive source costs 2.40, but the target still penalizes abstention because delayed supervision eventually identifies a unique outcome.
3. **Core-hard 0.9542:** below the retained ~0.97 frontier and therefore not acceptable. With only 40 evaluations/condition this needs confirmation, but no further V9 replication is justified before correcting the structurally wrong abstention economics.

## Next repair

Keep the R31 anchor, persistent hypothesis population, provenance dependence, temporal/source-instability features, and reusable grounded observation. Replace ambiguity-dependent abstention reward with a neutral generic abstention action value. Correct commits are rewarded from delayed grounded outcomes, wrong/non-unique commits are penalized, observation actions pay their real costs, and `UNKNOWN` is the zero-regret fallback. Then fitted action values decide whether another observation has positive net value. No ambiguity label, condition ID, fixed confidence threshold, or runtime probe count enters the learner.
