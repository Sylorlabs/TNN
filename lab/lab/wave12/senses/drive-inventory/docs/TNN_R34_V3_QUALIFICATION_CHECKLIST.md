# R34 v3 qualification checklist

This checklist is the exact closeout sequence for the isolated R34 v3 learner lane.

## Source boundary

- [ ] `r34_learner_core.zag` imports the observation layer only.
- [ ] No learner-core import of `world.zag` or `checkpoint.zag`.
- [ ] No `cw_` calls or `CWOutcome` references in learner core.
- [ ] Hidden regime and reward production remain harness/world owned.
- [ ] No Python or foreign ML runtime used for qualification.

## Native build and behavior

- [ ] compiler hash equals `3093d12dba9cc81b1dee69d2d4e604158d093b58f8f01ddab26c0f4297029956`
- [ ] native compile succeeds with zero external build tools
- [ ] baseline A = 8/16
- [ ] trained A = 16/16
- [ ] trained B = 16/16
- [ ] latent contexts = 2 represented by context mask/value 3
- [ ] return A = 15/16
- [ ] return evaluation performs no score/count updates
- [ ] total A+B updates = 48
- [ ] update-disabled B control = 0 updates, 12/24 positive
- [ ] reward-scrambled A control = 0/16 actual positive after training
- [ ] deterministic learner/world/ingress replay exact
- [ ] learner encode/decode round trip exact

## Persistence and causal continuity

- [ ] checkpoint is captured while delayed reward is pending
- [ ] fresh-process reload reproduces uninterrupted continuation exactly
- [ ] inner learner corruption refused after recomputing outer digest
- [ ] torn outer checkpoint refused
- [ ] learner, world, ingress, and pending causal fields are all represented in checkpoint state

## Evidence freeze

- [ ] `RECEIPT.txt` says `failures=0`
- [ ] `scientific_exposure=0`
- [ ] `canonical_r27_mutated=false`
- [ ] `learner_authority_granted=false`
- [ ] `learn_opened=false`
- [ ] `successor_promoted=false`
- [ ] source, compiler, binary, command, stdout/stderr, exit-code, and artifact hashes frozen
- [ ] resource telemetry recorded

R34 v3 remains an engineering witness until every box is backed by the frozen evidence directory.
