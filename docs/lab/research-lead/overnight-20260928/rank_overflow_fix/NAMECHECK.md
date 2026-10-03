# NAMECHECK: RANK-OVERFLOW-FIX

Lane: docs/lab/research-lead/overnight-20260928/rank_overflow_fix/
Worker: RANK-OVERFLOW-FIX (non-ledger task; claim minting paused).
Date: 2026-10-03.

## Step 0: toolchain verification (recorded before prereg commit)

- Safebin mandatory: PATH="$HOME/safebin" exported for every
  build/run in this lane.
- `command -v python3` -> empty (verified 2026-10-03).
- `command -v python` -> empty (verified 2026-10-03).
- `znc --version` -> znc 2026.07.0-dev (edition 2026).
- `cmp $HOME/safebin/znc
  src/tools/toolchain/znc_linux_x86_64_abed8aa1` -> identical
  (verified 2026-10-03, ZNC-CMP-IDENTICAL; re-verified this lane).
- No python invoked at any point in this lane; a forbidden
  interpreter invocation would make the wave PROCESS-FAIL.
- Pure Zag for all research logic, verifiers, and analysis.

## Step 1: identity

- Worker name: RANK-OVERFLOW-FIX.
- Parent task: fix Sim B's min-seq overflow model (RANK-PATTERN
  open thread: d5=22, d6=18 magnitude gap on overflow worlds),
  determine whether the fix makes Sim B exact, include cold
  misses in the scan-cost model.

## Step 2: lane conventions

- Build on RANK-PATTERN's rank_pattern.zag (additive only:
  seqmove-gated seq handling in sim_prosp, tro4 slot
  validation, prospective Sim B on all 7 worlds). No substrate
  changes, no redesign.
- Prereg committed alone before any implementation work.
- 3/3 byte-identical runs; sha256 recorded in REPORT.md.
- Commits local only, never pushed, explicit pathspecs, no
  `git reset` on the shared branch.
