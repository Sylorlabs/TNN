#!/bin/sh
# BUILD.sh -- reproduce F3 Phase 2 T-DISJ runs. Pure shell + znc.
# World concatenated from its committed frozen path, unmodified.
set -e
ZNC=/home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc
D=$(dirname "$0")
cat "$D/f3_p2.zag" "$D/../f2_ood/world_ood4.zag" > "$D/run_p2.zag"
$ZNC "$D/run_p2.zag" -o "$D/bin_p2"
"$D/bin_p2" > "$D/raw_p2_r1.txt" 2> "$D/raw_p2_r1.err"
"$D/bin_p2" > "$D/raw_p2_r2.txt" 2> "$D/raw_p2_r2.err"
"$D/bin_p2" > "$D/raw_p2_r3.txt" 2> "$D/raw_p2_r3.err"
echo "done"
