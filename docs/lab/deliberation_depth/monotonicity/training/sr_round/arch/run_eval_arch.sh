#!/bin/bash
# 37-leg eval matrix for SR ROUND arm ARCH (frozen PREREG_SR.md §7).
# Mech tag 9 in filenames (frozen analyze.py takes integer mech ids).
set -u
SR=~/workspace/tnn-lab/deliberation_depth/monotonicity/training/sr_round/arch
IT=~/workspace/tnn-lab/deliberation_depth/items_v2
CEIL=~/workspace/tnn-lab/deliberation_depth/ceiling/items/ceiling_battery.jsonl
RT=~/workspace/tnn-lab/deliberation_depth/monotonicity/redteam/redteam_battery.jsonl
M4R=~/workspace/tnn-lab/deliberation_depth/monotonicity/mechanisms/results
POLA=$SR/build/policy_arch_A
POLB=$SR/build/policy_arch_B
OUT=$SR/results
mkdir -p "$OUT"
pass=0; fail=0; failed=""
run_leg() { # battery_label items depth
  local blab=$1 items=$2 depth=$3
  local base="${blab}_m9_d${depth}"
  "$POLA" "$items" "$depth" 0 "$OUT/${base}_A.tsv"; local rca=$?
  "$POLB" "$items" "$depth" 0 "$OUT/${base}_B.tsv"; local rcb=$?
  if [ $rca -ne $rcb ]; then echo "RC-MISMATCH $base a=$rca b=$rcb"; fail=$((fail+1)); failed="$failed $base(rc)"; return; fi
  if cmp -s "$OUT/${base}_A.tsv" "$OUT/${base}_B.tsv" && cmp -s "$OUT/${base}_A.tsv.ms" "$OUT/${base}_B.tsv.ms"; then
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
echo "PASS=$pass FAIL=$fail"
if [ -n "$failed" ]; then echo "FAILED:$failed"; exit 1; fi
# M4 reference TSVs for the release-identity check (analyzer ref mech 4)
for f in "$M4R"/*_m4_d*_[AB].tsv; do cp "$f" "$OUT/"; done
echo "M4 reference TSVs copied: $(ls "$OUT"/*_m4_d*_A.tsv | wc -l) legs"
echo "ALL 37 ARCH LEGS DETERMINISTIC"
