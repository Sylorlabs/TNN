# R32 E51W — Trajectory-Critical Optimization-Dose Result

Date executed: 2026-08-30/31
Branch: `r32-agent-sequential-frontier`
Native result: **VALID STABLE PARTIAL — `TRAJECTORY_DOSE_STABLE_PARTIAL_SIGNAL`**
Canonical status: **R27 unchanged.**

## Integrity

- Native Zag v2 only: pass.
- E50 parent integrity: pass.
- Fresh domain-separated worlds: development stage 78, validation stage 79, sealed confirmation stage 80.
- Development: 12,960 episodes / 220,320 states.
- Validation: 5,400 episodes / 91,800 states.
- Confirmation: 10,800 allocated / **0 executed**.
- World partition/domain gate: pass; assignment failures: 0.
- UNKNOWN positive target count: 0.
- Fixed commit ordering, 32 routing cells, no new features, no cross-cell edges, no graph privilege.
- Forward/reverse dose identity: pass.
- Native builds byte-identical.
- Binary SHA-256: `ddbe4beb9278edcdfb678ae6823d6f4ccc9a0f8bce402d777608782c76c4725b`.
- Assembled source SHA-256: `d68204bd355bc5a70255f815695e28157ca98828cf2f931471aed2834ac59663`.
- E51W fragment SHA-256: `a7fe1ea11cc2192e9260e586ae4bedccfa06d4d03c0a60d7b211007b4b87d723`.
- Native workflow run: `33352559113`; exit code 0.
- Evidence artifact: `9744227958`; artifact ZIP SHA-256 `fa46f32f772e5e2e8aadfc17485c242a04a7c0b61b69dbf4094d6ca51816c31d`.

## Development trajectory curve

| Arm | Reachable / 12,960 | Trajectory violation loss |
|---|---:|---:|
| state-SSE 96-sweep control | 12,882 | 5,899,894 |
| trajectory 12 sweeps | 12,955 | 176,066 |
| trajectory 48 sweeps | 12,954 | 147,778 |
| trajectory 96 sweeps | 12,955 | 121,551 |
| trajectory 192 sweeps | **12,957** | 684,425 |

The 192-sweep treatment consumed the full four-round sweep budget (768 total sweeps), so higher optimization dose was not internally exhausted by an early no-update stop.

## Untouched validation reachability

| Arm | Known | No-unique UNKNOWN | Total |
|---|---:|---:|---:|
| state-SSE 96 control | 4,200 / 4,200 | 1,163 / 1,200 | 5,363 / 5,400 |
| trajectory 12 | 4,200 / 4,200 | 1,197 / 1,200 | 5,397 / 5,400 |
| trajectory 48 | 4,200 / 4,200 | 1,197 / 1,200 | 5,397 / 5,400 |
| trajectory 96 | **4,200 / 4,200** | **1,198 / 1,200** | **5,398 / 5,400** |
| trajectory 192 | **4,200 / 4,200** | **1,198 / 1,200** | **5,398 / 5,400** |

The 96-sweep arm is the preregistered stable-partial arm: it strictly gained one trajectory versus the 48-sweep arm with zero paired losses and zero switching/reversal losses. The 192-sweep arm tied it on validation while improving development reachable count.

## Interpretation

E51W strengthens the training-first diagnosis. With the cognitive substrate frozen, optimization dose alone moved the learner to exact known-state reachability and left only **2 / 1,200** no-unique trajectories without any reachable neutral UNKNOWN state.

This is not an exact rescue. Confirmation remained sealed and R32 is not promoted. It also does **not** justify graph or cross-context connectivity: the tested fixed local conditional-weight substrate is already within two validation trajectories of the exact terminal-reachability gate.

Because the highest-dose learner still used its full sweep budget and improved development reachability, the next conservative test is one more preregistered higher-dose curve on the identical trajectory objective. If higher dose fails to move validation, the next mechanism is the already-preregistered family of learner-owned preservation/replay acceptance objectives; only after that objective family plateaus would temporary cross-context connectivity be justified.
