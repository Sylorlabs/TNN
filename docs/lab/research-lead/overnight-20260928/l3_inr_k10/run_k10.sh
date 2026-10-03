#!/bin/sh
# run_k10.sh -- L3-INR-K10 probe runs. Invokes the FROZEN implementation's
# run_arm.sh verbatim (read-only); statedirs live in this lane.
# Usage: run_k10.sh  (seed fixed at 7, 3 runs per sequence)
# Sequences (fresh statedir per run i):
#   seq_pc_i: T5a(pc.world)                       [P-C probe-loop iteration]
#   seq_pd_i: T1(pd1.world) -> T4(pd2.world)      [P-D id-permuted revision]
#   seq_pe_i: T1(pd1.world) -> T4(pe2.world)      [P-E full-reversal revision]
set -e
export PATH="$HOME/safebin"
HERE=$(dirname "$0")
IMPL="$HERE/../l3_inr_impl"
RUNARM="$IMPL/run_arm.sh"
WORLDS="$HERE/worlds"
RUNS="$HERE/runs"
SEED=7
mkdir -p "$RUNS"
i=1
while [ $i -le 3 ]; do
  echo "=== run $i/3 ==="
  d="$RUNS/seq_pc_$i"
  "$RUNARM" "$d" T5a "$WORLDS/pc.world" "$SEED" || { echo "P-C run $i FAILED"; exit 1; }
  d="$RUNS/seq_pd_$i"
  "$RUNARM" "$d" T1 "$WORLDS/pd1.world" "$SEED" || { echo "P-D T1 run $i FAILED"; exit 1; }
  "$RUNARM" "$d" T4 "$WORLDS/pd2.world" "$SEED" || { echo "P-D T4 run $i FAILED"; exit 1; }
  d="$RUNS/seq_pe_$i"
  "$RUNARM" "$d" T1 "$WORLDS/pd1.world" "$SEED" || { echo "P-E T1 run $i FAILED"; exit 1; }
  "$RUNARM" "$d" T4 "$WORLDS/pe2.world" "$SEED" || { echo "P-E T4 run $i FAILED"; exit 1; }
  i=$((i+1))
done
echo "ALL K10 RUNS COMPLETE"
