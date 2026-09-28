#!/bin/bash
# STEP-3.7-FLASH championship leg-A run driver.
# Compiles src/step_trial.zag, then N=5 byte-identical runs of:
#   bind M2 4 <rep> 1   for rep 0..11  (M2 arm, D2 teaching route, all 12 reps)
#   btrap M2 4 <rep>    for rep 0..11  (binding + trap families)
#   bind M2 4 0 10                    (S10 no-degradation, rep 0)
# Logs to tnn/legA/evidence/logs/. Any divergence or nonzero exit -> FAIL.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
ZNC="$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1"
BLD="$HERE/build"
BIN="$BLD/step_trial_bin"
fail=0

mkdir -p "$BLD" "$HERE/evidence/logs"
echo "== compile step_trial.zag =="
(cd "$HERE/src" && "$ZNC" step_trial.zag -o "$BIN") || { echo "COMPILE FAIL"; exit 1; }

run_n5() { # base ; cmd...
  local base="$1"; shift
  for n in 1 2 3 4 5; do
    "$@" > "$HERE/evidence/logs/${base}.run${n}.log" 2>&1
    local e=$?
    if [ $e -ne 0 ]; then echo "FAIL: $base run$n exit=$e"; fail=1; return; fi
    if [ "$n" -gt 1 ] && ! cmp -s "$HERE/evidence/logs/${base}.run1.log" "$HERE/evidence/logs/${base}.run${n}.log"; then
      echo "FAIL: $base run$n differs from run1"; fail=1; return
    fi
  done
  cp "$HERE/evidence/logs/${base}.run1.log" "$HERE/evidence/logs/${base}.log"
  for n in 2 3 4 5; do rm "$HERE/evidence/logs/${base}.run${n}.log"; done
  echo "ok: $base (exit 0, 5x byte-identical)"
}

for rep in 0 1 2 3 4 5 6 7 8 9 10 11; do
  run_n5 "m2.bind.rep${rep}" "$BIN" bind M2 4 "$rep" 1
done
for rep in 0 1 2 3 4 5 6 7 8 9 10 11; do
  run_n5 "m2.btrap.rep${rep}" "$BIN" btrap M2 4 "$rep"
done
run_n5 "m2.bind.s10" "$BIN" bind M2 4 0 10

(cd "$HERE/evidence/logs" && sha256sum m2.*.log 2>/dev/null | sort > SHA256SUMS.txt; echo "hashed $(ls m2.*.log 2>/dev/null | wc -l) logs")
if [ $fail -ne 0 ]; then echo "RUN FAILURES PRESENT"; exit 1; fi
echo "ALL LEG-A RUNS OK"
