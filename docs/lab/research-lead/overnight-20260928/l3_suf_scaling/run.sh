#!/bin/sh
# run.sh -- run one (fam,sc) binary 3x, capturing stdout/stderr/exit.
# Usage: run.sh <fam> <sc>
set -u
export PATH="$HOME/safebin"
HERE=$(dirname "$0")
cd "$HERE"
fam=$1
sc=$2
mkdir -p runs
i=1
while [ $i -le 3 ]; do
  ./build/scale_${fam}_${sc} > runs/run_${fam}_${sc}_${i}.out 2> runs/run_${fam}_${sc}_${i}.err
  echo "run $i exit=$?"
  i=$((i+1))
done
echo "--- stdout sha256 ---"
sha256sum runs/run_${fam}_${sc}_1.out runs/run_${fam}_${sc}_2.out runs/run_${fam}_${sc}_3.out
echo "--- stderr (run 1) ---"
cat runs/run_${fam}_${sc}_1.err
echo "--- byte-identical check ---"
cmp runs/run_${fam}_${sc}_1.out runs/run_${fam}_${sc}_2.out && cmp runs/run_${fam}_${sc}_2.out runs/run_${fam}_${sc}_3.out && echo "3/3 BYTE-IDENTICAL"
