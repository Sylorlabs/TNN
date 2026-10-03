#!/bin/bash
# Run v6_verify_active turn-by-turn on all worlds, 3 runs each.
# Usage: run_all.sh
# Pure shell. No Python.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
BIN="$HERE/v6va_bin"
WORLDS="$HERE/worlds"
for w in v1 v2 v3 v4 v5 v6 v7 ctl; do
  for run in 1 2 3; do
    sd="$HERE/run_${w}_${run}_state"
    rm -rf "$sd"; mkdir -p "$sd"
    out="$HERE/VOUT_${w}_${run}.txt"
    : > "$out"
    wdir="$WORLDS/$w"
    # Split turns.jsonl into per-turn files and run sequentially
    n=0
    while IFS= read -r line; do
      tf="$sd/turn_${n}.json"
      printf '%s\n' "$line" > "$tf"
      "$BIN" "$tf" "$sd" "$wdir" >> "$out" 2>"$sd/stderr_${n}.txt"
      n=$((n+1))
    done < "$wdir/turns.jsonl"
  done
done
echo "done"
