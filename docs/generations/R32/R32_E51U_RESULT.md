# R32 E51U — Learner-Owned Local Interaction Foundry Result

Date executed: 2026-08-30
Branch: `r32-agent-sequential-frontier`
Canonical status: R27 remains canonical.

## Status

`VALID NATIVE NEGATIVE — NO_TESTED_LOCAL_INTERACTION_RESCUE`

E51U tested whether TNN could improve the residual commit-vs-UNKNOWN boundary by autonomously recruiting generic pairwise feature interactions inside the existing 32 learner-grown routed cells. The experiment was full native Zag v2 and did not change graph topology, commit ordering, UNKNOWN semantics, or learner-visible state.

## Native authority

- GitHub Actions run: `33348336371`
- source head: `1e06b312d0f12a2c61037fa57df17df779046205`
- artifact id: `9742857216`
- artifact digest: `sha256:db31663231ae8463ca7128412aca0c0e9b92157a59b009705d652820bb6fceba`
- assembled native source SHA256: `cdb61f960452932f7e9f189b9dc07e1456daec5d8fd4d1308df478416b99830a`
- native binary SHA256: `680c21f82be3bea72e99bf09a1e284a1cd990a9c6639e90e2bc3f589a413d5ac`
- frozen E45 core SHA256: `6812efb4c2cb990a59bd0f33f0a44469950201cac6633099fa4f4b2c7ae276e0`
- two native builds byte-identical: PASS
- native exit code: 0
- native execution runtime: about 381 s

## Integrity

- E50 parent integrity: PASS.
- stage-72/73/74 world/domain separation: PASS.
- development: 12,960 episodes / 220,320 states.
- validation: 5,400 episodes / 91,800 states.
- UNKNOWN nonzero target count: 0.
- evaluator truth exposed: 0.
- validation membership exposed: 0.
- graph privileged: 0.
- cross-cell edges added: 0.
- interaction forward/reverse identity: PASS.
- learner-selected interaction terms accepted: 64, exactly two per routed cell.
- researcher-selected feature pairs: 0.
- sealed confirmation executed: 0.

## Validation

| Arm | Mechanism | Known reachable | No-unique UNKNOWN reachable |
|---|---|---:|---:|
| A | 96-sweep conditional linear | 4,199 / 4,200 | 1,163 / 1,200 |
| B | 192-sweep conditional linear | 4,200 / 4,200 | 1,163 / 1,200 |
| C | 96-sweep + 1 local interaction/cell | 4,199 / 4,200 | 1,163 / 1,200 |
| D | 96-sweep + 2 local interactions/cell | 4,199 / 4,200 | 1,158 / 1,200 |

No interaction arm reached the exact gate or the partial-rescue gate. The two-term arm improved state-level negative-sign accuracy but worsened episode-level no-unique reachability and lost one switch/reversal trajectory relative to the 96-sweep control.

## Causal conclusion

Generic pairwise local interaction capacity is not the missing mechanism at this frontier. E51U is particularly informative because the nonlinear terms were nondegenerate, learner-selected, deterministic, and did alter the learned boundary, yet those state-level changes did not translate into a larger set of trajectories with a valid stopping action.

Combined with E51T, this indicates a mismatch between continued state-level residual fitting and the actual trajectory-level control objective. The next discriminator should therefore keep the same non-graph 32-cell architecture and test a trajectory-aware multiple-instance objective: known trajectories need at least one grounded-correct commit-capable stopping state, while trajectories whose preferred commit is harmful at every state need at least one state on the UNKNOWN side. Only if this objective change plateaus should dynamic cross-context connectivity be introduced.

No E51U result promotes R32 or establishes AGI/consciousness.