# R32 E51AD — Trajectory-Critical Conservative Mechanism Router Result

Date executed: 2026-08-31
Branch: `r32-agent-sequential-frontier`
Native result: **VALID NEGATIVE — `TRAJECTORY_ROUTER_NO_GAIN`**
Canonical status: **R27 remains canonical.**

## Native authority

Primary authoritative execution:

- GitHub Actions run: `33412828590`.
- job: `99556260320`.
- source head: `0d2f0fd698b5967be76b3785a730d8db99ce10d3`.
- evidence artifact id: `9766544317`.
- artifact ZIP SHA-256: `f7f2d9305e6b5d0c64b565c63111270ee13ac79ec5fe73c4d0255f8ab8a311f9`.
- preregistration SHA-256: `5e0301b325423c395d294072736c26e324c68907dd5d1e97f0ae9ec03628fb9c`.
- native fragment SHA-256: `7f1764797202c9b089c6b041a8ab4e1bcfa5ee5f30a52c5d3858ff93942e5841`.
- assembled native source SHA-256: `67ac4a8412e4098a9572a248bee2be1c9b6ea9699fd52cc568e5e25e1c132314`.
- frozen E45 core SHA-256: `6812efb4c2cb990a59bd0f33f0a44469950201cac6633099fa4f4b2c7ae276e0`.
- native binary SHA-256: `4d7f72660cd1e2b613de9cfbcf16cec2fc594452640bc3835e59cb6be5a155d4`.
- raw native ledger SHA-256: `b3487d42d31a0318b6ef1e0a8aac0282401d67b090b9bda79ab1810113e9c7c1`.
- summary ledger SHA-256: `ad6c82b34e47c2ed9a348ed5f3ef992fbd48202990a88fbebd35c597999b3e31`.
- double native build byte identity: PASS.
- native execution runtime: 1,201 seconds.
- native exit code: 0.

Deterministic later reproduction after the E51N support-layer recovery commit:

- GitHub Actions run: `33442861197`.
- source head: `33b2cc0051a9e6b39c7856f7bffcd07dc73116fb`.
- evidence artifact id: `9777527306`.
- artifact ZIP SHA-256: `227df3db87d8184bd5797424c514d1fe3c4ad1fdac8803bfe1462a351b07ea6b`.
- assembled native source SHA-256: `67ac4a8412e4098a9572a248bee2be1c9b6ea9699fd52cc568e5e25e1c132314`.
- native binary SHA-256: `4d7f72660cd1e2b613de9cfbcf16cec2fc594452640bc3835e59cb6be5a155d4`.
- raw native ledger SHA-256: `b3487d42d31a0318b6ef1e0a8aac0282401d67b090b9bda79ab1810113e9c7c1`.
- summary ledger SHA-256: `ad6c82b34e47c2ed9a348ed5f3ef992fbd48202990a88fbebd35c597999b3e31`.
- double native build byte identity: PASS.
- native execution runtime: 1,231 seconds.
- native exit code: 0.

The reproduction is byte- and ledger-identical on the scientific outputs. Runtime and artifact container differ only as execution-instance metadata.

### Source component hashes

- contract/support: `09a8af8419f538aaef5c5ee81ae1c4f1493a1b2aa25f852125162ed1555a1717`.
- critical fit: `eb544a4cf08bd69c0bd46567ef8fee7c8abeaad6e5caf5d4b0a384c08f11199d`.
- policy evaluation: `e85c74d52865700833fbc14952939622b929b4e2e313188c79fff71ad7654972`.
- direct reconstruction: `d0e5c1a6b7d31582446d3a1215c8ba2208a02182229386e4e1669548a6203e92`.
- router training: `365238637499a44911307d080753b5750c91c6a55a350fd1b6493b15fdb833e6`.
- validation/outcome: `d6b9d7e292eeaaa8f4104cc821a9eb2640b504b14863897cfaafbcb241c6c2e6`.
- main injection: `c042c1cfd68847cda002eaf10fad38ea3fe7f00bcf1dd90f62ea8bde544f86bd`.
- assembler: `1b4e3e5b7e2b3aa5a2463d8ac77b44109cf5b2e9810f1a2ad2533e7954007253`.

## Integrity

- E50 parent integrity: PASS.
- E51Y/E51X mature terminal reproduction: **4,200 / 4,200 known and 1,200 / 1,200 no-unique** full-tape reachability: PASS.
- E51AB local-384 direct reconstruction: PASS.
- direct global and local forward/reverse identity: PASS.
- direct target support and local nondegeneracy: PASS.
- stage-94/95/96 world and RNG-domain separation: PASS.
- world assignment failures: 0.
- stage-94 development: 12,960 episodes / 220,320 states.
- development classes: 12,334 PRESERVE; 290 DIRECT-ONLY; 336 NEITHER.
- positive-class replication factor: 43.
- expected critical fitting records: 24,804.
- critical-state reconstruction identity: PASS.
- global and local router forward/reverse identity: PASS.
- every learned arm preserved all 12,334 development PRESERVE trajectories.
- frozen mature terminal hash before/after validation: `238967492` / `238967492`.
- frozen direct-controller hash before/after validation: `1790306570` / `1790306570`.
- UNKNOWN learned parameter count: 0.
- evaluator truth, ambiguity, mode, and resource identity exposed to the gate: 0.
- topology and graph changes: 0.
- sealed stage-96 confirmation: 10,800 allocated / 0 executed.

## Router fits

| Fit | Dose | Rounds | Updates | Sweeps | Stop | Selection trace | Fit trace | Loss | Shift | Preserved | Direct-only admitted | Identity |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| global | — | — | 32 | 2 | — | `1776007755` | `1104845893` | `8,776,801,970` | -2,063 | 12,334 | 0 | PASS |
| local | 96 | 2 | 87,196 | 288 | 1 | `2107880281` | `1915333512` | 18,331,497 | -1,119 | 12,334 | 46 | PASS |
| local | 384 | 2 | 140,095 | 1,152 | 1 | `35500982` | `825629482` | 20,970,127 | -1,069 | 12,334 | 79 | PASS |

The local router learned nondegenerate direct admissions while satisfying the exact development preservation constraint. Those admissions did not generalize sufficiently to the untouched validation partition.

## Stage-95 validation

| Arm | Description | All reachable | Known reachable | No-unique UNKNOWN reachable | t0 success | t0 UNKNOWN | t0 wrong | Union regret |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 0 | frozen mature slot controller | 5,139 / 5,400 | 3,944 / 4,200 | 1,195 / 1,200 | 3,394 | 1,799 | 207 | 108 |
| 1 | prior score-max hybrid control | 5,204 / 5,400 | 4,023 / 4,200 | 1,181 / 1,200 | 3,393 | 1,792 | 215 | **43** |
| 2 | calibrated global trajectory router | 5,139 / 5,400 | 3,944 / 4,200 | 1,195 / 1,200 | 3,394 | 1,799 | 207 | 108 |
| 3 | calibrated local-96 trajectory router | 5,162 / 5,400 | 3,966 / 4,200 | 1,196 / 1,200 | 3,394 | 1,799 | 207 | 85 |
| 4 | calibrated local-384 trajectory router | 5,175 / 5,400 | 3,979 / 4,200 | 1,196 / 1,200 | 3,394 | 1,799 | 207 | 72 |
| 5 | evaluator-only frozen-mechanism union | 5,247 / 5,400 | 4,047 / 4,200 | 1,200 / 1,200 | 3,604 | 0 | 0 | 0 |

No learned router improved the preregistered arm-1 score-max control. The strongest learned router, local-384, recovered 36 more trajectories than the mature slot controller but remained 29 below score-max and 72 below the evaluator-only union ceiling. Its category regret was 68 known plus four no-unique trajectories.

Because no learned arm reached zero union regret, no validation winner existed and stage-96 confirmation remained sealed.

## Causal conclusion

The fixed mature slot and direct-candidate mechanisms are complementary, but a conservative scalar gate over the existing 32 terminal features does not reliably identify when to switch mechanisms on fresh trajectories. Exact development preservation was achievable, and local capacity admitted progressively more DIRECT-ONLY development trajectories, but the learned boundary did not generalize better than the existing score comparison.

This rejects the tested low-capacity routing geometry. It does **not** reject direct candidate action support or the mature slot controller. More importantly, E51AD cannot address trajectories outside the frozen mechanism union. Its validation union still missed 153 known trajectories, and routing cannot create candidate competence where neither fixed mechanism succeeds.

The next justified experiment is therefore E51AE: keep the mature controller and existing direct heads frozen, then train learner-owned candidate-value residuals with a resource-feasible trajectory-critical objective. The treatment must preserve every frozen-union development success while targeting only union-neither trajectories. This changes candidate learning geometry rather than adding topology or evaluator-visible inference features.

No R32 promotion, AGI, proto-AGI, consciousness, or inevitability claim is supported by E51AD.
