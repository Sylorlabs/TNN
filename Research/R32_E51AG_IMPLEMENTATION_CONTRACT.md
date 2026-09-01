# R32 E51AG — Implementation Contract

**Parent preregistration:** `Research/R32_E51AG_CURRENT_RESIDUAL_REPLICATION_PREREG.md`

## Frozen implementation

E51AG is a no-parameter-change replication audit of the successfully executed current E51AE lineage. It must not re-run E51AE stage 98 or alter the residual learner.

The assembler verifies the preregistration and six parent E51AE native fragments by Git blob SHA, then performs only deterministic namespace/stage substitutions:

- `E51AE/e51ae` -> `E51AG/e51ag`
- parent validation constant `98` -> replica-A stage `104`
- parent confirmation constant `99` -> sealed confirmation stage `107`
- schema/claim strings -> E51AG replication labels

The parent E51AE `02d_run_validation.zagfrag` is deliberately excluded. E51AG appends only its new replication contract and fresh-partition evaluation tail.

## Native reconstruction gate

Before any replica opens, native Zag must reproduce the frozen E51AE stage-97 state recorded in the corrected preregistration, including the exact 605-record critical set, selection trace/hash, global fit traces/losses, development outcomes, forward/reverse identities, and frozen terminal/direct hashes.

A failed reconstruction prevents all replica evaluation and produces `INVALID_E51AG_INTEGRITY_FAILURE`.

## Evaluation

Replicas A/B/C are stages 104/105/106, each 5400 episodes at 20/cell. The same five frozen arms are reported on every replica. No training function is called after stage-97 reconstruction.

Stage 107 confirmation remains unallocated computationally unless the same learned arm is exact on all three replicas. Only that lowest-numbered exact arm is evaluated at confirmation.

## Scientific immutability

Validation/confirmation results may not cause source changes to this implementation. Any infrastructure/compiler failure before native replica exposure may be repaired without changing the frozen treatment. Once any fresh replica output is exposed, treatment changes require a new experiment identifier/preregistration.

Python is restricted to source identity verification and deterministic assembly. Promotable cognition and evaluation policy remain native Zag v2.
