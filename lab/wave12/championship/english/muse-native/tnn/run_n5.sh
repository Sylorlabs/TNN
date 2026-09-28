#!/bin/bash
# N=5 byte-identical runs of a no-arg leg binary. Usage: run_n5.sh <legdir> <bin> <logbase>
set -u
LEG="$1"; BIN="$2"; BASE="$3"
HERE="$(cd "$(dirname "$0")" && pwd)"
SCR="$LEG/build/scratch5"; rm -rf "$SCR"; mkdir -p "$SCR" "$LEG/evidence/logs"
fail=0
for n in 1 2 3 4 5; do
  "$BIN" > "$SCR/${BASE}.run${n}.log" 2>&1 || { echo "FAIL $BASE run$n exit=$?"; fail=1; }
done
for n in 2 3 4 5; do
  cmp -s "$SCR/${BASE}.run1.log" "$SCR/${BASE}.run${n}.log" || { echo "DIVERGE $BASE run$n"; fail=1; }
done
if [ $fail -eq 0 ]; then
  cp "$SCR/${BASE}.run1.log" "$LEG/evidence/logs/${BASE}.log"
  echo "$BASE OK: 5x byte-identical"
else
  echo "$BASE FAILED"; exit 1
fi
