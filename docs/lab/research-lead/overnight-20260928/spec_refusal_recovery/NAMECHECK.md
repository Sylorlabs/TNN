# SPEC-REFUSAL-RECOVERY: NAMECHECK

**Lane:** docs/lab/research-lead/overnight-20260928/spec_refusal_recovery/
**Date:** 2026-10-03

## Step 0: Toolchain guard (mandatory)

- Worker activated safebin: `export PATH="$HOME/safebin"` before any build.
- `which python3` returns nothing; `which python` returns nothing.
- Pinned compiler: `$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
  (same pinned znc as the SPEC-EPOCHTAG lane).
- All research logic in pure Zag. No Python, C, JS, or Rust in verifiers,
  scorers, harnesses, or analysis. Output analysis via grep/cmp only.
- znc defect workarounds observed: no `as *i32` slice construction; dynamic
  output via single-buffer `o_app`/`o_i64` + one `_zag_raw_syscall` (never
  `_zag_print`); `if` nesting kept at 3 or fewer with hoisted flags; no
  `!(A && B)` in while conditions.
- Git: `/usr/bin/git` used directly for all commits (safebin git symlink
  breaks object/index writes with EPERM per AGENTS.md lesson); explicit
  pathspecs on every commit; never push.
- `da_learn.zag` is NOT modified in this lane (separate lane only, per task).
  Reused byte-unmodified: da_base.zag, da_module.zag, da_learn.zag,
  rb_world.zag, rb_fix.zag (spec_relationblind), et_world.zag, et_spec.zag
  (spec_epochtag). New: rr_spec.zag (recovery wrappers), rr_main.zag
  (harness), rr_build.sh.

## Steps 1..n: reserved for build/run verification records
