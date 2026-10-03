#!/bin/sh
# run.sh -- run each binary 3 times, capturing byte-exact stdout/stderr.
# Shell only. Fails loudly on nonzero exit.
set -u
LANE=$(dirname "$0")
: > "$LANE/outputs/runs.exitcodes"
for b in dephy_full dephy_c229 dephy_c235; do
  i=1
  while [ $i -le 3 ]; do
    "$LANE/bin/$b" > "$LANE/outputs/$b.run$i.log" 2> "$LANE/outputs/$b.run$i.err"
    ec=$?
    echo "$b run$i exit=$ec" >> "$LANE/outputs/runs.exitcodes"
    if [ $ec -ne 0 ]; then echo "RUN-FAIL: $b run$i exit=$ec"; exit 1; fi
    i=$((i+1))
  done
done
cat "$LANE/outputs/runs.exitcodes"
sha256sum "$LANE"/outputs/dephy_*.run?.log > "$LANE/outputs/sha256sums.txt"
cat "$LANE/outputs/sha256sums.txt"
echo "RUN-OK"
