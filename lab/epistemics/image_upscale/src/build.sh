#!/bin/bash
# Build the honest-upscale experiment (Micah order 2026-09-26 ~12:52 PDT).
# Pinned toolchain (same as the adaptive-layers fork).
set -e
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
cd "$(dirname "$0")"
"$ZNC" azprep.zag -o azprep_bin
"$ZNC" azupscale.zag -o azupscale_bin
"$ZNC" azoutpaint.zag -o azoutpaint_bin
echo "build ok"
