#!/bin/bash
# GROK leg-B run driver: class-4 direct §B.7 leg, N=5 byte-identical.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
LEGB="$HERE"
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
fail=0

BIN="$LEGB/build/grokb7"
mkdir -p "$LEGB/build" "$LEGB/evidence/logs"
(cd "$LEGB/src" && "$ZNC" -o "$BIN" grok_b7_direct.zag) || { echo "BUILD FAIL"; exit 1; }
echo "built $BIN"

for n in 1 2 3 4 5; do
  "$BIN" > "$LEGB/evidence/logs/b7_direct.run${n}.log" 2>&1
  e=$?
  if [ $e -ne 0 ]; then echo "FAIL: b7_direct run$n exit=$e"; fail=1; break; fi
  if [ "$n" -gt 1 ] && ! cmp -s "$LEGB/evidence/logs/b7_direct.run1.log" "$LEGB/evidence/logs/b7_direct.run${n}.log"; then
    echo "FAIL: b7_direct run$n differs from run1"; fail=1; break
  fi
done
if [ $fail -eq 0 ]; then
  cp "$LEGB/evidence/logs/b7_direct.run1.log" "$LEGB/evidence/logs/b7_direct.log"
  for n in 2 3 4 5; do rm "$LEGB/evidence/logs/b7_direct.run${n}.log"; done
  echo "ok: b7_direct (exit 0, 5x byte-identical)"
fi
(cd "$LEGB/evidence/logs" && sha256sum *.log 2>/dev/null | sort > SHA256SUMS.txt)
[ $fail -ne 0 ] && { echo "RUN FAILURES PRESENT"; exit 1; }
echo "ALL LEG-B RUNS OK"
