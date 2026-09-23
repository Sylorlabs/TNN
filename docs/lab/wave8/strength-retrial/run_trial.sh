#!/bin/bash
# Wave-8 strength re-trial runner: static checks -> compile -> GATE 2x ->
# S1 matrix 2x -> determinism -> kill/promotion analysis.
# Prereg: ~/workspace/tnn-lab/wave8/strength-retrial/PREREG_STRENGTH_V2.md
# No RNG anywhere; outputs must be byte-identical.
set -u
D=~/workspace/tnn-lab/wave8/strength-retrial
T=$D/trial
OUT=$D/evidence
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
mkdir -p "$OUT"
LOG="$OUT/runner.log"
: > "$LOG"
note(){ echo "$1" | tee -a "$LOG"; }
fail(){ note "RUNNER_FAIL,$1"; exit 1; }
pass=0; fail_n=0

note "== static checks =="
cd "$T" || exit 1
# 1. no direct strength writes outside strength_core.zag
for f in strength_learner.zag strength_trial.zag strength_checker.zag; do
  if grep -nE 'st_write_strength|st_clear_strength' "$f" >/dev/null 2>&1; then
    fail "strength write outside core in $f"
  fi
done
# 2. no RNG tokens in decision paths (learner/core/trial/checker)
if grep -rniE 'rand\(|srand|getrandom|/dev/urandom|rdtsc' strength_core.zag strength_learner.zag strength_trial.zag strength_checker.zag >/dev/null 2>&1; then
  fail "RNG token found"
fi
# 3. frozen formulas present verbatim
grep -q '(7\*m+13\*v+3)%10)<3' strength_learner.zag || fail "imp formula changed"
grep -q '(m+3)%10)<3' strength_learner.zag || fail "wrong formula changed"
grep -q '(m+3)%10)<3' strength_checker.zag || fail "checker wrong formula changed"
# implants k=0..5
grep -q 'k<=5' strength_learner.zag || fail "implant range changed (learner)"
grep -q 'k<=5' strength_checker.zag || fail "implant range changed (checker)"
# designation predicate
grep -q 'm%50' strength_learner.zag || fail "designation predicate missing"
grep -q 'lr_designated' strength_learner.zag || fail "lr_designated missing"
grep -q 'lr_designated' strength_trial.zag || fail "trial not using lr_designated"
# 4. bare @import
for f in strength_core.zag strength_learner.zag strength_trial.zag strength_checker.zag; do
  grep -q '^@import' "$f" || fail "$f import not bare"
done
# 5. P3 opcodes and roles present
grep -q 'ST_OP_PEXPIRED' strength_core.zag || fail "PEXPIRED opcode missing"
grep -q 'ST_ROLE_SYSTEM' strength_core.zag || fail "SYSTEM role missing"
# 6. no st_redeclare without cite_ep (signature check)
grep -q 'st_strengthen_cited' strength_core.zag || fail "st_strengthen_cited missing"
grep -q 'st_protection_expired' strength_core.zag || fail "st_protection_expired missing"
note "STATIC_OK"
pass=$((pass+1))

note "== compile =="
"$ZNC" strength_trial.zag --no-zagd --no-analyze --no-foreground-cache -o trial_bin || fail "compile"
note "COMPILE_OK"
pass=$((pass+1))
BIN="$T/trial_bin"

note "== GATE (2x per arm) =="
gate_fail=0
for arm in B C C-P3; do
  if [ "$arm" = "B" ]; then arm_num=1; elif [ "$arm" = "C" ]; then arm_num=2; else arm_num=3; fi
  for run in 1 2; do
    "$BIN" "$arm" GATE 0 S1 > "$OUT/gate_${arm}_r${run}.log" 2>&1
    ec=$?
    if [ $ec -ne 0 ]; then note "FAIL gate_${arm}_r${run} exit=$ec"; gate_fail=1; fi
  done
  if cmp -s "$OUT/gate_${arm}_r1.log" "$OUT/gate_${arm}_r2.log"; then
    note "PASS gate_${arm}_deterministic"
  else
    note "FAIL gate_${arm}_deterministic"; gate_fail=1
  fi
  if grep -q "^ST_GATE ${arm_num} 0$" "$OUT/gate_${arm}_r1.log"; then
    note "PASS gate_${arm}_checks"
  else
    note "FAIL gate_${arm}_checks"; gate_fail=1
  fi
done
if [ "$gate_fail" = "1" ]; then
  note "GATE FAILED - trial stops per prereg"
  echo "GATE_FAILED" > "$OUT/VERDICT.txt"
  exit 1
fi
note "GATE_OK"
pass=$((pass+1))

note "== S1 cells (2x each) =="
for arm in B C C-P3; do
  for cur in VUP WBS JI; do
    for var in 0 1 2; do
      for run in 1 2; do
        "$BIN" "$arm" "$cur" "$var" S1 > "$OUT/cell_${arm}_${cur}_${var}_r${run}.log" 2>&1
        ec=$?
        if [ $ec -ne 0 ]; then note "FAIL cell_${arm}_${cur}_${var}_r${run} exit=$ec"; fail_n=$((fail_n+1)); fi
      done
      if cmp -s "$OUT/cell_${arm}_${cur}_${var}_r1.log" "$OUT/cell_${arm}_${cur}_${var}_r2.log"; then
        : # deterministic
      else
        note "FAIL cell_${arm}_${cur}_${var}_deterministic"; fail_n=$((fail_n+1))
      fi
      if grep -q "^ST_INVALID 1$" "$OUT/cell_${arm}_${cur}_${var}_r1.log"; then
        note "FAIL cell_${arm}_${cur}_${var}_invalid"; fail_n=$((fail_n+1))
      fi
      if ! grep -q "^ST_DONE$" "$OUT/cell_${arm}_${cur}_${var}_r1.log"; then
        note "FAIL cell_${arm}_${cur}_${var}_nodone"; fail_n=$((fail_n+1))
      fi
    done
  done
done
note "S1 cells done: fail_n=$fail_n"
if [ "$fail_n" = "0" ]; then echo "S1_COMPLETE" > "$OUT/VERDICT.txt"; else echo "S1_FAILED" > "$OUT/VERDICT.txt"; fi
note "== done =="
