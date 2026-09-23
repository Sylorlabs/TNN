#!/bin/bash
# S4/S5/S1L measurement matrix — run AFTER the base/s1b/s2/s3 matrix finishes.
# 3 reps at 240K and 1M for s4, s5, s1l.
cd ~/workspace/tnn-lab/ops/storage-compression/src
export TMPDIR=~/workspace/tmp_commit
for scheme in s4 s5 s1l; do
  for spec in "240000 10000" "1000008 41667"; do
    set -- $spec
    for rep in 1 2 3; do
      ./$scheme\_bin train $1 24 $2 1 $rep ~/workspace/scale/corpus/texts > ~/workspace/tnn-lab/ops/storage-compression/evidence/${scheme}_N$1_rep$rep.log 2>&1
      echo "$scheme N=$1 rep=$rep rc=$? $(date +%H:%M:%S)"
    done
  done
done
echo MATRIX_S4_S5_S1L_DONE
