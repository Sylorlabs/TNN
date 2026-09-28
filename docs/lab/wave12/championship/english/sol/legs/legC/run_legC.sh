#!/bin/bash
# SOL leg-C run driver: class-3 teacher leg (teacher_id=40).
# N=5 byte-identical runs; any divergence or nonzero exit -> FAIL.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
BIN="$HERE/build/sol_teacher_leg_bin"
fail=0
mkdir -p "$HERE/evidence/logs"
for n in 1 2 3 4 5; do
  "$BIN" > "$HERE/evidence/logs/teacher_leg.run${n}.log" 2>&1
  e=$?
  if [ $e -ne 0 ]; then echo "FAIL: teacher_leg run$n exit=$e"; fail=1; break; fi
  if [ "$n" -gt 1 ] && ! cmp -s "$HERE/evidence/logs/teacher_leg.run1.log" "$HERE/evidence/logs/teacher_leg.run${n}.log"; then
    echo "FAIL: teacher_leg run$n differs from run1"; fail=1; break
  fi
done
if [ $fail -eq 0 ]; then
  cp "$HERE/evidence/logs/teacher_leg.run1.log" "$HERE/evidence/logs/teacher_leg.log"
  for n in 2 3 4 5; do rm "$HERE/evidence/logs/teacher_leg.run${n}.log"; done
  echo "ok: teacher_leg (exit 0, 5x byte-identical)"
fi
(cd "$HERE/evidence/logs" && sha256sum *.log 2>/dev/null | sort > SHA256SUMS.txt)
if [ $fail -ne 0 ]; then echo "RUN FAILURES PRESENT"; exit 1; fi
echo "ALL RUNS OK"
