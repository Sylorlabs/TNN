#!/bin/bash
# Run R2-10 sense batch on all R2 fixtures, score vs truth.
set -u
SENSE=~/workspace/tnn-lab/senses/pam-rebuild/round2/forks/R2-10/src/sense
FIX=~/workspace/tnn-lab/senses/pam-rebuild/round2/fixtures
OUT=~/workspace/tnn-lab/senses/pam-rebuild/round2/forks/R2-10/evidence
mkdir -p "$OUT"
for task in colordisc colorconst shapetrans pitchdisc timbredisc motiondir; do
  case $task in
    colordisc|colorconst|shapetrans) ext=img;;
    pitchdisc|timbredisc) ext=pcm;;
    motiondir) ext=vid;;
  esac
  ls "$FIX"/r2n_${task}_*.$ext "$FIX"/r2a_${task}_*.$ext 2>/dev/null | sort > /tmp/r210_$task.list
  "$SENSE" batch "$task" /tmp/r210_$task.list noemit - > "$OUT/batch_${task}.tsv" 2>/tmp/r210_$task.err
  echo "$task: $(wc -l < "$OUT/batch_${task}.tsv") lines, err: $(cat /tmp/r210_$task.err | head -1)"
done
