#!/bin/bash
# BESTOF legA: N=5 byte-identical runs for the full M2 matrix.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
BIN="$HERE/build/bestof_trial_bin"
LOGD="$HERE/evidence/logs"
mkdir -p "$LOGD"
fail=0
run_n5() { # base ; cmd...
  local base="$1"; shift
  for n in 1 2 3 4 5; do
    "$@" > "$LOGD/${base}.run${n}.log" 2>&1
    local e=$?
    if [ $e -ne 0 ]; then echo "FAIL: $base run$n exit=$e"; fail=1; return; fi
    if [ "$n" -gt 1 ] && ! cmp -s "$LOGD/${base}.run1.log" "$LOGD/${base}.run${n}.log"; then
      echo "FAIL: $base run$n differs from run1"; fail=1; return
    fi
  done
  cp "$LOGD/${base}.run1.log" "$LOGD/${base}.log"
  for n in 2 3 4 5; do rm "$LOGD/${base}.run${n}.log"; done
  echo "ok: $base (5x byte-identical)"
}
for rep in 0 1 2 3 4 5 6 7 8 9 10 11; do
  run_n5 "bind_M2_rep${rep}_s1" "$BIN" bind M2 4 "$rep" 1
done
run_n5 "bind_M2_rep0_s10" "$BIN" bind M2 4 0 10
for rep in 0 1 2 3 4 5 6 7 8 9 10 11; do
  run_n5 "btrap_M2_rep${rep}" "$BIN" btrap M2 4 "$rep"
done
(cd "$LOGD" && sha256sum *.log 2>/dev/null | sort > SHA256SUMS.txt)
if [ $fail -ne 0 ]; then echo "RUN FAILURES PRESENT"; exit 1; fi
echo "LEGA ALL RUNS OK"
