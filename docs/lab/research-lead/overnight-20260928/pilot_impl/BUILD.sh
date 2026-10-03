#!/bin/bash
# BUILD.sh -- H-NEW-3 pilot build.
# Compiles pilot.zag into 6 binaries (mode 0 = Arm A, modes 1..5 = Arm B)
# by injecting the MODE constant at build time. Same source for all.
# Pure Zag. No Python.
set -e
ZNC=~/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc
HERE=~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/pilot_impl
cd "$HERE"
mkdir -p build
for m in 0 1 2 3 4 5; do
  sed "s/MODE_PH/$m/" pilot.zag > build/pilot_m$m.zag
  "$ZNC" build/pilot_m$m.zag -o build/pilot_m$m 2>&1 | grep -v "warning: zagd" || true
done
echo "BUILD-DONE"
ls -la build/pilot_m[0-5] | awk '{print $NF, $5}'
