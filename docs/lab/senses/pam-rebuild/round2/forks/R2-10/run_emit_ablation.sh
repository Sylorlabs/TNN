#!/bin/bash
# B4 ablation: full emit run, then compare percepts/dispositions vs noemit.
set -u
R2=~/workspace/tnn-lab/senses/pam-rebuild/round2/forks/R2-10
SENSE=$R2/src/sense
FIX=~/workspace/tnn-lab/senses/pam-rebuild/round2/fixtures
OUT=$R2/evidence/battery
ART=$OUT/emit_artifacts
mkdir -p "$ART"
for task in colordisc colorconst shapetrans pitchdisc timbredisc motiondir; do
  case $task in
    colordisc|colorconst|shapetrans) ext=img;;
    pitchdisc|timbredisc) ext=pcm;;
    motiondir) ext=vid;;
  esac
  ls "$FIX"/r2n_${task}_*.$ext "$FIX"/r2a_${task}_*.$ext 2>/dev/null | sort > /tmp/r210_${task}.list
  "$SENSE" batch "$task" /tmp/r210_${task}.list emit "$ART" > "$OUT/emit_${task}_run1.tsv" 2>/tmp/r210_emit_$task.err
  echo "$task emit: $(wc -l < "$OUT/emit_${task}_run1.tsv") lines"
done
echo "BATTERY_EMIT_DONE"
