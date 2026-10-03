# SPEC-COMMIT-L: NAMECHECK

**Lane:** docs/lab/research-lead/overnight-20260928/spec_commit_l/
**Date:** 2026-10-03
**Status:** Non-ledger (claim minting paused). Local commits only, never pushed.

## Step 0: Toolchain guard (mandatory)

- Worker activated safebin: `export PATH="$HOME/safebin"` before any build.
- `which python3` returns nothing; `which python` returns nothing
  (verified 2026-10-03 on this machine before any lane work).
- Pinned compiler: `$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
  (sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef,
  identical to the SPEC-L-DISCIPLINE pinned znc; verified before building,
  re-verified in-script on every build).
- All research logic in pure Zag. No Python, C, JS, or Rust in verifiers,
  scorers, harnesses, or analysis. Output analysis via grep/cmp/awk/sed/
  shell arithmetic only.
- znc defect workarounds observed (per AGENTS.md and the parent lane):
  no `as *i32` slice construction (u8-backed get32/set32 only); dynamic
  output via single-buffer `o_app`/`o_i64` + one `_zag_raw_syscall` flush
  via o_flush (never `_zag_print`); `if` nesting kept at 3 or fewer with
  hoisted flags; no `!(A && B)` in while conditions; no `||` in Zag `if`
  conditions in new code (separate `if`s instead); no modulo operator
  (countdown counters for checkpoints); no `[]u8 as *u8` casts; i64 used
  for LCG state and threshold arithmetic (2^31 exceeds i32). New deltas
  (scl_commit_decide dispatch, pol-14 blk flag, nr_decide_ft hoisted
  lzmult/egl for pol 13/14/15) are depth-1 `if`s only with lets hoisted
  to function top level.
- Git: `/usr/bin/git` used directly for all commits (safebin git symlink
  breaks object/index writes with EPERM per AGENTS.md lesson); explicit
  pathspecs on every commit; commits local, never pushed.

## Step 1: Lane files

- PREREG.md: frozen questions, design, predictions, kill bars K1-K9.
- cl_spec.zag: copy-plus-delta of the parent lane's ld_spec.zag
  ([CL-DELTA] markers); the parent's file is never edited.
- cl_main.zag: harness main, 4 cells x 22 arms = 88 episodes.
- cl_build.sh: assemble + build + 3x run + kill-bar adjudication.
- cl_posthoc.sh: finding tables on the frozen data (post-hoc
  analysis only; must not move any frozen bar).

## Step 2: Provenance

- Cells, seeds, arrival mechanics, EWMA, margin test, flip mechanics,
  guard, and pol-3 code inherited unchanged from SPEC-L-DISCIPLINE
  (BUILD-PASS K1-K9); the parent's frozen ld_run1.txt (sha256
  36d63552f3e3ec5bfd664bc9b40a1043c47c89ce181881bd5c94726fc0781b4b)
  is the replication anchor for K4d.
- New arms: pol 13 "coml1" (L-free commit, L := 1), pol 14 "comlg"
  (L-free commit + minimum-data guard), pol 15 "comnoeg" (L-free
  commit, eager direction dropped). All three run the parent's noeg
  (pol 10) L-free flip discipline.
