#!/bin/bash
# Feature extraction: 12 runs, each twice (A/B) with byte-compare (§8 gate 1),
# then concatenated in fixed order into features.tsv.
set -u
TR=~/workspace/tnn-lab/deliberation_depth/monotonicity/training
SRC=$TR/src
IT=~/workspace/tnn-lab/deliberation_depth/items_v2
CIT=$TR/items
OUT=$TR/features
mkdir -p "$OUT"
pass=0; fail=0; failed=""
run_feat() { # name items family heldout outbase depths...
  local name=$1 items=$2 family=$3 heldout=$4 outbase=$5; shift 5
  "$SRC/feat_bin_a" "$items" "$family" "$heldout" "$OUT/${outbase}_A.tsv" "$@"
  local rca=$?
  "$SRC/feat_bin_b" "$items" "$family" "$heldout" "$OUT/${outbase}_B.tsv" "$@"
  local rcb=$?
  if [ $rca -ne $rcb ]; then echo "RC-MISMATCH $name a=$rca b=$rcb"; fail=$((fail+1)); failed="$failed $name(rc)"; return; fi
  if cmp -s "$OUT/${outbase}_A.tsv" "$OUT/${outbase}_B.tsv"; then
    pass=$((pass+1)); echo "OK $name ($(wc -l < "$OUT/${outbase}_A.tsv") cells)"
  else
    echo "BYTE-MISMATCH $name"; fail=$((fail+1)); failed="$failed $name(bytes)"
  fi
}
run_feat admit    "$IT/admit.jsonl"  admit    0 admit          1 2 4 8 16
run_feat revoke   "$IT/revoke.jsonl" revoke   0 revoke         1 2 4 8 16
run_feat logic    "$IT/logic.jsonl"  logic    0 logic          1 2 4 8 16
run_feat cost     "$IT/cost.jsonl"   cost     0 cost           1 2 4 8 16
run_feat trap     "$IT/trap.jsonl"   trap     0 trap           1 2 4 8 16
run_feat redteam  ~/workspace/tnn-lab/deliberation_depth/monotonicity/redteam/redteam_battery.jsonl redteam 0 redteam 1 2 4 8 16
run_feat ceilPev  "$CIT/ceiling_P_even.jsonl" P 0 ceilPev       1 2 4 8 16 32 64
run_feat ceilDev  "$CIT/ceiling_D_even.jsonl" D 0 ceilDev      1 2 4 8 16 32 64
run_feat ceilOev  "$CIT/ceiling_O_even.jsonl" O 0 ceilOev       1 2 4 8 16 32 64
run_feat ceilPod  "$CIT/ceiling_P_odd.jsonl"  P 1 ceilPod      1 2 4 8 16 32 64
run_feat ceilDod  "$CIT/ceiling_D_odd.jsonl"  D 1 ceilDod      1 2 4 8 16 32 64
run_feat ceilOod  "$CIT/ceiling_O_odd.jsonl"  O 1 ceilOod      1 2 4 8 16 32 64
echo "PASS=$pass FAIL=$fail"
if [ -n "$failed" ]; then echo "FAILED:$failed"; exit 1; fi
cat "$OUT/admit_A.tsv" "$OUT/revoke_A.tsv" "$OUT/logic_A.tsv" "$OUT/cost_A.tsv" \
    "$OUT/trap_A.tsv" "$OUT/redteam_A.tsv" \
    "$OUT/ceilPev_A.tsv" "$OUT/ceilDev_A.tsv" "$OUT/ceilOev_A.tsv" \
    "$OUT/ceilPod_A.tsv" "$OUT/ceilDod_A.tsv" "$OUT/ceilOod_A.tsv" > "$OUT/features.tsv"
wc -l "$OUT/features.tsv"
sha256sum "$OUT/features.tsv"
echo "ALL FEATURE LEGS DETERMINISTIC"
