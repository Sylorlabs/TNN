#!/bin/bash
# test_harness_fix.sh - verify the resume bug fix.
# Simulates an interrupted run, then resumes with old vs new logic.
# Zero Python. Shell + Zag driver binary only.
set -u

FIX_DIR="$(cd "$(dirname "$0")" && pwd)"
D="$(cd "$FIX_DIR/.." && pwd)"
DRIVER="$D/c1_zagdriver/zag_driver_bin"
WORLDS="$D/c1_clean/worlds"
C1BIN="$D/c1_clean/contestant_bin"
TESTBASE="/tmp/c1_harness_fix_test"

# Clean slate
rm -rf "$TESTBASE"
mkdir -p "$TESTBASE"

echo "=== Phase 1: Baseline (fresh dir, single run) ==="
d1="$TESTBASE/baseline_c1_w1_r1"
mkdir -p "$d1"
"$DRIVER" "$WORLDS/w1" "$C1BIN" "$d1" > "$d1/driver.log" 2>&1
score1=$(grep -o 'correct=[0-9]*' "$d1/costs.txt" | head -1 | cut -d= -f2)
facts1=$(grep -o 'facts=[0-9]*' "$d1/driver.log" | tail -1 | cut -d= -f2)
echo "baseline: correct=$score1 facts=$facts1"

echo ""
echo "=== Phase 2: OLD behavior (resume without clearing) ==="
d2="$TESTBASE/oldbug_c1_w1_r1"
mkdir -p "$d2"
# First run (simulates partial run before interruption)
"$DRIVER" "$WORLDS/w1" "$C1BIN" "$d2" > "$d2/driver.log" 2>&1
# Simulate interruption: delete costs.txt (as if killed before completion)
# but leave partial state/ behind
rm -f "$d2/costs.txt"
# Resume with OLD logic: mkdir -p only (no clearing)
mkdir -p "$d2"
"$DRIVER" "$WORLDS/w1" "$C1BIN" "$d2" > "$d2/driver.log" 2>&1
score2=$(grep -o 'correct=[0-9]*' "$d2/costs.txt" | head -1 | cut -d= -f2)
facts2=$(grep -o 'facts=[0-9]*' "$d2/driver.log" | tail -1 | cut -d= -f2)
echo "old-behavior: correct=$score2 facts=$facts2"
if [ "$facts2" -gt "$((facts1 * 3 / 2))" ]; then
  echo "OLD-BUG-REPRODUCED: facts doubled ($facts1 -> $facts2)"
else
  echo "OLD-BUG-NOT-REPRODUCED (unexpected)"
fi

echo ""
echo "=== Phase 3: NEW behavior (resume with rm -rf fix) ==="
d3="$TESTBASE/fixed_c1_w1_r1"
mkdir -p "$d3"
# First run (simulates partial run before interruption)
"$DRIVER" "$WORLDS/w1" "$C1BIN" "$d3" > "$d3/driver.log" 2>&1
# Simulate interruption: delete costs.txt, leave partial state/
rm -f "$d3/costs.txt"
# Resume with NEW logic: rm -rf before mkdir (the fix)
rm -rf "$d3"
mkdir -p "$d3"
"$DRIVER" "$WORLDS/w1" "$C1BIN" "$d3" > "$d3/driver.log" 2>&1
score3=$(grep -o 'correct=[0-9]*' "$d3/costs.txt" | head -1 | cut -d= -f2)
facts3=$(grep -o 'facts=[0-9]*' "$d3/driver.log" | tail -1 | cut -d= -f2)
echo "fixed-behavior: correct=$score3 facts=$facts3"
if [ "$score3" = "$score1" ] && [ "$facts3" = "$facts1" ]; then
  echo "FIX-VERIFIED: resume produces identical results to fresh run"
  echo "HARNESS-FIX-PASS"
else
  echo "FIX-FAILED: score=$score3 (expect $score1) facts=$facts3 (expect $facts1)"
  echo "HARNESS-FIX-FAIL"
fi

# Cleanup
rm -rf "$TESTBASE"
