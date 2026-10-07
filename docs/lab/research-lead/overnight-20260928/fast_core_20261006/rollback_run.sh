#!/bin/bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
. /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh
D=docs/lab/research-lead/overnight-20260928/fast_core_20261006
S=docs/lab/research-lead/overnight-20260928/compression_exec/tnn2_frozen_ref.zag
tnn_pure_zag_report > "$D/rollback_environment.txt"
grep -q 'VERDICT: PURE-ZAG-CLEAN' "$D/rollback_environment.txt"
sed '/^\/\/ ============ test battery/,$d' "$S" > "$D/rollback_prefix.txt"
cat "$D/rollback_prefix.txt" "$D/rollback_driver.zag" > "$D/rollback.zag"
sed '/^\/\/ Appended to unchanged frozen/,$d' "$D/rollback.zag" > "$D/rollback_check.txt"
cmp "$D/rollback_prefix.txt" "$D/rollback_check.txt"
rm "$D/rollback_prefix.txt" "$D/rollback_check.txt"
bash tools/tnn_loop_lint.sh "$D/rollback_driver.zag"
bash tools/tnn_bars_lint.sh "$D/rollback_driver.zag"
{ git rev-parse HEAD; shasum -a 256 "$TNN_ROOT/.bin/znc" "$S" "$D/ROLLBACK_PREREG.md" "$D/rollback_driver.zag" "$D/rollback.zag"; } > "$D/rollback_provenance.txt"
first_hash=''
for i in 1 2 3; do
  if znc "$D/rollback.zag" > "$D/rollback_compile$i.txt" 2>&1; then
    file "$D/rollback" >> "$D/rollback_compile$i.txt"
    hash=$(shasum -a 256 "$D/rollback"); echo "$hash" >> "$D/rollback_provenance.txt"
    if [ "$i" = 1 ]; then first_hash="$hash"; else test "$hash" = "$first_hash"; fi
    if "$D/rollback" > "$D/rollback_run$i.txt" 2>&1; then test -s "$D/rollback_run$i.txt";
    else cat "$D/rollback_run$i.txt"; exit 1; fi
  else cat "$D/rollback_compile$i.txt"; exit 1; fi
done
cmp "$D/rollback_run1.txt" "$D/rollback_run2.txt"
cmp "$D/rollback_run1.txt" "$D/rollback_run3.txt"
shasum -a 256 "$D/rollback_run1.txt" >> "$D/rollback_provenance.txt"
cat "$D/rollback_run1.txt"
