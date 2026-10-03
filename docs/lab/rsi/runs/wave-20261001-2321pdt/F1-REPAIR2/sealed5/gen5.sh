#!/bin/sh
# Fresh sealed fixture generator (wave-20261001-2321pdt lane F1-REPAIR2).
# Generates 24 fresh sealed sum2 worlds on the frozen 7300-series
# (PREREG_REPAIR2.md section 5), using the read-only pure-Zag f1_wgen
# copy whose byte-identical reproduction of a reference fixture is
# verified before any sealed generation. Pure shell + frozen wgen.
# This script runs only after the PREREG_REPAIR2.md commit.
set -u
LDIR="$(cd "$(dirname "$0")/.." && pwd)"
WGEN="$LDIR/dev/f1_wgen"
S5="$LDIR/sealed5"
mkdir -p "$S5"

# byte-identical reproduction check against a committed reference fixture
# (F1-REPAIR sealed4 s4_train_0.ep, 6100-series train seed 6100)
REF="/tmp/r2_refcheck.ep"
"$WGEN" sum2 6100 24 train "$REF" > /dev/null || { echo "WGEN FAIL refcheck"; exit 1; }
if ! cmp -s "$REF" "$LDIR/dev/ref_s4_train_0.ep"; then echo "WGEN REPRODUCTION MISMATCH"; exit 1; fi
echo "wgen reproduction OK"
rm -f "$REF"

i=0
while [ $i -lt 24 ]; do
    ts=$((7300 + 2 * i))
    hs=$((7301 + 2 * i))
    "$WGEN" sum2 "$ts" 24 train "$S5/s5_train_$i.ep" > /dev/null || { echo "GEN FAIL train $i"; exit 1; }
    "$WGEN" sum2 "$hs" 30 hide "$S5/s5_hidden_$i.ep" > /dev/null || { echo "GEN FAIL hidden $i"; exit 1; }
    "$WGEN" sum2 "$hs" 30 truth "$S5/s5_truth_$i.ep" > /dev/null || { echo "GEN FAIL truth $i"; exit 1; }
    i=$((i + 1))
done
echo "generated 24 fresh sealed worlds (7300-series)"
(cd "$S5" && sha256sum s5_train_*.ep s5_hidden_*.ep s5_truth_*.ep | sort > FIXTURE_SHA256.txt)
echo "wrote $S5/FIXTURE_SHA256.txt"
