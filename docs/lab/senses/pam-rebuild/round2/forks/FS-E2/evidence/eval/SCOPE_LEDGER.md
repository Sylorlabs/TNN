# FS-E2 Scope Ledger (formation-precondition side-ledger)

Standing rule (from PREREG_FS-E2, frozen 2026-09-24): a task earns install
authority iff its independently reproduced formation accuracy on the frozen
R2A normal sets is >= 85%. Scoping is re-measurable in future phases; no
task is permanently scoped out.

## Measurements (Phase 0, committed 28aa3938)

| Task | Formation accuracy | Scope |
|---|---|---|
| colordisc | 92.96% | IN SCOPE |
| pitchdisc | 97.92% | IN SCOPE |
| motiondir | 96.63% | IN SCOPE |
| colorconst | 56.81% | ABSTAIN (formation below precondition) |
| shapetrans | 80.56% | ABSTAIN (formation below precondition) |
| timbredisc | 38.89% | ABSTAIN (formation below precondition) |

## Path to scope for abstained tasks

Any abstained task re-measured at >= 85% formation accuracy on the frozen
R2A normal sets (same fixtures, same frozen definitions) in a future phase
earns install authority. This requires a formation improvement, not a
scoping-rule change. No formation work was done in this fork.
