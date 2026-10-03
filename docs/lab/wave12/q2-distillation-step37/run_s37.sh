#!/bin/bash
# Q2-STEP37 championship team: full N=5 run driver.
# Governed by prereg/PREREG_Q2_DISTILLATION.md (FROZEN 2026-09-21).
# Every mode runs 5 times; all 5 must be byte-identical (else FAIL).
#   Class 4 Track-5: bind (D2 arm) + btrap, reps 0..4, scale 1
#   Class 4 §B.7:    flaw4, reps 0..4
#   Class 3:         teach3, reps 0..4
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
SRC="$HERE/src"
LOGDIR="$HERE/evidence/logs"
BINDIR="$HERE/build"
ZNC="$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1"
mkdir -p "$LOGDIR"

echo "== assembling driver =="
python3 "$HERE/build/build_driver.py" || exit 1
python3 "$HERE/build/build_corpus_zag.py" || exit 1

echo "== building =="
"$ZNC" "$SRC/s37_trial.zag" --no-zagd --no-analyze --no-foreground-cache -o "$BINDIR/s37t_bin" || exit 1
BIN="$BINDIR/s37t_bin"

fail=0
run_five() { # base ; mode args...
  local base="$1"; shift
  local i e
  for i in 1 2 3 4 5; do
    "$BIN" "$@" > "$LOGDIR/${base}.run${i}.log" 2>&1; e=$?
    if [ $e -ne 0 ]; then echo "FAIL: $base run$i exit $e"; fail=1; return; fi
  done
  for i in 2 3 4 5; do
    if ! cmp -s "$LOGDIR/${base}.run1.log" "$LOGDIR/${base}.run${i}.log"; then
      echo "FAIL: $base run1 vs run$i differ"; fail=1; return
    fi
  done
  cp "$LOGDIR/${base}.run1.log" "$LOGDIR/${base}.log"
  rm "$LOGDIR/${base}".run?.log
  echo "ok: $base (exit 0, 5/5 byte-identical)"
}

echo "== class 4 Track-5: bind D2 x5 reps =="
for rep in 0 1 2 3 4; do
  run_five "bind_D2_rep${rep}_s1" bind S37D2 4 "$rep" 1
done

echo "== class 4 Track-5: btrap D2 x5 reps =="
for rep in 0 1 2 3 4; do
  run_five "btrap_D2_rep${rep}" btrap S37D2 4 "$rep"
done

echo "== class 4 direct §B.7: flaw4 x5 reps =="
for rep in 0 1 2 3 4; do
  run_five "flaw4_rep${rep}" flaw4 S37C4 "$rep"
done

echo "== class 3: teach3 x5 reps =="
for rep in 0 1 2 3 4; do
  run_five "teach3_rep${rep}" teach3 S37C3 "$rep"
done

echo "== hashing logs =="
( cd "$LOGDIR" && sha256sum *.log > SHA256SUMS.txt )
echo "fail=$fail"
exit $fail
