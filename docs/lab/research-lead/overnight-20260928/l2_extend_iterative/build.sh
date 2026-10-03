#!/bin/sh
# build.sh -- assemble and compile the L2-EXTENDN-1 battery.
# Pure shell + pinned znc only.
set -e
D=docs/lab/research-lead/overnight-20260928/l2_extend_iterative
ZNC=src/tools/toolchain/znc_linux_x86_64_abed8aa1
cd "$HOME/workspace/tnn-rsi"
cat "$D/cc_base.zag" "$D/un_patch.zag" "$D/adapt_patch.zag" \
    "$D/extn_patch.zag" "$D/extn_driver.zag" > "$D/extn_full.zag"
"$ZNC" "$D/extn_full.zag" -o "$D/extn_bin" > "$D/extn_compile.txt" 2>&1
echo "compile exit: $?"
sha256sum "$D/extn_full.zag" "$D/extn_bin"
