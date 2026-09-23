#!/usr/bin/env bash
# SI Arm 3 measurement matrix. Battery: loop/battery.json --budget 6
# (speed_intel/battery_si.json did not exist; reported in the writeup).
set -u
SI=~/workspace/tnn-lab/coding/reflection/speed_intel
LOOP=~/workspace/tnn-lab/coding/reflection/loop
R=$SI/work_a3/runs
mkdir -p $R

# 1) baseline: ORIGINAL driver + ORIGINAL learner, 3 reruns
for r in 1 2 3; do
  (cd $LOOP && python3 driver.py battery.json --budget 6 \
     --workdir $R/baseline_orig_r$r/work --out $R/baseline_orig_r$r.json \
     > $R/baseline_orig_r$r.log 2>&1) &
done
wait

# 2) sanity cell + mechanisms, 3 reruns each
for m in none a b c; do
  for r in 1 2 3; do
    (cd $SI && python3 driver_si.py ../loop/battery.json --budget 6 --mech $m \
       --workdir $R/mech${m}_r$r/work --out $R/mech${m}_r$r.json \
       > $R/mech${m}_r$r.log 2>&1) &
  done
  wait
done
echo ALL-DONE
