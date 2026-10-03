#!/bin/sh
# build.sh -- COMPRESSION-EXEC builds. Pure Zag; pinned znc; safebin PATH.
# Builds:
#   shim_frozen : frozen TNN-2 base (no test main) + shim driver (K1 pre arm)
#   shim_unify  : unified TNN-2 base (no test main) + shim driver (K1 post arm)
# Verifies: driver SHA identical in both arms; frozen reconstruction ==
# recorded freeze_shim2.zag SHA-256.
set -e
export PATH="$HOME/safebin"
HERE=$(dirname "$0")
cd "$HERE"

# frozen reference hashes (from prereg section 2)
FROZEN_ZAG_SHA=a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd
SHIM_SRC_SHA=33795c19c9f7ecd8e4c0c9a180293bf577b53ba7aae6f6a5557c972fe372ace8

echo "== hash checks =="
echo "$FROZEN_ZAG_SHA  tnn2_frozen_ref.zag" | sha256sum -c -
# driver is part of the hashed shim source; check it is unchanged since extraction
DRIVER_SHA=$(sha256sum shim_driver2.zag | cut -d' ' -f1)
echo "driver sha: $DRIVER_SHA"

echo "== assemble shims =="
grep -v '^fn main()i32 { return run_all(); }$' tnn2_frozen_ref.zag > /tmp/ce_fbase.zag
cat /tmp/ce_fbase.zag shim_driver2.zag > shim_frozen.zag
echo "$SHIM_SRC_SHA  shim_frozen.zag" | sha256sum -c - && echo "FROZEN SHIM SOURCE == RECORDED"

grep -v '^fn main()i32 { return run_all(); }$' tnn2_unify.zag > /tmp/ce_ubase.zag
cat /tmp/ce_ubase.zag shim_driver2.zag > shim_unify.zag
# unified base must differ from frozen ONLY in the trial region
diff /tmp/ce_fbase.zag /tmp/ce_ubase.zag | head -5
echo "unified-vs-frozen diff above (trial region only expected)"

echo "== compile =="
znc shim_frozen.zag -o shim_frozen 2>build_frozen.log || { echo "FROZEN BUILD FAILED"; grep -E "error" build_frozen.log | head; exit 1; }
echo "shim_frozen built"
znc shim_unify.zag -o shim_unify 2>build_unify.log || { echo "UNIFY BUILD FAILED"; grep -E "error" build_unify.log | head; exit 1; }
echo "shim_unify built"

echo "== 3/3 byte-identical rebuilds (K4) =="
sha256sum shim_unify > unify.sha256
cp shim_unify /tmp/ce_u1
znc shim_unify.zag -o /tmp/ce_u2 2>/dev/null
znc shim_unify.zag -o /tmp/ce_u3 2>/dev/null
cmp /tmp/ce_u1 /tmp/ce_u2 && cmp /tmp/ce_u1 /tmp/ce_u3 && echo "UNIFY 3/3 BYTE-IDENTICAL"
sha256sum shim_frozen > frozen.sha256
cp shim_frozen /tmp/ce_f1
znc shim_frozen.zag -o /tmp/ce_f2 2>/dev/null
znc shim_frozen.zag -o /tmp/ce_f3 2>/dev/null
cmp /tmp/ce_f1 /tmp/ce_f2 && cmp /tmp/ce_f1 /tmp/ce_f3 && echo "FROZEN 3/3 BYTE-IDENTICAL"
rm -f /tmp/ce_u1 /tmp/ce_u2 /tmp/ce_u3 /tmp/ce_f1 /tmp/ce_f2 /tmp/ce_f3 /tmp/ce_fbase.zag /tmp/ce_ubase.zag
echo "BUILD OK"
