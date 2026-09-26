#!/bin/bash
# build.sh — build nlingest + nlemit for the no-layers fork
set -e
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
cd "$(dirname "$0")"
$ZNC nlingest.zag -o nlingest_bin 2>nlingest_build.log || { echo "NLINGEST BUILD FAILED"; tail -30 nlingest_build.log; exit 1; }
$ZNC nlemit.zag -o nlemit_bin 2>nlemit_build.log || { echo "NLEMIT BUILD FAILED"; tail -30 nlemit_build.log; exit 1; }
echo "build ok"
