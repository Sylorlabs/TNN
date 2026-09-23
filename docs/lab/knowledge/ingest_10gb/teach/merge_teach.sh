#!/bin/bash
# merge_teach.sh — merge run-N facts, record SHA (glue; merge itself is merge_facts.py)
set -u
W=/home/hatch/workspace/scratch_10gb_work
T=/home/hatch/workspace/tnn-lab/knowledge/ingest_10gb/teach
N=$1   # 1 or 2
shift
# args: list of "name:outdir" pairs in fixed shard order
OUT=$W/facts_run$N.dat
SHARDS=""
for pair in "$@"; do
  name=${pair%%:*}
  dir=${pair#*:}
  f=$W/stage/${dir}/facts.dat
  if [ ! -f "$f" ]; then echo "MISSING shard $name: $f"; exit 1; fi
  SHARDS="$SHARDS $f"
done
echo "[merge] run $N shards:$SHARDS"
python3 $T/merge_facts.py "$OUT" $SHARDS
sha256sum "$OUT" | tee $W/facts_run$N.dat.sha256sum
echo "[merge] run $N done"
