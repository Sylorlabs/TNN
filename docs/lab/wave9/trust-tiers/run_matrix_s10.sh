#!/bin/bash
# Wave 9 trust-tiers S10 horizon stretch (conditional per prereg V2 §11).
# ONLY RUN if S1 completed with zero divergences / zero INVALID findings.
# Matrix: arms {T,N} x campaigns {A1..A6} x variant {0} x instance {00} x runs {0,1} x SCALE=10
# = 24 executions. Excludes A0, A1-MS, N0 per §11.
set -u
SUB="$HOME/workspace/tnn-lab/wave9/trust-tiers/substrate"
BIN="$SUB/trust_tiers.bin"
EV="$HOME/workspace/tnn-lab/wave9/trust-tiers/evidence/s10"
mkdir -p "$EV"
MANIFEST="$EV/cells.sha256"
: > "$MANIFEST"

[ -x "$BIN" ] || { echo "BINARY MISSING"; exit 2; }

total_runs=0
total_cells=0
divergences=0

for arm in T N; do
  for camp in A1 A2 A3 A4 A5 A6; do
    var=0
    inst=00
    base="${arm}_${camp}_${var}_${inst}_10"
    sel0="${arm}_${camp}_${var}_${inst}_0_10"
    sel1="${arm}_${camp}_${var}_${inst}_1_10"
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
      echo "DIVERGENCE cell=$base"
      echo "DIVERGENCE cell=$base sha0=$h0 sha1=$h1" >> "$EV/DIVERGENCES.txt"
      echo "STOPPING S10: determinism failure"
      exit 3
    fi
    sha256sum "$f0" "$f1" >> "$MANIFEST"
    total_cells=$((total_cells+1))
    echo "done $base (divergences=$divergences)"
  done
done

echo "== S10 stretch complete =="
echo "cells=$total_cells runs=$total_runs divergences=$divergences"
