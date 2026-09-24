#!/bin/bash
# NKEY full-corpus runs: V0 x1 (rebuild validation), V1 x2, V2 x2.
# Sequential, one store at a time (disk: 8.2G free, 4.7G/store).
# Determinism via manifest + aggregate store SHA (prereg deviation from
# diff -r, documented: disk cannot hold two full stores at once).
set -u
W=/home/hatch/workspace/scratch_10gb_work
FACTS=$W/dryrun/dryrun_facts.dat
BAD=/home/hatch/workspace/tmp10/bad.bin
NCAP=11292656
V0=/home/hatch/workspace/tnn-lab/knowledge/ingest_10gb/teach/v0test_bin
V1=$W/gate_v1_bin
V2=$W/gate_v2_bin
OUT=$W/nkey_fullrun.log

run_one() { # bin, tag
  local bin=$1 tag=$2
  local dir=$W/nkey_full_${tag}
  echo "[$(date -u +%H:%M:%S)] START $tag" | tee -a $OUT
  df -h /home/hatch | tail -1 | tee -a $OUT
  rm -rf $dir
  "$bin" ingest "$FACTS" "$BAD" "$dir/" $NCAP > $W/nkey_full_${tag}.log 2>&1
  echo "[$(date -u +%H:%M:%S)] DONE $tag rc=$?" | tee -a $OUT
  grep -E "^(n|nsealed|g1|g2|g3|lessons|lessons_rejected|negcontrol)" $dir/manifest.txt | tr '\n' ' ' | tee -a $OUT
  echo "" | tee -a $OUT
  grep "seal=" $dir/manifest.txt | tee -a $OUT
  ( cd $dir && find . -type f | sort | xargs sha256sum | sha256sum ) | tee -a $OUT
  grep -c "CAL=REJECT" $dir/audit.log | xargs echo "reject_lessons=" | tee -a $OUT
  cp $dir/manifest.txt $W/nkey_full_${tag}_manifest.txt
  grep "LESSON" $dir/audit.log > $W/nkey_full_${tag}_lessons.txt
}

run_one $V0 v0
rm -rf $W/nkey_full_v0
run_one $V1 v1a
rm -rf $W/nkey_full_v1a
run_one $V1 v1b
rm -rf $W/nkey_full_v1b
run_one $V2 v2a
rm -rf $W/nkey_full_v2a
run_one $V2 v2b
rm -rf $W/nkey_full_v2b
echo "[$(date -u +%H:%M:%S)] ALL DONE" | tee -a $OUT
