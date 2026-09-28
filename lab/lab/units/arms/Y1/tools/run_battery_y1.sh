#!/bin/bash
# run_battery_y1.sh — full 1x M1–M9 battery for the Y1 arm binary (+ memorizer),
# including the M6 memorizer control, the Y1 binding kill-1x trial, and the M8
# N=5 adversarial gate. Every leg runs twice with stdout diffed (byte-identical
# rule). Local to Y1; does not modify the frozen harness scripts.
# Usage: run_battery_y1.sh <y1-bin> <memorizer-bin> <corpus-root> <workdir>
set -u
BIN="$1"; MEM="$2"; CROOT="$3"; WORK="$4"
HARNESS="$(cd "$(dirname "$0")/../../harness" && pwd)"
mkdir -p "$WORK"
PASS=0; FAIL=0
leg() { # <mode> [bin]
    local mode="$1"; local bin="${2:-$BIN}"
    echo "=== leg $mode ==="
    if "$HARNESS/run_metric.sh" "$bin" "$mode" "$CROOT" "$WORK/$mode"; then
        PASS=$((PASS+1))
    else
        FAIL=$((FAIL+1)); echo "LEG FAILED: $mode"
    fi
}
leg m1-1x-prose
leg m1-1x-code
leg m2-t1-prose
leg m2-t1-code
leg m2-t2-prose
leg m2-t2-code
leg m2-t3-1x
leg m3-1x
leg m4-1x-prose
leg m4-1x-code
leg m5-baseline
leg m5-1x
leg m6-p2c-1x
leg m6-c2p-1x
leg memctrl-p2c-1x "$MEM"
leg memctrl-c2p-1x "$MEM"
leg m7-1x
leg kill-1x
echo "=== M8 gate ==="
mkdir -p "$WORK/m8"
if "$HARNESS/m8_gate.sh" "$BIN" "$CROOT" "$WORK/m8" > "$WORK/m8/GATE.txt" 2>&1; then
    tail -1 "$WORK/m8/GATE.txt"; PASS=$((PASS+1))
else
    tail -3 "$WORK/m8/GATE.txt"; FAIL=$((FAIL+1)); echo "M8 GATE FAILED"
fi
echo "=== assembling Y1 scorecard ==="
python3 "$(dirname "$0")/scorecard_assemble_y1.py" "$WORK" "$WORK/scorecard_y1_r1_1x.json"
echo "legs passed=$PASS failed=$FAIL"
[ "$FAIL" = "0" ]
