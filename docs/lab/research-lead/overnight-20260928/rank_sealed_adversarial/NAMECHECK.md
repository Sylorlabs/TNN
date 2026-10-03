# NAMECHECK: RANK-SEALED-ADVERSARIAL

Lane: docs/lab/research-lead/overnight-20260928/rank_sealed_adversarial/
Worker: RANK-SEALED-ADVERSARIAL (non-ledger task; claim minting paused).
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

- Worker name: RANK-SEALED-ADVERSARIAL.
- Parent task: sealed post-freeze adversarial generality test
  for Sim B (the fixed prospective predictor from
  RANK-OVERFLOW-FIX, VERDICT=PASS 8/8, exact on 7 worlds
  M2C2/V1-V6, 4 with overflow).
- This worker wears two hats separated by the prereg freeze:
  ADVERSARY (designs the sealed worlds, committed in
  PREREG.md before any implementation run) and EXPERIMENTER
  (builds and runs the frozen battery). The adversary's
  inputs are the 7 tested worlds' parameter coordinates and
  white-box mechanism analysis of the substrate and Sim B
  sources; the adversary observes no Sim B outputs on sealed
  worlds (none exist before the freeze).

## Step 2: lane conventions

- Build additively on RANK-OVERFLOW-FIX's rank_overflow_fix.zag:
  substrate functions byte-unchanged; only main() extended
  with sealed rows, plus two new driver helpers (teach_B2,
  run_dupkey) for the S7 access-pattern probe. No substrate
  changes, no redesign.
- Prereg committed alone before any implementation work.
- 3/3 byte-identical runs; sha256 recorded in REPORT.md.
- Commits local only, never pushed, explicit pathspecs, no
  `git reset` on the shared branch.
