#!/bin/bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
. /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh
D=docs/lab/research-lead/overnight-20260928/fast_core_20261006
S=docs/lab/research-lead/overnight-20260928/compression_exec/tnn2_frozen_ref.zag
tnn_pure_zag_report > "$D/ownership_environment.txt"
grep -q 'VERDICT: PURE-ZAG-CLEAN' "$D/ownership_environment.txt"
sed '/^\/\/ ============ test battery/,$d' "$S" > "$D/ownership_prefix.txt"
cat "$D/ownership_prefix.txt" "$D/ownership_driver.zag" > "$D/ownership.zag"
sed '/^\/\/ Appended to unchanged frozen/,$d' "$D/ownership.zag" > "$D/ownership_check.txt"
cmp "$D/ownership_prefix.txt" "$D/ownership_check.txt";rm "$D/ownership_prefix.txt" "$D/ownership_check.txt"
{ git rev-parse HEAD;shasum -a 256 "$TNN_ROOT/.bin/znc" "$S" "$D/OWNERSHIP_PREREG.md" "$D/ownership_driver.zag" "$D/ownership.zag"; } > "$D/ownership_provenance.txt"
for i in 1 2 3;do
  if znc "$D/ownership.zag" > "$D/ownership_compile$i.txt" 2>&1;then
    file "$D/ownership" >> "$D/ownership_compile$i.txt";shasum -a 256 "$D/ownership" >> "$D/ownership_provenance.txt"
    if "$D/ownership" > "$D/ownership_run$i.txt" 2>&1;then test -s "$D/ownership_run$i.txt";
    else cat "$D/ownership_run$i.txt";exit 1;fi
  else cat "$D/ownership_compile$i.txt";exit 1;fi
done
cmp "$D/ownership_run1.txt" "$D/ownership_run2.txt";cmp "$D/ownership_run1.txt" "$D/ownership_run3.txt"
shasum -a 256 "$D/ownership_run1.txt" >> "$D/ownership_provenance.txt"
cat "$D/ownership_run1.txt"
