# NAMECHECK.md -- FORMAL-COMPOSE-DAG3 worker

Worker: FORMAL-COMPOSE-DAG3. Lane:
`docs/lab/research-lead/overnight-20260928/formal_compose_dag3/`.
Task type: NON-LEDGER (claim minting paused).

## Step 0 -- toolchain guard (worker startup)

- Safebin active: `export PATH="$HOME/safebin"` before all
  build/run work. Verified 2026-10-03: `which python3` and
  `which python` return nothing under the safebin PATH.
- Pinned znc via `$HOME/safebin/znc` for all compiles.
- Pure Zag for all research logic (battery, invariant check,
  emit). Shell only for setup, znc, runs, sha256sum, cmp,
  git. No Python, no C, no other interpreter at any step.
- AGENTS.md miscompile workarounds apply: u8-backed state
  with get32/set32 (no `as *i32` slice construction), single
  preallocated emit buffer with cursor helpers and one
  `_zag_raw_syscall` write, no `!(A && B)` in while
  conditions (grep-checked), shallow if-nesting with hoisted
  flags, `_zag_malloc as *u8` pattern, linear scans only.
- Git: local commits only, never push, explicit pathspecs,
  no bare `git commit`, no `git reset` on the shared branch,
  git writes via /usr/bin/git if the safebin symlink EPERMs.

## Commit order

PREREG.md (+ this NAMECHECK.md, no implementation) committed
alone first. Implementation files committed only after the
prereg commit exists. REPORT.md committed after the runs.
