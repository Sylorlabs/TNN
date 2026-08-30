# R32 E51I — Terminal Margin and Ranking Geometry Audit Result

Date: 2026-08-30
Branch: `r32-agent-sequential-frontier`
Native result: `VALID DIAGNOSTIC — HETEROGENEOUS_CALIBRATION_REQUIRED`
Canonical status: R27 unchanged.

## Integrity

- E50 parent integrity: pass.
- 19,440 E51I seeds allocated; zero failures.
- Development: 3,240 episodes / 55,080 states.
- Validation: 5,400 episodes / 91,800 states.
- Confirmation: 10,800 allocated; executed 0.
- UNKNOWN target nonzero: 0.
- Linear fit forward/reverse identity: pass.
- UNKNOWN parameters remain zero: pass.
- Native builds byte-identical: SHA-256 `9f3ab03e4a3d27992cd930691d546a45aac23c52fb4fb127fb203a994b1b3985`.
- Raw ledger SHA-256 `2c520294c8640ebbc6691d775586f1565186e50d893989178fa5f06836043e17`.
- Native exit code 0; runtime 30 seconds.

## Baseline reachability

- Known reachable: 4,197 / 4,200.
- No-unique UNKNOWN reachable: 1,129 / 1,200.

## Exact geometry diagnosis

- Known episodes with **no correct commit ever top-ranked among commit actions**: **0 / 4,200**.
- Known episodes that are ranking-capable: **4,200 / 4,200**.
- Known episodes blocked only by UNKNOWN/sign calibration: **3**.
- No-unique episodes blocked by positive commit margin: **71**.

No-unique failure margin buckets (minimum best-commit score across the trajectory):
- <=25: 9
- 26–50: 9
- 51–100: 6
- 101–250: 25
- >250: 22

Known calibration-deficit buckets:
- <=25: 0
- 26–50: 2
- 51–100: 1
- 101–250: 0
- >250: 0

## Uniform commit-shift theorem for this validation set

Because a uniform shift leaves commit ordering unchanged:

- satisfying every known episode requires integer shift `s >= +57`;
- satisfying every no-unique episode requires `s <= -631`.

The intersection is empty. Exact uniform commit calibration is therefore impossible on this fresh validation set.

## Interpretation

This sharply narrows the residual terminal problem. The frozen learner already ranks the correct commit highest somewhere in **every known episode**. The remaining known failures are not action-ranking failures. They occur because neutral UNKNOWN sits above an otherwise-correct top commit.

At the same time, many no-unique episodes require strongly negative commit calibration, including 22 failures whose best achievable commit margin remains more than +250 above neutral. Therefore one global bias or temperature cannot solve both sides.

The next justified mechanism is a learner-owned **state-dependent scalar commit calibration** that preserves KEEP/CURRENT/RESTORE ordering and learns only whether committing in the current state is worth more or less than neutral UNKNOWN. E51I evaluator-side margins themselves must not become learner features.

No topology change is justified by E51I, and no R32 promotion claim is supported.
