#!/bin/sh
# build_g.sh -- build guarded variants for the XIO-DEPHYGIENE red team.
# G1: attack binaries with each guard in place.
# G2: C308 K-arm binaries (dephy_full, dephy_c229, dephy_c235) against
#     each guarded core/base, for byte-identity comparison with the
#     committed C308 baselines.
# Shell only: extraction, hashing, concatenation, pinned znc invocation.
# No research logic. Fails loudly on any verification mismatch.
set -u
LANE=$(dirname "$0")
ADAPT="$LANE/../xio_adapters"
HARDER="$LANE/../xio_harder"
DEPH="$LANE/../xio_dephygiene"
ZNC="$HOME/safebin/znc"
# SHA pins are read from build_rt.sh (single source of truth), never
# retyped here.
BASE_SHA=$(grep '^BASE_SHA=' "$LANE/build_rt.sh" | cut -d'"' -f2)
CORE_SHA=$(grep '^CORE_SHA=' "$LANE/build_rt.sh" | cut -d'"' -f2)

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

# Frozen base extract, byte-verified.
sed -n '1,1677p' "$ADAPT/xio_full.zag" > "$tmp/base.zag"
bsha=$(sha256sum "$tmp/base.zag" | cut -d' ' -f1)
if [ "$bsha" != "$BASE_SHA" ]; then
  echo "BUILD-FAIL: frozen base sha256 mismatch: $bsha"; exit 1
fi
echo "base OK sha256=$bsha"

# Stock repair core must still be the committed C308 core.
csha=$(sha256sum "$LANE/src/rt_core.zag" | cut -d' ' -f1)
if [ "$csha" != "$CORE_SHA" ]; then
  echo "BUILD-FAIL: rt_core.zag changed: $csha"; exit 1
fi
echo "core OK (byte-identical to committed C308 repair core)"

# A3 guard-variant base: must differ from the frozen base ONLY by
# ADDING the promote_graph tombstone-on-recycle hunk (no removed or
# altered lines).
diff "$tmp/base.zag" "$LANE/src/rt_base_g3.zag" > "$LANE/outputs/base_g3.diff" || true
if grep -q '^<' "$LANE/outputs/base_g3.diff"; then
  echo "BUILD-FAIL: base_g3 removes/alters frozen base lines:"; grep '^<' "$LANE/outputs/base_g3.diff"; exit 1
fi
if ! grep -q 'tombstone-on-recycle' "$LANE/outputs/base_g3.diff"; then
  echo "BUILD-FAIL: base_g3 diff missing guard marker"; exit 1
fi
echo "base_g3 diff OK (additive guard hunk only)"

# A2 guard-variant core: must differ from stock core ONLY in xio_dep_rel.
diff "$LANE/src/rt_core.zag" "$LANE/src/rt_core_g2.zag" > "$LANE/outputs/core_g2.diff" || true
echo "core_g2 diff lines: $(grep -c -E '^[<>]' "$LANE/outputs/core_g2.diff")"

# Compiler-defect pattern audit on all new/guard sources.
for f in "$LANE/src/rt_core_g2.zag" "$LANE/src/rt_attack_g2.zag" "$LANE/src/rt_base_g3.zag"; do
  if grep -n 'while.*!(' "$f" | grep -q .; then
    echo "BUILD-FAIL: negated conjunction in while condition: $f"; exit 1
  fi
done
echo "pattern audit OK"

# C308 drivers, verbatim, boundary-checked (same as C308 build.sh).
sed -n '1925,2109p' "$ADAPT/xio_full.zag" > "$tmp/drv_c229.zag"
head -1 "$tmp/drv_c229.zag" | grep -q 'xio_driver.zag -- H-XIO-1' || { echo "BUILD-FAIL: c229 driver head"; exit 1; }
tail -1 "$tmp/drv_c229.zag" | grep -q '^}' || { echo "BUILD-FAIL: c229 driver tail"; exit 1; }
sed -n '1925,2130p' "$HARDER/xhio_full.zag" > "$tmp/drv_c235.zag"
head -1 "$tmp/drv_c235.zag" | grep -q 'xhio_driver.zag -- H-XIO-2' || { echo "BUILD-FAIL: c235 driver head"; exit 1; }
tail -1 "$tmp/drv_c235.zag" | grep -q '^}' || { echo "BUILD-FAIL: c235 driver tail"; exit 1; }
dsha=$(sha256sum "$DEPH/src/dephy_driver.zag" | cut -d' ' -f1)
if [ "$dsha" != "e8c98245900a536ee1a91af6e55b5cddcb27a9e0e435df3d6cea2cd4565bf885" ]; then
  echo "BUILD-FAIL: dephy_driver.zag changed: $dsha"; exit 1
fi
echo "drivers OK (verbatim, boundary-checked)"

# Assemblies.
cat "$tmp/base.zag" "$LANE/src/rt_core_g2.zag" "$LANE/src/rt_attack_g2.zag" > "$LANE/rt_a123_g2.zag"
cat "$LANE/src/rt_base_g3.zag" "$LANE/src/rt_core.zag" "$LANE/src/rt_attack.zag" > "$LANE/rt_a123_g3.zag"
cat "$tmp/base.zag" "$LANE/src/rt_core_g2.zag" "$DEPH/src/dephy_driver.zag" > "$LANE/dephy_full_g2.zag"
cat "$tmp/base.zag" "$LANE/src/rt_core_g2.zag" "$tmp/drv_c229.zag" > "$LANE/dephy_c229_g2.zag"
cat "$tmp/base.zag" "$LANE/src/rt_core_g2.zag" "$tmp/drv_c235.zag" > "$LANE/dephy_c235_g2.zag"
cat "$LANE/src/rt_base_g3.zag" "$LANE/src/rt_core.zag" "$DEPH/src/dephy_driver.zag" > "$LANE/dephy_full_g3.zag"
cat "$LANE/src/rt_base_g3.zag" "$LANE/src/rt_core.zag" "$tmp/drv_c229.zag" > "$LANE/dephy_c229_g3.zag"
cat "$LANE/src/rt_base_g3.zag" "$LANE/src/rt_core.zag" "$tmp/drv_c235.zag" > "$LANE/dephy_c235_g3.zag"
echo "assemblies built"

# Compile with the pinned znc.
for t in rt_a123_g2 rt_a123_g3 dephy_full_g2 dephy_c229_g2 dephy_c235_g2 dephy_full_g3 dephy_c229_g3 dephy_c235_g3; do
  "$ZNC" "$LANE/$t.zag" -o "$LANE/bin/$t" 2>"$LANE/outputs/$t.compile.txt" || { echo "BUILD-FAIL: $t compile"; tail -5 "$LANE/outputs/$t.compile.txt"; exit 1; }
  echo "compiled $t"
done

sha256sum "$LANE"/rt_a123_g2.zag "$LANE"/rt_a123_g3.zag "$LANE"/dephy_*_g2.zag "$LANE"/dephy_*_g3.zag "$LANE"/bin/rt_a123_g2 "$LANE"/bin/rt_a123_g3 "$LANE"/bin/dephy_*_g2 "$LANE"/bin/dephy_*_g3 > "$LANE/outputs/guards_bins.sha256"
cat "$LANE/outputs/guards_bins.sha256"
echo "BUILD-OK"
