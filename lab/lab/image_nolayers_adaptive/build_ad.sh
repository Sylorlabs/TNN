#!/bin/bash
# build_ad.sh — build nlingest_ad + nlemit_ad for the no-layers adaptive-split fork
set -e
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
cd "$(dirname "$0")"
$ZNC nlingest_ad.zag -o nlingest_ad_bin 2>nlingest_ad_build.log || { echo "NLINGEST_AD BUILD FAILED"; tail -30 nlingest_ad_build.log; exit 1; }
$ZNC nlemit_ad.zag -o nlemit_ad_bin 2>nlemit_ad_build.log || { echo "NLEMIT_AD BUILD FAILED"; tail -30 nlemit_ad_build.log; exit 1; }
echo "build ok"
