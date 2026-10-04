#!/bin/bash
# Assemble fusion4.zag from step-3 base + fz1-4 + v4a-e chunks, then compile.
# Uses its own directory (v5), not a hardcoded v4 path.
set -e
cd "$(dirname "$0")"
head -1582 composer_base.zag > fusion4.zag
cat chunks/fz1.zag chunks/fz2.zag chunks/fz3.zag chunks/fz4.zag >> fusion4.zag
cat chunks/v4a.zag chunks/v4b.zag chunks/v4c.zag chunks/v4d.zag chunks/v4e.zag >> fusion4.zag
cat main_tail.zag >> fusion4.zag
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 fusion4.zag -o fusion4_bin --no-analyze
echo "BUILD_OK"
