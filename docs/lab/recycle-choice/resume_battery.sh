#!/bin/bash
# Resume Experiment A battery: skip cells where both r1/r2 logs exist.
set -u
cd ~/workspace/recycle-choice
OUT=logs/s1
OUT10=logs/s10
mkdir -p $OUT $OUT10
BIN_C=build_c/trial_a_c
BIN_D=build_d/trial_a_d
fails=0

run_cell() { # binary arm cur var scale outdir
    local bin=$1; local arm=$2; local cur=$3; local var=$4; local scale=$5; local outdir=$6
    local base="cell_${arm}_${cur}_${var}_${scale}"
    if [ -f "$outdir/${base}_r1.log" ] && [ -f "$outdir/${base}_r2.log" ]; then
        if cmp -s "$outdir/${base}_r1.log" "$outdir/${base}_r2.log"; then
            echo "skip (done): $base"
            return 0
        fi
    fi
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

echo "== S1 battery (resume) =="
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

echo "== S10 battery (resume) =="
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
