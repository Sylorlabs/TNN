#!/bin/bash
# Wave 9 trust-tiers S1 full matrix runner (RUN worker, 2026-09-20).
# Writes evidence/s1/{CELL}.run0.log / .run1.log + cells.sha256 manifest.
# CELL = {ARM}_{CAMP}_{VARIANT}_{INSTANCE}_{SCALE} (base); .run0/.run1 suffix = RUN value.
# On any paired-run divergence: records DIVERGENCE and STOPS (INVALID per prereg §8).
set -u
SUB="$HOME/workspace/tnn-lab/wave9/trust-tiers/substrate"
BIN="$SUB/trust_tiers.bin"
EV="$HOME/workspace/tnn-lab/wave9/trust-tiers/evidence/s1"
mkdir -p "$EV"
MANIFEST="$EV/cells.sha256"
: > "$MANIFEST"

[ -x "$BIN" ] || { echo "BINARY MISSING"; exit 2; }

total_runs=0
total_cells=0
divergences=0
declare -A per_arm_camp

for arm in T N B; do
  for camp in A0 A1 A2 A3 A4 A5 A6 N0; do
    # A0 is arm-T only per amended prereg §3
    if [ "$camp" = "A0" ] && [ "$arm" != "T" ]; then continue; fi
    for var in 0 1 2; do
      for inst in 00 01 02 03 04 05 06 07 08 09 10 11; do
        base="${arm}_${camp}_${var}_${inst}_1"
        sel0="${arm}_${camp}_${var}_${inst}_0_1"
        sel1="${arm}_${camp}_${var}_${inst}_1_1"
        f0="$EV/${base}.run0.log"
        f1="$EV/${base}.run1.log"
        if ! "$BIN" "$sel0" > "$f0" 2> "$EV/${base}.run0.err"; then
          echo "RCFAIL cell=$sel0 rc=$? (evidence preserved at $f0)"; exit 2
        fi
        if ! "$BIN" "$sel1" > "$f1" 2> "$EV/${base}.run1.err"; then
          echo "RCFAIL cell=$sel1 rc=$? (evidence preserved at $f1)"; exit 2
        fi
        total_runs=$((total_runs+2))
        h0=$(sha256sum "$f0" | cut -d' ' -f1)
        h1=$(sha256sum "$f1" | cut -d' ' -f1)
        if [ "$h0" != "$h1" ]; then
          divergences=$((divergences+1))
          echo "DIVERGENCE cell=$base (selectors $sel0 / $sel1)"
          echo "DIVERGENCE cell=$base sha0=$h0 sha1=$h1" >> "$EV/DIVERGENCES.txt"
          total_cells=$((total_cells+1))
          echo "STOPPING MATRIX: determinism failure (INVALID per prereg §8)"
          exit 3
        fi
        sha256sum "$f0" "$f1" >> "$MANIFEST"
        total_cells=$((total_cells+1))
        key="${arm}/${camp}"
        per_arm_camp[$key]=$(( ${per_arm_camp[$key]:-0} + 1 ))
        if [ $((total_cells % 100)) -eq 0 ]; then
          echo "progress: $total_cells cells, $total_runs runs, divergences=$divergences"
        fi
      done
    done
  done
done

echo "== S1 matrix complete =="
echo "cells=$total_cells runs=$total_runs divergences=$divergences"
echo "--- per (arm,camp) ---"
for key in $(echo "${!per_arm_camp[@]}" | tr ' ' '\n' | sort); do
  echo "$key cells=${per_arm_camp[$key]}"
done
