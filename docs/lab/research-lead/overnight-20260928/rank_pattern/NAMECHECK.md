# NAMECHECK: RANK-PATTERN

Lane: docs/lab/research-lead/overnight-20260928/rank_pattern/
Worker: RANK-PATTERN (non-ledger task; claim minting paused).
Date: 2026-10-03.

## Step 0: toolchain verification (recorded before prereg commit)

- Safebin mandatory: PATH="$HOME/safebin" exported for every
  build/run in this lane.
- `command -v python3` -> empty (verified 2026-10-03).
- `command -v python` -> empty (verified 2026-10-03).
- `znc --version` -> znc 2026.07.0-dev (edition 2026).
- `cmp $HOME/safebin/znc
  src/tools/toolchain/znc_linux_x86_64_abed8aa1` -> identical
  (verified 2026-10-03, ZNC-CMP-IDENTICAL).
- No python invoked at any point in this lane; a forbidden
  interpreter invocation would make the wave PROCESS-FAIL.
- Pure Zag for all research logic, verifiers, and analysis,
  including the in-binary FIFO-trace simulator and predictor.

## Step 1: identity

- Worker name: RANK-PATTERN.
- Parent task: investigate RANK-LAZY's K2 pattern-sensitivity
  (what about V3/V4 reverses the lazy win; principled predictor
  for when lazy ranking wins) and test the T_rank=1 threshold
  variant (re-rank below the promotion threshold, fronting
  entries that stay resident).

## Step 2: lane conventions

- Build on RANK-LAZY's rank_lazy.zag (carried over, additive
  changes only: cold event trace hooks, thresh_rerank_t with
  frozen T_rank=1 for rk=6, TR threading, in-binary predictor).
  No redesign of the substrate.
- Prereg committed alone before any implementation work.
- 3/3 byte-identical runs; sha256 recorded in REPORT.md.
- Commits local only, never pushed, explicit pathspecs, no
  `git reset` on the shared branch.
