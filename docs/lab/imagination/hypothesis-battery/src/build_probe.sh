#!/bin/bash
# Assemble probe_bin from step-5 chunks + probe tail (own main).
set -e
cd "$(dirname "$0")"
head -1582 composer_base.zag > probe_full.zag
cat chunks/fz1.zag chunks/fz2.zag chunks/fz3.zag chunks/fz4.zag >> probe_full.zag
cat chunks/v4a.zag chunks/v4b.zag chunks/v4c.zag chunks/v4d.zag chunks/v4e.zag >> probe_full.zag
cat probe.zag >> probe_full.zag
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 probe_full.zag -o probe_bin --no-analyze
echo "BUILD_OK"
