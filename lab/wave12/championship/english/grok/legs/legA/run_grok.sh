#!/bin/bash
# GROK leg-A run driver: N=5 byte-identical runs per command.
# Builds grokt from legs/legA/src, then runs:
#   12 S1 reps: bind M2 4 <rep> 1 + btrap M2 4 <rep>
#   1 S10 run:  bind M2 4 0 10
# Logs to legs/legA/evidence/logs/. Any divergence or nonzero exit -> FAIL.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
LEGA="$HERE"
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
fail=0
RUNS=5

BIN="$LEGA/build/grokt"
mkdir -p "$LEGA/build" "$LEGA/evidence/logs"
(cd "$LEGA/src" && "$ZNC" -o "$BIN" grok_trial.zag) || { echo "BUILD FAIL"; exit 1; }
echo "built $BIN"

run_n5() { # base ; cmd...
  local base="$1"; shift
  for n in 1 2 3 4 5; do
    "$@" > "$LEGA/evidence/logs/${base}.run${n}.log" 2>&1
    local e=$?
    if [ $e -ne 0 ]; then echo "FAIL: $base run$n exit=$e"; fail=1; return; fi
    if [ "$n" -gt 1 ] && ! cmp -s "$LEGA/evidence/logs/${base}.run1.log" "$LEGA/evidence/logs/${base}.run${n}.log"; then
      echo "FAIL: $base run$n differs from run1"; fail=1; return
    fi
  done
  cp "$LEGA/evidence/logs/${base}.run1.log" "$LEGA/evidence/logs/${base}.log"
  for n in 2 3 4 5; do rm "$LEGA/evidence/logs/${base}.run${n}.log"; done
  echo "ok: $base (exit 0, 5x byte-identical)"
}

for rep in $(seq 0 11); do
  run_n5 "m2_bind_r${rep}"  "$BIN" bind  M2 4 "$rep" 1
  run_n5 "m2_trap_r${rep}"  "$BIN" btrap M2 4 "$rep"
done
run_n5 "m2_bind_s10" "$BIN" bind M2 4 0 10

(cd "$LEGA/evidence/logs" && sha256sum *.log 2>/dev/null | sort > SHA256SUMS.txt; echo "hashed $(ls *.log 2>/dev/null | wc -l) logs")
if [ $fail -ne 0 ]; then echo "RUN FAILURES PRESENT"; exit 1; fi
echo "ALL LEG-A RUNS OK"
