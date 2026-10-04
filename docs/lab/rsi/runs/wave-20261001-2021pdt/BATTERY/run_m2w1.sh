#!/bin/bash
# M2-W1 interactive driver loop (mechanical shell; all routing logic in the Zag driver).
# Usage: run_m2w1.sh <run#> <envelope> <world_out> <trans_out> <log_out> <state>
# Grows the world file from the template; runs the frozen shim on incremental
# snippets with persistent state; logs ACTs with roles resolved by the driver.
set -e
export PATH="$HOME/safebin"
LANE=/home/hatch/workspace/tnn-rsi/docs/lab/rsi/runs/wave-20261001-2021pdt/BATTERY
DRIVER=$LANE/v2_m2w1_driver_bin
SHIM=/home/hatch/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/core_freeze_tnn2_shim/freeze_shim2_bin
RUN=$1; ENVELOPE=$2; WORLD=$3; TRANS=$4; LOG=$5; STATE=$6

# World starts empty; driver step 0 emits the fixed template (bias seeds).
# The template file m2w1v2_template.txt is the sealed pre-run record.
> $WORLD
> $TRANS
> $LOG
rm -f $STATE

STEP=0
LAST="none"
while true; do
  OUT=$($DRIVER $ENVELOPE $STEP $LAST)
  if echo "$OUT" | grep -q "^D+"; then break; fi
  echo "$OUT" | grep "^W+" | sed 's/^W+//' > /tmp/v2_step.txt
  echo "$OUT" | grep "^L+" | sed 's/^L+//' >> $LOG
  cat /tmp/v2_step.txt >> $WORLD
  if [ -s /tmp/v2_step.txt ]; then
    $SHIM /tmp/v2_step.txt $STATE > /tmp/v2_step_out.txt
    cat /tmp/v2_step_out.txt >> $TRANS
    C=$(grep "^CHOICE " /tmp/v2_step_out.txt | tail -1 | awk '{print $2}')
    if [ -n "$C" ]; then LAST=$C; else LAST="none"; fi
  else
    LAST="none"
  fi
  STEP=$(echo "$OUT" | grep "^N+" | sed 's/^N+//')
done
echo "M2-W1 run $RUN done steps=$STEP"
