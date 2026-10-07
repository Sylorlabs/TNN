#!/bin/bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
. /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh
D=docs/lab/research-lead/overnight-20260928/fast_protocol_20261006
tnn_pure_zag_report > "$D/order_environment.txt"
grep -q 'VERDICT: PURE-ZAG-CLEAN' "$D/order_environment.txt"
sed '/^fn main()i32 {/,$d' "$D/protocol.zag" > "$D/order_prefix.txt"
cat "$D/order_prefix.txt" "$D/order_driver.zag" > "$D/order.zag"
sed '/^\/\/ Appended to original protocol/,$d' "$D/order.zag" > "$D/order_check.txt"
cmp "$D/order_prefix.txt" "$D/order_check.txt";rm "$D/order_prefix.txt" "$D/order_check.txt"
{ git rev-parse HEAD;shasum -a 256 "$TNN_ROOT/.bin/znc" "$D/protocol.zag" "$D/ORDER_PREREG.md" "$D/order_driver.zag" "$D/order.zag"; } > "$D/order_provenance.txt"
for i in 1 2 3; do
  if znc "$D/order.zag" > "$D/order_compile$i.txt" 2>&1; then
    file "$D/order" >> "$D/order_compile$i.txt";shasum -a 256 "$D/order" >> "$D/order_provenance.txt"
    if "$D/order" > "$D/order_run$i.txt" 2>&1; then test -s "$D/order_run$i.txt";
    else cat "$D/order_run$i.txt";exit 1;fi
  else cat "$D/order_compile$i.txt";exit 1;fi
done
cmp "$D/order_run1.txt" "$D/order_run2.txt";cmp "$D/order_run1.txt" "$D/order_run3.txt"
shasum -a 256 "$D/order_run1.txt" >> "$D/order_provenance.txt"
cat "$D/order_run1.txt"
