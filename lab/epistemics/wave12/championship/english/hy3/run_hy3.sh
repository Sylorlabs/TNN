#!/bin/bash
# HY3-ENGLISH championship run driver: compile + N=5 byte-identical runs per leg.
# Logs to tnn/legX/evidence/logs/. Any divergence or nonzero exit -> FAIL.
# Usage: run_hy3.sh <legA|legB|legC>
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
LEG="${1:?usage: run_hy3.sh <legA|legB|legC>}"
case "$LEG" in
  legA) MAIN=hy3_trial.zag; BIN=hy3_trial_bin ;;
  legB) MAIN=hy3_b7_direct.zag; BIN=hy3_b7_direct_bin ;;
  legC) MAIN=hy3_teacher_leg.zag; BIN=hy3_teacher_leg_bin ;;
  *) echo "unknown leg $LEG"; exit 2 ;;
esac
fail=0
RUNS=5
SRCDIR="$HERE/tnn/$LEG/src"
LOGDIR="$HERE/tnn/$LEG/evidence/logs"
mkdir -p "$LOGDIR"

echo "== compiling $LEG ($MAIN)"
(cd "$SRCDIR" && "$ZNC" "$MAIN" -o "$BIN") || { echo "FAIL: compile $LEG"; exit 1; }
echo "ok: compiled $LEG"

run_n5() { # base ; cmd...
  local base="$1"; shift
  for n in 1 2 3 4 5; do
    "$@" > "$LOGDIR/${base}.run${n}.log" 2>&1
    local e=$?
    if [ $e -ne 0 ]; then echo "FAIL: $base run$n exit=$e"; fail=1; return; fi
    if [ "$n" -gt 1 ] && ! cmp -s "$LOGDIR/${base}.run1.log" "$LOGDIR/${base}.run${n}.log"; then
      echo "FAIL: $base run$n differs from run1"; fail=1; return
    fi
  done
  cp "$LOGDIR/${base}.run1.log" "$LOGDIR/${base}.log"
  for n in 2 3 4 5; do rm "$LOGDIR/${base}.run${n}.log"; done
  echo "ok: $base (exit 0, 5x byte-identical)"
}

BINPATH="$SRCDIR/$BIN"
case "$LEG" in
  legA)
    for rep in 0 1 2 3 4 5 6 7 8 9 10 11; do
      run_n5 "bind_M2_rep${rep}_s1" "$BINPATH" bind M2 4 "$rep" 1
    done
    run_n5 "bind_M2_rep0_s10" "$BINPATH" bind M2 4 0 10
    ;;
  legB) run_n5 "hy3b" "$BINPATH" ;;
  legC) run_n5 "hy3c" "$BINPATH" ;;
esac

(cd "$LOGDIR" && sha256sum *.log 2>/dev/null | sort > SHA256SUMS.txt; echo "hashed $(ls *.log 2>/dev/null | wc -l) logs")
if [ $fail -ne 0 ]; then echo "RUN FAILURES PRESENT"; exit 1; fi
echo "ALL RUNS OK ($LEG)"
