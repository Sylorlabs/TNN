# NAMECHECK: RANK-LAZY

Lane: docs/lab/research-lead/overnight-20260928/rank_lazy/
Worker: RANK-LAZY (non-ledger task; claim minting paused).
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
- Pure Zag for all research logic, verifiers, and analysis.

## Step 1: identity

- Worker name: RANK-LAZY.
- Parent task: convert RANK-CHEAP's exploratory NET4=1097 net win
  into a frozen result; freeze NET4 < 1132 as the headline kill
  bar; add a threshold-crossed re-rank variant (rk=5).

## Step 2: lane conventions

- Build on RANK-CHEAP's rank_cheap.zag (carried over, additive
  changes only). No redesign of the substrate.
- Prereg committed alone before any implementation work.
- 3/3 byte-identical runs; sha256 recorded in REPORT.md.
- Commits local only, never pushed, explicit pathspecs, no
  `git reset` on the shared branch.
