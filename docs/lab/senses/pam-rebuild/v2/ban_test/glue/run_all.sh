#!/bin/bash
# Official ban-trial execution battery (post-prereg).
# Runs each variant 3x on the frozen stream + all 14 traps; records sha256
# digests; asserts byte-identical reruns. Pure-Zag mechanism; zero RNG.
set -e
BT=~/workspace/tnn-lab/senses/pam-rebuild/v2/ban_test
BB=~/workspace/ban_test_build
OUT=$BT/evidence/runs
mkdir -p $OUT
echo "run,stream,variant,sha256" > $OUT/digests.csv
sha() { sha256sum "$1" | cut -d' ' -f1; }
# frozen stream
for v in 0 1 2 3; do
  for r in 1 2 3; do
    f=$OUT/frozen_v${v}_r${r}.txt
    $BB/bantest $BT/evidence/stream.txt $v $f 2>/dev/null
    echo "r$r,frozen,$v,$(sha $f)" >> $OUT/digests.csv
  done
done
# traps
for t in $BT/evidence/traps/*.stream; do
  n=$(basename $t .stream)
  for v in 0 1 2 3; do
    for r in 1 2 3; do
      f=$OUT/${n}_v${v}_r${r}.txt
      $BB/bantest $t $v $f 2>/dev/null
      echo "r$r,$n,$v,$(sha $f)" >> $OUT/digests.csv
    done
  done
done
# byte-identity check: all 3 runs per (stream,variant) identical
python3 - <<'EOF'
import csv, collections
d = collections.defaultdict(set)
for row in csv.DictReader(open("/home/hatch/workspace/tnn-lab/senses/pam-rebuild/v2/ban_test/evidence/runs/digests.csv")):
    d[(row["stream"], row["variant"])].add(row["sha256"])
bad = {k: v for k, v in d.items() if len(v) != 1}
print("groups:", len(d), "non-identical:", len(bad))
for k, v in bad.items():
    print("MISMATCH", k, v)
assert not bad, "byte-identity FAILED"
print("BYTE-IDENTICAL: all", len(d), "groups x3 runs")
EOF
