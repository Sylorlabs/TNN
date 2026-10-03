#!/bin/bash
# Reproduce the round-2 delete-logic verification end to end.
# Builds dd_r2 with the pinned toolchain (from adopt/, so the driver tests
# the CANONICAL store + merge gate), runs all four modes TWICE, and
# byte-compares run 1 vs run 2 (B7 determinism).
set -e
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
D=~/workspace/tnn-lab/ops/storage-compression/dedup/r2
A=~/workspace/tnn-lab/ops/storage-compression/adopt
cd "$A"
"$ZNC" ../dedup/r2/dd_r2.zag -o ../dedup/r2/dd_r2 --no-analyze 2>&1 | grep -v -i "warning\|wrote" || true
cd "$D"
for m in sealfix merge chain adv; do
  ./dd_r2 $m > "out_${m}_1.txt" 2>&1
  ./dd_r2 $m > "out_${m}_2.txt" 2>&1
done
ok=1
for m in sealfix merge chain adv; do
  if cmp -s "out_${m}_1.txt" "out_${m}_2.txt"; then
    echo "$m: run1 == run2 (byte-identical)"
  else
    echo "$m: RUNS DIFFER"; ok=0
  fi
  if grep -q ",ok=1" "out_${m}_1.txt"; then
    echo "$m: ok=1"
  else
    echo "$m: NO ok=1 MARKER"; ok=0
  fi
done
rm -f out_*_1.txt out_*_2.txt
[ $ok -eq 1 ] && echo ALL_MODES_PASS_AND_REPRODUCED || { echo REPRODUCTION_MISMATCH; exit 1; }
