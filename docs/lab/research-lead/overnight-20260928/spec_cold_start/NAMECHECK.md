# SPEC-COLD-START: NAMECHECK

**Lane:** docs/lab/research-lead/overnight-20260928/spec_cold_start/
**Date:** 2026-10-03
**Status:** Non-ledger (claim minting paused). Local commits only, never pushed.

## Step 0: Toolchain guard (mandatory)

- Worker activated safebin: `export PATH="$HOME/safebin"` before any build.
- `which python3` returns nothing; `which python` returns nothing
  (verified 2026-10-03 on this machine before any lane work).
- Pinned compiler: `$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
  (sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef,
  identical to the SPEC-ABSTENTION-TRAP pinned znc; verified before building,
  re-verified in-script on every build).
- All research logic in pure Zag. No Python, C, JS, or Rust in verifiers,
  scorers, harnesses, or analysis. Output analysis via grep/cmp/awk/shell
  arithmetic only.
- znc defect workarounds observed (per AGENTS.md and the parent lane):
  no `as *i32` slice construction (u8-backed get32/set32 only); dynamic
  output via single-buffer `o_app`/`o_i64` + one `_zag_raw_syscall` flush
  via o_flush (never `_zag_print`); `if` nesting kept at 3 or fewer with
  hoisted flags (the guard condition is computed as a hoisted `blk`
  flag, never nested deeper than 2); no `!(A && B)` in while conditions;
  no modulo operator (countdown counters for checkpoints); no `[]u8 as *u8`
  casts; i64 used for LCG state and threshold arithmetic (2^31 exceeds
  i32). No `||` in Zag `if` conditions in new code (separate `if`s instead).
- Git: `/usr/bin/git` used directly for all commits (safebin git symlink
  breaks object/index writes with EPERM per AGENTS.md lesson); explicit
  pathspecs on every commit; never push; retry with sleep backoff on
  index.lock contention, never remove the lock while others are active.
- `da_learn.zag` is NOT modified in this lane (separate lane only, per
  task). Reused byte-unmodified from sibling lanes: da_base.zag,
  da_module.zag, da_learn.zag (disagreement_attribution), rb_world.zag,
  rb_fix.zag (spec_relationblind), et_world.zag, et_spec.zag
  (spec_epochtag), rr_spec.zag (spec_refusal_recovery), ld_spec.zag
  (spec_lazy_default), plus at_spec.zag (spec_abstention_trap, the
  parent lane: superseded by copy-plus-delta, never edited). New lane
  files only: cs_spec.zag (cold-start policy layer: byte-copy of the
  parent's at_spec.zag with a minimal documented [CS-DELTA]: the
  pol-4 minimum-data guard in cs_checkpoint, pol-4 naming/episode
  plumbing; the estimator, margin test, commit rule, flip rule, and
  pol-3 code are the parent's, unchanged; pol 3 dormant, not swept),
  cs_main.zag (harness: 4 cold-start cells x 10 arms), cs_build.sh
  (build + 3 runs + bar adjudication). probe.zag is pre-prereg design
  tooling (arrival counts only), not experiment implementation.

## Step 1: Prereg discipline

- PREREG.md (frozen kill bars K1-K8, frozen predictions, falsifiers)
  committed strictly before any implementation file exists in this
  lane. This NAMECHECK.md is committed alongside the prereg, before
  implementation. K1 verified via git log order on the lane
  directory: probe (fc4f4cb2b) -> PREREG (e414d0733) ->
  NAMECHECK -> implementation.
