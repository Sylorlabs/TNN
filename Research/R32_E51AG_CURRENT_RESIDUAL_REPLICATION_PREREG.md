# R32 E51AG — Current Residual Replication / Generalization Audit Preregistration

**Status:** Frozen preregistration. This document must exist on GitHub before the E51AG native implementation is published or any E51AG validation replica is executed.

## Question

E51AE's independently reproduced native treatment was a valid negative result on sealed stage 98: the frozen slot+direct union scored `5260/5400`, while each learned residual arm scored `5132/5400`. E51AG asks whether that regression is a stable property of the reproduced learner or an idiosyncrasy of the single stage-98 partition.

E51AG does **not** reopen stage 98, does not tune the E51AE learner, and does not rehabilitate the invalid historical E51AF lineage. It reconstructs the current E51AE stage-97 learner exactly and audits it unchanged on unused world/RNG partitions.

## Frozen source lineage

The cognitive source is the six E51AE native fragments from branch state `b0a0f2d06861685569fb7fb064b5378ac05d80ed`, transformed only by deterministic namespace/stage substitution for E51AG assembly:

- `01a_contract_selection.zagfrag` Git blob `7881bf966d0a41dbb01abca61be438446b58ea77`
- `01b_objective_fit.zagfrag` Git blob `dcf6a244c1589b56065d2ce3349827de55777ac7`
- `01c_evaluation.zagfrag` Git blob `e739fb1c5f3529ceda2f8edd7a66d96891c9b71e`
- `02a_run_direct.zagfrag` Git blob `d056a87e525699d1f7532bdc4a01b22af386a7ea`
- `02b_run_development.zagfrag` Git blob `f2bc7df4e5211962ccf7d6159eb4f6ecb7ae5652`
- `02c_run_local.zagfrag` Git blob `2157436269c77126a3a1a606b3bdd9c8be837f34`

The E51AE stage-98 validation tail is excluded. Python may only verify these identities, perform deterministic namespace/stage substitution, assemble source, and package evidence. All learner reconstruction and evaluation remain native Zag v2.

## Frozen learner reconstruction target

Before any E51AG replica is interpretable, native reconstruction must reproduce the current E51AE development lineage:

- development stage: `97`
- development episodes: `12960`
- frozen slot-covered: `11920`
- direct-required: `289`
- union-neither-known: `315`
- union-neither-no-unique: `1`
- frozen union development: `12209`
- expected/observed critical records: `605`
- critical trace: `1700609257`
- critical hash: `1163026376`
- global/local fit identity gates: `1`
- frozen training gate: `1`
- global development preservation: `12209/12209`
- global rescue: `0`
- global margin loss: `862822722`
- all evaluator target fields remain isolated from learner-visible records

Any disagreement in pinned source identities, reconstruction ledger, world/domain integrity, forward/reverse fit identity, or frozen-controller hashes makes E51AG `INVALID_E51AG_INTEGRITY_FAILURE` before replica interpretation.

## Fixed treatments

The five arms are unchanged from E51AE:

0. frozen mature-slot + frozen direct-candidate union control
1. frozen global trajectory-critical residual
2. frozen local-96 trajectory-critical residual
3. frozen local-384 trajectory-critical residual
4. evaluator direct-action oracle, non-deployable diagnostic

No arm may train or alter parameters after stage-97 reconstruction. UNKNOWN remains exactly zero and has no learned head. No router, topology, graph, feature, task-ID, mode/resource identity, ambiguity label, evaluator truth, or validation membership may enter learner-visible state.

## Fresh partitions

Three independent validation replicas are frozen:

- replica A: stage `104`, `5400` episodes, `91800` states, `20` episodes/cell
- replica B: stage `105`, same allocation
- replica C: stage `106`, same allocation

Each contains exactly `4200` known and `1200` no-unique episodes under the existing generator. Stage `98` must not execute in E51AG.

Stage `107` is sealed confirmation: `10800` episodes, `183600` states, `40` episodes/cell. It executes only if the **same learned arm** (1–3) is exact on all three validation replicas.

## Frozen decision rules

For each replica, report all five arms, known/no-unique totals, mode reachability, and resource reachability.

`CURRENT_RESIDUAL_REPLICATION_EXACT`:
- the same learned arm 1–3 reaches `5400/5400`, `4200/4200` known, and `1200/1200` no-unique on A, B, and C;
- stage-107 confirmation executes for the lowest-numbered such arm;
- confirmation must reach `10800/10800`, `8400/8400` known, `2400/2400` no-unique;
- all integrity gates remain exact.

`CURRENT_RESIDUAL_REPLICATION_STABLE_IMPROVEMENT`:
- no all-three exact winner exists;
- the same learned arm beats arm 0 in total reachability on A, B, and C;
- that arm preserves `1200/1200` no-unique on all three and is not worse than arm 0 on known reachability on any replica;
- confirmation remains sealed.

`CURRENT_RESIDUAL_REPLICATION_STABLE_NEGATIVE`:
- no learned arm beats arm 0 in total reachability on any of A, B, or C;
- confirmation remains sealed.

`CURRENT_RESIDUAL_REPLICATION_UNSTABLE`:
- valid integrity, but neither exact, stable-improvement, nor stable-negative criteria hold.

`INVALID_E51AG_INTEGRITY_FAILURE`:
- any preregistered source/reconstruction/world/frozen-model/evaluation integrity gate fails. No scientific interpretation of replica performance is allowed.

If an exact all-three winner fails stage-107 confirmation, report `CURRENT_RESIDUAL_REPLICATION_EXACT_NOT_CONFIRMED` rather than promoting it.

## Interpretation boundary

E51AG is a replication/generalization audit of one frozen residual mechanism. It cannot establish AGI, proto-AGI, consciousness, or inevitable scaling. A stable negative closes this residual-support line and favors escalation toward learner-owned prototype/local memory or a more fundamental representation/routing redesign. Stable improvement or instability instead establishes partition sensitivity that must be diagnosed without tuning on these sealed replicas.
