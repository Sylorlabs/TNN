#!/bin/sh
# BUILD.sh -- F3 Phase 3 build and test.
# Prereg: 97287f87c. Pure Zag. No Python.
ZNC=/home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc
D=docs/lab/research-lead/overnight-20260928/f3_phase3
set -e
echo "=== T-CONJ (ADV1) ==="
cat $D/f3_p3.zag ../f2_ablation/world_adv1.zag > $D/run_p3c.zag
$ZNC $D/run_p3c.zag -o $D/bin_p3c 2> $D/build_p3c.err || (cat $D/build_p3c.err; exit 1)
i=1
while [ $i -le 3 ]; do
  $D/bin_p3c > $D/raw_p3c_r$i.txt 2> $D/raw_p3c_r$i.err
  echo "run $i done"
  i=$((i+1))
done
echo "=== T-NEG ==="
cat $D/f3_p3.zag $D/world_tneg.zag > $D/run_p3n.zag
$ZNC $D/run_p3n.zag -o $D/bin_p3n 2> $D/build_p3n.err || (cat $D/build_p3n.err; exit 1)
i=1
while [ $i -le 3 ]; do
  $D/bin_p3n > $D/raw_p3n_r$i.txt 2> $D/raw_p3n_r$i.err
  echo "run $i done"
  i=$((i+1))
done
echo "=== md5 ==="
md5sum $D/raw_p3c_r*.txt $D/raw_p3n_r*.txt
echo "=== verdicts ==="
grep "F3P3 RESULT" $D/raw_p3c_r1.txt $D/raw_p3n_r1.txt
