#!/bin/bash
# legA M2 battery: bind (12 reps s1 + rep0 s10) + btrap (12 reps), 5x runs,
# byte-identical across runs. Canonical logs -> evidence/logs/.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
BIN="$HERE/build/muset"
SCR="$HERE/build/scratch"
rm -rf "$SCR"; mkdir -p "$SCR" evidence/logs
fail=0
for n in 1 2 3 4 5; do
  d="$SCR/run$n"; mkdir -p "$d"
  for r in $(seq 0 11); do
    "$BIN" bind M2 4 "$r" 1  > "$d/bind_M2_rep${r}_s1.log" 2>&1 || { echo "FAIL bind rep$r run$n"; fail=1; }
    "$BIN" btrap M2 4 "$r"   > "$d/btrap_M2_rep${r}.log" 2>&1 || { echo "FAIL btrap rep$r run$n"; fail=1; }
  done
  "$BIN" bind M2 4 0 10 > "$d/bind_M2_rep0_s10.log" 2>&1 || { echo "FAIL bind s10 run$n"; fail=1; }
done
# byte-compare runs 2..5 against run 1
for n in 2 3 4 5; do
  for f in "$SCR/run1"/*.log; do
    b="$(basename "$f")"
    cmp -s "$f" "$SCR/run$n/$b" || { echo "DIVERGE: run$n $b"; fail=1; }
  done
done
if [ $fail -eq 0 ]; then
  cp "$SCR"/run1/*.log evidence/logs/
  (cd evidence/logs && sha256sum *.log | sort > SHA256SUMS.txt)
  echo "legA battery OK: 25 logs x 5 runs byte-identical"
else
  echo "legA battery FAILED"; exit 1
fi
