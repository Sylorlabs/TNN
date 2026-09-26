#!/bin/bash
# PB3 remaining-problems runner with generous timeout (600s).
# Separate file so the chain50 runner's script offset is not disturbed.
set -u
CACHEPFX="${1:-n5f}"
PATTERN="$2"
N5=~/workspace/n5_recovery/n5_bin
R4B=~/workspace/tnn-lab/math_logic/round4/batteries
R3B=~/workspace/tnn-lab/math_logic/round3/batteries
KNOW=$R4B/knowledge/KNOWLEDGE_STORE_NL.md
OUT=~/workspace/n5_recovery/runs
LOG=$OUT/RUNLOG.txt
mkdir -p $OUT/pb3
cd ~/workspace/tnn-lab/math_logic/round4/engines/n5
echo -n "" > /tmp/${CACHEPFX}_cache_clean.txt
for f in $PATTERN; do
  n=$(basename "$f" .txt)
  if [ -f "$OUT/pb3/${n}_r1.out" ] && [ -s "$OUT/pb3/${n}_r1.out" ] && \
     [ -f "$OUT/pb3/${n}_r2.out" ] && [ -s "$OUT/pb3/${n}_r2.out" ] && \
     [ -f "$OUT/pb3/${n}_r3.out" ] && [ -s "$OUT/pb3/${n}_r3.out" ]; then
    if cmp -s "$OUT/pb3/${n}_r1.out" "$OUT/pb3/${n}_r2.out" && \
       cmp -s "$OUT/pb3/${n}_r1.out" "$OUT/pb3/${n}_r3.out"; then
      echo "pb3 $n SKIP-OK $(grep -h '^VERDICT:' $OUT/pb3/${n}_r1.out | head -1)"
      continue
    fi
  fi
  echo "pb3 $n running (600s x3)..."
  for r in 1 2 3; do
    cp /tmp/${CACHEPFX}_cache_clean.txt /tmp/${CACHEPFX}_cache_run.txt
    timeout 600 "$N5" "$f" "$KNOW" /tmp/${CACHEPFX}_cache_run.txt /tmp/${CACHEPFX}_stage_run.txt > "$OUT/pb3/${n}_r${r}.out" 2>&1
    rc=$?
    [ $rc -ne 0 ] && echo "RC$rc pb3 $n run$r" | tee -a $LOG
  done
  cmp -s "$OUT/pb3/${n}_r1.out" "$OUT/pb3/${n}_r2.out" || echo "NONDET pb3 $n r1!=r2" | tee -a $LOG
  cmp -s "$OUT/pb3/${n}_r1.out" "$OUT/pb3/${n}_r3.out" || echo "NONDET pb3 $n r1!=r3" | tee -a $LOG
  echo "pb3 $n $(grep -h '^VERDICT:' $OUT/pb3/${n}_r1.out | head -1)"
done | tee -a "$OUT/RUNLOG_PB3SLOW.txt"
echo "PB3-SLOW done"
