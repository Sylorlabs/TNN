# NAMECHECK: GEN-REDIM

Worker: gen-redim. Date: 2026-10-03.
Lane: `docs/lab/research-lead/overnight-20260928/gen_redim/`
Task: re-dimension GEN's scratch arena from hard-coded 4-MAP layout to a
dynamic NM-parameterized layout; preserve all compositional semantics;
verify on the GEN-STRESS S1-S5 battery (original predictions) plus the
frozen nm<=4 regression batteries.

## Step 0: toolchain guard (worker governance)

- Safebin active: `export PATH="$HOME/safebin"` at session start.
- `which python3` returns nothing; `which python` returns nothing.
- All computational research operations in pure Zag via pinned safebin
  znc. Shell only for: znc, binary runs, git ops, file assembly,
  byte-verification (cmp/sha256sum/diff/grep/sed/awk).
- No forbidden interpreter invocation. Any such invocation would make
  this wave PROCESS-FAIL.
- Git via /usr/bin/git directly (safebin git symlink EPERM defect, per
  AGENTS.md); explicit pathspecs only; never git reset on the shared
  branch; dedicated lane branch lane-genredim-20261003.

## Step 1: frozen source digests (verified before implementation)

GEN-STRESS lane
(docs/lab/research-lead/overnight-20260928/gen_stress/, branch
lane-genstress-20261003), the frozen mechanism under test:
- ref_gs_base.zag (frozen d6_base.zag):
  a53cdf0126ab1501fb70d9b14c2f745e0ef1838209753df8a0c6d0daf484bbcb
- ref_gs_gen.zag (frozen d6_gen.zag, 270 lines, main at 240-270):
  d6f1f9d8f4747293bb7a8e99474660347dc24693f62f3d25caaf1d83c19c9d9a
- gs_new.zag (frozen GEN-STRESS setups + driver):
  f23258bb6ad3b140f5b741ba90576fa8503f167c884948604c971987d1186c81

Frozen reference outputs (byte-identity targets):
- gen_cycles/ref_diamond_out.txt (diamond battery, nm<=4):
  962ca4f0f65228d92b007b5194852f2778d7b52e583442e8bf687b451bc76f84
- gen_cycles/ref_gg_out.txt (generality battery, nm=4):
  4b81226d665735820fec1ec4c0dc3e0447b9947b8069f8618b8ad59e87740752

GEN-STRESS original predictions (PREREG.md Section 6, this branch):
- S1: ANS=2 TRIES=29, exact 30-line block, no WIDEN
- S2: ANS=219 TRIES=48, exact 51-line block, no WIDEN
  (NOTE: this block is shown in the GEN-REDIM PREREG to contain
  hand-derivation errors; the corrected rule-derived block is the
  frozen kill-bar target. See PREREG Section 6.)
- S3: WIDEN=1, ANS=207 TRIES=8, exact 10-line block
- S4: ANS=-2 TRIES=48, exact 49-line block, no WIDEN=1
- S5: ARM=GEN PROB=S5 ANS=-2 TRIES=2734; 3 INTER= lines;
  2731 INTER2= lines; zero WIDEN=1 lines

Lane reference copies (byte-copies, verified by sha256 in build.sh):
- ref_rd_base.zag <= gen_stress/ref_gs_base.zag
- ref_rd_gen.zag <= gen_stress/ref_gs_gen.zag
- ref_gs_new.zag <= gen_stress/gs_new.zag (setup source)

## Step 0-clean: clean-reproduction worker guard (GEN-REDIM-CLEAN)

- Safebin activated as the very first action of the reproduction
  session: `export PATH="$HOME/safebin"`, before any other command.
- `which python3` -> nothing. `which python` -> nothing.
  `which perl`, `which ruby`, `which node` -> nothing.
- This worker performed NO python3/python/perl/ruby/node invocation
  at any point; all verification via safebin tools (znc, sh, cmp,
  diff, grep, sed, awk, sha256sum, wc, cut, tail).
- The implementation sources (rbase.zag, rgen.zag, drivers, PREREG.md)
  were NOT modified; build.sh re-run from the committed frozen
  state constitutes the clean reproduction.

## Step 2: prereg commit order

- This NAMECHECK.md (Steps 0-2) + PREREG.md commit strictly precedes
  all implementation (new .zag files, builds, runs).
- C1 audits this via git log order on branch lane-genredim-20261003.
