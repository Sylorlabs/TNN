#!/bin/sh
# build_h7r.sh -- build the H7R sealed experiment binary. Pure shell, no Python.
# 1. extract the prototype substrate from the frozen substrate commit (read-only;
#    the frozen tnn2.zag is never modified)
# 2. append the H7R consumer (hypothesis, frozen spec) and the sealed driver
#    (worlds chosen post-freeze)
# 3. repoint main to h7r_main; compile with the pinned znc
set -e
export PATH="$HOME/safebin"
LANE=docs/lab/rsi/runs/wave-20261001-2321pdt/H7R
cd "$HOME/workspace/tnn-rsi"
git show a11dde4b9:docs/lab/rsi/runs/wave-20261001-2321pdt/TNN3-SUBSTRATE/substrate_proto.zag > "$LANE/substrate_proto.zag"
sha256sum "$LANE/substrate_proto.zag"
cp "$LANE/substrate_proto.zag" "$LANE/h7r_proto.zag"
cd "$LANE"
sed -i 's|return proto_main();|return h7r_main();|' h7r_proto.zag
grep -c "return h7r_main();" h7r_proto.zag
cat h7r_consumer.zag h7r_driver.zag >> h7r_proto.zag
wc -l h7r_proto.zag
"$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1" h7r_proto.zag -o h7r_proto 2>&1 | grep -vi "A0102\|zagd unavailable\|note:\|hint:\|-->" | head -5
ls -la h7r_proto
