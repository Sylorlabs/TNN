#!/bin/bash
# WB verification runner: runs each cell twice (A/B), diffs results+ledgers.
# Usage: run_cell.sh <cellname> <items> <config>
set -u
D=~/workspace/tnn-lab/deliberation_depth/monotonicity/instrumentation
BIN=$D/src/wb_trace
CELL="$1"; ITEMS="$2"; CFG="$3"
LOG=$D/logs/${CELL}.log
{
echo "== $CELL A"
$BIN "$ITEMS" "$CFG" "$D/run/${CELL}_A.jsonl" "$D/run/${CELL}_A.ledger"
echo "== $CELL B"
$BIN "$ITEMS" "$CFG" "$D/run/${CELL}_B.jsonl" "$D/run/${CELL}_B.ledger"
if cmp -s "$D/run/${CELL}_A.jsonl" "$D/run/${CELL}_B.jsonl" && cmp -s "$D/run/${CELL}_A.ledger" "$D/run/${CELL}_B.ledger"; then
  echo "DETERMINISM-OK $CELL"
else
  echo "DETERMINISM-FAIL $CELL"
fi
} > "$LOG" 2>&1
cat "$LOG" | tail -2