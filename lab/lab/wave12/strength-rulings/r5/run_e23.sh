#!/bin/bash
# Ruling 5 E2/E3 runner: scripted treatment harness.
# E2: frozen/p3 x cites=1. E3: frozen/p3/forced x cites=0. Each x2, diffed.
set -u
R=~/workspace/tnn-lab/wave12/strength-rulings/r5
T=$R/trial
OUT=$R/evidence/e23
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
mkdir -p "$OUT"
LOG="$OUT/runner.log"
: > "$LOG"
note(){ echo "$1" | tee -a "$LOG"; }
fail(){ note "RUNNER_FAIL,$1"; exit 1; }
fail_n=0
note "== static checks =="
cd "$T" || exit 1
if grep -rniE 'rand\(|srand|getrandom|/dev/urandom|rdtsc' \
    "$R/r5_treatments.zag" >/dev/null 2>&1; then fail "RNG token found"; fi
if grep -q '^@import' "$R/r5_treatments.zag"; then :; else fail "import not bare"; fi
note "STATIC_OK"
note "== compile =="
"$ZNC" "$R/r5_treatments.zag" --no-zagd --no-analyze --no-foreground-cache \
  -o "$R/r5_treat_bin" || fail "compile"
note "COMPILE_OK"
note "== E2 (cites=1) =="
for cfg in frozen p3; do
  for run in 1 2; do
    "$R/r5_treat_bin" "$cfg" 1 > "$OUT/e2_${cfg}_r${run}.log" 2>&1
    ec=$?
    if [ $ec -ne 0 ]; then note "FAIL e2_${cfg}_r${run} exit=$ec"; fail_n=$((fail_n+1)); fi
    if ! grep -q "^R5_DONE$" "$OUT/e2_${cfg}_r${run}.log"; then
      note "FAIL e2_${cfg}_r${run} nodone"; fail_n=$((fail_n+1)); fi
  done
  if cmp -s "$OUT/e2_${cfg}_r1.log" "$OUT/e2_${cfg}_r2.log"; then :;
  else note "FAIL e2_${cfg} nondeterministic"; fail_n=$((fail_n+1)); fi
done
note "== E3 (cites=0) =="
for cfg in frozen p3 forced; do
  for run in 1 2; do
    "$R/r5_treat_bin" "$cfg" 0 > "$OUT/e3_${cfg}_r${run}.log" 2>&1
    ec=$?
    if [ $ec -ne 0 ]; then note "FAIL e3_${cfg}_r${run} exit=$ec"; fail_n=$((fail_n+1)); fi
    if ! grep -q "^R5_DONE$" "$OUT/e3_${cfg}_r${run}.log"; then
      note "FAIL e3_${cfg}_r${run} nodone"; fail_n=$((fail_n+1)); fi
  done
  if cmp -s "$OUT/e3_${cfg}_r1.log" "$OUT/e3_${cfg}_r2.log"; then :;
  else note "FAIL e3_${cfg} nondeterministic"; fail_n=$((fail_n+1)); fi
done
note "fail_n=$fail_n"
if [ "$fail_n" = 0 ]; then echo "E23_COMPLETE" > "$OUT/VERDICT.txt"; else echo "E23_FAILED" > "$OUT/VERDICT.txt"; fi
