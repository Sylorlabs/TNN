# SPEC-LAZY-DEFAULT: NAMECHECK

**Lane:** docs/lab/research-lead/overnight-20260928/spec_lazy_default/
**Date:** 2026-10-03

## Step 0: Toolchain guard (mandatory)

- Worker activated safebin: `export PATH="$HOME/safebin"` before any build.
- `which python3` returns nothing; `which python` returns nothing.
- Pinned compiler: `$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
  (symlinked as `$HOME/safebin/znc`; sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef,
  identical to the SPEC-DRIFTRATE-SWEEP pinned znc).
- All research logic in pure Zag. No Python, C, JS, or Rust in verifiers,
  scorers, harnesses, or analysis. Output analysis via grep/cmp only.
- znc defect workarounds observed: no `as *i32` slice construction (u8-backed
  get32/set32 only); dynamic output via single-buffer `o_app`/`o_i64` + one
  `_zag_raw_syscall` flush via o_flush (never `_zag_print`); `if` nesting
  kept at 3 or fewer with hoisted flags; no `!(A && B)` in while conditions;
  no modulo operator (countdown counters instead).
- Git: `/usr/bin/git` used directly for all commits (safebin git symlink
  breaks object/index writes with EPERM per AGENTS.md lesson); explicit
  pathspecs on every commit; never push; retry with sleep backoff on
  index.lock contention, never remove the lock while others are active.
- `da_learn.zag` is NOT modified in this lane (separate lane only, per
  task). Reused byte-unmodified: da_base.zag, da_module.zag, da_learn.zag
  (disagreement_attribution), rb_world.zag, rb_fix.zag
  (spec_relationblind), et_world.zag, et_spec.zag (spec_epochtag),
  rr_spec.zag (spec_refusal_recovery, the lazy on-demand mechanism). New
  lane files only: ld_spec.zag (default-policy layer), ld_main.zag
  (harness), ld_build.sh (build + run + bar adjudication).
