#!/bin/bash
# Re-test: rebuilt binary with T3/T6 instrument repairs.
# Every btrap cell (36) x2 runs + bind rep0 per arm x2. Byte-identity required.
set -u
HERE="$(cd "$(dirname "$0")/.." && pwd)"
BIN="$HERE/build/t5t_bin"
LOGDIR="$HERE/retest/logs"
REF="$HERE/evidence/logs"
fail=0
run_twice() { # base, args...
  local base="$1"; shift
  "$BIN" "$@" > "$LOGDIR/${base}.run1.log" 2>&1; local e1=$?
  "$BIN" "$@" > "$LOGDIR/${base}.run2.log" 2>&1; local e2=$?
  if [ $e1 -ne 0 ] || [ $e2 -ne 0 ]; then echo "FAIL(exit): $base $e1/$e2"; fail=1; return; fi
  if ! cmp -s "$LOGDIR/${base}.run1.log" "$LOGDIR/${base}.run2.log"; then
    echo "FAIL(nondet): $base"; fail=1; return
  fi
  mv "$LOGDIR/${base}.run1.log" "$LOGDIR/${base}.log"
  rm "$LOGDIR/${base}.run2.log"
  if [ -f "$REF/${base}.log" ]; then
    if cmp -s "$LOGDIR/${base}.log" "$REF/${base}.log"; then
      echo "ok: $base (deterministic, byte-identical to committed)"
    else
      echo "DIFFERS from committed: $base (score change? see below)"
    fi
  else
    echo "ok: $base (deterministic, no committed reference)"
  fi
}
for rep in 0 1 2 3 4 5 6 7 8 9 10 11; do
  run_twice "btrap_Z_rep${rep}" btrap Z 0 "$rep"
  run_twice "btrap_X_rep${rep}" btrap X 1 "$rep"
  run_twice "btrap_Y_rep${rep}" btrap Y 2 "$rep"
done
for L in Z X Y; do
  a=0; [ "$L" = X ] && a=1; [ "$L" = Y ] && a=2
  run_twice "bind_${L}_rep0_s1" bind "$L" "$a" 0 1
done
[ $fail -ne 0 ] && { echo "RETEST FAILURES"; exit 1; }
echo "RETEST COMPLETE: all deterministic"
