#!/bin/bash
BIN=~/workspace/strength-round4/capacity/src/trial_bin_cap
OUT=~/workspace/strength-round4/capacity/evidence
fail=0
for arm in B B2; do
  for cur in VUP WBS JI; do
    for var in 0 1 2; do
      f1=$OUT/s10_cell_${arm}_${cur}_${var}_r1.log
      f2=$OUT/s10_cell_${arm}_${cur}_${var}_r2.log
      $BIN $arm $cur $var S10 > $f1 2>&1; rc1=$?
      $BIN $arm $cur $var S10 > $f2 2>&1; rc2=$?
      if [ $rc1 -ne 0 ] || [ $rc2 -ne 0 ]; then echo "RCFAIL $arm $cur $var"; fail=1; fi
      if ! cmp -s $f1 $f2; then echo "DIFF $arm $cur $var"; fail=1; fi
    done
  done
done
echo "s10_done fail=$fail"
