# NAMECHECK: FORMAL-COMPOSE-E2E worker

Date: 2026-10-03. Worker: FORMAL-COMPOSE-E2E (drive the actual
L2-EXTEND-XDOMAIN and L2-SPECIALIZE-XDOMAIN learner stacks against
the rank-slot store from FORMAL-COMPOSE-PORT instead of their
unconstrained edge stores; non-ledger task, claim minting paused).
Lane: docs/lab/research-lead/overnight-20260928/formal_compose_e2e/
Branch: tnn-native-lab. Commits local only, never pushed.

## Step 0: toolchain guard

- PATH set to $HOME/safebin at session start for all build/run work.
- `which python3 python` returns nothing (exit 1) under safebin PATH
  (verified 2026-10-03 before any build).
- Pinned znc 2026.07.0-dev (edition 2026) via safebin.
- All scientific computation in pure Zag. Shell used only for
  safebin setup, znc, binary runs, sha256sum, and git.
- AGENTS.md miscompile workarounds followed: u8-backed state with
  get32/set32 helpers (no `as *i32` slice construction), single
  preallocated emit buffer with cursor-returning emit helpers and one
  _zag_raw_syscall write, no `!(A && B)` in while conditions
  (grep-checked before freeze), if nesting kept shallow with hoisted
  sub-conditions, `_zag_malloc as *u8` allocation pattern,
  linear-scan only (no hash-table probe loops), stdout bytes
  hand-verified per binary.

## Commit discipline

- Explicit pathspecs on every commit (shared-branch rule).
- No bare `git commit`. No `git reset` on the shared branch.
- Git writes via /usr/bin/git (safebin git symlink has known EPERM
  issue on object/index writes).
- PREREG.md committed alone before any implementation file exists
  (prereg commit-order self-check).
