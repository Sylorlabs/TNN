# R32 E51Z — Resource-Constrained Stopping-State Oracle Audit Result

Date executed: 2026-08-30/31
Branch: `r32-agent-sequential-frontier`
Native result: **VALID DIAGNOSTIC — `MIXED_STOPPING_FAILURE`**
Canonical status: **R27 remains canonical.**

## Native authority

- GitHub Actions run: `33360243129`.
- source head: `1051465b88cdd4252b98dbd1b7854fccff530392`.
- evidence artifact id: `9746666407`.
- artifact ZIP SHA-256: `493b5149f9f56f02503b0006986777a29f8c28ec5c244a09c422e997347d4da8`.
- assembled native source SHA-256: `7cff04abca9a7b229d1b1c50f3a2b64f6f35b882cb79fea3522efc076e233498`.
- E51Z audit fragment SHA-256: `1942afc4949fd3aa549a329381f941363f708c0908961b218e4deb1b0af13b04`.
- E51Z injection SHA-256: `7bec2104b3dcf22a16545e8319adc8c550c506b17351b5b57507a0d9c3c79428`.
- assembly script SHA-256: `6a5d18ab919c4df64f5cbe5fa3d24c41fbf303d18690460781a8d9c7eb3a5619`.
- frozen E45 core SHA-256: `6812efb4c2cb990a59bd0f33f0a44469950201cac6633099fa4f4b2c7ae276e0`.
- native binary SHA-256: `60f765e4350d8aa11a6b2b05fcfdcdcc36b46b4b480ae21ccdca61bf103381bf`.
- two native builds byte-identical: PASS.
- native exit code: 0.
- native execution runtime: about 713 s.

## Integrity

- E50 parent integrity: PASS.
- E51Y terminal reproduction: 4,200 / 4,200 known + 1,200 / 1,200 no-unique: PASS.
- E51Y training integrity: PASS.
- stage-87 worlds: `87,000,000 .. 87,005,399`.
- world partition gate: PASS; domain gate: PASS; assignment failures: 0.
- audit episodes: 5,400; audit states: 91,800.
- learner updates during stage 87: 0.
- terminal parameter hash before/after: `238967492` / `238967492`.
- continuation parameter hash before/after: `1588117845` / `1588117845`.
- frozen-parameter gate: PASS.
- evaluator truth/oracle/bucket information exposed to learner: none.
- topology changed: no; graph privileged: no.
- overall E51Z integrity: PASS.

## Finding 1 — E51X reachability does not survive the resource path exactly

Every fresh audit trajectory still contains a successful terminal state somewhere when the full 17-state tape is enumerated:

- full-trajectory successful terminal reachability: **5,400 / 5,400**.

But E51Y cannot necessarily reach all of those states before observation becomes infeasible:

- cost-feasible successful terminal reachability: **5,074 / 5,400**;
- missing: **326 / 5,400**;
- missing known: **319 / 4,200**;
- missing no-unique: **7 / 1,200**.

Therefore the strict E51Y no-unique zero-wrong gate is structurally impossible for at least seven fresh no-unique trajectories under the frozen E51X terminal learner and E51Y resource transition geometry. This is a new, narrower terminal-reachability veto: not unconstrained state reachability, but **resource-constrained terminal reachability**.

The sum of first successful state indices was 8,240 over all 5,400 episodes, while the sum of last resource-feasible state indices was 48,743, confirming substantial but heterogeneous feasible horizons rather than one fixed observation cutoff.

## Finding 2 — scalar utility and strict success/safety are not aligned

The unconstrained utility-optimal stopping oracle achieved total grounded utility **2,367,895**, but only **4,394 / 5,400** of its chosen terminal stops were grounded-successful.

On no-unique episodes:

- utility-oracle unsafe commits: **49**;
- unsafe utility-optimal commits even though a resource-feasible safe UNKNOWN stop existed: **42**.

The safety-constrained success oracle covered 5,074 episodes and accumulated utility **1,682,092** over those covered trajectories.

At the state level:

- reachable states where continuing was required to preserve access to a later grounded-successful stop: **17,592**;
- states where that success-preservation requirement said CONTINUE but E51Y's exact scalar utility advantage was `<= 0` and therefore its binary target said STOP: **2,328**;
  - known: **1,995**;
  - no-unique: **333**.

Thus E51Y's training objective is not merely imperfectly fitted. On thousands of reachable states, its finite scalar utility target explicitly conflicts with the capability/safety requirement later imposed by validation.

## Finding 3 — no exact continuation representation alias was found

Across all **91,800** fresh continuation states:

- exact duplicate effective 32-feature rows: **0**;
- exact utility-advantage conflict keys: **0**;
- exact utility-advantage conflict rows: **0**;
- exact success-preservation conflict keys: **0**;
- exact success-preservation conflict rows: **0**.

So the observed failures cannot be attributed to two evaluator-distinct stopping requirements collapsing to one identical learner-visible continuation vector on this audit population.

## Finding 4 — the learned continuation heads also have large calibration error

Fresh stage-87 policy totals:

| Arm | Utility | Oracle regret | FP CONTINUE | FN CONTINUE | Known success | Known wrong | No-unique UNKNOWN | No-unique wrong |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| t0 terminal control | 925,000 | 1,442,895 | 0 | 0 | 1,221 | 25 | 995 | 205 |
| linear CONTINUE | 570,337 | 1,797,558 | 1,294 | 1,608 | 2,112 | 275 | 725 | 475 |
| local CONTINUE-96 | 438,170 | 1,929,725 | 912 | 1,219 | 2,483 | 477 | 916 | 284 |
| local CONTINUE-384 | 440,951 | 1,926,944 | 909 | 1,227 | 2,472 | 475 | 916 | 284 |

The local heads reduce classification mistakes relative to the global linear policy in some regions but remain very far from the oracle stopping policy and still lose net utility versus the t0 control.

Magnitude auditing also shows errors are not confined to near-zero advantages. For example, the local-384 learner misclassified **8,762** states in the `> +500` exact-advantage bucket and **798** states in the `<= -500` bucket over resource-accessible audit states. Binary sign supervision plus the tested local fit therefore does not adequately approximate the exact stopping value surface.

## Causal classification

E51Z flags three real failure classes simultaneously:

1. **resource-constrained terminal reachability veto**;
2. **utility/success-safety objective conflict**;
3. **continuation value calibration error**.

Exact representation conflict was not observed.

The frozen outcome is therefore `MIXED_STOPPING_FAILURE`.

## Next binding sequence

The resource-constrained terminal veto must be repaired before a five-way sequential policy can satisfy the strict safety gate. The next experiment should keep the same 32-feature non-graph terminal substrate and first audit/optimize terminal success **inside the resource-feasible prefix**, not over the unconstrained full tape.

After cost-feasible terminal success is exact, continuation should be retrained with a trajectory-level success-preservation objective that treats preserving access to a grounded-optimal terminal action as the primary criterion and observation utility/cost as the secondary criterion. This is the same capability-first principle that made E51V–X successful and avoids encoding evaluator ambiguity labels into learner state.

No dynamic graph/cross-context connectivity is justified by E51Z. No R32 promotion or AGI/consciousness claim is supported.