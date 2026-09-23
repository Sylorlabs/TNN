#!/bin/bash
# Ruling 5 E1 runner: unmodified wave-8 trial, VUP S1 cells B/C/C-P3 x variants x2.
set -u
R=~/workspace/tnn-lab/wave12/strength-rulings/r5
T=$R/trial
OUT=$R/evidence/e1
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
mkdir -p "$OUT"
LOG="$OUT/runner.log"
: > "$LOG"
note(){ echo "$1" | tee -a "$LOG"; }
fail(){ note "RUNNER_FAIL,$1"; exit 1; }
fail_n=0
note "== static checks (trial sources unmodified wave-8) =="
cd "$T" || exit 1
if grep -rniE 'rand\(|srand|getrandom|/dev/urandom|rdtsc' \
    strength_core.zag strength_checker.zag strength_learner.zag strength_trial.zag \
    >/dev/null 2>&1; then fail "RNG token found"; fi
for f in strength_core.zag strength_checker.zag strength_learner.zag strength_trial.zag; do
  if grep -q '^@import' "$f"; then :; else fail "$f import not bare"; fi
done
note "STATIC_OK"
note "== compile =="
"$ZNC" "$T/strength_trial.zag" --no-zagd --no-analyze --no-foreground-cache \
  -o "$R/r5_bin" || fail "compile"
note "COMPILE_OK"
note "== E1 cells =="
for arm in B C C-P3; do
  for v in 0 1 2; do
    for run in 1 2; do
      "$R/r5_bin" "$arm" VUP "$v" S1 > "$OUT/cell_${arm}_VUP_${v}_r${run}.log" 2>&1
      ec=$?
      if [ $ec -ne 0 ]; then note "FAIL cell_${arm}_VUP_${v}_r${run} exit=$ec"; fail_n=$((fail_n+1)); fi
      if ! grep -q "^ST_DONE$" "$OUT/cell_${arm}_VUP_${v}_r${run}.log"; then
        note "FAIL cell_${arm}_VUP_${v}_r${run} nodone"; fail_n=$((fail_n+1)); fi
    done
    if cmp -s "$OUT/cell_${arm}_VUP_${v}_r1.log" "$OUT/cell_${arm}_VUP_${v}_r2.log"; then
      : # deterministic
    else note "FAIL cell_${arm}_VUP_${v} nondeterministic"; fail_n=$((fail_n+1)); fi
  done
done
note "fail_n=$fail_n"
if [ "$fail_n" = 0 ]; then echo "E1_COMPLETE" > "$OUT/VERDICT.txt"; else echo "E1_FAILED" > "$OUT/VERDICT.txt"; fi
