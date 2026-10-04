#!/bin/bash
# Eval matrix runner for a frozen trained policy (§8 gate 4).
# Usage: run_eval.sh <tag> <policy_bin> <mech_id> <gate01>
#   tag: 10x | 100x | full
set -u
TAG=$1; POLBIN=$2; MECH=$3; GATE=$4
TR=~/workspace/tnn-lab/deliberation_depth/monotonicity/training
IT=~/workspace/tnn-lab/deliberation_depth/items_v2
CEIL=~/workspace/tnn-lab/deliberation_depth/ceiling/items/ceiling_battery.jsonl
RT=~/workspace/tnn-lab/deliberation_depth/monotonicity/redteam/redteam_battery.jsonl
OUT=$TR/results_$TAG
mkdir -p "$OUT"
pass=0; fail=0; failed=""
run_leg() { # battery_label items depth
  local blab=$1 items=$2 depth=$3
  local base="${blab}_m${MECH}_d${depth}"
  "$POLBIN" "$items" "$depth" "$GATE" "$OUT/${base}_A.tsv"
  local rca=$?
  "$POLBIN" "$items" "$depth" "$GATE" "$OUT/${base}_B.tsv"
  local rcb=$?
  if [ $rca -ne $rcb ]; then echo "RC-MISMATCH $base a=$rca b=$rcb"; fail=$((fail+1)); failed="$failed $base(rc)"; return; fi
  if cmp -s "$OUT/${base}_A.tsv" "$OUT/${base}_B.tsv"; then
    pass=$((pass+1))
  else
    echo "BYTE-MISMATCH $base"; fail=$((fail+1)); failed="$failed $base(bytes)"
  fi
}
for depth in 1 2 4 8 16; do
  run_leg admit   "$IT/admit.jsonl"  $depth
  run_leg revoke  "$IT/revoke.jsonl" $depth
  run_leg logic   "$IT/logic.jsonl"  $depth
  run_leg trap    "$IT/trap.jsonl"   $depth
  run_leg cost    "$IT/cost.jsonl"   $depth
  run_leg redteam "$RT"              $depth
done
for depth in 1 2 4 8 16 32 64; do
  run_leg ceiling "$CEIL" $depth
done
echo "TAG=$TAG PASS=$pass FAIL=$fail"
if [ -n "$failed" ]; then echo "FAILED:$failed"; exit 1; fi
# copy frozen M4 TSVs in for the release-identity check (analyzer ref mech 4)
M4R=~/workspace/tnn-lab/deliberation_depth/monotonicity/mechanisms/results
for f in "$M4R"/*_m4_d*_[AB].tsv; do cp "$f" "$OUT/"; done
echo "M4 reference TSVs copied: $(ls "$OUT"/*_m4_d*_A.tsv | wc -l) legs"
echo "ALL $TAG LEGS DETERMINISTIC"
