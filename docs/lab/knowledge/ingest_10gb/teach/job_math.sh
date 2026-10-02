#!/bin/bash
# job_math.sh — chunk SE math Posts.xml, clean -> stage/se_math_run1
set -u
W=/home/hatch/workspace/scratch_10gb_work
T=/home/hatch/workspace/tnn-lab/knowledge/ingest_10gb/teach
echo "[math] chunking Posts.xml"
python3 $T/chunk_se.py $W/se_math/Posts.xml $W/stage/se_math_in math
echo "[math] cleaning"
python3 $T/clean2.py --raw $W/stage/se_math_in --out $W/stage/se_math_run1
echo "[math] DONE rc=$?"
