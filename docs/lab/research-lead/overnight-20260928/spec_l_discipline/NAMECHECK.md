# SPEC-L-DISCIPLINE: NAMECHECK

**Lane:** docs/lab/research-lead/overnight-20260928/spec_l_discipline/
**Date:** 2026-10-03
**Status:** Non-ledger (claim minting paused). Local commits only, never pushed.

## Step 0: Toolchain guard (mandatory)

- Worker activated safebin: `export PATH="$HOME/safebin"` before any build.
- `which python3` returns nothing; `which python` returns nothing
  (verified 2026-10-03 on this machine before any lane work).
- Pinned compiler: `$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
  (sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef,
  identical to the SPEC-FLIP-THRESHOLD pinned znc; verified before building,
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
  (nr_decide_ft hoisted egl flag for pol 10/12, lzmult = 1 for pol
  10/11/12) are depth-1 `if`s only; the com == 1 branch nests at most 2.
- Git: `/usr/bin/git` used directly for all commits (safebin git symlink
  breaks object/index writes with EPERM per AGENTS.md lesson); explicit
  pathspecs on every commit; never push; retry with sleep backoff on
  index.lock contention, never remove the lock while others are active.
- `da_learn.zag` is NOT modified in this lane (separate lane only, per
  task). Reused byte-unmodified from sibling lanes: da_base.zag,
  da_module.zag, da_learn.zag (disagreement_attribution), rb_world.zag,
  rb_fix.zag (spec_relationblind), et_world.zag, et_spec.zag
  (spec_epochtag), rr_spec.zag (spec_refusal_recovery), ld_spec.zag
  (spec_lazy_default). The flip-threshold lane's ft_spec.zag is superseded
  by copy-plus-delta (ld_spec.zag), never edited. New lane files only:
  ld_spec.zag (L-discipline policy layer: byte-copy of the parent's
  ft_spec.zag with minimal documented [LD-DELTA]s: nr_decide_ft gains
  the hoisted egl flag (egl = 1 for pol 10/12, else egl = L;
  `if(egl*phid>phin){ eg=1; }`) and lzmult = 1 for pol 10/11/12 so all
  three new arms use the fix2 lazy bar; pol 8/9 branches kept dormant,
  not swept; nr_decide itself, the commit rule, the eager-decisive
  direction's form, the EWMA, the grid, and pol-3 code are the parent's,
  unchanged; pol 3 dormant, not swept), ld_main.zag (harness: 4
  inherited cells x 22 arms), ld_build.sh (build + 3 runs + bar
  adjudication), ld_posthoc.sh (post-hoc finding tables on the frozen
  data, including the J' = rb + rf L-free scoring).

## Step 1: Prereg discipline

- PREREG.md (frozen kill bars K1-K9, frozen mechanism analysis of where
  L enters after fix2, frozen predictions with J' calibrated from the
  parent's frozen ft_run1.txt, falsifiers) committed strictly before
  any implementation file exists in this lane. This NAMECHECK.md is
  committed alongside the prereg, before implementation. K1 verified via
  git log order on the lane directory: PREREG -> NAMECHECK ->
  implementation.
- No new seed probe: regime cells (R = 21/60/82/120) and their D32/Q32
  properties are inherited from SPEC-FLIP-LATENCY / SPEC-FLIP-THRESHOLD
  frozen data; the probe-inversion pattern is cited, not re-run.
- J' calibration (finding, not a bar): from the parent's frozen R = 60
  lines, fix2 has od = 10, rs = 22, rebuilds = 32 at every L, so
  J'_fix2 = 32 + 10 = 42 at every L; adapt L = 7 has od = 3, rs = 118,
  rebuilds = 121, so J'_adapt(7) = 121 + 3 = 124; eager has
  rebuilds = 133, refusals = 0, so J'_eager = 133. The K7b findings use
  inequalities on the measured data; the exact calibrated values are
  frozen predictions.
- Scope note: the four conditions are exactly neither / eager-direction
  / J-accounting / both. The pre-shift commit rule keeps L in all arms
  (out of scope); its L-dependence on R = 120 (cm = 0 at L = 1/3 vs
  cm = 2 at L = 7/10 in the frozen parent data) is reported as a
  finding bounding the L-free claim, not a variant.
