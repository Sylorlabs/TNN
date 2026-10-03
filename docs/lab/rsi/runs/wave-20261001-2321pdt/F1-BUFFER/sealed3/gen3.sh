#!/bin/sh
# Fresh sealed fixture generator (wave-20261001-2321pdt lane F1-BUFFER).
# Generates 24 fresh sealed sum2 worlds on the frozen 8100-series
# (PREREG_BUFFER.md section 4), using the read-only pure-Zag f1_wgen
# copy whose byte-identical reproduction of a reference fixture was
# verified before any sealed generation. Pure shell + frozen wgen.
# This script runs only after the PREREG_BUFFER.md commit.
set -u
LDIR="$(cd "$(dirname "$0")/.." && pwd)"
WGEN="$LDIR/dev/f1_wgen"
S3="$LDIR/sealed3"
mkdir -p "$S3"

i=0
while [ $i -lt 24 ]; do
    ts=$((8100 + 2 * i))
    hs=$((8101 + 2 * i))
    "$WGEN" sum2 "$ts" 24 train "$S3/s3_train_$i.ep" > /dev/null || { echo "GEN FAIL train $i"; exit 1; }
    "$WGEN" sum2 "$hs" 30 hide "$S3/s3_hidden_$i.ep" > /dev/null || { echo "GEN FAIL hidden $i"; exit 1; }
    "$WGEN" sum2 "$hs" 30 truth "$S3/s3_truth_$i.ep" > /dev/null || { echo "GEN FAIL truth $i"; exit 1; }
    i=$((i + 1))
done
echo "generated 24 fresh sealed worlds (8100-series)"
(cd "$S3" && sha256sum s3_train_*.ep s3_hidden_*.ep s3_truth_*.ep | sort > FIXTURE_SHA256.txt)
echo "wrote $S3/FIXTURE_SHA256.txt"
