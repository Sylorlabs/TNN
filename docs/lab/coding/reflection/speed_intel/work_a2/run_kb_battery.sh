#!/bin/bash
# 2a battery: 24 frozen GEN specs, plan+gen, flat (original binary) vs idx.
set -u
W2=$(pwd)
ORIG=../../kb/bin/kb_main
KB=../../kb/hidden_files/kb.dat
SPECS=../../kb/tests/specs.txt
mkdir -p logs
: > logs/plan_flat.log; : > logs/plan_idx.log; : > logs/plan_idx_full.log
: > logs/gen_flat.log; : > logs/gen_idx.log
while IFS=$'\t' read -r kind id spec rest; do
  [ "$kind" = "GEN" ] || continue
  echo "### $id $spec" >> logs/plan_flat.log
  "$ORIG" plan "$KB" "$spec" >> logs/plan_flat.log
  echo "### $id $spec" >> logs/plan_idx_full.log
  ./kb_main_si plan kb_si.dat "$spec" idx kb_si.idx >> logs/plan_idx_full.log
  # strip the trailing PLAN scored= line for the selection diff
  head -n -1 logs/plan_idx_full.log | tail -n +$(( $(wc -l < logs/plan_idx_full.log) - 4 )) >> /dev/null
  echo "### $id $spec" >> logs/gen_flat.log
  "$ORIG" gen "$KB" "$spec" >> logs/gen_flat.log
  echo "### $id $spec" >> logs/gen_idx.log
  ./kb_main_si gen kb_si.dat "$spec" idx kb_si.idx >> logs/gen_idx.log
done < "$SPECS"
# build selection-only idx log: drop every "PLAN scored=" line
grep -v "^PLAN scored=" logs/plan_idx_full.log > logs/plan_idx.log
echo "specs done"
