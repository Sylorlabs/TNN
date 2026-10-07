#!/bin/bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
. /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh
D=docs/lab/research-lead/overnight-20260928/fast_core_20261006
S=docs/lab/research-lead/overnight-20260928/compression_exec/tnn2_frozen_ref.zag
tnn_pure_zag_report > "$D/conflict_environment.txt"
grep -q 'VERDICT: PURE-ZAG-CLEAN' "$D/conflict_environment.txt"
sed '/^\/\/ ============ test battery/,$d' "$S" > "$D/conflict_prefix.txt"
cat "$D/conflict_prefix.txt" "$D/conflict_driver.zag" > "$D/conflict.zag"
sed '/^\/\/ Appended to unchanged frozen/,$d' "$D/conflict.zag" > "$D/conflict_check.txt"
cmp "$D/conflict_prefix.txt" "$D/conflict_check.txt"
rm "$D/conflict_prefix.txt" "$D/conflict_check.txt"
bash tools/tnn_loop_lint.sh "$D/conflict_driver.zag"
bash tools/tnn_bars_lint.sh "$D/conflict_driver.zag"
{ git rev-parse HEAD; shasum -a 256 "$TNN_ROOT/.bin/znc" "$S" "$D/CONFLICT_PREREG.md" "$D/conflict_driver.zag" "$D/conflict.zag"; } > "$D/conflict_provenance.txt"
first_hash=''
for i in 1 2 3; do
  if znc "$D/conflict.zag" > "$D/conflict_compile$i.txt" 2>&1; then
    file "$D/conflict" >> "$D/conflict_compile$i.txt"
    hash=$(shasum -a 256 "$D/conflict"); echo "$hash" >> "$D/conflict_provenance.txt"
    if [ "$i" = 1 ]; then first_hash="$hash"; else test "$hash" = "$first_hash"; fi
    if "$D/conflict" > "$D/conflict_run$i.txt" 2>&1; then test -s "$D/conflict_run$i.txt";
    else cat "$D/conflict_run$i.txt"; exit 1; fi
  else cat "$D/conflict_compile$i.txt"; exit 1; fi
done
cmp "$D/conflict_run1.txt" "$D/conflict_run2.txt"
cmp "$D/conflict_run1.txt" "$D/conflict_run3.txt"
shasum -a 256 "$D/conflict_run1.txt" >> "$D/conflict_provenance.txt"
cat "$D/conflict_run1.txt"
