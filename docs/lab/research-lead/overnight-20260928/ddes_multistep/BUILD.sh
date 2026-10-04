#!/bin/sh
# BUILD.sh -- build ddes_multistep.zag with the pinned znc. Pure shell.
set -e
ZNC=/home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc
D=docs/lab/research-lead/overnight-20260928/ddes_multistep
"$ZNC" "$D/ddes_multistep.zag" -o "$D/ddes_multistep_bin"
echo BUILD-OK
