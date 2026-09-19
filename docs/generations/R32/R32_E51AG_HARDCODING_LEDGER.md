# R32 E51AG — Hardcoding Ledger

E51AG adds no task solution, semantic category, benchmark answer, grammar/vocabulary rule, social rule, evaluator truth feature, ambiguity label, task ID, mode/resource identity, or validation-membership feature to the learner.

## Allowed frozen constants

The following are verifier/infrastructure constants and are not learner-visible cognitive knowledge:

- parent source Git blob identities;
- exact stage-97 reconstruction ledger values;
- fresh stage identifiers 104/105/106 and sealed confirmation stage 107;
- episode/cell allocations and expected known/no-unique counts;
- exact/stable-improvement/stable-negative outcome thresholds;
- compiler/source hashes and byte-identity gates;
- resource ceilings and workflow timeouts.

The exact reconstruction numbers are used only to decide whether the frozen parent was reproduced before evaluation. They are never fed to policy features, residual heads, candidate scores, slot scores, or action selection.

## Learner-visible state

Unchanged from E51AE:

- existing 32 evaluator-blind terminal features;
- frozen mature-slot controller;
- frozen E51AB direct-candidate controller;
- frozen E51AE residual heads reconstructed from stage 97;
- UNKNOWN fixed to exactly zero with no learned UNKNOWN head.

## Prohibited leakage

Stages 104–107, world IDs, evaluator correctness, no-unique labels, mode/resource identity, outcome class, replica identity, and confirmation eligibility are evaluator-only. They must not enter learner-visible records or parameters.

## Topology

No topology, graph, routing, or connection-system change is introduced in E51AG. This experiment audits generalization of the current residual mechanism only.
