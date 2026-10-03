# NAMECHECK.md -- L2-ESS-COMPOSE

Worker: L2-ESS-COMPOSE subagent (depth 2/2), 2026-10-03.
Lane: `docs/lab/research-lead/overnight-20260928/l2_ess_compose/`
Non-ledger task (claim minting paused).

## Step 0: toolchain guard (mandatory)

- Safebin active: `export PATH="$HOME/safebin"` at session start.
- `which python3` -> empty. `which python` -> empty. Verified 2026-10-03.
- `which znc` -> `/home/hatch/safebin/znc`, pinned build
  `znc 2026.07.0-dev (edition 2026)`.
- All research logic (learner, world, driver, analysis) in pure Zag.
  Shell used only for: invoking znc, running binaries, git ops,
  file moves/copies, grep-based trace audits. No python3/python/C/Rust/JS
  in verifiers, scorers, harnesses, or analysis at any point.
- If a forbidden executable is invoked, this wave is automatically
  PROCESS-FAIL per the worker toolchain guard.

## Base sources (read-only, never modified)

- Learner base: `../l2_compose_chain3/learner.zag` (1696 lines; the
  frozen [6,5,4] composition learner; zero operator-semantic changes
  in this lane).
- World: `../l2_compose_chain3/world_E.zag` reused byte-identical.
- Standing mechanism reference: `../l2_ess_curriculum/learner.zag`
  (st_standing_eval / op_standing_update / st_sig algebra).

## State layout note

The chain3 learner documents `1412..` as caller-allocated scratch and
nothing in the learner or driver reads/writes offsets >= 1412 (verified
by grep before implementation). The standing cell table and control
i32s are placed there; no existing offset moves. Driver state buffers
grow 8192 -> 16384 bytes (driver-side allocation only).
