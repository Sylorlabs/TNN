#!/bin/bash
# Phase 4 probe runner: 3 runs (2x plain + 1x MALLOC_PERTURB_=165), byte-identical required (K6).
# usage: run_probe.sh <probe-id>   (probe-id like s1, s2, ... r1 ...)
set -u
BIN=~/workspace/phase4/build/p4_bin
SEALED=~/workspace/phase4/sealed/probes
RTSEALED=~/workspace/phase4/redteam/probes
RES=~/workspace/phase4/results
mkdir -p "$RES"
P="$1"
if [ -f "$SEALED/$P.txt" ]; then SRC="$SEALED/$P.txt";
elif [ -f "$RTSEALED/$P.txt" ]; then SRC="$RTSEALED/$P.txt";
else echo "$P: no such probe"; exit 2; fi
"$BIN" "$SRC" > "$RES/$P.r1" || { echo "$P: run1 crashed"; exit 1; }
"$BIN" "$SRC" > "$RES/$P.r2" || { echo "$P: run2 crashed"; exit 1; }
MALLOC_PERTURB_=165 "$BIN" "$SRC" > "$RES/$P.r3" || { echo "$P: run3 crashed"; exit 1; }
h1=$(sha256sum "$RES/$P.r1" | cut -d' ' -f1)
h2=$(sha256sum "$RES/$P.r2" | cut -d' ' -f1)
h3=$(sha256sum "$RES/$P.r3" | cut -d' ' -f1)
if [ "$h1" = "$h2" ] && [ "$h2" = "$h3" ]; then
  cp "$RES/$P.r1" "$RES/$P.out"
  echo "$P DETERMINISM OK sha256=$h1"
else
  echo "$P DETERMINISM FAIL r1=$h1 r2=$h2 r3=$h3"
  exit 1
fi
