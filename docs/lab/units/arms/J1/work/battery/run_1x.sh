#!/bin/bash
# J1 1x battery runner
# Runs all modes sequentially, captures output and METRIC_JSON
set -e
J1=~/workspace/tnn-lab/units/arms/J1/work/j1
MEM=~/workspace/tnn-lab/units/arms/harness/memorizer/work/build/memorizer_bin
CORPORA=~/workspace/tnn-lab/units/arms/harness/corpora/r1
WORK=~/workspace/tnn-lab/units/arms/J1/work/battery/r1_1x

run_mode() {
    local mode=$1
    local bin=${2:-$J1}
    echo "=== $mode ==="
    mkdir -p "$WORK/$mode"
    # Skip if fragment.json already exists and is non-empty (resume)
    if [ -s "$WORK/$mode/fragment.json" ]; then
        echo "SKIP $mode (fragment exists)"
        return 0
    fi
    cd "$WORK/$mode"
    timeout 1800 $bin "$mode" "$CORPORA" > stdout.log 2> stderr.log
    local rc=$?
    echo "exit: $rc" >> stdout.log
    # extract METRIC_JSON
    grep "^METRIC_JSON " stdout.log | sed 's/^METRIC_JSON //' > fragment.json || true
    cd - > /dev/null
    return $rc
}

# M1
run_mode "m1-1x-prose"
run_mode "m1-1x-code"

# M2
run_mode "m2-t1-prose"
run_mode "m2-t1-code"
run_mode "m2-t2-prose"
run_mode "m2-t2-code"
run_mode "m2-t3-1x"

# M3
run_mode "m3-1x"

# M4
run_mode "m4-1x-prose"
run_mode "m4-1x-code"

# M5
run_mode "m5-1x"
run_mode "m5-baseline"

# M6 (need to check memctrl modes)
run_mode "m6-p2c-1x"
run_mode "m6-c2p-1x"
run_mode "memctrl-p2c-1x" "$MEM"
run_mode "memctrl-c2p-1x" "$MEM"

# M7
run_mode "m7-1x"

echo "Battery complete"
