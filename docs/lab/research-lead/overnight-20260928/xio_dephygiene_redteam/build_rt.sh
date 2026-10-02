#!/bin/sh
# build_rt.sh -- assemble and compile the red-team attack binary.
# Shell only: extraction, hashing, concatenation, pinned znc invocation.
# No research logic. Fails loudly on any verification mismatch.
set -u
LANE=$(dirname "$0")
ADAPT="$LANE/../xio_adapters"
ZNC="$HOME/safebin/znc"
BASE_SHA="dc0e86d44db11390e6e7d2450e1b52d7fb8f8012b42346dc4d4739ef888d1ab6"
CORE_SHA="f873bd70343021a58f92e330b7c4043ac4e233f7887c8ee92131b6b7900c6c13"

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

# Frozen base: xio_full.zag lines 1-1677, byte-verified.
sed -n '1,1677p' "$ADAPT/xio_full.zag" > "$tmp/base.zag"
bsha=$(sha256sum "$tmp/base.zag" | cut -d' ' -f1)
if [ "$bsha" != "$BASE_SHA" ]; then
  echo "BUILD-FAIL: frozen base sha256 mismatch: $bsha"; exit 1
fi
echo "base OK sha256=$bsha"

# Attack core must be a byte-copy of the committed C308 repair core.
csha=$(sha256sum "$LANE/src/rt_core.zag" | cut -d' ' -f1)
if [ "$csha" != "$CORE_SHA" ]; then
  echo "BUILD-FAIL: rt_core.zag is not the committed C308 core: $csha"; exit 1
fi
echo "core OK (byte-identical to committed C308 repair core)"

# Compiler-defect pattern audit on new attack source.
if grep -n 'while.*!(' "$LANE/src/rt_attack.zag" | grep -q .; then
  echo "BUILD-FAIL: negated conjunction in while condition"; exit 1
fi
echo "pattern audit OK"

# Assembly.
cat "$tmp/base.zag" "$LANE/src/rt_core.zag" "$LANE/src/rt_attack.zag" > "$LANE/rt_a123.zag"
echo "assembly built"

# Compile with the pinned znc.
"$ZNC" "$LANE/rt_a123.zag" -o "$LANE/bin/rt_a123" 2>"$LANE/outputs/rt_a123_compile.txt" || { echo "BUILD-FAIL: rt_a123 compile"; cat "$LANE/outputs/rt_a123_compile.txt"; exit 1; }
echo "binary compiled"

sha256sum "$LANE/src/rt_core.zag" "$LANE/src/rt_attack.zag" \
  "$LANE/rt_a123.zag" "$LANE/bin/rt_a123" > "$LANE/outputs/rt_sources_bins.sha256"
cat "$LANE/outputs/rt_sources_bins.sha256"
echo "BUILD-OK"
