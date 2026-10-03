# NAMECHECK.md -- COMPOSE-BACKCHAIN-1

Worker: COMPOSE-BACKCHAIN-1 (retry). Lane:
`docs/lab/research-lead/overnight-20260928/compose_backchain_1/`.
Non-ledger task (claim minting paused).

## Step 0: toolchain guard verification (recorded before any build)

- Ran `docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
  (already present from prior lanes); `export PATH="$HOME/safebin"`.
- `which python3` -> nothing. `which python` -> nothing. Confirmed:
  no `python3`/`python` resolves in the worker PATH.
- Safebin contains 36 allowed tools (coreutils + git); pinned znc at
  `~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`.
- All research logic will be pure Zag, compiled with the pinned znc.
  Shell use is limited to: invoking znc, running binaries, git ops,
  moving/copying files. No Python, C/C++, JavaScript, or Rust in
  verifiers, scorers, harnesses, or analysis.
- If a forbidden executable is invoked, this wave is automatically
  PROCESS-FAIL.

## Naming check

- Lane name `compose_backchain_1` matches the assigned lane.
- Hypothesis under test: A (BACKCHAIN), per COMPOSE-GENERAL-1 Section 4.
- No identifier in this lane collides with `compose_suspend_1`
  (prefix `bc_` vs `sus_` on all source files; separate binaries
  `bc_bin` / `bc_blind_bin`).
