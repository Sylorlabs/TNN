#!/bin/bash
# K1 1x battery runner: runs every mode twice (a/b) for byte-identical determinism.
# Usage: ./run_battery.sh <round_dir>
# Each mode's stdout is captured; the two runs are diffed.
set -u
BIN=/home/hatch/workspace/tnn-lab/units/arms/K1/cl/k1test
CORP=/home/hatch/workspace/tnn-lab/units/arms/harness/corpora/r1
OUT=${1:?round dir required}
mkdir -p "$OUT"

# mode -> extra args (after mode)
declare -A ARGS
ARGS[m1-1x-prose]="$CORP"
ARGS[m1-1x-code]="$CORP"
ARGS[m2-t1-prose]="$CORP"
ARGS[m2-t1-code]="$CORP"
ARGS[m2-t2-prose]="$CORP"
ARGS[m2-t2-code]="$CORP"
ARGS[m2-t3-1x]="$CORP"
ARGS[m3-1x]="$CORP"
ARGS[m4-1x-prose]="$CORP"
ARGS[m4-1x-code]="$CORP"
ARGS[m5-baseline]=""
ARGS[m5-1x]="$CORP $OUT/m5_work"
ARGS[m6-p2c-1x]="$CORP"
ARGS[m6-c2p-1x]="$CORP"
ARGS[m7-1x]="$CORP"
ARGS[m8-1x]="$CORP $OUT/m8_work none"
ARGS[k1-dedup-1x]="$CORP"
ARGS[k1-chain-1x]="$CORP"
ARGS[k1-role-1x]="$CORP"
ARGS[k1-selftest]=""

MODES="m1-1x-prose m1-1x-code m2-t1-prose m2-t1-code m2-t2-prose m2-t2-code m2-t3-1x m3-1x m4-1x-prose m4-1x-code m5-baseline m5-1x m6-p2c-1x m6-c2p-1x m7-1x m8-1x k1-dedup-1x k1-chain-1x k1-role-1x k1-selftest"

PASS=0; FAIL=0; FAILED_MODES=""
for m in $MODES; do
  echo "=== $m ==="
  "$BIN" "$m" ${ARGS[$m]} > "$OUT/${m}_a.txt" 2>&1; rca=$?
  echo "rc=$rca" >> "$OUT/${m}_a.txt"
  "$BIN" "$m" ${ARGS[$m]} > "$OUT/${m}_b.txt" 2>&1; rcb=$?
  echo "rc=$rcb" >> "$OUT/${m}_b.txt"
  if [ $rca -ne 0 ] || [ $rcb -ne 0 ]; then
    echo "  FAIL: nonzero rc (a=$rca b=$rcb)"
    FAIL=$((FAIL+1)); FAILED_MODES="$FAILED_MODES $m(rc)"
  elif cmp -s "$OUT/${m}_a.txt" "$OUT/${m}_b.txt"; then
    echo "  PASS: byte-identical"
    PASS=$((PASS+1))
  else
    echo "  FAIL: outputs differ"
    FAIL=$((FAIL+1)); FAILED_MODES="$FAILED_MODES $m(diff)"
  fi
done
echo "=== battery done: pass=$PASS fail=$FAIL ==="
[ -n "$FAILED_MODES" ] && echo "failed:$FAILED_MODES"
