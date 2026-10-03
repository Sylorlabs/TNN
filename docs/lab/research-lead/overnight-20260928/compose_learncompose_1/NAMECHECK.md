# NAMECHECK.md -- COMPOSE-LEARNCOMPOSE-1

Worker: COMPOSE-LEARNCOMPOSE-1. Lane:
`docs/lab/research-lead/overnight-20260928/compose_learncompose_1/`.
Non-ledger task (claim minting paused).

## Step 0: toolchain guard verification (recorded before any build)

- Safebin already present from prior lanes
  (`docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`);
  `export PATH="$HOME/safebin"`.
- `which python3` -> nothing. `which python` -> nothing. Confirmed:
  no `python3`/`python` resolves in the worker PATH.
- Pinned znc at
  `~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`.
- All research logic will be pure Zag, compiled with the pinned znc.
  Shell use is limited to: invoking znc, running binaries, git ops,
  moving/copying files. No Python, C/C++, JavaScript, or Rust in
  verifiers, scorers, harnesses, or analysis.
- If a forbidden executable is invoked, this wave is automatically
  PROCESS-FAIL.

## Naming check

- Lane name `compose_learncompose_1` matches the assigned lane.
- Hypothesis under test: C (LEARN-COMPOSE), per COMPOSE-GENERAL-1
  Section 6 (learner-owned composition policy, contract-defined
  revision operators).
- No identifier in this lane collides with `compose_backchain_1`
  (`bc_`) or `compose_suspend_1` (`sus_`): all source files use the
  `lc_` prefix; binaries are `lc_bin` / `lc_fc1_bin` /
  `lc_blind_bin`.
- Substrate files (`lc_base.zag`, `lc_thunk.zag`, `lc_search.zag`,
  `lc_world.zag`) are verbatim copies of the BACKCHAIN-1 substrate
  (same function names and logic); only the file names and header
  comments change. This is deliberate: C's cold-start IS the
  regressive substrate, so C = substrate + composition memory. Any
  behavioral difference between A and C is attributable to the
  memory layer alone.
