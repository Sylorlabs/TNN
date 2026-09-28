#!/bin/bash
# STEP-3.7-FLASH championship leg-C run driver (class-3 teacher leg).
# Compiles src/step_teacher_leg.zag, then N=5 byte-identical runs (no args).
# Logs to tnn/legC/evidence/logs/. Any divergence or nonzero exit -> FAIL.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
ZNC="$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1"
BLD="$HERE/build"
BIN="$BLD/step_teacher_leg_bin"
fail=0

mkdir -p "$BLD" "$HERE/evidence/logs"
echo "== compile step_teacher_leg.zag =="
(cd "$HERE/src" && "$ZNC" step_teacher_leg.zag -o "$BIN") || { echo "COMPILE FAIL"; exit 1; }

for n in 1 2 3 4 5; do
  "$BIN" > "$HERE/evidence/logs/stepc.run${n}.log" 2>&1
  e=$?
  if [ $e -ne 0 ]; then echo "FAIL: stepc run$n exit=$e"; fail=1; break; fi
  if [ "$n" -gt 1 ] && ! cmp -s "$HERE/evidence/logs/stepc.run1.log" "$HERE/evidence/logs/stepc.run${n}.log"; then
    echo "FAIL: stepc run$n differs from run1"; fail=1; break
  fi
done
if [ $fail -eq 0 ]; then
  cp "$HERE/evidence/logs/stepc.run1.log" "$HERE/evidence/logs/stepc.log"
  for n in 2 3 4 5; do rm "$HERE/evidence/logs/stepc.run${n}.log"; done
  echo "ok: stepc (exit 0, 5x byte-identical)"
fi
(cd "$HERE/evidence/logs" && sha256sum stepc.log | sort > SHA256SUMS.txt)
if [ $fail -ne 0 ]; then echo "RUN FAILURES PRESENT"; exit 1; fi
echo "ALL LEG-C RUNS OK"
