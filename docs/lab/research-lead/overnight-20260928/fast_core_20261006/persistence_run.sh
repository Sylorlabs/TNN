#!/bin/bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
. /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh
D=docs/lab/research-lead/overnight-20260928/fast_core_20261006
S=docs/lab/research-lead/overnight-20260928/compression_exec/tnn2_frozen_ref.zag
tnn_pure_zag_report > "$D/persistence_environment.txt"
grep -q 'VERDICT: PURE-ZAG-CLEAN' "$D/persistence_environment.txt"
sed '/^\/\/ ============ test battery/,$d' "$S" > "$D/persistence_prefix.txt"
cat "$D/persistence_prefix.txt" "$D/persistence_driver.zag" > "$D/persistence.zag"
sed '/^\/\/ Appended to unchanged frozen/,$d' "$D/persistence.zag" > "$D/persistence_check.txt"
cmp "$D/persistence_prefix.txt" "$D/persistence_check.txt";rm "$D/persistence_prefix.txt" "$D/persistence_check.txt"
{ git rev-parse HEAD;shasum -a 256 "$TNN_ROOT/.bin/znc" "$S" "$D/PERSISTENCE_PREREG.md" "$D/persistence_driver.zag" "$D/persistence.zag"; } > "$D/persistence_provenance.txt"
for i in 1 2 3;do
  if znc "$D/persistence.zag" > "$D/persistence_compile$i.txt" 2>&1;then
    file "$D/persistence" >> "$D/persistence_compile$i.txt";shasum -a 256 "$D/persistence" >> "$D/persistence_provenance.txt"
    if "$D/persistence" > "$D/persistence_run$i.txt" 2>&1;then test -s "$D/persistence_run$i.txt";
    else cat "$D/persistence_run$i.txt";exit 1;fi
  else cat "$D/persistence_compile$i.txt";exit 1;fi
done
cmp "$D/persistence_run1.txt" "$D/persistence_run2.txt";cmp "$D/persistence_run1.txt" "$D/persistence_run3.txt"
shasum -a 256 "$D/persistence_run1.txt" >> "$D/persistence_provenance.txt"
cat "$D/persistence_run1.txt"
