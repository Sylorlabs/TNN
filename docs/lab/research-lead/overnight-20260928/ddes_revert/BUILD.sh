#!/bin/sh
# BUILD.sh -- compile ddes_revert.zag with the pinned znc toolchain.
# Usage: ./BUILD.sh   (run from the ddes_revert/ directory)
set -e
ZNC=/home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc
if [ ! -x "$ZNC" ]; then
  echo "BUILD-FAIL: znc not found or not executable at $ZNC" >&2
  exit 1
fi
"$ZNC" build ddes_revert.zag -o ddes_revert_bin
chmod +x ddes_revert_bin
echo "BUILD-OK ddes_revert_bin"
