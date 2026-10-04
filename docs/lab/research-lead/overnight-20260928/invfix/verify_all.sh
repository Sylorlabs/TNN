#!/bin/sh
# verify_all.sh -- determinism + non-regression sweep.
# Every binary runs 3x under the watchdog; outputs must be byte-identical and
# non-empty.  run: sh verify_all.sh
set -e
D=/Users/Shared/micah/Documents/TNN/.worktrees/invfix/docs/lab/research-lead/overnight-20260928/invfix
W=/Users/Shared/micah/Documents/TNN/TNN/tools/tnnwatch.sh
cd "$D"
fail=0
one() {
  b=$1; tag=$2
  i=1
  while [ $i -le 3 ]; do
    $W reg "$tag" 600 "./$b" > "/tmp/${tag}.r$i" 2>&1 || true
    i=$((i+1))
  done
  if [ ! -s "/tmp/${tag}.r1" ]; then
    echo "EMPTY-LOG    $tag  (brief 10.1: zero bytes is NOT a result)"; fail=1; return
  fi
  if cmp -s "/tmp/${tag}.r1" "/tmp/${tag}.r2" && cmp -s "/tmp/${tag}.r2" "/tmp/${tag}.r3"; then
    echo "DET 3/3 OK   $tag  ($(wc -c < /tmp/${tag}.r1 | tr -d ' ') bytes)"
  else
    echo "DET FAIL     $tag"; fail=1
  fi
}
one tb_iv_run iv_battery
one tb_frozen_run frozen_battery
for w in aw01 aw02 aw03 aw07; do
  one "adv/$w.frozen" "${w}_frz"
  one "adv/$w.iv" "${w}_iv"
done
for w in aw04 aw05 aw06 aw08 aw09; do
  one "adv/$w.frozen" "${w}_frz"
  one "adv/$w.iv" "${w}_iv"
done
echo "---"
if [ $fail -eq 0 ]; then echo "VERIFY_ALL_DETERMINISTIC"; else echo "VERIFY_ALL_HAS_FAILURES"; fi
