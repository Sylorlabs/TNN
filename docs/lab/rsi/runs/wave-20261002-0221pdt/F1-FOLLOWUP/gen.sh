#!/bin/sh
# Sealed fixture generation (F1-FOLLOWUP, wave-20261002-0221pdt).
# Generates 40 fresh sealed sum2 worlds with the frozen 53xx seed series
# from PREREG_F1FOLLOWUP.md section 3, using this lane's pure-Zag f1_wgen
# copy (byte-identical reproduction of prior Part 2 fixtures verified
# before any sealed generation). Pure shell + frozen wgen. No Python.
set -u
LDIR="$(cd "$(dirname "$0")" && pwd)"
WGEN="$LDIR/dev/f1_wgen"
S="$LDIR/sealed"
mkdir -p "$S"

i=0
while [ $i -lt 40 ]; do
    ts=$((5300 + 2 * i))
    hs=$((5301 + 2 * i))
    "$WGEN" sum2 "$ts" 24 train "$S/s3_train_$i.ep" > /dev/null || { echo "GEN FAIL train $i"; exit 1; }
    "$WGEN" sum2 "$hs" 30 hide "$S/s3_hidden_$i.ep" > /dev/null || { echo "GEN FAIL hidden $i"; exit 1; }
    "$WGEN" sum2 "$hs" 30 truth "$S/s3_truth_$i.ep" > /dev/null || { echo "GEN FAIL truth $i"; exit 1; }
    i=$((i + 1))
done
echo "generated 40 sealed worlds"
(cd "$S" && sha256sum s3_train_*.ep s3_hidden_*.ep s3_truth_*.ep | sort > FIXTURE_SHA256.txt)
echo "wrote $S/FIXTURE_SHA256.txt"
