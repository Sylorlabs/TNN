# R32 E51 — Action-Value Geometry Audit

Date: 2026-08-28

Status: `AUDIT_COMPLETE — NO NEW EXPERIMENT PREREGISTERED`

## Finding

E45–E50 use a four-way *terminal* target. `e45_terminal_value` assigns the
three commit actions their delayed grounded utility (`1000`, `-1200`, or
`-2000`) and assigns UNKNOWN the neutral no-commit value `0`. E50 then fixes the
UNKNOWN target and every UNKNOWN-head parameter at zero. This is not an
ambiguity label or confidence threshold: UNKNOWN wins only when no commit has a
positive learned value.

There is no native evidence that a positive UNKNOWN target is justified. Making
UNKNOWN positive at this point would be an arbitrary abstention bias and would
contradict the no-positive-warrant semantics.

The more consequential limitation is scope: E50 evaluates a static terminal
choice at each tape time. Its batch target has no explicit action whose value is
the delayed consequence of *continuing an already initiated investigation*.
The core already contains generic option state, discriminative predictions,
source dependence, accumulated option cost, learned shadow price, and a
continuation-versus-termination comparison. But E50's 4-action batch target
does not qualify that continuation value against terminal alternatives.

## Consequence for the next experiment

Do not alter UNKNOWN value. If E51 is pursued, it must be a fresh native,
pre-registered sequential action-value discriminator. The treatment must add a
grounded continuation action trained only from delayed utility/regret (including
actual observation cost) and compared at each step against terminate actions.
It must not consume evaluator mode, truth, ambiguity labels, a fixed duration,
or a fixed observation count. It needs a sequential validation ledger rather
than E50's static per-time terminal ledger, with a matched terminal-only
control, fresh manifests, sealed confirmation, and explicit no-unique and
known-resolution safety gates.

This conclusion follows directly from source inspection of
`tnn_r32_e50_provenance_temporal_contention_discriminator.zag` and the valid E50
negative. It is an architecture audit, not a quantitative result and does not
change canonical status: R27 remains canonical.
