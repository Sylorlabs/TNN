#!/bin/bash
# Battery v2 execution: 3 blocks x 3 runs. Deterministic shell.
# Verifies frozen shim hash before each block and after the battery (K-S3v2).
# Usage: run_battery.sh
set -e
export PATH="$HOME/safebin"
LANE=/home/hatch/workspace/tnn-rsi/docs/lab/rsi/runs/wave-20261001-2021pdt/BATTERY
SHIM=/home/hatch/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/core_freeze_tnn2_shim/freeze_shim2_bin
FROZEN_SHIM_SHA="9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954"
cd $LANE

check_shim() {
  local h=$(sha256sum $SHIM | awk '{print $1}')
  if [ "$h" != "$FROZEN_SHIM_SHA" ]; then
    echo "FROZEN SHIM HASH MISMATCH: $h"
    exit 1
  fi
  echo "shim hash OK ($1)"
}

run_fixed() { # <world> <state> <transcript>
  $SHIM $1 $2 > $3
  local rc=$?
  if [ $rc -ne 0 ]; then echo "SHIM EXIT $rc on $1"; exit 1; fi
}

for BLOCK in m1 m2 m3; do
  check_shim "before block $BLOCK"
  for RUN in 1 2 3; do
    STATE=$LANE/${BLOCK}_state_run${RUN}.bin
    rm -f $STATE
    if [ "$BLOCK" = "m1" ]; then
      run_fixed $LANE/m1w1v2_world.txt $STATE $LANE/${BLOCK}_run${RUN}_w1.txt
      run_fixed $LANE/m1w2v2_world.txt $STATE $LANE/${BLOCK}_run${RUN}_w2.txt
      run_fixed $LANE/m1w3v2_world.txt $STATE $LANE/${BLOCK}_run${RUN}_w3.txt
      $LANE/v2_inspect_state_bin $STATE $LANE/m1w1v2_world.txt > $LANE/${BLOCK}_inspect_run${RUN}.txt
    fi
    if [ "$BLOCK" = "m2" ]; then
      $LANE/run_m2w1.sh $RUN $LANE/m2w1v2_envelope_run${RUN}.txt \
        $LANE/m2w1v2_world_run${RUN}.txt $LANE/m2w1_trans_run${RUN}.txt \
        $LANE/m2w1_log_run${RUN}.txt $STATE
      run_fixed $LANE/m2w2v2_world.txt $STATE $LANE/${BLOCK}_run${RUN}_w2.txt
      run_fixed $LANE/m2w3v2_world.txt $STATE $LANE/${BLOCK}_run${RUN}_w3.txt
      $LANE/v2_inspect_state_bin $STATE $LANE/m2w1v2_world_run${RUN}.txt > $LANE/${BLOCK}_inspect_run${RUN}.txt
    fi
    if [ "$BLOCK" = "m3" ]; then
      run_fixed $LANE/m3w1v2_world.txt $STATE $LANE/${BLOCK}_run${RUN}_w1.txt
      run_fixed $LANE/m3w2v2_world.txt $STATE $LANE/${BLOCK}_run${RUN}_w2.txt
      run_fixed $LANE/m3w3v2_world.txt $STATE $LANE/${BLOCK}_run${RUN}_w3.txt
      $LANE/v2_inspect_state_bin $STATE $LANE/m3w1v2_world.txt > $LANE/${BLOCK}_inspect_run${RUN}.txt
    fi
    echo "BLOCK $BLOCK RUN $RUN DONE"
  done
done
check_shim "after battery"
# tnn2.zag unchanged (K-S3v2)
ZAG_SHA=$(sha256sum /home/hatch/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag | awk '{print $1}')
if [ "$ZAG_SHA" != "a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd" ]; then
  echo "TNN2.ZAG HASH MISMATCH"; exit 1
fi
echo "tnn2.zag hash OK"
echo "BATTERY RUN COMPLETE"
