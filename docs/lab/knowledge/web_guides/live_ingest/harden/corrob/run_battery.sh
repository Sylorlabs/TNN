#!/bin/bash
# Full CORROB-1 battery: 70 cases x 3 modes x 2 reps = 420 runs.
# Usage: bash run_battery.sh <outdir>
set -u
cd ~/workspace/liharden/corrob
OUT=${1:-evidence/battery}
mkdir -p "$OUT" logs
CORROB=$PWD/build/corrob_bin
WEBG=~/workspace/rt_bf1/build/bin_webg_bf1
jobs=/tmp/cb_jobs_$$
: > "$jobs"
python3 battery_cases.py | grep -v '^total=' | while IFS=$'\t' read -r name path; do
  for m in verdict verdictd verdictm; do
    for rep in 1 2; do
      echo "python3 run_corrob.py $CORROB $WEBG \"$path\" $OUT $rep $m"
    done
  done
done > "$jobs"
wc -l "$jobs"
xargs -P 8 -I{} sh -c '{}' < "$jobs" > logs/battery_stdout.txt 2> logs/battery_stderr.txt
echo "done rc=$?"
