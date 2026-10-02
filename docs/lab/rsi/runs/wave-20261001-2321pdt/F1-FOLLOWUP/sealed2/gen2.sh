#!/bin/sh
# Part 2 sealed fixture generator (wave-20261001-2321pdt lane F1-FOLLOWUP).
# Generates 24 fresh sealed sum2 worlds (frozen seed series from
# PREREG_PART2 section 2) using the pure-Zag f1_wgen copy, whose
# byte-identical reproduction of F1 sealed fixtures was verified before
# any sealed generation. Pure shell + frozen wgen. No Python.
set -u
LDIR="$(cd "$(dirname "$0")/.." && pwd)"
WGEN="$LDIR/dev/f1_wgen"
S2="$LDIR/sealed2"
mkdir -p "$S2"

i=0
while [ $i -lt 24 ]; do
    ts=$((5100 + 2 * i))
    hs=$((5101 + 2 * i))
    "$WGEN" sum2 "$ts" 24 train "$S2/s2_train_$i.ep" > /dev/null || { echo "GEN FAIL train $i"; exit 1; }
    "$WGEN" sum2 "$hs" 30 hide "$S2/s2_hidden_$i.ep" > /dev/null || { echo "GEN FAIL hidden $i"; exit 1; }
    "$WGEN" sum2 "$hs" 30 truth "$S2/s2_truth_$i.ep" > /dev/null || { echo "GEN FAIL truth $i"; exit 1; }
    i=$((i + 1))
done
echo "generated 24 sealed worlds"
(cd "$S2" && sha256sum s2_train_*.ep s2_hidden_*.ep s2_truth_*.ep | sort > FIXTURE_SHA256.txt)
echo "wrote $S2/FIXTURE_SHA256.txt"
