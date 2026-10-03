# NAMECHECK.md -- IVWC-KSENSITIVITY

## Step 0: toolchain guard (recorded at lane startup, before any work)

- Ran `docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
  equivalent: `export PATH="$HOME/safebin"` at session start.
- `which python3` returns nothing under the safebin PATH.
- `which python` returns nothing under the safebin PATH.
- Compiler: `$HOME/safebin/znc` (pinned znc 2026.07.0-dev, edition 2026).
- All computational research operations in this lane are pure Zag,
  compiled with the pinned znc. Shell is used only for: invoking znc,
  running the binary, git operations, file moves/copies, sha256sum.
- Git writes use `/usr/bin/git` directly (the `$HOME/safebin/git`
  symlink is known to fail object/index writes with EPERM per
  AGENTS.md 2026-10-03; git itself remains an allowed tool).
- Lane: `docs/lab/research-lead/overnight-20260928/ivwc_ksensitivity/`
- Non-ledger task (claim minting paused). Commits local on
  `tnn-native-lab` with explicit pathspecs via GIT_INDEX_FILE plumbing
  (shared worktree; the shared index is left untouched).

## Step 1: task identity

Build the K-sensitivity curve: sealed profit as a function of the
GO/NO-GO decision bar K, over the committed IVWC sealed tables.
Follow-up to IVWC-LEARNERK (BUILD-PASS K1-K10), which named the
K-sensitivity curve as the remaining frontier ("for which K do the
rankings change?") and explicitly did not test it.

## Step 2: scope

Measurement wave on committed tables. No world, no learner, no new
mechanism, no verdict arms beyond the fixed-bar sweep
(GO iff adjucb > K) and the revealed-preference bar re-computed at
hypothetical train costs. L0/L1 measurement; no learning claim.

## Step 3: cleanliness

Zero python3/python invocations in this lane, all steps. Any
forbidden-interpreter invocation would make the wave PROCESS-FAIL
automatically; none occurred.
