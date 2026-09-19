# R32 E51AC — Additive Direct-Candidate Hybrid Result

Date executed: 2026-08-31
Branch: `r32-agent-sequential-frontier`
Native result: **VALID PARTIAL — `DIRECT_CANDIDATE_COMPLEMENT_PARTIAL`**
Canonical status: **R27 remains canonical.**

## Native authority

- GitHub Actions run: `33371199421`.
- job: `99422508279`.
- source head: `5ebee0972b1832604d13060ead4b38606fb245b3`.
- evidence artifact id: `9750599172`.
- artifact ZIP SHA-256: `777f0bc4affbdefc497a37beb20194adbde86c19aafb6f75d5207d11c7c60552`.
- assembled source SHA-256: `14e719598364c14f03fcb10a7a7b4b19da175aa37f58d36f5c2e7a964227a669`.
- E51AC fragment SHA-256 values:
  - hybrid helpers: `fb3f8f3c249f7f75766f212f057588dbc401defac3b559e4b53bfe33689a09c8`;
  - run/gates: `15f33503deeda4b0693e50f8871c0ed2d95de9d5d9ff19f5ab60c143f4e33fa2`;
  - injection: `521c178b056dc002396f10d4319e4b93b4e0488414e4830a197dafc1d8d5a72d`.
- native binary SHA-256: `c50311e9a60dc7c0e642f02b9ce966327dd76e736b2b6e4c4d5bac6bc6540299`.
- double native build byte identity: PASS.
- raw ledger SHA-256: `734da801d99facd6e0b8e29e61a092929517c126e771ad709af9ae7e47f1baa3`.
- native exit code: 0.
- native runtime: 959 seconds.

## Integrity

- E50 parent integrity: PASS.
- E51Y/E51X terminal reproduction: **4,200 / 4,200 known + 1,200 / 1,200 no-unique** full-tape reachability: PASS.
- native Zag v2 only: PASS.
- evaluator truth exposed to learner: 0.
- ambiguity label exposed: 0.
- learned UNKNOWN head: 0.
- topology/graph changes: 0.
- stage-92 validation worlds: 5,400 episodes / 91,800 states.
- stage-93 confirmation worlds: 10,800 allocated / 0 executed.
- validation world IDs: `92,000,000` through `92,005,399`.
- sealed confirmation world IDs: `93,000,000` through `93,010,799`.
- world/domain partition gates: PASS; assignment failures: 0.
- reconstructed E51AB development: 12,960 episodes / 220,320 states.
- global and local-384 direct-head forward/reverse identity: PASS.
- local-384 direct learner nondegeneracy: PASS.
- mature terminal parameter hash before/after validation: `238967492` / `238967492`.
- overall training and validation integrity: PASS.

## Validation reachability

| Arm | All reachable | Known reachable | No-unique UNKNOWN reachable | t0 success | t0 UNKNOWN | t0 wrong |
|---|---:|---:|---:|---:|---:|---:|
| Frozen mature slot controller | 5,156 / 5,400 | 3,962 / 4,200 | 1,194 / 1,200 | 3,526 | 1,651 | 223 |
| UNKNOWN-only direct fallback | 5,212 / 5,400 | 4,040 / 4,200 | 1,172 / 1,200 | 3,528 | 1,639 | 233 |
| Score-max additive hybrid | 5,213 / 5,400 | 4,041 / 4,200 | 1,172 / 1,200 | 3,527 | 1,639 | 234 |
| Evaluator-only union ceiling | 5,260 / 5,400 | 4,060 / 4,200 | 1,200 / 1,200 | 3,755 | 0 | 0 |

The best deployable hybrid gained **57 episodes** over the frozen mature controller, comprising a net gain of 79 known trajectories and a loss of 22 no-unique trajectories. Neither deployable arm reached the exact validation gate, so stage-93 confirmation remained sealed.

## Complement decomposition

| Category | Episodes | Slot reachable | Direct reachable | Union reachable | Both | Slot only | Direct only | Neither |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| No-unique | 1,200 | 1,194 | 1,200 | 1,200 | 1,194 | 0 | 6 | 0 |
| Known | 4,200 | 3,962 | 3,835 | 4,060 | 3,737 | 225 | 98 | 140 |

The frozen direct learner therefore contains real complementary support: it reaches 98 known trajectories missed by the mature slot controller and all six no-unique trajectories missed by that controller. However, 140 known trajectories remain unreachable by either learner, so routing alone cannot make the current pair exact.

## Interpretation

E51AC establishes two distinct limits.

First, direct candidate commitment is useful as an additive mechanism. Both deployable hybrids improve total resource-feasible reachability over the frozen mature slot controller, and the evaluator-only union advances the frontier from 5,156 to 5,260 episodes.

Second, the fixed action learners are not sufficient for exact rescue. The direct mechanism sometimes overrides or replaces safe mature behavior, reducing no-unique reachability from 1,194 to 1,172, while 140 known trajectories remain outside the support of both learners. A better router can potentially recover part of the 47-episode gap between the best deployable hybrid and the union ceiling, but it cannot resolve the 140 known union misses.

The next justified experiment must therefore separate two questions without changing topology: (1) whether a learner-owned trajectory-critical admission objective can preserve mature successes while selecting the frozen direct candidate mechanism only on whole-trajectory rescues; and (2) whether candidate-value learning itself requires a trajectory-critical residual objective to extend support beyond the present union ceiling.

No R32 promotion, AGI, or consciousness claim is supported.
