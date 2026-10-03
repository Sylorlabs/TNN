# SPEC-NOISY-RATES: NAMECHECK

**Lane:** docs/lab/research-lead/overnight-20260928/spec_noisy_rates/
**Date:** 2026-10-03
**Status:** Non-ledger (claim minting paused). Local commits only, never pushed.

## Step 0: Toolchain guard (mandatory)

- Worker activated safebin: `export PATH="$HOME/safebin"` before any build.
- `which python3` returns nothing; `which python` returns nothing.
- Pinned compiler: `$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
  (sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef,
  identical to the SPEC-ADAPTIVE-SWITCH pinned znc).
- All research logic in pure Zag. No Python, C, JS, or Rust in verifiers,
  scorers, harnesses, or analysis. Output analysis via grep/cmp/awk/shell
  arithmetic only.
- znc defect workarounds observed: no `as *i32` slice construction (u8-backed
  get32/set32 only); dynamic output via single-buffer `o_app`/`o_i64` + one
  `_zag_raw_syscall` flush via o_flush (never `_zag_print`); `if` nesting
  kept at 3 or fewer with hoisted flags; no `!(A && B)` in while conditions;
  no modulo operator (hand-rolled `s - (s/d)*d`; countdown counters for
  checkpoints); no `[]u8 as *u8` casts; i64 used for LCG state and
  threshold arithmetic (2^31 exceeds i32).
- Git: `/usr/bin/git` used directly for all commits (safebin git symlink
  breaks object/index writes with EPERM per AGENTS.md lesson); explicit
  pathspecs on every commit; never push; retry with sleep backoff on
  index.lock contention, never remove the lock while others are active.
- `da_learn.zag` is NOT modified in this lane (separate lane only, per
  task). Reused byte-unmodified: da_base.zag, da_module.zag, da_learn.zag
  (disagreement_attribution), rb_world.zag, rb_fix.zag
  (spec_relationblind), et_world.zag, et_spec.zag (spec_epochtag),
  rr_spec.zag (spec_refusal_recovery), ld_spec.zag (spec_lazy_default,
  the lazy on-demand query path and ld_grid). New lane files only:
  nr_spec.zag (noisy-rate policy layer: bursty arrival processes, EWMA
  rate/variance estimation, confidence-interval margin test, commit /
  re-check logic), nr_main.zag (harness), nr_build.sh (build + run +
  bar adjudication).
