#!/bin/bash
# run_tryit.sh — build try_laws (if needed), run it 3x, and require
# byte-identical stdout across runs (sha256). Fails loudly on any
# build/run/scenario/determinism problem.
set -u
cd "$(dirname "$0")"
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1

if [ ! -x try_laws.bin ] || [ try_laws.zag -nt try_laws.bin ]; then
  echo "== build try_laws"
  "$ZNC" build try_laws.zag -o try_laws.bin || { echo "BUILD_FAIL"; exit 1; }
fi

for i in 1 2 3; do
  ./try_laws.bin > "tryit.run$i.out" 2>/dev/null || { echo "RUN_FAIL run$i"; exit 1; }
done

h1=$(sha256sum tryit.run1.out | cut -d' ' -f1)
h2=$(sha256sum tryit.run2.out | cut -d' ' -f1)
h3=$(sha256sum tryit.run3.out | cut -d' ' -f1)
det_ok=1
[ "$h1" = "$h2" ] || det_ok=0
[ "$h2" = "$h3" ] || det_ok=0

scen_ok=0
grep -q "TRYIT: 5/5 scenarios behaved as expected — ALL OK" tryit.run1.out && scen_ok=1

cat tryit.run1.out
rm -f tryit.run1.out tryit.run2.out tryit.run3.out

if [ "$scen_ok" != "1" ]; then
  echo "SCENARIO FAIL: a TRY scenario did not behave as expected"
  exit 1
fi
if [ "$det_ok" != "1" ]; then
  echo "DETERMINISM FAIL: the 3 runs produced different output"
  echo "  run1 sha256: $h1"
  echo "  run2 sha256: $h2"
  echo "  run3 sha256: $h3"
  exit 1
fi
echo "DETERMINISM: 3/3 byte-identical"
