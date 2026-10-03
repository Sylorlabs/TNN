#!/bin/bash
# T-05 eval: 22 legs x2 (A/B) per arm per scale.
set -u
T=~/workspace/tnn-lab/deliberation_depth/monotonicity/training/backlog/t05
ITEMDIR=~/workspace/tnn-lab/deliberation_depth/items_v2
CEIL=~/workspace/tnn-lab/deliberation_depth/ceiling/items/ceiling_battery.jsonl
OUT=$T/results
mkdir -p "$OUT"
ARM=$1; SCALE=$2
SUFFIX=$SCALE; if [ "$SCALE" = "100x" ]; then SUFFIX=""; else SUFFIX="_${SCALE}"; fi
BIN_A=$T/polbuild/${ARM}${SUFFIX}_a/policy5_bin
BIN_B=$T/polbuild/${ARM}${SUFFIX}_b/policy5_bin
pass=0; fail=0; failed=""
run_leg() {
  local blab=$1 items=$2 depth=$3
  local base="${blab}_t05${ARM}_${SCALE}_d${depth}"
  "$BIN_A" "$items" "$depth" 0 "$OUT/${base}_A.tsv"; local rca=$?
  "$BIN_B" "$items" "$depth" 0 "$OUT/${base}_B.tsv"; local rcb=$?
  if [ $rca -ne $rcb ] || [ $rca -ne 0 ]; then
    echo "RC $base a=$rca b=$rcb"; fail=$((fail+1)); failed="$failed $base(rc)"; return
  fi
  if cmp -s "$OUT/${base}_A.tsv" "$OUT/${base}_B.tsv"; then pass=$((pass+1));
  else echo "BYTE-MISMATCH $base"; fail=$((fail+1)); failed="$failed $base(bytes)"; fi
}
for depth in 1 2 4 8 16; do
  run_leg admit "$ITEMDIR/admit.jsonl" $depth
  run_leg logic "$ITEMDIR/logic.jsonl" $depth
  run_leg trap  "$ITEMDIR/trap.jsonl"  $depth
done
for depth in 1 2 4 8 16 32 64; do
  run_leg ceiling "$CEIL" $depth
done
echo "EVAL t05${ARM} ${SCALE}: PASS=$pass FAIL=$fail"
if [ -n "$failed" ]; then echo "FAILED:$failed"; exit 1; fi
echo "ALL LEGS DETERMINISTIC"
