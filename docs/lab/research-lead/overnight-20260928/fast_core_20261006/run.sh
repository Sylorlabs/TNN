#!/bin/bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
. /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh
D=docs/lab/research-lead/overnight-20260928/fast_core_20261006
S=docs/lab/research-lead/overnight-20260928/compression_exec/tnn2_frozen_ref.zag
tnn_pure_zag_report > "$D/environment.txt"
grep -q 'VERDICT: PURE-ZAG-CLEAN' "$D/environment.txt"
sed '/^\/\/ ============ test battery/,$d' "$S" > "$D/prefix.txt"
cat "$D/prefix.txt" "$D/driver.zag" > "$D/core.zag"
sed '/^\/\/ Appended to unchanged frozen/,$d' "$D/core.zag" > "$D/check.txt"
cmp "$D/prefix.txt" "$D/check.txt";rm "$D/prefix.txt" "$D/check.txt"
{ git rev-parse HEAD;shasum -a 256 "$TNN_ROOT/.bin/znc" "$S" "$D/PREREG.md" "$D/driver.zag" "$D/core.zag"; } > "$D/provenance.txt"
for i in 1 2 3;do
  if znc "$D/core.zag" > "$D/compile$i.txt" 2>&1;then
    file "$D/core" >> "$D/compile$i.txt";shasum -a 256 "$D/core" >> "$D/provenance.txt"
    if "$D/core" > "$D/run$i.txt" 2>&1;then test -s "$D/run$i.txt";
    else cat "$D/run$i.txt";exit 1;fi
  else cat "$D/compile$i.txt";exit 1;fi
done
cmp "$D/run1.txt" "$D/run2.txt";cmp "$D/run1.txt" "$D/run3.txt"
shasum -a 256 "$D/run1.txt" >> "$D/provenance.txt"
cat "$D/run1.txt"
