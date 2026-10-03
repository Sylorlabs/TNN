#!/bin/sh
# BUILD.sh -- compile causal_revert.zag with the pinned znc toolchain.
# Usage: ./BUILD.sh   (run from the causal_revert/ directory)
set -e
ZNC=/home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc
if [ ! -x "$ZNC" ]; then
  echo "BUILD-FAIL: znc not found or not executable at $ZNC" >&2
  exit 1
fi
"$ZNC" build causal_revert.zag -o causal_revert_bin
chmod +x causal_revert_bin
echo "BUILD-OK causal_revert_bin"
