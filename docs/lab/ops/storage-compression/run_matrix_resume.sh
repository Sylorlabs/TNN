#!/bin/bash
# Resume S4/S5/S1L matrix from s4 1M (s4 240K already done).
cd ~/workspace/tnn-lab/ops/storage-compression/src
export TMPDIR=~/workspace/tmp_commit
EV=~/workspace/tnn-lab/ops/storage-compression/evidence
# s4 1M (rep1 was interrupted, re-run all 3)
for rep in 1 2 3; do
  ./s4_bin train 1000008 24 41667 1 $rep ~/workspace/scale/corpus/texts > $EV/s4_N1000008_rep$rep.log 2>&1
  echo "s4 N=1000008 rep=$rep rc=$? $(date +%H:%M:%S)"
done
# s5: 240K and 1M
for spec in "240000 10000" "1000008 41667"; do
  set -- $spec
  for rep in 1 2 3; do
    ./s5_bin train $1 24 $2 1 $rep ~/workspace/scale/corpus/texts > $EV/s5_N$1_rep$rep.log 2>&1
    echo "s5 N=$1 rep=$rep rc=$? $(date +%H:%M:%S)"
  done
done
# s1l: 240K and 1M
for spec in "240000 10000" "1000008 41667"; do
  set -- $spec
  for rep in 1 2 3; do
    ./s1l_bin train $1 24 $2 1 $rep ~/workspace/scale/corpus/texts > $EV/s1l_N$1_rep$rep.log 2>&1
    echo "s1l N=$1 rep=$rep rc=$? $(date +%H:%M:%S)"
  done
done
echo MATRIX_RESUME_DONE
