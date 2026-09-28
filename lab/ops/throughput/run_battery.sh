#!/bin/bash
# Throughput battery runner. Sequential (avoid self-inflicted contention).
# Logs -> ops/throughput/runs/
set -u
THR=~/workspace/tnn-lab/ops/throughput
RUNS=$THR/runs
TEXTS=~/workspace/scale/corpus/texts
mkdir -p "$RUNS"

echo "=== learner ==="
for spec in "240 10" "2400 100" "24000 1000" "240000 10000"; do
  set -- $spec; N=$1; M=$2
  for rep in 1 2 3 4 5; do
    log=$RUNS/learner_N${N}_rep${rep}.log
    echo "run learner N=$N rep=$rep"
    $THR/thru_learner_bin train $N 24 $M 1 $rep "$TEXTS" > "$log" 2>&1
    echo "exit=$? THRU: $(grep -h THRU "$log" | tr '\n' ' ')"
  done
done

echo "=== dialogue ==="
cd ~/workspace/tnn-lab/dialogue
for rep in 1 2 3 4 5; do
  log=$RUNS/dialogue_rep${rep}.log
  echo "run dialogue rep=$rep"
  $THR/dlg_thru_bin > "$log" 2>&1
  echo "exit=$? THRU: $(grep -h THRU "$log" | tr '\n' ' ')"
done
echo "=== battery done ==="
