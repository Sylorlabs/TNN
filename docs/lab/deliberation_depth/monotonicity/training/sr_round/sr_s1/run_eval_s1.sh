#!/bin/bash
# Eval matrix runner for the FROZEN SR-S1 released policy (post-Stage-2, SIGNAL_DISCONNECT).
# 37 legs exactly as training/run_eval.sh: admit, revoke, logic, trap, cost,
# redteam x depths {1,2,4,8,16} (30) + ceiling x depths {1,2,4,8,16,32,64} (7).
# Mech tag 16 (frozen analyze.py takes integer mech ids; 15=SR-S9, 14/9 taken).
# Policy: src/policy_s1.zag + src/s1_release.zag — 8-input head from the FROZEN
# post-Stage-2 weights, M4 release skeleton. Zero training code, no mask code path.
# Usage: run_eval_s1.sh
set -u
S1=~/workspace/tnn-lab/deliberation_depth/monotonicity/training/sr_round/sr_s1
MECH=16
TR=~/workspace/tnn-lab/deliberation_depth/monotonicity/training
IT=~/workspace/tnn-lab/deliberation_depth/items_v2
CEIL=~/workspace/tnn-lab/deliberation_depth/ceiling/items/ceiling_battery.jsonl
RT=~/workspace/tnn-lab/deliberation_depth/monotonicity/redteam/redteam_battery.jsonl
OUT=$S1/results
mkdir -p "$OUT"
pass=0; fail=0; failed=""
run_leg() { # battery_label items depth
  local blab=$1 items=$2 depth=$3
  local base="${blab}_m${MECH}_d${depth}"
  "$S1/build/pol_a/policy_s1_a" "$items" "$depth" 0 "$OUT/${base}_A.tsv"
  local rca=$?
  "$S1/build/pol_b/policy_s1_b" "$items" "$depth" 0 "$OUT/${base}_B.tsv"
  local rcb=$?
  if [ $rca -ne $rcb ]; then echo "RC-MISMATCH $base a=$rca b=$rcb" >&2; fail=$((fail+1)); failed="$failed $base(rc)"; return; fi
  if cmp -s "$OUT/${base}_A.tsv" "$OUT/${base}_B.tsv"; then
    pass=$((pass+1))
  else
    echo "BYTE-MISMATCH $base" >&2; fail=$((fail+1)); failed="$failed $base(bytes)"
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
echo "TAG=sr-s1-100x MECH=16 PASS=$pass FAIL=$fail"
if [ -n "$failed" ]; then echo "FAILED:$failed"; exit 1; fi
# copy frozen M4 TSVs in for the release-identity check (analyzer ref mech 4)
M4R=~/workspace/tnn-lab/deliberation_depth/monotonicity/mechanisms/results
for f in "$M4R"/*_m4_d*_[AB].tsv; do cp "$f" "$OUT/"; done
echo "M4 reference TSVs copied: $(ls "$OUT"/*_m4_d*_A.tsv | wc -l) legs"
echo "ALL SR-S1 LEGS DETERMINISTIC"
