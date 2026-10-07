#!/bin/bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
. /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh
D=docs/lab/research-lead/overnight-20260928/fast_core_20261006
S=docs/lab/research-lead/overnight-20260928/compression_exec/tnn2_frozen_ref.zag
tnn_pure_zag_report > "$D/reach_environment.txt"
grep -q 'VERDICT: PURE-ZAG-CLEAN' "$D/reach_environment.txt"
sed '/^\/\/ ============ test battery/,$d' "$S" > "$D/reach_prefix.txt"
cat "$D/reach_prefix.txt" "$D/reach_driver.zag" > "$D/reach.zag"
sed '/^\/\/ Appended to unchanged frozen/,$d' "$D/reach.zag" > "$D/reach_check.txt"
cmp "$D/reach_prefix.txt" "$D/reach_check.txt";rm "$D/reach_prefix.txt" "$D/reach_check.txt"
{ git rev-parse HEAD;shasum -a 256 "$TNN_ROOT/.bin/znc" "$S" "$D/REACHABILITY_PREREG.md" "$D/reach_driver.zag" "$D/reach.zag"; } > "$D/reach_provenance.txt"
for i in 1 2 3;do
  if znc "$D/reach.zag" > "$D/reach_compile$i.txt" 2>&1;then
    file "$D/reach" >> "$D/reach_compile$i.txt";shasum -a 256 "$D/reach" >> "$D/reach_provenance.txt"
    if "$D/reach" > "$D/reach_run$i.txt" 2>&1;then test -s "$D/reach_run$i.txt";
    else cat "$D/reach_run$i.txt";exit 1;fi
  else cat "$D/reach_compile$i.txt";exit 1;fi
done
cmp "$D/reach_run1.txt" "$D/reach_run2.txt";cmp "$D/reach_run1.txt" "$D/reach_run3.txt"
shasum -a 256 "$D/reach_run1.txt" >> "$D/reach_provenance.txt"
cat "$D/reach_run1.txt"
