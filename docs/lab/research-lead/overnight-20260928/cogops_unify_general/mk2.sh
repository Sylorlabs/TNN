#!/bin/sh
# mk2.sh -- same as mk.sh but for the SS-state-probe additives (which carry
# their own output sink for the strat_sel input log).
set -eu
. /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh
D="$(cd "$(dirname "$0")" && pwd)"
INC="$1"; TAG="$2"
cat "$D/ref/base.zag" "$D/ref/world.zag" "$D/ref/frozen_prefix.zag" "$INC" "$D/ref/main.zag" > "$D/probe/S_$TAG.zag"
/Users/Shared/micah/Documents/TNN/TNN/tools/zbuild.sh "$D/probe/S_$TAG.zag" > "$D/out/$TAG.buildlog" 2>&1 || { echo "$TAG BUILD-FAIL"; tail -4 "$D/out/$TAG.buildlog"; exit 1; }
cp /tmp/cogops_unify_out.txt "$D/out/$TAG.txt"
cp /tmp/cogops_unify_ss.txt "$D/out/$TAG.ss" 2>/dev/null || echo "(no ss log)"
rm -f /tmp/cogops_unify_out.txt
echo "$TAG: $(wc -l < "$D/out/$TAG.ss" | tr -d ' ') strat_sel calls logged"
