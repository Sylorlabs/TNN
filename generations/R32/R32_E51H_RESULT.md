# R32 E51H — Neutral-Relative Preference Result

Date: 2026-08-30
Branch: `r32-agent-sequential-frontier`
Native result: `VALID NEGATIVE — NO_TESTED_OBJECTIVE_RESCUE`
Canonical status: R27 unchanged.

## Integrity

- E50 parent integrity: pass.
- 19,440 E51H seeds allocated; zero failures.
- Development: 3,240 episodes / 55,080 states.
- Validation: 5,400 episodes / 91,800 states.
- Confirmation: 10,800 allocated; executed 0.
- Absolute UNKNOWN target nonzero: 0.
- Preference UNKNOWN target nonzero: 0.
- Preference commit targets: 82,923 positive and 82,317 negative.
- Absolute linear forward/reverse identity: pass.
- Neutral-relative linear forward/reverse identity: pass.
- UNKNOWN parameters remain zero: pass.
- Hinge means/structure forward-reverse identity: pass.
- Learner-selected hinge commit terms: 12; UNKNOWN terms: 0.
- Native builds byte-identical: SHA-256 `81314b650e0a4be33eeacc10692dd3f73d258c379a77f1022ce7eacfbe4f8817`.
- Raw ledger SHA-256 `fbb585f7a4c8537023667850c07da8354f5c320253fa98a6886ed28ccb689e7e`.
- Native exit code 0; runtime 40 seconds.

## Validation reachability

| Arm | Known reachable | No-unique UNKNOWN reachable |
|---|---:|---:|
| A — absolute-utility linear | 4,196 / 4,200 | 1,122 / 1,200 |
| B — neutral-relative preference linear | 4,199 / 4,200 | 1,086 / 1,200 |
| C — preference + learner hinge residuals | 4,197 / 4,200 | 1,108 / 1,200 |

Neither experimental arm improved the preregistered frontier. Confirmation remained sealed.

## Interpretation

Changing supervision from absolute grounded utility to the sign of commit utility relative to neutral UNKNOWN did not rescue terminal reachability. It nearly repaired known reachability but made no-unique abstention materially worse. Adding learner-selected hinge capacity recovered part of that loss but still failed both the exact and partial gates.

E51H therefore rejects the narrow hypothesis that the residual E51E/E51G failure is solved by replacing per-action value regression with simple neutral-relative preference targets while keeping the same state and action heads.

Per preregistration, the next step is an exact margin/ranking geometry audit before any topology rewrite.

No R32 promotion claim is supported by E51H.
