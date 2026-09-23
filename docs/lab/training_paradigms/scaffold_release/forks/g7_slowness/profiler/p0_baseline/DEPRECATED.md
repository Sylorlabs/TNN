# DEPRECATED — old scaffold arm (E38 / 392-entry ledger)

**Status: SUPERSEDED. Do not build on this arm.**

Per **Micah's ruling 2026-09-23**:

- The guided-learning paradigm is now called **"guided learning (gl)"**.
- **FL2 (provisional install + eliminative revocation) is the default
  guided-learning path.** Canonical reference implementation:
  `training_paradigms/scaffold_release/gl_default/`
  (`gl_learner.zag` + `gl_substrate.zag`, verified honest 269 / lying 271
  audit entries, byte-identical reruns).
- This arm — the original scaffold with learner-initiated disconnect at E38
  and the 392-entry per-episode heartbeat ledger — is **deprecated**.
- Per-episode heartbeat auditing is dead everywhere else (see
  `training_paradigms/scaffold_release/HEARTBEAT_KILL.md`).

## Why this directory is kept (and frozen)

This is the **one documented exception** to the heartbeat kill: the arm is
kept **byte-identical for reference/reproducibility** of the historical
E38/392 result (the G7 slowness baseline: 1.4–2.7x teaching cost vs the
deliberate-teaching baseline, the number the free-lunch investigation
measured against). Its frozen ledger (392 entries, 128 of them heartbeat)
is the record future crews compare against. The exact code is also
recoverable from git history.

Do not "fix" the heartbeat here — that would destroy the reference.
New work goes in `gl_default/`.
