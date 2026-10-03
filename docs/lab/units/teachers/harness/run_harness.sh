#!/bin/bash
# run_harness.sh — Build and run the Track B teacher harness test suite.
#
# Usage:
#   ./run_harness.sh [mode...]     Build (if needed) and run specified modes,
#                                  or all 13 modes if none given.
#   ./run_harness.sh --build-only  Only compile, do not run.
#
# Modes: smoke codec malformed seq tripwire replay defer hint oracle det
#        pertA pertB cost
#
# Exit code: 0 if all requested modes PASS, 1 otherwise.
set -u

HARNESS_DIR="$(cd "$(dirname "$0")" && pwd)"
ZNC="$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1"
SRC="$HARNESS_DIR/harness.zag"
BIN="${HARNESS_BIN:-/tmp/harness_bin}"

ALL_MODES="smoke codec malformed seq tripwire replay defer hint oracle det pertA pertB cost"

if [ "${1:-}" = "--build-only" ]; then
    "$ZNC" "$SRC" --no-zagd -o "$BIN"
    echo "build exit=$?"
    exit $?
fi

# Build
"$ZNC" "$SRC" --no-zagd -o "$BIN" > /tmp/harness_build.log 2>&1
if [ $? -ne 0 ]; then
    echo "BUILD FAILED"
    tail -20 /tmp/harness_build.log
    exit 1
fi
echo "build OK: $BIN"

MODES="${@:-$ALL_MODES}"
fails=0
for m in $MODES; do
    out=$(timeout 120 "$BIN" "$m" 2>&1)
    rc=$?
    status=$(echo "$out" | tail -1)
    if [ $rc -eq 0 ]; then
        echo "PASS $m"
    else
        echo "FAIL $m (exit=$rc): $status"
        fails=$((fails+1))
    fi
done

if [ $fails -eq 0 ]; then
    echo "ALL_OK"
    exit 0
else
    echo "$fails mode(s) FAILED"
    exit 1
fi
