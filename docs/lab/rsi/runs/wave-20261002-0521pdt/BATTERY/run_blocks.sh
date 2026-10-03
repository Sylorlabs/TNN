#!/bin/bash
# run_blocks.sh -- E10 block runner (deterministic shell).
# Usage: run_blocks.sh <run#>
# Runs M1, M2, M3 blocks end to end; each block starts from fresh state,
# state persists across worlds within a block. T-K3 shim hash verified
# before the run. Exit nonzero on any shim/driver failure (fail-closed).
set -e
export PATH="$HOME/safebin"
DIR=~/workspace/tnn-rsi/docs/lab/rsi/runs/wave-20261002-0521pdt/BATTERY
SHIM=~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/core_freeze_tnn2_shim/freeze_shim2_bin
RUN=$1
. "$DIR/PI_ENV.sh"

echo "9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954  $SHIM" | sha256sum -c -

# M1 block
rm -f "$DIR/m1_state_run${RUN}.bin"
for w in m1w1 m1w2 m1w3; do
  "$SHIM" "$DIR/${w}_world.txt" "$DIR/m1_state_run${RUN}.bin" > "$DIR/${w}_trans_run${RUN}.txt"
done
"$DIR/e10_inspect_bin" "$DIR/m1_state_run${RUN}.bin" > "$DIR/m1_inspect_run${RUN}.txt"

# M2 block (persistent state w1 -> w2 -> w3)
"$DIR/e10_m2_driver.sh" w1 "$RUN" 1
"$DIR/e10_m2_driver.sh" w2 "$RUN" 0
"$DIR/e10_m2_driver.sh" w3 "$RUN" 0
"$DIR/e10_inspect_bin" "$DIR/m2_state_run${RUN}.bin" > "$DIR/m2_inspect_run${RUN}.txt"

# M3 block
rm -f "$DIR/m3_state_run${RUN}.bin"
for w in m3w1 m3w2 m3w3; do
  "$SHIM" "$DIR/${w}_world.txt" "$DIR/m3_state_run${RUN}.bin" > "$DIR/${w}_trans_run${RUN}.txt"
done
"$DIR/e10_inspect_bin" "$DIR/m3_state_run${RUN}.bin" > "$DIR/m3_inspect_run${RUN}.txt"
echo "run $RUN complete"
