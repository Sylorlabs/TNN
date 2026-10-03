#!/bin/bash
# H-0 feature extraction: 12 family-runs x2 (A/B), byte-compare, concat.
set -u
T=~/workspace/tnn-lab/deliberation_depth/monotonicity/training
SRC=$T/src
W=$T/work
mkdir -p "$W"
ITEMDIR=~/workspace/tnn-lab/deliberation_depth/items_v2
RT=~/workspace/tnn-lab/deliberation_depth/monotonicity/redteam/redteam_battery.jsonl
CE=$T/items
D5="1 2 4 8 16"
D7="1 2 4 8 16 32 64"
pass=0; fail=0; failed=""
run_feat() { # label items family heldout depths...
  local label=$1 items=$2 family=$3 heldout=$4
  shift 4
  local depths="$*"
  "$SRC/feat_bin_a" "$items" "$family" "$heldout" "$W/${label}_A.tsv" $depths
  local rca=$?
  "$SRC/feat_bin_b" "$items" "$family" "$heldout" "$W/${label}_B.tsv" $depths
  local rcb=$?
  if [ $rca -ne $rcb ]; then
    echo "RC-MISMATCH $label a=$rca b=$rcb"; fail=$((fail+1)); failed="$failed $label(rc)"; return
  fi
  if [ $rca -ne 0 ]; then
    echo "NONZERO-RC $label rc=$rca"; fail=$((fail+1)); failed="$failed $label(rc$rc)"; return
  fi
  if cmp -s "$W/${label}_A.tsv" "$W/${label}_B.tsv"; then
    pass=$((pass+1)); echo "OK $label $(wc -l < "$W/${label}_A.tsv") cells"
  else
    echo "BYTE-MISMATCH $label"; fail=$((fail+1)); failed="$failed $label(bytes)"
  fi
}
run_feat admit  "$ITEMDIR/admit.jsonl"  admit 0 $D5
run_feat revoke "$ITEMDIR/revoke.jsonl" revoke 0 $D5
run_feat logic  "$ITEMDIR/logic.jsonl"  logic 0 $D5
run_feat cost   "$ITEMDIR/cost.jsonl"   cost 0 $D5
run_feat trap   "$ITEMDIR/trap.jsonl"   trap 0 $D5
run_feat redteam "$RT"                  redteam 0 $D5
run_feat Peven  "$CE/ceiling_P_even.jsonl" P 0 $D7
run_feat Deven  "$CE/ceiling_D_even.jsonl" D 0 $D7
run_feat Oeven  "$CE/ceiling_O_even.jsonl" O 0 $D7
run_feat Podd   "$CE/ceiling_P_odd.jsonl"  P 1 $D7
run_feat Dodd   "$CE/ceiling_D_odd.jsonl"  D 1 $D7
run_feat Odd    "$CE/ceiling_O_odd.jsonl"  O 1 $D7
echo "FEAT PASS=$pass FAIL=$fail"
if [ -n "$failed" ]; then echo "FAILED:$failed"; exit 1; fi
for l in admit revoke logic cost trap redteam Peven Deven Oeven Podd Dodd Odd; do
  cat "$W/${l}_A.tsv"
done > "$W/features.tsv"
echo "features.tsv: $(wc -l < "$W/features.tsv") lines"
cmp -s "$W/features.tsv" /dev/null; echo done
