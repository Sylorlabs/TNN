#!/bin/bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
. /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh
D=docs/lab/research-lead/overnight-20260928/fast_core_20261006
S=docs/lab/research-lead/overnight-20260928/compression_exec/tnn2_frozen_ref.zag
tnn_pure_zag_report > "$D/object_environment.txt"
grep -q 'VERDICT: PURE-ZAG-CLEAN' "$D/object_environment.txt"
sed '/^\/\/ ============ test battery/,$d' "$S" > "$D/object_prefix.txt"
cat "$D/object_prefix.txt" "$D/object_driver.zag" > "$D/object.zag"
sed '/^\/\/ Appended to unchanged frozen/,$d' "$D/object.zag" > "$D/object_check.txt"
cmp "$D/object_prefix.txt" "$D/object_check.txt"
rm "$D/object_prefix.txt" "$D/object_check.txt"
bash tools/tnn_loop_lint.sh "$D/object_driver.zag"
bash tools/tnn_bars_lint.sh "$D/object_driver.zag"
{ git rev-parse HEAD; shasum -a 256 "$TNN_ROOT/.bin/znc" "$S" "$D/OBJECT_PREREG.md" "$D/object_driver.zag" "$D/object.zag"; } > "$D/object_provenance.txt"
first_hash=''
for i in 1 2 3; do
  if znc "$D/object.zag" > "$D/object_compile$i.txt" 2>&1; then
    file "$D/object" >> "$D/object_compile$i.txt"
    hash=$(shasum -a 256 "$D/object"); echo "$hash" >> "$D/object_provenance.txt"
    if [ "$i" = 1 ]; then first_hash="$hash"; else test "$hash" = "$first_hash"; fi
    if "$D/object" > "$D/object_run$i.txt" 2>&1; then test -s "$D/object_run$i.txt";
    else cat "$D/object_run$i.txt"; exit 1; fi
  else cat "$D/object_compile$i.txt"; exit 1; fi
done
cmp "$D/object_run1.txt" "$D/object_run2.txt"
cmp "$D/object_run1.txt" "$D/object_run3.txt"
shasum -a 256 "$D/object_run1.txt" >> "$D/object_provenance.txt"
cat "$D/object_run1.txt"
