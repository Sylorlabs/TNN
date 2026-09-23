#!/bin/bash
# run_all.sh — TOGETHER ENGLISH championship canonical N=5 battery.
# Pure Zag, zero RNG. Every command runs 5 times; all 5 outputs must be
# byte-identical (cmp), else the battery FAILS.
#
# Legs (prereg):
#   teach rep 0..4 scale 1   (class-2 build + Track-5 scoring, 5 reps)
#   btrap rep 0..4           (class-2 learned-arm trap battery, 5 reps)
#   teach rep 0 scale 10     (S10 no-degradation leg)
#   b7c2                     (class-2 learner takes §B.7 as judging student)
#   teacher                  (class-1: TNN-teacher leg + student Track-5 battery)
set -u
cd "$(dirname "$0")/.."
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
BIN=build/bin/cc_en
LOGDIR=evidence/logs
mkdir -p "$LOGDIR" build/bin

echo "== building =="
"$ZNC" src/cc_driver.zag -o "$BIN" 2> "$LOGDIR/build.log"
if [ ! -x "$BIN" ]; then echo "BUILD FAILED"; tail -20 "$LOGDIR/build.log"; exit 1; fi
echo "build ok: $BIN"

FAIL=0
run5() { # run5 <tag> <cmd...>: run 5x, byte-compare all to run0
  local tag="$1"; shift
  echo "== $tag =="
  local k
  for k in 0 1 2 3 4; do
    "$BIN" "$@" > "$LOGDIR/${tag}_run${k}.txt" 2>&1
    local rc=$?
    if [ $rc -ne 0 ]; then echo "FAIL: $tag run$k exit=$rc"; FAIL=1; fi
  done
  for k in 1 2 3 4; do
    if ! cmp -s "$LOGDIR/${tag}_run0.txt" "$LOGDIR/${tag}_run${k}.txt"; then
      echo "FAIL: $tag run$k differs from run0 (not byte-identical)"
      FAIL=1
    fi
  done
  echo "ok: $tag (5/5 byte-identical)"
}

for r in 0 1 2 3 4; do run5 "teach_${r}_s1" teach "$r" 1; done
for r in 0 1 2 3 4; do run5 "btrap_${r}" btrap "$r"; done
run5 "teach_0_s10" teach 0 10
run5 "b7c2" b7c2
run5 "teacher" teacher

if [ $FAIL -ne 0 ]; then echo "BATTERY FAILED"; exit 1; fi
echo "BATTERY PASSED: all legs 5/5 byte-identical, all exit 0"
