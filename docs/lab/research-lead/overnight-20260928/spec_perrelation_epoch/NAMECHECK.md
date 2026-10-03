# SPEC-PERRELATION-EPOCH: NAMECHECK

**Lane:** docs/lab/research-lead/overnight-20260928/spec_perrelation_epoch/
**Date:** 2026-10-03

## Step 0: Toolchain guard (mandatory)

- Worker activated safebin: `export PATH="$HOME/safebin"` before any build.
- `which python3` returns nothing; `which python` returns nothing.
- Pinned compiler: `$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
  (same pinned znc as the SPEC-EPOCHTAG and SPEC-REFUSAL-RECOVERY lanes).
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
  (spec_epochtag), rr_spec.zag (spec_refusal_recovery). New: pe_world.zag
  (per-relation epoch table + drifts), pe_spec.zag (per-relation epoch
  gate + per-bucket relation-epoch stamping), pe_rr.zag (recovery
  wrappers), pe_main.zag (harness), pe_build.sh.
- Memory layout verified free before use: world arena A offsets 776+
  (facts end at 772, world epoch at 772; verified no reused file writes A
  at 776+); learner L tag slots at 13500/13564/13628 (da_learn max 13296,
  et tags end at 13492, L is 16384 bytes).

## Step 1: build/run verification (2026-10-03)

- `./pe_build.sh` run from the lane directory under safebin PATH.
- (To be filled after the build: clean build, 3x exit 0, empty stderr,
  byte-identity, kill-bar adjudication.)
