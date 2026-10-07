#!/bin/bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
. /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh
D=docs/lab/research-lead/overnight-20260928/fast_core_20261006
S=docs/lab/research-lead/overnight-20260928/compression_exec/tnn2_frozen_ref.zag
tnn_pure_zag_report > "$D/region_environment.txt"
grep -q 'VERDICT: PURE-ZAG-CLEAN' "$D/region_environment.txt"
sed '/^\/\/ ============ test battery/,$d' "$S" > "$D/region_prefix.txt"
cat "$D/region_prefix.txt" "$D/region_driver.zag" > "$D/region.zag"
sed '/^\/\/ Appended to unchanged frozen/,$d' "$D/region.zag" > "$D/region_check.txt"
cmp "$D/region_prefix.txt" "$D/region_check.txt"
rm "$D/region_prefix.txt" "$D/region_check.txt"
bash tools/tnn_loop_lint.sh "$D/region_driver.zag"
bash tools/tnn_bars_lint.sh "$D/region_driver.zag"
{ git rev-parse HEAD; shasum -a 256 "$TNN_ROOT/.bin/znc" "$S" "$D/REGION_PREREG.md" "$D/region_driver.zag" "$D/region.zag"; } > "$D/region_provenance.txt"
first_hash=''
for i in 1 2 3; do
  if znc "$D/region.zag" > "$D/region_compile$i.txt" 2>&1; then
    file "$D/region" >> "$D/region_compile$i.txt"
    hash=$(shasum -a 256 "$D/region"); echo "$hash" >> "$D/region_provenance.txt"
    if [ "$i" = 1 ]; then first_hash="$hash"; else test "$hash" = "$first_hash"; fi
    if "$D/region" > "$D/region_run$i.txt" 2>&1; then test -s "$D/region_run$i.txt";
    else cat "$D/region_run$i.txt"; exit 1; fi
  else cat "$D/region_compile$i.txt"; exit 1; fi
done
cmp "$D/region_run1.txt" "$D/region_run2.txt"
cmp "$D/region_run1.txt" "$D/region_run3.txt"
shasum -a 256 "$D/region_run1.txt" >> "$D/region_provenance.txt"
cat "$D/region_run1.txt"
