#!/bin/sh
# build.sh -- assemble and compile the three DEP-hygiene binaries.
# Shell only: extraction, hashing, concatenation, pinned znc invocation.
# No research logic. Fails loudly on any verification mismatch.
set -u
LANE=$(dirname "$0")
ADAPT="$LANE/../xio_adapters"
HARDER="$LANE/../xio_harder"
IDFIX="$LANE/../xio_idfix"
ZNC="$HOME/safebin/znc"
BASE_SHA="dc0e86d44db11390e6e7d2450e1b52d7fb8f8012b42346dc4d4739ef888d1ab6"

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

# Frozen base: xio_full.zag lines 1-1677, byte-verified.
sed -n '1,1677p' "$ADAPT/xio_full.zag" > "$tmp/base.zag"
bsha=$(sha256sum "$tmp/base.zag" | cut -d' ' -f1)
if [ "$bsha" != "$BASE_SHA" ]; then
  echo "BUILD-FAIL: frozen base sha256 mismatch: $bsha"; exit 1
fi
echo "base OK sha256=$bsha"

# Pristine idfix core extract for the audit diff.
sed -n '1678,1960p' "$IDFIX/idfix_full.zag" > "$tmp/idfix_core.txt"

# Original drivers, verbatim, boundary-checked.
sed -n '1925,2109p' "$ADAPT/xio_full.zag" > "$tmp/drv_c229.zag"
head -1 "$tmp/drv_c229.zag" | grep -q 'xio_driver.zag -- H-XIO-1' || { echo "BUILD-FAIL: c229 driver head"; exit 1; }
tail -1 "$tmp/drv_c229.zag" | grep -q '^}' || { echo "BUILD-FAIL: c229 driver tail"; exit 1; }
sed -n '1925,2130p' "$HARDER/xhio_full.zag" > "$tmp/drv_c235.zag"
head -1 "$tmp/drv_c235.zag" | grep -q 'xhio_driver.zag -- H-XIO-2' || { echo "BUILD-FAIL: c235 driver head"; exit 1; }
tail -1 "$tmp/drv_c235.zag" | grep -q '^}' || { echo "BUILD-FAIL: c235 driver tail"; exit 1; }
echo "drivers OK (verbatim, boundary-checked)"

# Audit: repaired core differs from pristine idfix core only by addition
# plus the two documented function replacements. Save the diff.
diff "$tmp/idfix_core.txt" "$LANE/src/dephygiene_core.zag" > "$LANE/outputs/core_diff.txt" || true
echo "core diff saved to outputs/core_diff.txt"

# Assemblies.
cat "$tmp/base.zag" "$LANE/src/dephygiene_core.zag" "$LANE/src/dephy_driver.zag" > "$LANE/dephy_full.zag"
cat "$tmp/base.zag" "$LANE/src/dephygiene_core.zag" "$tmp/drv_c229.zag" > "$LANE/dephy_c229.zag"
cat "$tmp/base.zag" "$LANE/src/dephygiene_core.zag" "$tmp/drv_c235.zag" > "$LANE/dephy_c235.zag"
echo "assemblies built"

# Compile with the pinned znc.
"$ZNC" "$LANE/dephy_full.zag" -o "$LANE/bin/dephy_full" 2>"$LANE/outputs/dephy_full_compile.txt" || { echo "BUILD-FAIL: dephy_full compile"; exit 1; }
"$ZNC" "$LANE/dephy_c229.zag" -o "$LANE/bin/dephy_c229" 2>"$LANE/outputs/dephy_c229_compile.txt" || { echo "BUILD-FAIL: dephy_c229 compile"; exit 1; }
"$ZNC" "$LANE/dephy_c235.zag" -o "$LANE/bin/dephy_c235" 2>"$LANE/outputs/dephy_c235_compile.txt" || { echo "BUILD-FAIL: dephy_c235 compile"; exit 1; }
echo "binaries compiled"

# Checksums of sources and binaries.
sha256sum "$LANE/src/dephygiene_core.zag" "$LANE/src/dephy_driver.zag" \
  "$LANE/dephy_full.zag" "$LANE/dephy_c229.zag" "$LANE/dephy_c235.zag" \
  "$LANE/bin/dephy_full" "$LANE/bin/dephy_c229" "$LANE/bin/dephy_c235" \
  > "$LANE/outputs/sources_bins.sha256"
cat "$LANE/outputs/sources_bins.sha256"
echo "BUILD-OK"
