# NAMECHECK: RECLAMATION-H1B (importance-weighted liveness, corrected K13)

Worker: RECLAMATION-H1B worker (non-ledger task; claim minting paused).
Lane: docs/lab/research-lead/overnight-20260928/reclamation_h1b/

## Step 0: Toolchain guard (recorded at lane startup)

- safebin at $HOME/safebin; PATH exported to $HOME/safebin for every
  run command.
- `which python3` and `which python` return nothing under that PATH
  (verified 2026-10-03 at lane startup).
- znc resolves inside safebin as the pinned compiler
  (znc 2026.07.0-dev (edition 2026)); cmp against
  src/tools/toolchain/znc_linux_x86_64_abed8aa1: byte-identical
  (verified 2026-10-03 before the prereg commit).
- No build is required in this lane: the mechanism is the frozen H1
  binary, copied byte-identically after the prereg commit. Its
  sha256 (c0f48d00b43966bcc06e4cd9d9aad863c668d970a8d1674d2335f42073f7774d)
  is recorded in the prereg and re-verified after copying; any
  mismatch voids the lane.
- Shell use limited to: mkdir, binary execution, sha256sum, cmp, git
  ops, file reads/writes. No forbidden executable invoked. No
  PROCESS-FAIL condition triggered.
- Git writes via /usr/bin/git directly (safebin git symlink EPERM
  lesson, 2026-10-03); explicit pathspecs; no git reset; local only,
  never pushed.
- The H1 source (importance_h1.zag) is copied into this lane only as
  a reference record; it is not compiled here and is not modified.
  Mechanism identity for this lane is the binary hash.

## Conventions carried from the parent lane

- Pure Zag for all scientific computation (already embodied in the
  frozen binary; no new scientific code is written or compiled).
- Prereg committed alone before any binary copy or run (strict commit
  order); this prereg freezes all predicted values and kill bars.
- 3/3 byte-identical runs (sha256 equal) required; determinism bar is
  VOID-grade.
- Frozen kill bars are never weakened or reinterpreted after results.
- The mechanism is NOT modified: the only change relative to H1 is
  the prereg derivation of K13 (ret=14, post=5, rawA=20), which the
  H1 REPORT identified as a worker arithmetic error and which an
  eviction trace on a debug build verified against the corrected
  numbers.
