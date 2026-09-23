# gl_default — canonical guided-learning (gl) default

Per **Micah's ruling 2026-09-23**: the guided-learning paradigm's default path
is **FL2 — provisional install + eliminative revocation**. This directory is the
reference implementation future crews build on. Terminology: "guided learning
(gl)" replaces "scaffold release" / "guided release".

## Files

- `gl_substrate.zag` — canonical memory substrate (store, audit ledger, episode
  schedule, simulation twins), including the three frozen guided-learning op
  codes: `TN_OP_PINSTALL=16`, `TN_OP_PROMOTE=17`,
  `TN_OP_UNINSTALL_PROVISIONAL=18`.
- `gl_learner.zag` — the reference guided learner (`arm_gl`) plus the
  in-binary teaching baseline (`arm_a`) it is compared against.
- `run_gl.sh` — verification runner: no-RNG static check, select/simulation
  region token check, no-accumulation check, compile, two-run byte-identity,
  all `TN_CHECK` lines, headline totals.

## Mechanism

1. The trainer's scaffolded teaching installs the rule **provisionally**
   (`TN_OP_PINSTALL`, aux = installed policy).
2. Action selection reads only the committed survivor, else the provisional
   install — structurally independent of the contradiction signal.
3. On each world episode the learner runs the no-audit twins of the other
   two actions against scratch state; if the provisional install is
   contradicted by its own world observation, it uninstalls the provisional
   and commits the winner (`TN_OP_UNINSTALL_PROVISIONAL` + `TN_OP_COMMIT`).
4. A provisional install that survives to the release point is promoted
   (`TN_OP_PROMOTE`) to permanent, unkillable state.
5. Learner-initiated `SIGNAL_DISCONNECT` ends the scaffolded phase; what
   persists after disconnect is what was learned.

## Frozen numbers (2026-09-23, verified by `run_gl.sh`)

| stream | audit total | scaffold signal events |
|---|---|---|
| honest | 269 | E14 provisional CONTEST install, E15 learner-fired disconnect, E48 promotion |
| lying | 271 | E14 provisional REKEY install, E15 disconnect, E29 contradiction → uninstall REKEY + commit CONTEST |
| deliberate-teaching baseline | 267 | (reference only) |

Event-driven audit: the scaffold signal is logged **only** on the contradiction
event (lying E29) — no per-episode heartbeat. Verified byte-identical reruns
(sha256 `c45ea5cccff592039e3a970eadc6bccb750067381c0ae62580bf2857b87b90ba`,
2026-09-23; re-verify before citing).

## Known limitation

FL2 acts the lie during E15–E29 until contradictory world evidence arrives; a
never-contradicted lie remains installed. Revocation is driven by world
evidence, not by the trainer — that is the design, and its boundary.

## For future crews

Build on `gl_learner.zag` / `gl_substrate.zag`, keep zero randomness in every
decision path, keep the audit event-driven, and keep reruns byte-identical.
The old scaffold arm (E38/392) is deprecated — see
`../forks/g7_slowness/profiler/p0_baseline/DEPRECATED.md`.
