# NAMECHECK: L2-TRANSFER-SUBST Worker

Worker: L2 Transfer-Subst Worker (subagent, 2026-10-02).
Parent mandate: L2-TRANSFER-SUBST, run the C298 SUBSTITUTE operator
in the ARITHMETIC substrate with zero per-domain retuning.

## Step 0: Toolchain guard (recorded BEFORE any implementation)

- Ran `docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`;
  result: SAFEBIN-READY, 36 tools linked, pinned znc OK
  (`src/tools/toolchain/znc_linux_x86_64_abed8aa1`).
- `export PATH="$HOME/safebin"` for all subsequent shell work.
- `which python3` -> nothing (exit 1). `which python` -> nothing
  (exit 1). Setup script self-verified: "python3 absent from
  safebin PATH (OK)", "python absent from safebin PATH (OK)".
- Rule accepted: any invocation of a forbidden interpreter
  (python/python3 or equivalent) makes this wave PROCESS-FAIL.
- All computation in pure Zag, compiled with the pinned znc.
  Shell used only for: znc invocation, running built binaries,
  git operations, file moves/copies, text checks (grep/cmp/
  sha256sum/diff).
- Pinned-znc defect workarounds observed (from AGENTS.md):
  u8-backed cells with ig/is-style helpers (the copied learner
  uses get32/set32 byte ops, no `as *i32` slice construction);
  no `_zag_print` for dynamic output (single preallocated buffer
  plus one raw-syscall write loop, stdout bytes verified);
  no `as []f64`/`as []i64` length reliance; if-nesting kept at
  3 or fewer with hoisted flags; no `!(... && ...)` in any
  `while` condition (new Zag grepped for `while.*!(` before
  build); node budget far under the 1024-node workspace cap;
  bulk MAP teaching via direct m_teach calls.

## Step 1: Name collisions

- Directory `l2_transfer_subst/` is new; no collision with
  existing `l2_substitute/` (the chain-family source lane).
- File names (PREREG.md, NAMECHECK.md, REPORT.md, learner.zag,
  world.zag, driver.zag, arith_full.zag, arith_bin,
  arith_compile.txt, arith_run1/2/3.txt) do not collide with
  anything in the repo.
- Binary name `arith_bin` is distinct from `sub_bin`.
- The learner file `learner.zag` is INTENDED to be
  byte-identical to `l2_substitute/learner.zag`; this is the
  mechanism-generality bar K-11, verified by sha256/cmp, not a
  collision.

## Dev notes

- 2026-10-02: Step 0 guard recorded. PREREG.md written and
  committed alone next (commit-order self-check K-0).
