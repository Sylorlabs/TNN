#!/bin/sh
# run.sh -- build and run l3c_form.zag deterministically. Pure shell.
# Usage: sh run.sh
# Produces: l3c_form_bin, run1.txt run2.txt run3.txt (mode 1),
#           run_abl.txt (mode 0), sha256sums.txt
set -u
D=$(dirname "$0")
ZNC=~/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc
cd "$D" || exit 1

"$ZNC" check l3c_form.zag --strict --no-zagd || exit 1
"$ZNC" l3c_form.zag -o l3c_form_bin --no-zagd || exit 1

./l3c_form_bin 1 > run1.txt || exit 1
./l3c_form_bin 1 > run2.txt || exit 1
./l3c_form_bin 1 > run3.txt || exit 1
./l3c_form_bin 0 > run_abl.txt || exit 1

sha256sum run1.txt run2.txt run3.txt run_abl.txt > sha256sums.txt
cat sha256sums.txt

if cmp -s run1.txt run2.txt && cmp -s run2.txt run3.txt; then
  echo "DETERMINISM_3OF3=PASS (byte-identical)"
else
  echo "DETERMINISM_3OF3=FAIL"
  exit 1
fi
