# R32 E51AB — Direct Candidate Commit Action Support Result

Date executed: 2026-08-31
Branch: `r32-agent-sequential-frontier`
Native result: **VALID NEGATIVE — `DIRECT_CANDIDATE_ACTION_SUPPORT_UNCONFIRMED_COMPARE_LEDGER`**
Canonical status: **R27 remains canonical.**

## Native authority

- GitHub Actions run: `33368710200`.
- source head: `c8ff4e6d7ce7f23672bccb9cf7f07e87fabcfa4f`.
- evidence artifact id: `9749736196`.
- artifact ZIP SHA-256: `3d924079131cae0a847c9aa35507cde4f0dd5f03273781b8f228de334febe2d6`.
- assembled source SHA-256: `c0497699578578e20ed098326955127db8a1aa1671294df7ef400f51b7cb363d`.
- E51AB fragment SHA-256 values:
  - direct-candidate helpers: `e20f14bf07d8f42bc02e2f21f4f4789efb17dbb74364174d6d9a1e29dfe6146c`;
  - run/gates: `0656264ddf75903f0ef85c9a66d4ea862ee940324ed97a9b9af6ad279ff322a6`;
  - injection: `f32b386bf3ef645301e388f07c5a8fec7900166092aa0ca20803cf0ad8e6425c`.
- native binary SHA-256: `93626c6e5f8101cb72d442d5a7e29f90d8d0247f047821bdb6cbc2d12175c08a`.
- double native build byte identity: PASS.
- raw ledger SHA-256: `4b439cbe1cf0eee5254317f030434183eae966a5abae4a03455da307229caa39`.
- native exit code: 0.
- native runtime: 1,154 seconds.

## Integrity

- E50 parent integrity: PASS.
- E51Y/E51X terminal reproduction: **4,200 / 4,200 known + 1,200 / 1,200 no-unique** full-tape reachability: PASS.
- native Zag v2 only: PASS.
- evaluator truth exposed to learner: 0.
- ambiguity label exposed: 0.
- learned UNKNOWN head: 0.
- topology/graph changes: 0.
- stage-89 development worlds: 12,960 episodes / 220,320 states.
- stage-90 validation worlds: 5,400 episodes / 91,800 states.
- stage-91 confirmation: 10,800 allocated / 0 executed.
- world/domain partition gates: PASS; assignment failures: 0.
- candidate targets contained positive and negative grounded support for both candidates.
- global and local forward/reverse fit identity: PASS.
- local learner nondegeneracy: PASS.
- mature E51Y terminal parameter hash before/after: `238967492` / `238967492`.
- overall training and validation integrity: PASS.

## Validation reachability

| Arm | All reachable | Known reachable | No-unique UNKNOWN reachable | t0 success | t0 UNKNOWN | t0 wrong |
|---|---:|---:|---:|---:|---:|---:|
| Frozen mature slot actions | 5,144 / 5,400 | 3,949 / 4,200 | 1,195 / 1,200 | 3,396 | 1,785 | 219 |
| Direct candidate — global linear | 1,746 / 5,400 | 546 / 4,200 | 1,200 / 1,200 | 1,200 | 4,200 | 0 |
| Direct candidate — local 96 | 4,462 / 5,400 | 3,262 / 4,200 | 1,200 / 1,200 | 1,209 | 4,177 | 14 |
| Direct candidate — local 384 | 4,524 / 5,400 | 3,324 / 4,200 | 1,200 / 1,200 | 1,217 | 4,160 | 23 |

No direct arm passed the exact validation gate; confirmation therefore remained sealed.

## Interpretation

E51AA established that generic direct candidate commitment is required in principle because `KEEP / CURRENT / RESTORE` cannot express the grounded-correct answer in every resource-feasible prefix. E51AB shows that **replacing** the mature E51Y terminal controller with newly regressed candidate-return heads is not the correct implementation.

The direct heads learned a strong safe-abstention tendency: every tested direct arm exposed UNKNOWN on all 1,200 no-unique trajectories. However, the same heads suppressed valid commitment on too many known trajectories. Even the strongest local-384 arm reached only 3,324 / 4,200 known episodes, far below the mature slot controller's 3,949 / 4,200 on the same fresh partition.

This is not evidence against direct candidate actions themselves. It is evidence against making low-support direct candidate regressors replace mature slot-based terminal competence. The next smallest justified test is an **additive hybrid audit**: retain the frozen E51Y terminal policy and ask whether the already-selected E51AB local-384 candidate learner supplies complementary reachable successes on the mature policy's fresh resource-feasible misses. Only if that union is materially positive should a learner-owned router be trained.

No R32 promotion, AGI, or consciousness claim is supported.