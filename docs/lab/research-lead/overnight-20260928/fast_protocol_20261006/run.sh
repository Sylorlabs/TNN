#!/bin/bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
. /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh
D=docs/lab/research-lead/overnight-20260928/fast_protocol_20261006
P=docs/lab/research-lead/overnight-20260928/p6struct/precond.zag
tnn_pure_zag_report > "$D/environment.txt"
grep -q 'VERDICT: PURE-ZAG-CLEAN' "$D/environment.txt"
sed '/^\/\/ ---- problem constants/,$d' "$P" > "$D/prefix.txt"
cat "$D/prefix.txt" "$D/driver.zag" > "$D/protocol.zag"
sed '/^\/\/ Appended to allocation/,$d' "$D/protocol.zag" > "$D/check.txt"
cmp "$D/prefix.txt" "$D/check.txt"; rm "$D/prefix.txt" "$D/check.txt"
{ git rev-parse HEAD; shasum -a 256 "$TNN_ROOT/.bin/znc" "$P" "$D/PREREG.md" "$D/driver.zag" "$D/protocol.zag"; } > "$D/provenance.txt"
for i in 1 2 3; do
  if znc "$D/protocol.zag" > "$D/compile$i.txt" 2>&1; then
    file "$D/protocol" >> "$D/compile$i.txt"
    shasum -a 256 "$D/protocol" >> "$D/provenance.txt"
    if "$D/protocol" > "$D/run$i.txt" 2>&1; then test -s "$D/run$i.txt";
    else cat "$D/run$i.txt"; exit 1; fi
  else cat "$D/compile$i.txt"; exit 1; fi
done
cmp "$D/run1.txt" "$D/run2.txt"; cmp "$D/run1.txt" "$D/run3.txt"
shasum -a 256 "$D/run1.txt" >> "$D/provenance.txt"
cat "$D/run1.txt"
