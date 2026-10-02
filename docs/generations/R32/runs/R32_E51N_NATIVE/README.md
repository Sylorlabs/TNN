# R32 E51N Native Support Layer

This directory contains the compiler-checked native support layer for the preregistered E51N calibration-frontier replication. It does not execute the empirical learner and does not promote R32. R27 remains canonical.

## Expanded evaluator namespace

E51N assigns every executable episode one globally unique ordinal across three replicas. Each replica has 6,480 development episodes followed by 5,400 validation episodes, for 11,880 worlds per replica and 35,640 executable worlds total.

The shared transport maps `(ordinal, domain)` to `2,000,003 + ordinal × 16 + domain`. The five evaluator-only domains use residues 1, 3, 5, 7, and 9 for truth, history, passive evidence, active evidence, and resource state. Invalid replicas, partitions, indices, ordinals, and domain residues are rejected with `-1`.

`01_namespace_gate.zagfrag` proves the frozen counts, disjoint replica/partition ranges, domain separation, boundary mappings, exclusion of the historical tied-seed tuple form, signed-32-bit safety, and zero confirmation execution. The proof calls the same `e51n_world_ordinal` and `e51n_world_component_id` functions intended for the empirical driver.

## Shared frozen replication reducer

`04_replication_reducer.template.zagfrag` is materialized with the exact function-declaration dialect detected from the compiled native lineage. The empirical driver must call these functions rather than reimplement the decision rule:

- `e51n_pareto_pass`: neither reachability dimension decreases and at least one increases strictly;
- `e51n_replication_gate`: at least two of three replicas pass and the pooled counts pass;
- `e51n_contrast_replicated`: accepts raw known/no-unique base and treatment counts for all three replicas, computes replica and pooled decisions internally, and returns the frozen contrast decision;
- `e51n_arm_count_pair_valid`: rejects impossible validation counts;
- `e51n_exact_arm_pass` and `e51n_replica_any_exact`: implement the diagnostic exact-arm gate;
- `e51n_frozen_outcome_code`: maps integrity and the three preregistered contrast decisions to the five frozen E51N outcomes.

## Native self-tests

The namespace-only executable tests valid and invalid partition addressing, component-domain guards, positive and negative replication cases, positive and negative raw-count reduction, count bounds, exact-arm scanning, all four scientific outcome codes, and integrity failure. These tests validate implementation semantics only; they are not empirical E51N results.

## Assembly and CI

`.github/scripts/e51n_namespace_assemble.py` builds the frozen E51X/E51Y/E51AB lineage only as a syntax/runtime substrate, detects its exact Zag function declaration dialect, replaces the expensive main body with the E51N proof and self-tests, and writes the assembled source plus materialized transport/reducer evidence.

`.github/workflows/r32-e51n-namespace-native.yml` hashes all inputs, compiles twice with the persisted official Linux x86-64 Zag compiler, requires byte-identical binaries, executes the native gate, requires every frozen marker, and uploads the complete evidence set.

## Shared integrity contract

`05_integrity_contract.template.zagfrag` converts the remaining preregistered integrity requirements into reusable native gates. It fixes the per-replica episode composition, requires UNKNOWN targets and parameters to remain zero, requires both positive and negative sign targets, makes confirmation non-executable even after an exact validation result, and combines the twelve parent/namespace/determinism/blindness/nondegeneracy flags into one integrity decision. The empirical runner must supply measured flags to this contract before any scientific outcome code is emitted.

## Scientific outcome emission boundary

`06_outcome_emitter.template.zagfrag` is the sole native mapping from the frozen outcome code to E51N scientific result markers. It also emits the three contrast decisions and the diagnostic exact-arm flag. The support executable calls the outcome emitter only with invalid code `99`, which must return zero and emit no scientific marker; valid scientific markers can therefore appear only in the future empirical runner after measured integrity and validation decisions are available.

## Fixed arm schedule

`07_arm_schedule.template.zagfrag` assigns stable integer arm IDs: `0=BASE`, `1=D1C0`, `2=D1C4`, `3=D2C0`, and `4=D2C4`. It provides the frozen dose and hinge count for each arm and maps the 1× dose to 3,240 development episodes and the 2× dose to 6,480. Invalid arm and dose IDs return `-1` or fail the arm contract. The support executable exhaustively checks the complete five-arm table.

## Exhaustive namespace audit

`08_exhaustive_namespace_audit.zagfrag` enumerates all 35,640 executable ordinals and all five component domains in native Zag. It requires the resulting 178,200 component IDs to be globally strictly increasing, verifies the exact count, and freezes checksum `162379` modulo 1,000,003. This runtime enumeration is independent of the boundary checks and uses the same guarded transport functions as the future empirical driver.

## Frozen learner-facing constants

`09_learning_contract.template.zagfrag` fixes the inherited E51M task definition: 32 terminal features, UNKNOWN value exactly 0, correct commit value +1000, no-unique commit value -1200, wrong commit value -2000, and at most four hinge terms in the capacity arms. Its native contract rejects any altered value. This module does not expose evaluator identity or add a feature; it constrains the future runner to the preregistered state and utility geometry.
