# NAMECHECK: L3-SUF-1-SCALING worker

**Worker:** L3-SUF-1-SCALING (subagent, depth 2/2)
**Date:** 2026-10-03
**Task:** scaling study of the frozen L3-SUF-1 resolution-records mechanism. Non-ledger task.

## Step 0: toolchain guard verification

- `export PATH="$HOME/safebin"` is set before every build/run command.
- `which python3` returns nothing under the safebin PATH (verified 2026-10-03; see build log).
- `which znc` resolves to `$HOME/safebin/znc` (pinned toolchain).
- All research logic (world builders, driver, scoring) is pure Zag.
  Shell is used only for: invoking znc, running binaries, git ops,
  file moves/copies, sha256sum. No Python, C/C++, JavaScript, or Rust
  anywhere in the lane.
- If a forbidden executable is invoked, this wave is automatically
  PROCESS-FAIL per the worker toolchain guard.

## Step 1: frozen-source integrity

- The builder's `src/` is linked READ-ONLY (concatenated at build time,
  never edited). sha256 of each frozen source recorded at build time in
  `build/frozen_src.sha256` (re-verified before every build).
- The adversary's sealed worlds and KEY.md are NOT inspected or linked.
- Scaling worlds (`scale_world.zag`) and the driver (`scale_main.zag`)
  are this worker's own code.

## Step 2: prereg discipline

- PREREG.md frozen and committed BEFORE any implementation file exists
  under l3_suf_scaling/ (commit-order self-check: freeze commit contains
  only PREREG.md + NAMECHECK.md).
- Kill bars SC-K1..SC-K6 are discrimination instruments; a FAIL at some
  scale is the intended signal (scaling envelope), not a verdict on the
  L3 claim.

## Step 3: determinism

- 3/3 byte-identical stdout per run; sha256 digests recorded in runs/.
- Fixed RNG seeds per (family, scale). No wall-clock in program output
  (runtime measured externally via shell).
