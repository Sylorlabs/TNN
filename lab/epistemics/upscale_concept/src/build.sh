#!/bin/bash
set -e
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
"$ZNC" uprobe.zag -o uprobe_bin
echo "build ok"
