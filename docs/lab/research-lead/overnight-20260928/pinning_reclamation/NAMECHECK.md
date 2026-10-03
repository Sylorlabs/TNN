# NAMECHECK: PINNING-RECLAMATION

Worker: PINNING-RECLAMATION worker (non-ledger task; claim minting paused).
Lane: docs/lab/research-lead/overnight-20260928/pinning_reclamation/

## Step 0: Toolchain guard (recorded at lane startup)

- safebin at $HOME/safebin (49 tools); znc resolves inside safebin as a
  symlink to the pinned compiler (byte-identical to
  src/tools/toolchain/znc_linux_x86_64_abed8aa1,
  znc 2026.07.0-dev (edition 2026); cmp SAME).
- PATH exported to $HOME/safebin for every build/run command.
- `which python3` and `which python` return nothing under that PATH.
- Shell use limited to: mkdir, znc invocation, binary execution,
  sha256sum, cmp, git ops, file reads/writes. No forbidden executable
  invoked. No PROCESS-FAIL condition triggered.
- Git writes via /usr/bin/git directly (safebin git symlink EPERM
  lesson, 2026-10-03); explicit pathspecs; no git reset; local only,
  never pushed.

## Conventions carried from EVICTION-POLICY (parent lane)

- Pure Zag for all scientific computation.
- Prereg committed alone before implementation (strict commit order).
- 3/3 byte-identical runs (sha256 equal) required; determinism bar is
  VOID-grade.
- Frozen kill bars are never weakened or reinterpreted after results.
