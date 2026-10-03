#!/bin/sh
# Fresh sealed fixture generator (wave-20261001-2321pdt lane F1-REPAIR).
# Generates 24 fresh sealed sum2 worlds on the frozen 6100-series
# (PREREG_REPAIR.md section 5), using the read-only pure-Zag f1_wgen
# copy whose byte-identical reproduction of a reference fixture was
# verified before any sealed generation. Pure shell + frozen wgen.
# This script runs only after the PREREG_REPAIR.md commit.
set -u
LDIR="$(cd "$(dirname "$0")/.." && pwd)"
WGEN="$LDIR/dev/f1_wgen"
S4="$LDIR/sealed4"
mkdir -p "$S4"

i=0
while [ $i -lt 24 ]; do
    ts=$((6100 + 2 * i))
    hs=$((6101 + 2 * i))
    "$WGEN" sum2 "$ts" 24 train "$S4/s4_train_$i.ep" > /dev/null || { echo "GEN FAIL train $i"; exit 1; }
    "$WGEN" sum2 "$hs" 30 hide "$S4/s4_hidden_$i.ep" > /dev/null || { echo "GEN FAIL hidden $i"; exit 1; }
    "$WGEN" sum2 "$hs" 30 truth "$S4/s4_truth_$i.ep" > /dev/null || { echo "GEN FAIL truth $i"; exit 1; }
    i=$((i + 1))
done
echo "generated 24 fresh sealed worlds (6100-series)"
(cd "$S4" && sha256sum s4_train_*.ep s4_hidden_*.ep s4_truth_*.ep | sort > FIXTURE_SHA256.txt)
echo "wrote $S4/FIXTURE_SHA256.txt"
