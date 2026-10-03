#!/bin/bash
# Build the loop learner binary. Run from the loop/ directory.
set -e
ZNC=/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
mkdir -p work
"$ZNC" learner.zag -o work/learner --no-analyze --no-zagd
./work/learner gate "smoke test" | head -1
