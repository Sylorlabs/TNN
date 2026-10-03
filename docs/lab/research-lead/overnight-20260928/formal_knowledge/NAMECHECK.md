# NAMECHECK: FORMAL-KNOWLEDGE worker

Date: 2026-10-03. Worker: FORMAL-KNOWLEDGE (design task, non-ledger;
claim minting paused). Lane:
docs/lab/research-lead/overnight-20260928/formal_knowledge/
Branch: tnn-native-lab. Commits local only, never pushed.

## Step 0: toolchain guard

- PATH set to $HOME/safebin at session start for all build/run work.
- `which python3 python` returns nothing (exit 1) under safebin PATH.
- Pinned znc 2026.07.0-dev (edition 2026) via safebin.
- All scientific computation in pure Zag. Shell used only for
  safebin setup, znc, binary runs, sha256sum, and git.
- AGENTS.md miscompile workarounds followed: u8-backed state with
  get32/set32 helpers (no `as *i32` slice construction), single
  preallocated emit buffer with cursor-returning e1str/e1i64 and one
  _zag_raw_syscall write, no `!(A && B)` in while conditions, if
  nesting at most 2, `_zag_malloc as *u8` allocation pattern.

## Commit discipline

- Explicit pathspecs on every commit (shared-branch rule).
- No bare `git commit`. No `git reset` on the shared branch.
- Git writes via /usr/bin/git (safebin git symlink has known EPERM
  write failures).
