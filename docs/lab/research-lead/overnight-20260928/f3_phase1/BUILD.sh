#!/bin/sh
# BUILD.sh -- reproduce F3 Phase 1 R-A/R-B runs. Pure shell + znc.
# Worlds are concatenated from their committed frozen paths, unmodified.
set -e
ZNC=/home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc
D=$(dirname "$0")
cat "$D/f3_p1.zag" "$D/../autosci2/world_a2.zag" > "$D/run_p1a.zag"
cat "$D/f3_p1.zag" "$D/../autosci2/world_b2.zag" > "$D/run_p1b.zag"
$ZNC "$D/run_p1a.zag" -o "$D/bin_p1a"
$ZNC "$D/run_p1b.zag" -o "$D/bin_p1b"
"$D/bin_p1a" > "$D/raw_p1a.txt" 2> "$D/raw_p1a.err"
"$D/bin_p1b" > "$D/raw_p1b.txt" 2> "$D/raw_p1b.err"
echo "done"
