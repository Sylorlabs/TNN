#!/bin/bash
# Head-to-head S1 matrix: B vs B1 vs B2, 2x each, byte-identity enforced.
BIN=~/workspace/strength-round4/capacity/src/trial_bin_cap
OUT=~/workspace/strength-round4/capacity/evidence
fail=0
for arm in B B1 B2; do
  for cur in VUP WBS JI; do
    for var in 0 1 2; do
      f1=$OUT/cell_${arm}_${cur}_${var}_r1.log
      f2=$OUT/cell_${arm}_${cur}_${var}_r2.log
      $BIN $arm $cur $var S1 > $f1 2>&1; rc1=$?
      $BIN $arm $cur $var S1 > $f2 2>&1; rc2=$?
      if [ $rc1 -ne 0 ] || [ $rc2 -ne 0 ]; then echo "RCFAIL $arm $cur $var $rc1 $rc2"; fail=1; fi
      if ! cmp -s $f1 $f2; then echo "DIFF $arm $cur $var"; fail=1; fi
    done
  done
done
# GATE for the new arms
for arm in B1 B2; do
  $BIN $arm GATE 0 S1 > $OUT/gate_${arm}_r1.log 2>&1
  $BIN $arm GATE 0 S1 > $OUT/gate_${arm}_r2.log 2>&1
  if ! cmp -s $OUT/gate_${arm}_r1.log $OUT/gate_${arm}_r2.log; then echo "GATE DIFF $arm"; fail=1; fi
done
echo "matrix_done fail=$fail"
