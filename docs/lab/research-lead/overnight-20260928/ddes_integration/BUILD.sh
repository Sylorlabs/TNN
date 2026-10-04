#!/bin/sh
# BUILD.sh -- build ddes_integ.zag with the pinned znc. Pure shell.
set -e
ZNC=/home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc
D=docs/lab/research-lead/overnight-20260928/ddes_integration
"$ZNC" "$D/ddes_integ.zag" -o "$D/ddes_integ_bin"
echo BUILD-OK
