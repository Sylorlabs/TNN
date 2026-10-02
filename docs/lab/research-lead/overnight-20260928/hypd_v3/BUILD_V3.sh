#!/bin/bash
# BUILD_V3.sh -- Hypothesis D v3: build three configurations.
# Pure shell + znc. No Python anywhere.
# The three configurations differ ONLY in the two V3MODE constant lines
# (frozen in PREREG_HYPD_V3.md section 3). The committed source is v3-both.
set -u
ZNC=/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1
D=docs/lab/research-lead/overnight-20260928/hypd_v3
cd ~/workspace/tnn-rsi || exit 1
# v3-both: SEL_MODE=1, CARRY_MODE=1 (committed source as-is)
"$ZNC" "$D/hyp_d_v3.zag" -o "$D/hyp_d_v3_bin" 2> "$D/build.err" || exit 1
# v3-selection-only: SEL_MODE=1, CARRY_MODE=0
sed 's/let CARRY_MODE:i32=1;/let CARRY_MODE:i32=0;/' "$D/hyp_d_v3.zag" > /tmp/hyp_d_v3_selonly.zag
grep -c "V3MODE-CARRY: 1=v3 seed pool, 0=v2 silent insert" /tmp/hyp_d_v3_selonly.zag
"$ZNC" /tmp/hyp_d_v3_selonly.zag -o "$D/hyp_d_v3_selonly_bin" 2>> "$D/build.err" || exit 1
# v3-carry-only: SEL_MODE=0, CARRY_MODE=1
sed 's/let SEL_MODE:i32=1;/let SEL_MODE:i32=0;/' "$D/hyp_d_v3.zag" > /tmp/hyp_d_v3_carryonly.zag
"$ZNC" /tmp/hyp_d_v3_carryonly.zag -o "$D/hyp_d_v3_carryonly_bin" 2>> "$D/build.err" || exit 1
echo "BUILD_DONE"
