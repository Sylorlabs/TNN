# R32 E51G — Matched Value-Function Capacity Result

Date: 2026-08-30
Branch: `r32-agent-sequential-frontier`
Native result: `VALID NEGATIVE — NO_TESTED_VALUE_CAPACITY_RESCUE`
Canonical status: R27 unchanged.

## Integrity

- E50 parent integrity: pass.
- Fresh E51G seed manifest: 19,440 allocated; zero assignment failures.
- Development: 3,240 episodes / 55,080 sequential terminal states.
- Validation: 5,400 episodes / 91,800 sequential terminal states.
- Sealed confirmation: 10,800 allocated; executed 0.
- UNKNOWN nonzero targets: 0.
- Linear UNKNOWN nonzero parameters: 0.
- Linear batch forward/reverse identity: pass.
- Pairwise Foundry forward/reverse identity: pass.
- Hinge means forward/reverse identity: pass.
- Hinge Foundry forward/reverse identity: pass.
- Pairwise commit terms selected: 12; UNKNOWN terms: 0.
- Hinge commit terms selected: 12; UNKNOWN terms: 0.
- Structure integrity gate: pass.
- Native builds byte-identical.
- Native binary SHA-256: `61e1b6f4005bb9125d78fd8b09d7db00a5ac3ff95a05a49d2c182a7995a6d621`.
- Assembled source SHA-256: `243b386854f9d3d1cdca197f712da16d1916ee1d63d2b43ff40a62ab4ba9ad4b`.
- Primary E51G fragment SHA-256: `66f4d1d6bbbbab8e9e86f93b25b62da6045ec14996cc8b361f71187d183e7c87`.
- Main-injection SHA-256: `141c518a740f2903f13713592b6d9560db3f6b2c35efaabac4b2df4ac0b8bb57`.
- Raw ledger SHA-256: `420c21da3ae404875810020666d52da57d23b3c9e5cc4a454cf43c1df95303f7`.
- Native runtime: 56 seconds; exit code 0.

## Validation reachability

| Arm | Known reachable | No-unique UNKNOWN reachable | Residual known veto | Residual no-unique veto |
|---|---:|---:|---:|---:|
| A — fresh matched linear | 4,198 / 4,200 | 1,135 / 1,200 | 2 | 65 |
| B — sparse learner-selected pairwise residuals | 4,198 / 4,200 | 1,133 / 1,200 | 2 | 67 |
| C — sparse learner-selected data-mean hinge residuals | 4,197 / 4,200 | 1,150 / 1,200 | 3 | 50 |

The historical E51E primary linear result was 4,200/4,200 known and 1,125/1,200 no-unique. Fresh E51G therefore confirms that terminal reachability remains close to, but not at, the exact gate and varies across fresh worlds.

## What the learner selected

The pairwise arm deterministically recruited four terms for each commit action and none for UNKNOWN. The selected pairs differed by action; no researcher-selected E49 conjunction was imposed.

The hinge arm likewise recruited four terms for each commit action and none for UNKNOWN. Feature identity, hinge direction, data-derived mean, coefficient, and stopping point were selected from development residual improvement only.

Thus both nonlinear mechanisms were nondegenerate and had causal effect on the validation decision boundary.

## Interpretation

E51G rejects the narrow hypothesis that a modest increase in generic nonlinear terminal-value capacity, while preserving the same per-state squared-error training objective, is sufficient to eliminate the E51E reachability veto.

The hinge arm is especially diagnostic: it improved no-unique reachability by 15 episodes relative to the fresh linear control but lost one additional known episode. The pairwise arm slightly worsened no-unique reachability without repairing the two known misses. This is the same qualitative abstention-versus-resolution tradeoff seen earlier, now under learner-selected nonlinear structure.

Combined with E51F's zero exact state aliases, the next causal question is the **approximation/objective geometry**: whether the value regression objective is fitting average per-state utilities while the actual control requirement depends on action ordering and at-least-one-good-stopping-state reachability along each trajectory.

Per the E51G preregistration, no topology rewrite is justified yet. The next experiment must diagnose or change the decision objective on the same learner-visible state before testing graph/self-connection changes.

No R32 promotion claim is supported by E51G.
