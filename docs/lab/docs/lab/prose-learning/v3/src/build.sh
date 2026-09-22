#!/bin/sh
# PROSE-LEARN3 build: pure Zag -> native binary. No RNG anywhere.
set -e
ZNC="$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1"
cd "$(dirname "$0")"
"$ZNC" prose_learn3.zag -o prose_learn3
