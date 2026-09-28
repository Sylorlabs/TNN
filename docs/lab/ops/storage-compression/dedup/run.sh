#!/bin/bash
# Reproduce the duplicate-fact investigation end to end.
# Builds dd_main with the pinned toolchain, runs all five modes, and
# byte-compares fresh outputs against the committed evidence files.
set -e
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
D=~/workspace/tnn-lab/ops/storage-compression/dedup
cd "$D/src"
"$ZNC" dd_main.zag -o dd_main --no-analyze 2>&1 | grep -v zagd || true
./dd_main scan  > "$D/out_scan.txt"  2>&1
./dd_main prove > "$D/out_prove.txt" 2>&1
./dd_main exp1 1 > "$D/out_exp1_p1.txt" 2>&1
./dd_main exp1 5 > "$D/out_exp1_p5.txt" 2>&1
./dd_main exp2  > "$D/out_exp2.txt"  2>&1
# strip run-added marker lines before comparing
strip() { grep -v -E '^(DONE|EXIT=)' "$1"; }
ok=1
for m in scan prove exp1_p1 exp1_p5 exp2; do
  if cmp -s <(strip "$D/out_$m.txt") <(strip "$D/run_$m.txt"); then
    echo "$m: MATCHES committed evidence"
  else
    echo "$m: DIFFERS from committed evidence"; ok=0
  fi
done
rm -f "$D/out_"*.txt
[ $ok -eq 1 ] && echo ALL_MODES_REPRODUCED || { echo REPRODUCTION_MISMATCH; exit 1; }
