#!/bin/sh
# build.sh -- assemble and compile the L2-EXTENDN-2 battery.
# Pure shell + pinned znc only.
set -e
D=docs/lab/research-lead/overnight-20260928/l2_extendn2_revision
ZNC=src/tools/toolchain/znc_linux_x86_64_abed8aa1
cd "$HOME/workspace/tnn-rsi"
cat "$D/cc_base.zag" "$D/un_patch.zag" "$D/adapt_patch.zag" \
    "$D/rv_patch.zag" "$D/rv_driver.zag" > "$D/rv_full.zag"
"$ZNC" "$D/rv_full.zag" -o "$D/rv_bin" > "$D/rv_compile.txt" 2>&1
echo "compile exit: $?"
sha256sum "$D/rv_full.zag" "$D/rv_bin"
