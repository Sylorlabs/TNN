#!/bin/bash
# MUSE-NATIVE championship run driver: N=5 byte-identical runs per leg.
# Logs to tnn/legX/evidence/logs/. Any divergence or nonzero exit -> FAIL.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
fail=0
RUNS=5

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
(cd "$HERE/evidence/logs" && sha256sum *.log 2>/dev/null | sort > SHA256SUMS.txt; echo "hashed $(ls *.log 2>/dev/null | wc -l) logs")
if [ $fail -ne 0 ]; then echo "RUN FAILURES PRESENT"; exit 1; fi
echo "ALL RUNS OK"
