#!/bin/bash
# v2 eval: 37 legs x2 (A/B) for a trained policy tag.
# Usage: run_eval.sh <tag> <mechid>
set -u
T=~/workspace/tnn-lab/deliberation_depth/monotonicity/training/v2
W=$T/work
ITEMDIR=~/workspace/tnn-lab/deliberation_depth/items_v2
RT=~/workspace/tnn-lab/deliberation_depth/monotonicity/redteam/redteam_battery.jsonl
CEIL=~/workspace/tnn-lab/deliberation_depth/ceiling/items/ceiling_battery.jsonl
OUT=$W/results
mkdir -p "$OUT"
TAG=$1; MECH=$2
BIN_A=$W/policy_bin_${TAG}_a
BIN_B=$W/policy_bin_${TAG}_b
pass=0; fail=0; failed=""
run_leg() { # battery_label items depth
  local blab=$1 items=$2 depth=$3
  local base="${blab}_m${MECH}_d${depth}"
  "$BIN_A" "$items" "$depth" 0 "$OUT/${base}_A.tsv"
  local rca=$?
  "$BIN_B" "$items" "$depth" 0 "$OUT/${base}_B.tsv"
  local rcb=$?
  if [ $rca -ne $rcb ] || [ $rca -ne 0 ]; then
    echo "RC $base a=$rca b=$rcb"; fail=$((fail+1)); failed="$failed $base(rc)"; return
  fi
  if cmp -s "$OUT/${base}_A.tsv" "$OUT/${base}_B.tsv"; then
    pass=$((pass+1))
  else
    echo "BYTE-MISMATCH $base"; fail=$((fail+1)); failed="$failed $base(bytes)"
  fi
}
for depth in 1 2 4 8 16; do
  run_leg admit   "$ITEMDIR/admit.jsonl"  $depth
  run_leg revoke  "$ITEMDIR/revoke.jsonl" $depth
  run_leg logic   "$ITEMDIR/logic.jsonl"  $depth
  run_leg trap    "$ITEMDIR/trap.jsonl"   $depth
  run_leg cost    "$ITEMDIR/cost.jsonl"   $depth
  run_leg redteam "$RT"                   $depth
done
for depth in 1 2 4 8 16 32 64; do
  run_leg ceiling "$CEIL" $depth
done
echo "EVAL $TAG: PASS=$pass FAIL=$fail"
if [ -n "$failed" ]; then echo "FAILED:$failed"; exit 1; fi
echo "ALL LEGS DETERMINISTIC"
