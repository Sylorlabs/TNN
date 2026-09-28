#!/bin/bash
# WC eval: frozen 37-leg matrix (PREREG_SR §2), A/B byte-identical per leg.
# Adapted from frozen training/run_eval.sh (same legs, same items).
set -u
T=~/workspace/tnn-lab/deliberation_depth/monotonicity/training/sr_round/wc
IT=~/workspace/tnn-lab/deliberation_depth/items_v2
CEIL=~/workspace/tnn-lab/deliberation_depth/ceiling/items/ceiling_battery.jsonl
RT=~/workspace/tnn-lab/deliberation_depth/monotonicity/redteam/redteam_battery.jsonl
OUT=$T/results
mkdir -p "$OUT"
BIN_A=$T/polbuild/wc_a/policy_wc_bin
BIN_B=$T/polbuild/wc_b/policy_wc_bin
pass=0; fail=0; failed=""
run_leg() {
  local blab=$1 items=$2 depth=$3
  local base="${blab}_wc_d${depth}"
  "$BIN_A" "$items" "$depth" 0 "$OUT/${base}_A.tsv"; local rca=$?
  "$BIN_B" "$items" "$depth" 0 "$OUT/${base}_B.tsv"; local rcb=$?
  if [ $rca -ne $rcb ] || [ $rca -ne 0 ]; then
    echo "RC $base a=$rca b=$rcb"; fail=$((fail+1)); failed="$failed $base(rc)"; return
  fi
  if cmp -s "$OUT/${base}_A.tsv" "$OUT/${base}_B.tsv"; then pass=$((pass+1));
  else echo "BYTE-MISMATCH $base"; fail=$((fail+1)); failed="$failed $base(bytes)"; fi
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
echo "EVAL wc: PASS=$pass FAIL=$fail"
if [ -n "$failed" ]; then echo "FAILED:$failed"; exit 1; fi
# copy frozen M4 TSVs in for the release-identity check (analyzer ref mech 4)
M4R=~/workspace/tnn-lab/deliberation_depth/monotonicity/mechanisms/results
for f in "$M4R"/*_m4_d*_[AB].tsv; do cp "$f" "$OUT/"; done
echo "M4 reference TSVs copied: $(ls "$OUT"/*_m4_d*_A.tsv | wc -l) legs"
echo "ALL WC LEGS DETERMINISTIC"
