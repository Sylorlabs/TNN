# R32 E51AE — hardcoding ledger

Date frozen: 2026-08-31

## Generic / verifier-side constants retained

- Fresh evaluator stages 97/98/99 and their fixed episode counts are partition identifiers, not learner inputs.
- Resource ceilings and existing E45/E51 verifier mechanics are inherited generic experimental substrate.
- Candidate action indices 0/1 are the pre-existing generic `COMMIT(candidate)` action interface, not task object IDs or benchmark answers.
- Consequence units `+1000 / -2000 / -1200` are the already-preregistered grounded action-value scale.
- UNKNOWN is fixed at exactly zero as a safety/reference action and has no learned parameter.
- Local coordinate-sweep ceilings 96 and 384, four critical rounds, and the deterministic replication rule are preregistered resource/dose controls.

## Explicitly not hardcoded into cognition

No grammar, vocabulary, semantic category, benchmark answer, task-specific object ID, social rule, ambiguity label, evaluator truth, mode identity, resource identity, stage/world identity, validation membership, or task solution is a learner feature or parameter.

The E51AE support classes and grounded targets are evaluator-only training/evaluation bookkeeping. Selected training records have target/evaluator fields 34–37 zeroed before fitting. The learner sees only the inherited 32 evaluator-blind terminal features.

No graph or topology preference is introduced. The frozen routing partition is inherited unchanged from the prior native lineage.
