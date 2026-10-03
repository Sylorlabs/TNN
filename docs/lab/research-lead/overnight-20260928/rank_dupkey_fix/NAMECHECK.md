# NAMECHECK: RANK-DUPKEY-FIX

Lane: docs/lab/research-lead/overnight-20260928/rank_dupkey_fix/
Worker: RANK-DUPKEY-FIX (non-ledger task; claim minting paused).
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
- Git writes via /usr/bin/git directly: the safebin `git`
  symlink is known to fail writes with EPERM on this
  worktree (AGENTS.md shared-workspace lesson, 2026-10-03).

## Step 1: identity

- Worker name: RANK-DUPKEY-FIX.
- Parent task: implement the duplicate-key repair in Sim B
  (lowest-slot hit semantics) recommended by
  RANK-SEALED-ADVERSARIAL's REPORT.md, and investigate
  whether duplicate cold residency is intended substrate
  semantics.
- This worker wears two hats separated by the prereg freeze:
  REPAIR DESIGNER (frozen repair spec + sealed S9 world +
  kill bars, committed in PREREG.md before any
  implementation) and EXPERIMENTER (builds and runs the
  frozen battery). The repair is designed from white-box
  mechanism analysis of the substrate (`cold_lookup` hits
  the lowest slot) and Sim B (`sim_prosp` charges the
  latest-install slot via the `ks` map); no Sim B outputs
  on the sealed repair-validation worlds exist before the
  freeze.

## Step 2: lane conventions

- Build additively on RANK-SEALED-ADVERSARIAL's
  rank_sealed_adversarial.zag: substrate functions
  byte-unchanged (K1 anchor); rows 0-34 identical; only
  `sim_prosp` extended with the seqmove=2 repair variant,
  one new driver (`run_dupkey_pm1`) for the S9 sealed
  promote probe, rows 35-36, and the RES3 prospective
  suite. No substrate changes, no redesign.
- Prereg committed alone before any implementation work
  (commit-order self-check).
- 3/3 byte-identical runs; sha256 recorded in REPORT.md.
- Commits local only, never pushed, explicit pathspecs, no
  `git reset` on the shared branch.
