# NAMECHECK.md -- COMPOSE-ADVERSARY

Worker: COMPOSE-ADVERSARY. Lane:
`docs/lab/research-lead/overnight-20260928/compose_adversary/`.
Branch: `tnn-native-lab`. Non-ledger task (claim minting paused).

## Step 0: toolchain guard verification (recorded before any build)

- Safebin already present at `$HOME/safebin` (36 allowed tools:
  coreutils + git + pinned znc). `export PATH="$HOME/safebin"`.
- `which python3` -> nothing (rc=1). `which python` -> nothing
  (rc=1). Confirmed: no `python3`/`python` resolves in the worker
  PATH.
- Pinned znc at
  `~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
  resolves via safebin (`which znc`).
- All research logic in this lane is pure Zag, compiled with the
  pinned znc. Shell use is limited to: invoking znc, running
  binaries, git ops, moving/copying files. No Python, C/C++,
  JavaScript, or Rust in world builders, witness checkers, or
  analysis.
- If a forbidden executable is invoked, this wave is automatically
  PROCESS-FAIL.

## Naming check

- Lane name `compose_adversary` matches the assigned lane.
- Role: adversary. This lane designs SEALED WORLDS for hypotheses
  A (BACKCHAIN), B (SUSPEND), C (LEARN-COMPOSE). It does not
  implement, modify, or re-tune any mechanism.
- No identifier in this lane collides with builder lanes. All new
  Zag symbols use the `adv_` prefix. Builder lane directories
  (`compose_backchain_1`, `compose_suspend_1`,
  `compose_learncompose_1`) are read-only to this worker; no file
  there is created, modified, or deleted.
- Sealed worlds live in `adv_worlds.zag` (world builders) and are
  validated by `adv_witness.zag` (independent witness checker).
  The adversary does NOT execute any mechanism binary on the
  sealed worlds. That is reserved for the independent sealed
  evaluation run by the parent.
