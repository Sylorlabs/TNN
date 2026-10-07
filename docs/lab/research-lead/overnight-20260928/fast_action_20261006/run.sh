#!/bin/bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
. /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh
D=docs/lab/research-lead/overnight-20260928/fast_action_20261006
M=docs/lab/research-lead/overnight-20260928/fast_iteration_20261006/method.zag
tnn_pure_zag_report > "$D/environment.txt"
grep -q 'VERDICT: PURE-ZAG-CLEAN' "$D/environment.txt"
sed '/^fn main()i32 {/,$d' "$M" > "$D/prefix.txt"
cat "$D/prefix.txt" "$D/action_driver.zag" > "$D/action.zag"
sed '/^\/\/ Appended to generic method/,$d' "$D/action.zag" > "$D/check.txt"
cmp "$D/prefix.txt" "$D/check.txt"
rm "$D/prefix.txt" "$D/check.txt"
{ git rev-parse HEAD; shasum -a 256 "$TNN_ROOT/.bin/znc" "$M" "$D/PREREG.md" "$D/action_driver.zag" "$D/action.zag"; } > "$D/provenance.txt"
for i in 1 2 3; do
  if znc "$D/action.zag" > "$D/action_compile$i.txt" 2>&1; then
    file "$D/action" >> "$D/action_compile$i.txt"
    file "$D/action" | grep -q 'Mach-O.*arm64'
    shasum -a 256 "$D/action" >> "$D/provenance.txt"
    if "$D/action" > "$D/action_run$i.txt" 2>&1; then test -s "$D/action_run$i.txt";
    else cat "$D/action_run$i.txt"; exit 1; fi
  else cat "$D/action_compile$i.txt"; exit 1; fi
done
cmp "$D/action_run1.txt" "$D/action_run2.txt"
cmp "$D/action_run1.txt" "$D/action_run3.txt"
shasum -a 256 "$D/action_run1.txt" >> "$D/provenance.txt"
cat "$D/action_run1.txt"
