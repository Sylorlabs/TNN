#!/bin/bash
# SWE-ENGLISH championship runner: build all three legs with the lab ZNC,
# then execute N=5 byte-identical runs per leg.
#
#   legA (class-4 Track-5): reps 0..4, bind + btrap, 5 runs each
#   legB (class-4 direct §B.7): 5 runs
#   legC (class-3 teacher): 5 runs
#
# Logs: legs/<leg>/evidence/logs/. Binaries: legs/<leg>/build/ (NOT committed).
# Usage: ./run_all.sh   (from swe/build; set SKIP_BUILD=1 to reuse binaries)
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
SWE="$(dirname "$HERE")"
ZNC="$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1"
export ZAG_CACHE_DIR="$SWE/build/.zag-cache-run"

echo "=== [1/4] generating swe_corpus.zag from the frozen corpus ==="
python3 "$HERE/build_corpus_zag.py" || exit 1

if [ "${SKIP_BUILD:-0}" != "1" ]; then
echo "=== [2/4] compiling legs with the lab ZNC ==="
for leg in legA legB legC; do
  mkdir -p "$SWE/legs/$leg/build"
done
( cd "$SWE/legs/legA/src" && "$ZNC" swe_trial.zag -o "$SWE/legs/legA/build/swe_trial" ) || exit 1
( cd "$SWE/legs/legB/src" && "$ZNC" swe_b7_direct.zag -o "$SWE/legs/legB/build/swe_b7_direct" ) || exit 1
( cd "$SWE/legs/legC/src" && "$ZNC" swe_teacher_leg.zag -o "$SWE/legs/legC/build/swe_teacher_leg" ) || exit 1
echo "builds OK"
fi

echo "=== [3/4] N=5 runs per leg (resumable: existing logs are kept) ==="
# legA: 5 reps x (bind + btrap) x 5 runs
for rep in 0 1 2 3 4; do
  for i in 1 2 3 4 5; do
    b="$SWE/legs/legA/evidence/logs/swe4_r${rep}_n${i}.log"
    t="$SWE/legs/legA/evidence/logs/swe4_btrap_r${rep}_n${i}.log"
    if [ ! -s "$b" ]; then
      "$SWE/legs/legA/build/swe_trial" bind SWE4 4 "$rep" 1 > "$b" 2>&1 || exit 1
    fi
    if [ ! -s "$t" ]; then
      "$SWE/legs/legA/build/swe_trial" btrap SWE4 4 "$rep" > "$t" 2>&1 || exit 1
    fi
  done
  echo "legA rep $rep: bind + btrap 5/5 done"
done
# legB: 5 runs
for i in 1 2 3 4 5; do
  f="$SWE/legs/legB/evidence/logs/flaw4_run${i}.log"
  if [ ! -s "$f" ]; then
    "$SWE/legs/legB/build/swe_b7_direct" > "$f" 2>&1 || exit 1
  fi
done
echo "legB: 5/5 done"
# legC: 5 runs
for i in 1 2 3 4 5; do
  f="$SWE/legs/legC/evidence/logs/teach3_run${i}.log"
  if [ ! -s "$f" ]; then
    "$SWE/legs/legC/build/swe_teacher_leg" > "$f" 2>&1 || exit 1
  fi
done
echo "legC: 5/5 done"

echo "=== [4/4] hashing evidence ==="
for leg in legA legB legC; do
  ( cd "$SWE/legs/$leg/evidence/logs" && sha256sum *.log > ../SHA256SUMS.txt )
done
echo "ALL RUNS COMPLETE"
