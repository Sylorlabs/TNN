#!/bin/bash
# Prototype runs: 1x/10x x2, 100x (4 chunks) x2. Mirrors run_all.sh.
cd ~/workspace/tnn-lab/dialogue/cmp_scale || exit 1
mkdir -p runs_p
run_one() {
  local name=$1 batt=$2
  local d=runs_p/$name
  mkdir -p "$d"
  cp engine/kb.txt engine/gaz.txt "$d/"
  cp "$batt" "$d/battery.txt"
  local t0=$(date +%s%N)
  (cd "$d" && ../../engine/dialogue_bin > run.log 2>&1)
  local t1=$(date +%s%N)
  local ms=$(( (t1 - t0) / 1000000 ))
  local n=$(grep -c "DIALOGUE" "$batt")
  echo "$name questions=$n ms=$ms" | tee -a runs_p/TIMING.txt
}
: > runs_p/TIMING.txt
run_one p1x_1 battery_1x.txt
run_one p1x_2 battery_1x.txt
run_one p10x_1 battery_10x.txt
run_one p10x_2 battery_10x.txt
for c in 1 2 3 4; do
  run_one p100x_p${c}_1 battery_100x_p${c}.txt
  run_one p100x_p${c}_2 battery_100x_p${c}.txt
done
echo ALLDONE
