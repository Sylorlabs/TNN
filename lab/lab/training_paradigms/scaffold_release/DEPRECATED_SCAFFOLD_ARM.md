# DEPRECATED_SCAFFOLD_ARM — pointer (2026-09-23)

The old scaffold arm (E38 learner-initiated disconnect, 392-entry per-episode
heartbeat ledger) is **deprecated / superseded** per Micah's 2026-09-23 ruling:

- Paradigm name: **"guided learning (gl)"** (replaces "scaffold release").
- **Default path: FL2** (provisional install + eliminative revocation).
  Canonical implementation: `gl_default/` (`gl_learner.zag`, `gl_substrate.zag`,
  `run_gl.sh`; honest 269 / lying 271 audit entries, byte-identical reruns).
- **Per-episode heartbeat auditing is dead** — removed from every live fork;
  see `HEARTBEAT_KILL.md` for the full sweep record.

The old arm is retained **only** for reference/reproducibility, frozen
byte-identical, at:

- `forks/g7_slowness/profiler/p0_baseline/` (see its `DEPRECATED.md`)

Do not build new work on the old arm. Build on `gl_default/`.
