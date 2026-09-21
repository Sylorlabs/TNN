#!/bin/bash
# TOGETHER pipeline shakedown + evidence runs.
# Usage: run_all.sh <binary> <outdir> [reps] [scale]
# Runs, per rep: teach (class-2 Track-5), b7c2 (class-2 §B.7),
# teacher (class-1 leg + student battery), btrap (class-2 traps).
# Each mode runs twice per rep; outputs are diffed for byte-identity.
set -u
BIN="$1"
OUT="$2"
REPS="${3:-5}"
SCALE="${4:-1}"
mkdir -p "$OUT"
FAIL=0
for rep in $(seq 0 $((REPS-1))); do
  for mode in teach b7c2 teacher btrap; do
    if [ "$mode" = "teach" ]; then
      args="$rep $SCALE"
    elif [ "$mode" = "btrap" ]; then
      args="$rep"
    else
      args=""
    fi
    # shellcheck disable=SC2086
    "$BIN" $mode $args > "$OUT/${mode}_r${rep}_a.log" 2>&1
    # shellcheck disable=SC2086
    "$BIN" $mode $args > "$OUT/${mode}_r${rep}_b.log" 2>&1
    if ! cmp -s "$OUT/${mode}_r${rep}_a.log" "$OUT/${mode}_r${rep}_b.log"; then
      echo "NONDET: $mode rep $rep"
      FAIL=1
    else
      echo "OK: $mode rep $rep (byte-identical)"
    fi
  done
done
# cross-rep determinism of the teacher selection
if [ "$REPS" -gt 1 ]; then
  if ! cmp -s "$OUT/teach_r0_a.log" "$OUT/teach_r1_a.log"; then
    echo "NOTE: teach rep0 != rep1 (expected: reps are identical seeds, should match)"
  else
    echo "OK: teach rep0 == rep1"
  fi
fi
exit $FAIL
