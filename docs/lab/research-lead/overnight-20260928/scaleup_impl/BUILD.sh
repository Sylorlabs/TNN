#!/bin/bash
# BUILD.sh -- Scale-Up Battery build.
# Compiles scaleup.zag into 9 binaries (mode 0 = Arm A, modes 1..8 = Arm B)
# by injecting the MODE constant at build time. Same source for all.
# Pure Zag. No Python.
set -e
ZNC=~/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc
HERE=~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/scaleup_impl
cd "$HERE"
mkdir -p build
for m in 0 1 2 3 4 5 6 7 8; do
  sed "s/MODE_PH/$m/" scaleup.zag > build/scaleup_m$m.zag
  "$ZNC" build/scaleup_m$m.zag -o build/scaleup_m$m 2>&1 | grep -v "warning: zagd" || true
done
echo "BUILD-DONE"
ls -la build/scaleup_m[0-8] | awk '{print $NF, $5}'
