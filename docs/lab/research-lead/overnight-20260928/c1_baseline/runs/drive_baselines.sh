#!/bin/bash
# drive_baselines.sh - run all 45 baseline runs (3 baselines x 5 worlds x 3 reps).
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
BASE="$HERE/.."
WORLDS="$BASE/../c1_clean/worlds"
OUT="$HERE"
for b in mem freq rand; do
  for w in w0 w1 w2 h0 h1; do
    for r in 1 2 3; do
      d="$OUT/${b}_${w}_r${r}"
      mkdir -p "$d"
      "$HERE/run_race.sh" "$WORLDS/$w" "$BASE/${b}_bin" "$d" > "$d/driver.log" 2>&1
      echo "done $b $w r$r: $(grep -h 'queries=' "$d/costs.txt" 2>/dev/null || tail -2 "$d/costs.txt" 2>/dev/null | head -1)"
    done
  done
done
echo ALL-DONE
