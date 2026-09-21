#!/usr/bin/env bash
# Q2-SWE class-4 (arm D / index 4) leg: reps 0..4, bind x2 byte-identical,
# btrap D2 x2 byte-identical per rep. Run AFTER the corpus is frozen and
# committed. Source model for the corpus: swe-1-6-slow:free ONLY.
set -euo pipefail
D=~/workspace/tnn-lab/wave12/q2-distillation-swe
cd "$D/build"
python3 build_corpus_zag.py
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
"$ZNC" "$D/src/swe_trial.zag" --no-zagd --no-analyze --no-foreground-cache -o "$D/build/swe_bin"
mkdir -p "$D/evidence/logs"
for rep in 0 1 2 3 4; do
  for run in a b; do
    ./swe_bin bind "SWE4" 4 "$rep" 1 > "$D/evidence/logs/swe4_r${rep}_${run}.log" 2>&1
    ./swe_bin btrap "SWE4" 4 "$rep" > "$D/evidence/logs/swe4_btrap_r${rep}_${run}.log" 2>&1
  done
  # byte-identity of the two runs (full-file sha256)
  sa=$(sha256sum "$D/evidence/logs/swe4_r${rep}_a.log" | cut -d' ' -f1)
  sb=$(sha256sum "$D/evidence/logs/swe4_r${rep}_b.log" | cut -d' ' -f1)
  ta=$(sha256sum "$D/evidence/logs/swe4_btrap_r${rep}_a.log" | cut -d' ' -f1)
  tb=$(sha256sum "$D/evidence/logs/swe4_btrap_r${rep}_b.log" | cut -d' ' -f1)
  if [ "$sa" != "$sb" ]; then echo "MISMATCH bind rep $rep"; exit 1; fi
  if [ "$ta" != "$tb" ]; then echo "MISMATCH btrap rep $rep"; exit 1; fi
  echo "rep $rep: bind byte-identical ($sa), btrap byte-identical ($ta)"
done
echo "class-4 leg complete: 10 bind + 10 btrap logs"
