#!/bin/sh
# COGOPS-UNIFY-GENERAL build+run harness (orchestration only).
#
# Usage: mk.sh <variant-additive.zag> <tag>
# Concatenates the FROZEN prefix (ref/frozen_prefix.zag, 1331 lines,
# sha256 750cb01d...), the common base arena (ref/base.zag), the
# common world (ref/world.zag = c12 world, sha256 46c6b0dc101f) and the
# common main (ref/main.zag = c15 main, 792 lines) with the supplied
# strategy additive section, compiles with the pinned macos-arm64 znc,
# runs, and copies the flushed output to out/<tag>.txt.
#
# Only the additive section varies between variants. That is the whole
# point: it makes strat_sel the single independent variable.
#
# VERIFIED: variant c15 reproduces cogops_rescueaware/c15_run1.txt
# byte-identically.
set -eu
. /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh
Z=/Users/Shared/micah/Documents/TNN/TNN/tools/zbuild.sh
D="$(cd "$(dirname "$0")" && pwd)"
INC="$1"
TAG="$2"
SRC="$D/probe/U_$TAG.zag"
cat "$D/ref/base.zag" "$D/ref/world.zag" "$D/ref/frozen_prefix.zag" \
    "$INC" "$D/ref/main.zag" > "$SRC"
$Z "$SRC" > "$D/out/$TAG.buildlog" 2>&1
cp /tmp/cogops_unify_out.txt "$D/out/$TAG.txt"
rm -f /tmp/cogops_unify_out.txt
echo "$TAG: $(wc -l < "$D/out/$TAG.txt" | tr -d ' ') lines  $(shasum -a 256 "$D/out/$TAG.txt" | cut -c1-16)"
