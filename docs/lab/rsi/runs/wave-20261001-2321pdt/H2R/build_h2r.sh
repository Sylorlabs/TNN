#!/bin/sh
# build_h2r.sh -- deterministic build of the H2R experiment harness.
# Pure shell. No Python.
# Usage: sh build_h2r.sh [practice|sealed]
#   practice: build with practice_worlds.zag (implementation testing only)
#   sealed:   build with worlds_sealed.zag (the sealed evaluation)
# Steps:
#   1. copy the extracted prototype substrate (never modified) to h2r_full.zag
#   2. swap the dev-harness main entry proto_main -> h2r_main (mechanical)
#   3. append h2r_impl.zag (the H2R learner + driver) and the worlds file
#   4. compile with the pinned znc
set -e
export PATH="$HOME/safebin"
LANE=docs/lab/rsi/runs/wave-20261001-2321pdt/H2R
cd "$HOME/workspace/tnn-rsi"
MODE="${1:-practice}"
if [ "$MODE" = "sealed" ]; then
  WORLDS="$LANE/worlds_sealed.zag"
  OUT="$LANE/h2r_sealed"
else
  WORLDS="$LANE/practice_worlds.zag"
  OUT="$LANE/h2r_practice"
fi
cp "$LANE/substrate_proto.zag" "$LANE/h2r_full.zag"
# mechanical main swap (the prototype's own dev entry -> the H2R driver)
sed -i 's|fn main()i32 { return proto_main(); }|fn main()i32 { return h2r_main(); }|' "$LANE/h2r_full.zag"
grep -c "return h2r_main()" "$LANE/h2r_full.zag"
cat "$LANE/h2r_impl.zag" "$WORLDS" >> "$LANE/h2r_full.zag"
wc -l "$LANE/h2r_full.zag"
"$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1" "$LANE/h2r_full.zag" -o "$OUT" 2>&1 | grep -v "warning\[A0102\]\|--> \|= note\|= hint\|^$\|zagd unavailable" | head -10
ls -la "$OUT"
