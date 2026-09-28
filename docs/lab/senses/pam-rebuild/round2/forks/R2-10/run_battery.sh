#!/bin/bash
# R2-10 full mechanical battery (fixed binary). Deterministic; 3 runs.
set -u
R2=~/workspace/tnn-lab/senses/pam-rebuild/round2/forks/R2-10
SENSE=$R2/src/sense
FIX=~/workspace/tnn-lab/senses/pam-rebuild/round2/fixtures
OUT=$R2/evidence/battery
mkdir -p "$OUT"
for task in colordisc colorconst shapetrans pitchdisc timbredisc motiondir; do
  case $task in
    colordisc|colorconst|shapetrans) ext=img;;
    pitchdisc|timbredisc) ext=pcm;;
    motiondir) ext=vid;;
  esac
  ls "$FIX"/r2n_${task}_*.$ext "$FIX"/r2a_${task}_*.$ext 2>/dev/null | sort > "$OUT/list_${task}.txt"
  echo "$task: $(wc -l < "$OUT/list_${task}.txt") trials"
done
for run in 1 2 3; do
  for task in colordisc colorconst shapetrans pitchdisc timbredisc motiondir; do
    "$SENSE" batch "$task" "$OUT/list_${task}.txt" noemit - > "$OUT/noemit_${task}_run${run}.tsv" 2>"$OUT/noemit_${task}_run${run}.err"
    echo "run$run $task noemit: $(wc -l < "$OUT/noemit_${task}_run${run}.tsv") lines"
  done
done
echo BATTERY_NOEMIT_DONE
