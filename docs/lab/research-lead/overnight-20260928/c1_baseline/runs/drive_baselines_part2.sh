#!/bin/bash
# drive_baselines_part2.sh - remaining runs: freq h1 x3, rand x15.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
BASE="$HERE/.."
WORLDS="$BASE/../c1_clean/worlds"
OUT="$HERE"
for r in 1 2 3; do
  d="$OUT/freq_h1_r${r}"
  mkdir -p "$d"
  "$HERE/run_race.sh" "$WORLDS/h1" "$BASE/freq_bin" "$d" > "$d/driver.log" 2>&1
  echo "done freq h1 r$r"
done
for w in w0 w1 w2 h0 h1; do
  for r in 1 2 3; do
    d="$OUT/rand_${w}_r${r}"
    mkdir -p "$d"
    "$HERE/run_race.sh" "$WORLDS/$w" "$BASE/rand_bin" "$d" > "$d/driver.log" 2>&1
    echo "done rand $w r$r"
  done
done
echo ALL-DONE
