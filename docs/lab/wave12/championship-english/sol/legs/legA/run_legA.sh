#!/bin/bash
# SOL leg-A run driver: M2 arm (armidx 4), reps 0-11 at scale 1 + rep 0 at
# scale 10. Each config: N=5 byte-identical runs; any divergence or nonzero
# exit -> FAIL. Logs to evidence/logs/.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
BIN="$HERE/build/sol_trial_bin"
fail=0

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

mkdir -p "$HERE/evidence/logs"
for rep in 0 1 2 3 4 5 6 7 8 9 10 11; do
  run_n5 "bind_M2_rep${rep}_s1" "$BIN" bind M2 4 "$rep" 1
done
run_n5 "bind_M2_rep0_s10" "$BIN" bind M2 4 0 10
for rep in 0 1 2 3 4 5 6 7 8 9 10 11; do
  run_n5 "btrap_M2_rep${rep}_s1" "$BIN" btrap M2 4 "$rep" 1
done
(cd "$HERE/evidence/logs" && sha256sum *.log 2>/dev/null | sort > SHA256SUMS.txt; echo "hashed $(ls *.log 2>/dev/null | wc -l) logs")
if [ $fail -ne 0 ]; then echo "RUN FAILURES PRESENT"; exit 1; fi
echo "ALL RUNS OK"
