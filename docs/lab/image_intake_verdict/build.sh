#!/bin/bash
# build.sh — build the intake fidelity probe
set -e
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
cd "$(dirname "$0")"
$ZNC intake_probe.zag -o intake_probe 2>intake_probe_build.log || { echo "PROBE BUILD FAILED"; tail -30 intake_probe_build.log; exit 1; }
echo "build ok"
