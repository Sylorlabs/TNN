#!/bin/bash
# build_promotion.sh — build the promoted intake path + retired controls
set -e
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
cd "$(dirname "$0")"
$ZNC intake.zag -o intake_bin 2>build_promotion.log || { echo "INTAKE BUILD FAILED"; tail -30 build_promotion.log; exit 1; }
$ZNC controls.zag -o controls_bin 2>>build_promotion.log || { echo "CONTROLS BUILD FAILED"; tail -30 build_promotion.log; exit 1; }
echo "build ok"
