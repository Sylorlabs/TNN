# R32 E51AG — Current Residual Replication / Generalization Audit Preregistration

**Status:** Frozen corrected preregistration.

**Correction boundary:** This file supersedes the first preregistration draft committed at `e7924cd7a66dff3f579b1cd60010d2991fbce8aa`. That draft accidentally copied stale E51AE ledger numbers from a handoff summary. The correction below is derived from the preserved native artifact and Actions transcript for run `33452596868`, job `99685597571`. This correction is being committed **before any E51AG implementation exists and before any E51AG validation replica executes**. No E51AG outcome was available when these values were frozen.

## Question

The independently reproduced E51AE native treatment was a valid negative on sealed stage 98: the frozen slot+direct union reached `5260/5400`, while each learned residual arm reached `5132/5400`. E51AG asks whether that total-reachability regression is stable under unused world/RNG partitions or specific to stage 98.

E51AG does **not** reopen stage 98, tune the residual learner, or rehabilitate the invalid historical E51AF lineage. It reconstructs the current E51AE stage-97 learner exactly and audits unchanged treatments on fresh partitions.

## Frozen source lineage

The cognitive source is the six current E51AE native fragments, pinned by Git blob identity:

- `Research/R32_E51AE_NATIVE/01a_contract_selection.zagfrag` — `7881bf966d0a41dbb01abca61be438446b58ea77`
- `Research/R32_E51AE_NATIVE/01b_objective_fit.zagfrag` — `dcf6a244c1589b56065d2ce3349827de55777ac7`
- `Research/R32_E51AE_NATIVE/01c_evaluation.zagfrag` — `e739fb1c5f3529ceda2f8edd7a66d96891c9b71e`
- `Research/R32_E51AE_NATIVE/02a_run_direct.zagfrag` — `d056a87e525699d1f7532bdc4a01b22af386a7ea`
- `Research/R32_E51AE_NATIVE/02b_run_development.zagfrag` — `f2bc7df4e5211962ccf7d6159eb4f6ecb7ae5652`
- `Research/R32_E51AE_NATIVE/02c_run_local.zagfrag` — `2157436269c77126a3a1a606b3bdd9c8be837f34`

Assembly may only perform deterministic `E51AE/e51ae` namespace substitution plus frozen stage substitution (`98 -> 104`, `99 -> 107`) and append the separately preregistered E51AG replication tail. The E51AE stage-98 validation tail is excluded. Python is assembly/infrastructure only; all learner reconstruction and evaluation remain native Zag v2.

For provenance, the source actually executed in E51AE run `33452596868` had fragment SHA-256 `9d4ecc675e0c57e50c07deef22a2e86f57810110c588a8833a24a4192cf291c8`, assembled-source SHA-256 `dea2368cc3795b8e547a454f8d10f5f7db9613107753fb443e57f7e70484ecf1`, and binary SHA-256 `4a562e967341f8b14fd3f5ef8e1b76b8517856dd08f3f81bca4a79ffbf026b94`.

## Frozen learner reconstruction target

Before any E51AG replica is interpretable, native reconstruction must reproduce the stage-97 E51AE ledger exactly:

- development episodes: `12960`
- development states: `220320`
- slot-covered: `12355`
- direct-required: `289`
- union-neither-known: `315`
- union-neither-no-unique: `1`
- frozen union development: `12644`
- neither replication factor: `1`
- expected/observed critical records: `605`
- critical selection trace: `354012291`
- critical record/target hash: `841951745`
- critical record-isolation gate: `1`
- candidate-0 residual support signs: `297 positive / 308 negative / 0 neutral`
- candidate-1 residual support signs: `302 positive / 303 negative / 0 neutral`
- global candidate-0 fit: `32,2,547504260,254939881,identity=1`
- global candidate-1 fit: `32,2,444148704,274963742,identity=1`
- global development: `preserve=12135`, `rescue=230`, `margin_loss=6272814`, development gate `0`
- local-96 final development: `preserve=12135`, `rescue=230`, `margin_loss=6272814`, development gate `0`, forward/reverse identity `1`
- local-384 final development: `preserve=12135`, `rescue=230`, `margin_loss=6272814`, development gate `0`, forward/reverse identity `1`
- terminal frozen hash before/after training: `238967492`
- direct frozen hash before/after training: `1790306570`
- pre-validation integrity gate: `1`

The learned treatments' development gates being `0` are part of the frozen parent result, not a reason to alter the learner. E51AG is specifically auditing whether the same frozen behavior generalizes across fresh partitions.

Any disagreement in source identities, the values above, world/domain integrity, forward/reverse fit identity, target isolation, or frozen-controller hashes makes E51AG `INVALID_E51AG_INTEGRITY_FAILURE` before replica interpretation.

## Fixed treatments

0. frozen mature-slot + frozen direct-candidate union control
1. frozen global trajectory-critical residual
2. frozen local-96 trajectory-critical residual
3. frozen local-384 trajectory-critical residual
4. evaluator direct-action oracle, non-deployable diagnostic

No arm trains or changes parameters after stage-97 reconstruction. UNKNOWN remains exactly zero with no learned head. No router, topology, graph, task ID, mode/resource identity, ambiguity label, evaluator truth, hidden validation membership, or benchmark answer enters learner-visible state.

## Fresh partitions

Three validation replicas are frozen:

- A: stage `104`, `5400` episodes, `91800` states, `20` episodes/cell
- B: stage `105`, same allocation
- C: stage `106`, same allocation

Expected composition per replica is `4200` known and `1200` no-unique. Stage `98` must not execute anywhere in E51AG.

Stage `107` is sealed confirmation: `10800` episodes, `183600` states, `40` episodes/cell. It executes only if the **same learned arm** 1–3 is exact on A, B, and C.

## Frozen decision rules

For every replica, report all five arms plus mode/resource reachability.

### `CURRENT_RESIDUAL_REPLICATION_EXACT`
The same learned arm 1–3 reaches `5400/5400`, `4200/4200` known, and `1200/1200` no-unique on A, B, and C. The lowest-numbered such arm alone proceeds to stage 107. Confirmation must reach `10800/10800`, `8400/8400` known, and `2400/2400` no-unique with all integrity gates exact.

If the all-three exact arm fails stage 107, report `CURRENT_RESIDUAL_REPLICATION_EXACT_NOT_CONFIRMED`.

### `CURRENT_RESIDUAL_REPLICATION_STABLE_IMPROVEMENT`
No all-three exact winner exists; the same learned arm beats arm 0 in total reachability on A, B, and C; that arm preserves `1200/1200` no-unique on all three; and its known reachability is not below arm 0 on any replica. Confirmation remains sealed.

### `CURRENT_RESIDUAL_REPLICATION_STABLE_NEGATIVE`
No learned arm beats arm 0 in total reachability on **any** of A, B, or C. Confirmation remains sealed.

### `CURRENT_RESIDUAL_REPLICATION_UNSTABLE`
Integrity is valid, but none of the exact, stable-improvement, or stable-negative rules apply.

### `INVALID_E51AG_INTEGRITY_FAILURE`
Any frozen source/reconstruction/world/model/evaluation integrity gate fails. Replica performance is then not scientifically interpretable.

## Interpretation boundary

This is a no-parameter-change replication/generalization audit of one residual mechanism. It cannot establish AGI, proto-AGI, consciousness, or inevitable scaling. A stable negative closes this residual-support line and supports escalation toward learner-owned prototype/local memory or a more fundamental representation/routing redesign. Stable improvement or instability instead establishes partition sensitivity to diagnose in a new preregistered experiment without tuning on these sealed replicas.
