# TNN-2 Independent Reproducer NAMECHECK

## Step 0: Toolchain guard (mandatory)

Run at worker start, 2026-10-01 UTC:

- Created `$HOME/safebin` and linked only allowed tools:
  `git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack`.
- Exported `PATH="$HOME/safebin"`.
- `which python3 python` returned nothing (`guard-check-done`).
- No forbidden executable was invoked at any point in this wave.
- Pinned compiler verified: `$HOME/safebin/znc` resolves via symlink to
  `src/tools/toolchain/znc_linux_x86_64_abed8aa1`;
  both paths SHA-256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`;
  `znc version` reports `znc 2026.07.0-dev (edition 2026)`.

**Guard status: PASS. No Python, C/C++, JS, Rust, or other interpreters used.
All computation via znc-compiled Zag; shell used only to invoke znc, run
binaries, do git operations, and move/copy files.**

## Step 1: Identity of worker and mission

- Worker: TNN-2 Independent Reproducer.
- Build under test: commit `f4de7ff46` (TNN2-BUILD-PASS).
- HEAD at reproduction time: `f4de7ff46` exactly (build under test is HEAD).

## Step 2: Owned path only

- Owned: `docs/lab/research-lead/overnight-20260928/tnn2_repro/` only.
- `tnn2_build/` was read-only; never modified.
- Source compiled in a clean scratch directory (`/tmp/tnn2_repro_clean`); the
  committed `tnn2_bin` was never copied as a build input.

## Step 3: What this reproduction establishes

- Source hash verification: PASS.
- From-scratch compile with pinned znc: PASS.
- Fresh binary byte-identical to committed `tnn2_bin`: PASS.
- Three test-suite runs: 46/46 each, byte-identical to each other and to
  committed `run1/2/3.txt`: PASS.
- Spot checks of the three changes: PASS.
- Verdict: TNN2-REPRO-PASS. This is a reproduction verdict only, not SURVIVES.
