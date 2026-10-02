#!/bin/bash
# BUILD.sh -- GENEXEC2-P build and conformance verification.
# Pure shell + znc. No Python anywhere.
set -u
ZNC=/home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc
D=docs/lab/research-lead/overnight-20260928/genexec2p
cd ~/workspace/tnn-rsi || exit 1
"$ZNC" "$D/genexec2p.zag" -o "$D/genexec2p_bin" || exit 1
"$D/genexec2p_bin" > "$D/PVM_RAW_1.txt" 2> "$D/PVM_RAW_1.err"
"$D/genexec2p_bin" > "$D/PVM_RAW_2.txt" 2> "$D/PVM_RAW_2.err"
"$D/genexec2p_bin" > "$D/PVM_RAW_3.txt" 2> "$D/PVM_RAW_3.err"
md5sum "$D/PVM_RAW_1.txt" "$D/PVM_RAW_2.txt" "$D/PVM_RAW_3.txt"
grep -E "^C[0-9] |^CONFORM" "$D/PVM_RAW_1.txt"
echo "BUILD_DONE"
