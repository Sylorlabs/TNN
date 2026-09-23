#!/bin/bash
# GROK leg-C run driver: class-3 TNN-teacher leg, N=5 byte-identical.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
LEGC="$HERE"
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
fail=0

BIN="$LEGC/build/grokt44"
mkdir -p "$LEGC/build" "$LEGC/evidence/logs"
(cd "$LEGC/src" && "$ZNC" -o "$BIN" grok_teacher_leg.zag) || { echo "BUILD FAIL"; exit 1; }
echo "built $BIN"

for n in 1 2 3 4 5; do
  "$BIN" > "$LEGC/evidence/logs/teacher_leg.run${n}.log" 2>&1
  e=$?
  if [ $e -ne 0 ]; then echo "FAIL: teacher_leg run$n exit=$e"; fail=1; break; fi
  if [ "$n" -gt 1 ] && ! cmp -s "$LEGC/evidence/logs/teacher_leg.run1.log" "$LEGC/evidence/logs/teacher_leg.run${n}.log"; then
    echo "FAIL: teacher_leg run$n differs from run1"; fail=1; break
  fi
done
if [ $fail -eq 0 ]; then
  cp "$LEGC/evidence/logs/teacher_leg.run1.log" "$LEGC/evidence/logs/teacher_leg.log"
  for n in 2 3 4 5; do rm "$LEGC/evidence/logs/teacher_leg.run${n}.log"; done
  echo "ok: teacher_leg (exit 0, 5x byte-identical)"
fi
(cd "$LEGC/evidence/logs" && sha256sum *.log 2>/dev/null | sort > SHA256SUMS.txt)
[ $fail -ne 0 ] && { echo "RUN FAILURES PRESENT"; exit 1; }
echo "ALL LEG-C RUNS OK"
