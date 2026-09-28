#!/bin/bash
# build.sh — build tlingest + tlemit for the TNN-chooses-its-layers fork
set -e
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
cd "$(dirname "$0")"
$ZNC tlingest.zag -o tlingest_bin 2>tlingest_build.log || { echo "TLINGEST BUILD FAILED"; tail -40 tlingest_build.log; exit 1; }
$ZNC tlemit.zag -o tlemit_bin 2>tlemit_build.log || { echo "TLEMIT BUILD FAILED"; tail -40 tlemit_build.log; exit 1; }
echo "build ok"
