#!/bin/bash
# Z6 1x battery: every leg twice, byte-identical stdout required.
set -u
Z6=~/workspace/tnn-lab/units/arms/Z6
CORP=~/workspace/tnn-lab/units/arms/harness/corpora/r1
AUX=$Z6/.work
EV=$AUX/evidence/1x
BIN=$AUX/z6_1x
mkdir -p "$EV"
echo "== build =="
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 "$Z6/cl/arm.zag" -o "$BIN" 2>&1 | grep -iE "error" && exit 1
echo "build ok"
LEGS="m1-1x-prose m1-1x-code m2-t1-prose m2-t1-code m2-t2-prose m2-t2-code m2-t3-1x m3-1x m4-prose m4-code m5-1x m6-code-prose m6-prose-code m7-1x m8-p0 m8-p1 m8-p2 m8-p3 m8-p4 m8-p5"
FAIL=0
for leg in $LEGS; do
  echo "== $leg =="
  "$BIN" "$leg" "$CORP" "$AUX" > "$EV/$leg.run1.log" 2>&1
  rc1=$?
  "$BIN" "$leg" "$CORP" "$AUX" > "$EV/$leg.run2.log" 2>&1
  rc2=$?
  if [ $rc1 -ne 0 ] || [ $rc2 -ne 0 ]; then echo "FAIL($leg): rc $rc1/$rc2"; FAIL=1; continue; fi
  if ! cmp -s "$EV/$leg.run1.log" "$EV/$leg.run2.log"; then
    echo "FAIL($leg): stdout differs between runs"; FAIL=1; continue
  fi
  echo "ok($leg): rc=0, byte-identical"
done
# collect METRIC_JSON lines
: > "$EV/metrics_1x.jsonl"
for leg in $LEGS; do
  grep -h "^METRIC_JSON" "$EV/$leg.run1.log" >> "$EV/metrics_1x.jsonl" || true
done
wc -l "$EV/metrics_1x.jsonl"
if [ $FAIL -eq 0 ]; then echo "BATTERY PASS"; else echo "BATTERY FAIL"; exit 1; fi
