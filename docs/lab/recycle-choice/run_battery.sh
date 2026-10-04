#!/bin/bash
# Experiment A battery runner.
# Runs: arms C/M (choice binary), D (delete binary) x curricula x variants x scales, 2x each.
# Every run is byte-diffed (r1 vs r2). Foreground sequential (background & jobs
# + relative redirects yield empty logs in this sandbox).
set -u
cd ~/workspace/recycle-choice
OUT=logs/s1
OUT10=logs/s10
mkdir -p $OUT $OUT10

run_cell() { # binary arm cur var scale outdir
    local bin=$1; local arm=$2; local cur=$3; local var=$4; local scale=$5; local outdir=$6
    local base="cell_${arm}_${cur}_${var}_${scale}"
    ./$bin $arm $cur $var $scale > $outdir/${base}_r1.log 2>&1
    local e1=$?
    ./$bin $arm $cur $var $scale > $outdir/${base}_r2.log 2>&1
    local e2=$?
    if [ $e1 -ne 0 ] || [ $e2 -ne 0 ]; then
        echo "FAIL(exit $e1/$e2): $base"
        return 1
    fi
    if ! cmp -s $outdir/${base}_r1.log $outdir/${base}_r2.log; then
        echo "FAIL(diff): $base"
        return 1
    fi
    echo "ok: $base"
    return 0
}

BIN_C=build_c/trial_a_c
BIN_D=build_d/trial_a_d
fails=0

echo "== S1 battery =="
for arm in C M D; do
    bin=$BIN_C
    if [ "$arm" = "D" ]; then bin=$BIN_D; fi
    for cur in VUP WBS JI; do
        for v in 0 1 2 3 4 5; do
            run_cell $bin $arm $cur $v s1 $OUT || fails=$((fails+1))
        done
    done
    echo "S1 $arm done"
done

echo "== S10 battery =="
for arm in C M D; do
    bin=$BIN_C
    if [ "$arm" = "D" ]; then bin=$BIN_D; fi
    for cur in VUP WBS JI; do
        for v in 0 1 2; do
            run_cell $bin $arm $cur $v s10 $OUT10 || fails=$((fails+1))
        done
    done
    echo "S10 $arm done"
done

echo "battery done, fails=$fails"
