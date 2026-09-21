#!/bin/bash
# Q2 LLM-distillation comparison — full run driver.
# Governed by prereg/PREREG_Q2_DISTILLATION.md (FROZEN 2026-09-21).
# Runs every (label, rep, scale) twice; verifies byte-identity; hashes logs.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
SRC="$HERE/src"
LOGDIR="$HERE/evidence/logs"
BIN="$HERE/build/q2t_bin"
ZNC="$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1"
mkdir -p "$LOGDIR" "$HERE/build"

echo "== building =="
"$ZNC" "$SRC/q2_trial.zag" --no-zagd --no-analyze --no-foreground-cache -o "$BIN" || exit 1

fail=0
run_twice() { # mode args... ; outfile base
  local base="$1"; shift
  "$BIN" "$@" > "$LOGDIR/${base}.run1.log" 2>&1; local e1=$?
  "$BIN" "$@" > "$LOGDIR/${base}.run2.log" 2>&1; local e2=$?
  if [ $e1 -ne 0 ] || [ $e2 -ne 0 ]; then
    echo "FAIL: $base exit codes $e1/$e2"; fail=1; return
  fi
  if ! cmp -s "$LOGDIR/${base}.run1.log" "$LOGDIR/${base}.run2.log"; then
    echo "FAIL: $base runs differ"; fail=1; return
  fi
  cp "$LOGDIR/${base}.run1.log" "$LOGDIR/${base}.log"
  rm "$LOGDIR/${base}.run2.log"
  echo "ok: $base (exit 0, byte-identical)"
}

echo "== binding leg: 12 reps x 2 arms x scale 1 (bind, twice each) =="
for rep in 0 1 2 3 4 5 6 7 8 9 10 11; do
  run_twice "bind_D1_rep${rep}_s1" bind D1 3 "$rep" 1
  run_twice "bind_D2_rep${rep}_s1" bind D2 4 "$rep" 1
done

echo "== trap batteries: 12 reps x 2 arms (btrap, twice each) =="
for rep in 0 1 2 3 4 5 6 7 8 9 10 11; do
  run_twice "btrap_D1_rep${rep}" btrap D1 3 "$rep"
  run_twice "btrap_D2_rep${rep}" btrap D2 4 "$rep"
done

echo "== S10 leg: 1 rep per arm, scale 10 (twice each) =="
run_twice "bind_D1_rep0_s10" bind D1 3 0 10
run_twice "bind_D2_rep0_s10" bind D2 4 0 10

echo "== hashing logs =="
(cd "$LOGDIR" && sha256sum *.log | sort > SHA256SUMS.txt)
cat "$LOGDIR/SHA256SUMS.txt"

if [ $fail -ne 0 ]; then echo "RUN FAILURES PRESENT"; exit 1; fi
echo "ALL RUNS OK"
