#!/bin/sh
# gen.sh - generate the 40 sealed fixtures (55xx series) for the F1
# seed-sensitivity finding lane, wave-20261002-0521pdt.
# Frozen fixture design: PREREG_SEEDSENS.md section 3.
# Pure shell + the pinned-znc-compiled f1_wgen. No Python.
set -u
LDIR="$(cd "$(dirname "$0")" && pwd)"
WGEN="$LDIR/dev/f1_wgen"
S5="$LDIR/sealed5"
mkdir -p "$S5"

i=0
while [ $i -lt 40 ]; do
    ts=$((5500 + 2 * i))
    hs=$((5501 + 2 * i))
    "$WGEN" sum2 "$ts" 24 train "$S5/s5_train_$i.ep" > /dev/null || { echo "GEN FAIL train $i"; exit 1; }
    "$WGEN" sum2 "$hs" 30 hide "$S5/s5_hidden_$i.ep" > /dev/null || { echo "GEN FAIL hidden $i"; exit 1; }
    "$WGEN" sum2 "$hs" 30 truth "$S5/s5_truth_$i.ep" > /dev/null || { echo "GEN FAIL truth $i"; exit 1; }
    i=$((i + 1))
done
echo "generated 40 sealed worlds (55xx series)"
(cd "$S5" && sha256sum s5_train_*.ep s5_hidden_*.ep s5_truth_*.ep | sort > FIXTURE_SHA256.txt)
echo "wrote $S5/FIXTURE_SHA256.txt"
