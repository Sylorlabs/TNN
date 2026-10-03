# SPEC-ABSTENTION-TRAP: NAMECHECK

**Lane:** docs/lab/research-lead/overnight-20260928/spec_abstention_trap/
**Date:** 2026-10-03
**Status:** Non-ledger (claim minting paused). Local commits only, never pushed.

## Step 0: Toolchain guard (mandatory)

- Worker activated safebin: `export PATH="$HOME/safebin"` before any build.
- `which python3` returns nothing; `which python` returns nothing
  (verified 2026-10-03 on this machine before any lane work).
- Pinned compiler: `$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
  (sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef,
  identical to the SPEC-REGIME-CHANGE pinned znc; verified before building,
  re-verified in-script on every build).
- All research logic in pure Zag. No Python, C, JS, or Rust in verifiers,
  scorers, harnesses, or analysis. Output analysis via grep/cmp/awk/shell
  arithmetic only.
- znc defect workarounds observed (per AGENTS.md and the parent lane):
  no `as *i32` slice construction (u8-backed get32/set32 only); dynamic
  output via single-buffer `o_app`/`o_i64` + one `_zag_raw_syscall` flush
  via o_flush (never `_zag_print`); `if` nesting kept at 3 or fewer with
  hoisted flags; no `!(A && B)` in while conditions; no modulo operator
  (countdown counters for checkpoints); no `[]u8 as *u8` casts; i64 used
  for LCG state and threshold arithmetic (2^31 exceeds i32). No `||` in
  Zag `if` conditions in new code (separate `if`s instead).
- Git: `/usr/bin/git` used directly for all commits (safebin git symlink
  breaks object/index writes with EPERM per AGENTS.md lesson); explicit
  pathspecs on every commit; never push; retry with sleep backoff on
  index.lock contention, never remove the lock while others are active.
- `da_learn.zag` is NOT modified in this lane (separate lane only, per
  task). Reused byte-unmodified from sibling lanes: da_base.zag,
  da_module.zag, da_learn.zag (disagreement_attribution), rb_world.zag,
  rb_fix.zag (spec_relationblind), et_world.zag, et_spec.zag
  (spec_epochtag), rr_spec.zag (spec_refusal_recovery), ld_spec.zag
  (spec_lazy_default, the lazy on-demand query path and ld_grid).
  New lane files only: at_spec.zag (abstention-trap policy layer:
  derived from the parent's rc_spec.zag with a minimal documented
  delta: the pol-3 deferred re-check branch in at_checkpoint, the lc
  late-commit flag at CS+116, pol-3 naming/episode plumbing; the
  estimator, margin test, commit rule, and flip rule are the parent's,
  unchanged), at_main.zag (harness: 6 trap/boundary cells x 10 arms),
  at_build.sh (build + 3 runs + bar adjudication). probe.zag is
  pre-prereg design tooling (arrival counts only), not experiment
  implementation.

## Step 1: Prereg discipline

- PREREG.md (frozen kill bars K1-K8, frozen predictions, falsifiers)
  committed strictly before any implementation file exists in this
  lane (commit c75ed50ae). This NAMECHECK.md is committed alongside
  the prereg, before implementation. K1 verified via git log order on
  the lane directory: probe (de48ebc8a) -> PREREG (c75ed50ae) ->
  NAMECHECK -> implementation.
