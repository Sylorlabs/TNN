#!/bin/bash
# Finish the 4 interrupted D S10 cells (absolute paths, durable).
set -u
W=~/workspace/recycle-choice
BIN=$W/build_d/trial_a_d
OUT=$W/logs/s10
fails=0
run_cell() { # arm cur var
    local arm=$1 cur=$2 v=$3
    local base="cell_${arm}_${cur}_${v}_s10"
    if [ -f "$OUT/${base}_r1.log" ] && [ -f "$OUT/${base}_r2.log" ] && cmp -s "$OUT/${base}_r1.log" "$OUT/${base}_r2.log"; then
        echo "skip (done): $base"; return 0
    fi
    $BIN $arm $cur $v s10 > "$OUT/${base}_r1.log" 2>&1; e1=$?
    $BIN $arm $cur $v s10 > "$OUT/${base}_r2.log" 2>&1; e2=$?
    if [ $e1 -ne 0 ] || [ $e2 -ne 0 ]; then echo "FAIL(exit $e1/$e2): $base"; return 1; fi
    if ! cmp -s "$OUT/${base}_r1.log" "$OUT/${base}_r2.log"; then echo "FAIL(diff): $base"; return 1; fi
    echo "ok: $base"; return 0
}
run_cell D WBS 1 || fails=$((fails+1))
run_cell D WBS 2 || fails=$((fails+1))
run_cell D JI 1  || fails=$((fails+1))
run_cell D JI 2  || fails=$((fails+1))
echo "finish_a done, fails=$fails"
