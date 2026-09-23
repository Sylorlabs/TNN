#!/bin/bash
# Baseline runs: 1x/10x x2, 100x (4 chunks) x2. Times each run.
cd ~/workspace/tnn-lab/dialogue/cmp_scale || exit 1
BIN=../../baseline/dialogue_bin
mkdir -p runs
run_one() {
  local name=$1 batt=$2
  local d=runs/$name
  mkdir -p "$d"
  cp baseline/kb.txt baseline/gaz.txt "$d/"
  cp "$batt" "$d/battery.txt"
  local t0=$(date +%s%N)
  (cd "$d" && ../../baseline/dialogue_bin > run.log 2>&1)
  local t1=$(date +%s%N)
  local ms=$(( (t1 - t0) / 1000000 ))
  local n=$(grep -c "DIALOGUE" "$batt")
  echo "$name questions=$n ms=$ms" | tee -a runs/TIMING.txt
}
: > runs/TIMING.txt
run_one r1x_1 battery_1x.txt
run_one r1x_2 battery_1x.txt
run_one r10x_1 battery_10x.txt
run_one r10x_2 battery_10x.txt
for c in 1 2 3 4; do
  run_one r100x_p${c}_1 battery_100x_p${c}.txt
  run_one r100x_p${c}_2 battery_100x_p${c}.txt
done
echo ALLDONE
