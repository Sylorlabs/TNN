#!/bin/sh
# few-shot ladder: 5 reps per config, byte-identity on log minus timing line.
cd ~/workspace/scale-fewshot/driver
BIN=./fewshot_learner
TEXTS=~/workspace/scale/corpus/texts
RDIR=~/workspace/scale-fewshot/runs
mkdir -p "$RDIR"
# N C M OFF label
CONFIGS="192,24,8,0,n192 128,16,8,0,n128 96,24,4,0,n096 64,16,4,0,n064 48,24,2,0,n048 32,16,2,0,n032 24,24,1,0,n024 16,16,1,0,n016 8,8,1,0,n008 4,4,1,0,n004 2,2,1,0,n002 1,1,1,0,n001 1,1,1,6,n001_plant 2,2,1,5,n002_mixed"
: > "$RDIR/identity.txt"
for cfg in $CONFIGS; do
  N=$(echo "$cfg" | cut -d, -f1); C=$(echo "$cfg" | cut -d, -f2)
  M=$(echo "$cfg" | cut -d, -f3); OFF=$(echo "$cfg" | cut -d, -f4)
  LBL=$(echo "$cfg" | cut -d, -f5)
  for r in 0 1 2 3 4; do
    "$BIN" eval "$N" "$C" "$M" 1 "$r" "$TEXTS" "$OFF" > "$RDIR/${LBL}_r${r}.log" 2>&1 || echo "RUNFAIL $LBL r$r"
  done
  H=$(grep -v SCALE_RECALL_TIMING "$RDIR/${LBL}_r"*.log | md5sum | awk '{print $1}' | sort -u | tr '\n' ' ')
  NH=$(echo "$H" | wc -w)
  echo "$LBL N=$N C=$C M=$M OFF=$OFF nhash=$NH $H" | tee -a "$RDIR/identity.txt"
done
echo "LADDER DONE"
