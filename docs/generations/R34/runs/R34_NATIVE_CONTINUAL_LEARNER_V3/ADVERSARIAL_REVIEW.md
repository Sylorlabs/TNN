# R34 V3 adversarial review

This review records the failure modes the V3 qualification must actively exclude. It is an engineering review of a bounded continuing-world learner, not a scientific or general-intelligence claim.

## Hidden-state leakage

The learner core must remain structurally unable to access evaluator-owned world state. `r34_learner_core.zag` may import the observation contract and shared bounded primitives. It must not import `world.zag` or `checkpoint.zag`, call `cw_*`, reference `CWOutcome`, read a regime variable, or own world/checkpoint transport sizes. The evaluator harness owns regime changes, world stepping, reward delivery, persistence orchestration, and scoring.

The static isolation check is mandatory because behavioral success alone cannot prove absence of evaluator leakage.

## Reward and answer leakage

Object choice is made before the outcome is observed. The learner receives a scalar delayed outcome only after a touch action has been recorded. Credit must be refused unless the delivered action id exactly matches the pending initiating action id. The learner must not receive the hidden regime or the evaluator's preferred object as a feature.

The reward-scrambled control is required to demonstrate that acquisition depends on the sign of experienced outcomes. The update-disabled control is required to demonstrate that the training result is not produced by the harness alone.

## Continual-learning illusion

The A -> B -> A sequence can be gamed by a single overwritten policy. V3 therefore requires a second latent context to be allocated after outcome surprise and requires the earlier A behavior to be reused on return. Return evaluation must occur without score/count updates so the retained behavior cannot be relearned during the measurement window.

The first return probe is expected to expose the hidden switch, so the preregistered retained-A score remains 15/16 rather than pretending the learner can infer an unobserved regime change before evidence arrives.

## Persistence illusion

Serialization of learner weights alone is insufficient. The outer checkpoint must carry learner state, pending causal credit, world state, and ingress state together. Qualification must checkpoint while delayed credit is pending, reload in a fresh process, and require exact continuation against uninterrupted execution.

An attacker can recompute an outer checkpoint digest after corrupting the learner section. The inner learner-state digest must independently detect that corruption. A torn outer checkpoint must also be refused.

## Determinism and replay

Equal learner seed, world seed, and experience stream must produce exact learner state, exact world bytes, and exact ingress state. Determinism is an engineering property used for diagnosis; it is not treated as evidence of intelligence.

## Claim boundary

Passing V3 supports only the bounded claims exercised here: native online adaptation from observations and delayed scalar outcomes, delayed causal credit, latent-context retention/reuse, deterministic replay, and complete-state fresh-process continuation. It does not establish general perception, language competence, broad transfer, scaling behavior, or superiority to an LLM.

