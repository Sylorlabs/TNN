#!/bin/sh
# build.sh -- assemble and compile the L2-COMBINED battery.
# Pure shell + pinned znc only. No Python.
set -e
D=docs/lab/research-lead/overnight-20260928/l2_combined
ZNC=src/tools/toolchain/znc_linux_x86_64_abed8aa1
cd "$HOME/workspace/tnn-rsi"
cat "$D/cc_base.zag" "$D/un_patch.zag" "$D/adapt_patch.zag" \
    "$D/extn_patch.zag" "$D/l2c_patch.zag" "$D/l2c_driver.zag" > "$D/l2c_full.zag"
"$ZNC" "$D/l2c_full.zag" -o "$D/l2c_bin" > "$D/l2c_compile.txt" 2>&1
echo "compile exit: $?"
sha256sum "$D/l2c_full.zag" "$D/l2c_bin"
