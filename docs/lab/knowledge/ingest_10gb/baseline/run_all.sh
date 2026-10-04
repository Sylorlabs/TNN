#!/bin/bash
# Phase 1A baseline runner (glue). Runs each battery twice; all pairs must be byte-identical.
# Usage: run_all.sh   (run from the baseline dir)
set -u
BASE="$(cd "$(dirname "$0")" && pwd)"
BIN="$HOME/workspace/tnn-lab/dialogue/dialogue_bin"
DIAL="$HOME/workspace/tnn-lab/dialogue"
RUNS="$BASE/runs"
mkdir -p "$RUNS"

want_bin="912c809e0d8206f5ceb096d79a54e735337180f5dccc8bded6f1d25a7c023bd5"
got_bin="$(sha256sum "$BIN" | cut -d' ' -f1)"
[ "$got_bin" = "$want_bin" ] || { echo "BINARY MISMATCH: $got_bin"; exit 1; }
echo "binary OK: $got_bin"

run_battery () {  # name battery_src
  local name="$1" src="$2"
  for rep in 1 2; do
    d="$RUNS/${name}_rep${rep}"
    rm -rf "$d"; mkdir -p "$d"
    cp "$DIAL/kb.txt" "$DIAL/gaz.txt" "$d/"
    cp "$src" "$d/battery.txt"
    ( cd "$d" && "$BIN" > "output.log" 2> "stderr.log" )
    echo "ran $name rep$rep: $(wc -c < "$d/output.log") bytes"
  done
  if cmp -s "$RUNS/${name}_rep1/output.log" "$RUNS/${name}_rep2/output.log"; then
    echo "DETERMINISM OK: $name rep1 == rep2"
    sha256sum "$RUNS/${name}_rep1/output.log"
  else
    echo "DETERMINISM FAILED: $name rep1 != rep2 — RUN INVALID"
    exit 1
  fi
}

run_battery dialogue "$BASE/DIALOGUE_BATTERY.txt"
run_battery knowledge "$BASE/batteries/knowledge_battery.txt"
run_battery reasoning "$BASE/batteries/reasoning_battery.txt"
echo "ALL RUNS COMPLETE AND BYTE-IDENTICAL"
