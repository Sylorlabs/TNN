# NAMECHECK: FORMAL-COMPOSE-PORT worker

Date: 2026-10-03. Worker: FORMAL-COMPOSE-PORT (port the FORMAL-COMPOSE
rank-slot store into a live composition lane as the edge store for
L2 attach ops extend/specialize/graft; non-ledger task, claim minting
paused). Lane:
docs/lab/research-lead/overnight-20260928/formal_compose_port/
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
  preallocated emit buffer with cursor-returning e1str/e1i64 and one
  _zag_raw_syscall write, no `!(A && B)` in while conditions
  (grep-checked before freeze), if nesting at most 2,
  `_zag_malloc as *u8` allocation pattern, linear-scan only
  (no hash-table probe loops), stdout bytes hand-verified per binary.

## Commit discipline

- Explicit pathspecs on every commit (shared-branch rule).
- No bare `git commit`. No `git reset` on the shared branch.
- Git writes via /usr/bin/git (safebin git symlink has known EPERM
  write failures). Retry on index.lock with sleep backoff; never
  remove another worker's lock.
- Commit order: PREREG.md + NAMECHECK.md committed alone before any
  implementation file exists (prereg first commit strictly precedes
  implementation first commit).
