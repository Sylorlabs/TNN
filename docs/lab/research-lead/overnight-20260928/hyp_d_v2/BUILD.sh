#!/bin/bash
# BUILD.sh -- D v2 K4-clean rerun: build and 3 deterministic runs.
# Pure shell + znc. No Python anywhere.
set -u
ZNC=/home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc
D=docs/lab/research-lead/overnight-20260928/hyp_d_v2
cd ~/workspace/tnn-rsi || exit 1
"$ZNC" "$D/hyp_d_v2.zag" -o "$D/hyp_d_v2_bin" || exit 1
"$D/hyp_d_v2_bin" > "$D/HYPD_V2_RAW_1.txt" 2> "$D/HYPD_V2_RAW_1.err"
"$D/hyp_d_v2_bin" > "$D/HYPD_V2_RAW_2.txt" 2> "$D/HYPD_V2_RAW_2.err"
"$D/hyp_d_v2_bin" > "$D/HYPD_V2_RAW_3.txt" 2> "$D/HYPD_V2_RAW_3.err"
md5sum "$D/HYPD_V2_RAW_1.txt" "$D/HYPD_V2_RAW_2.txt" "$D/HYPD_V2_RAW_3.txt"
grep -E "^TASK |^VM |^VERDICT |^TRICK_CHECK " "$D/HYPD_V2_RAW_1.txt"
echo "BUILD_DONE"
