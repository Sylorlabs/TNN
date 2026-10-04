#!/bin/bash
# Full measurement matrix runner. Each leg run twice (A/B) with byte-compare.
set -u
MECHDIR=~/workspace/tnn-lab/deliberation_depth/monotonicity/mechanisms
BINDIR=$MECHDIR
ITEMDIR=~/workspace/tnn-lab/deliberation_depth/items_v2
CEIL=~/workspace/tnn-lab/deliberation_depth/ceiling/items/ceiling_battery.jsonl
RT=$MECHDIR/../redteam/redteam_battery.jsonl
OUT=$MECHDIR/results
mkdir -p "$OUT"
BIN_A=$BINDIR/mech_bin_a
BIN_B=$BINDIR/mech_bin_b
pass=0; fail=0; failed_legs=""
run_leg() { # battery_label items depth mech
  local blab=$1 items=$2 depth=$3 mech=$4
  local base="${blab}_m${mech}_d${depth}"
  "$BIN_A" "$items" "$mech" "$depth" "$OUT/${base}_A.tsv"
  local rca=$?
  "$BIN_B" "$items" "$mech" "$depth" "$OUT/${base}_B.tsv"
  local rcb=$?
  if [ $rca -ne $rcb ]; then
    echo "RC-MISMATCH $base a=$rca b=$rcb"; fail=$((fail+1)); failed_legs="$failed_legs $base(rc)"; return
  fi
  if cmp -s "$OUT/${base}_A.tsv" "$OUT/${base}_B.tsv"; then
    pass=$((pass+1))
  else
    echo "BYTE-MISMATCH $base"; fail=$((fail+1)); failed_legs="$failed_legs $base(bytes)"
  fi
}
for mech in 0 1 2 3 4 5 6 7 8; do
  for depth in 1 2 4 8 16; do
    run_leg admit    "$ITEMDIR/admit.jsonl"  $depth $mech
    run_leg revoke   "$ITEMDIR/revoke.jsonl" $depth $mech
    run_leg logic    "$ITEMDIR/logic.jsonl"  $depth $mech
    run_leg trap     "$ITEMDIR/trap.jsonl"   $depth $mech
    run_leg cost     "$ITEMDIR/cost.jsonl"   $depth $mech
    run_leg redteam  "$RT"                   $depth $mech
  done
  for depth in 1 2 4 8 16 32 64; do
    run_leg ceiling "$CEIL" $depth $mech
  done
done
echo "PASS=$pass FAIL=$fail"
if [ -n "$failed_legs" ]; then echo "FAILED:$failed_legs"; exit 1; fi
echo "ALL LEGS DETERMINISTIC"
