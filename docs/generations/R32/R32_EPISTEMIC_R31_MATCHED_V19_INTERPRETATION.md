# R32 V19 — Isolated UNRESOLVED_TEMPORAL Action

Status: **REFERENCE_ONLY / ROUTING IMPROVED / FUTURE-RESOLVABILITY DEFICIT REMAINS**

V19 restores untouched V16 KEEP/COMMIT/EPOCH/INSPECT/standard-UNKNOWN values. The learned nonstationary mass is isolated as a separate `UNRESOLVED_TEMPORAL` abstention action with expected delayed-regret utility `m*(+1) + (1-m)*(-1.2)`. No tuned confidence threshold is used.

Reusable no-unique UNKNOWN improves **0.555 -> 0.625** while reusable wrong commitment averages **0.127**. This is materially better isolated than V18 broadcast integration.

However, resolvable success is only **0.6425** vs V16 0.7725. Stable-weak is **0.88**, unstable-then-stable **0.55**, replacement **0.64**, reversal **0.50**. Cost-too-high UNKNOWN remains 1.00.

## Causal classification

The remaining failure is **temporal horizon / future resolvability**, not broad Q contamination. A transiently unstable history can look nonstationary now even when another affordable observation will later collapse the current-epoch hypothesis. V19 sometimes abstains before learning that future value.

## Decision

- Keep V16 historical + current-epoch hypotheses and untouched base Q values.
- Keep isolated routing for the unresolved temporal hypothesis; do not broadcast it.
- Reject V19's terminal value based only on persistent-nonconvergence probability.
- Next learn a separate **future resolvability / value-of-waiting hypothesis** from actual multi-step observation trajectories. `UNRESOLVED_TEMPORAL` should win only when delayed nonconvergence evidence is high *and* affordable future observation value is low. This must be learned from delayed outcomes/cost, not a fixed probe count or ambiguity label.
- R27 remains canonical pending native Zag qualification.
