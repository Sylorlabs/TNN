#!/bin/bash
# run_ob_b.sh — build + unit-test the ONE-BRAIN variant B organs.
# Pure Zag (this script is glue only). Fails loudly on any check failure
# or any byte difference between the two runs.
set -u
ZNC="$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1"
cd "$(dirname "$0")"

fail=0
for t in fl2 pam mem arbiter; do
  echo "=== build ob_test_$t ==="
  "$ZNC" "ob_test_$t.zag" -o "ob_test_$t" 2>&1 | grep -i "error" && fail=1
  echo "=== run ob_test_$t (x2, byte-identity) ==="
  "./ob_test_$t" > "run_${t}_1.txt" 2>&1
  "./ob_test_$t" > "run_${t}_2.txt" 2>&1
  cmp -s "run_${t}_1.txt" "run_${t}_2.txt" || { echo "NOT BYTE-IDENTICAL: $t"; fail=1; }
  grep -q "^OB_FAILURES,0$" "run_${t}_1.txt" || { echo "FAILURES in $t:"; grep "^OB_FAILURES" "run_${t}_1.txt"; fail=1; }
  echo "checks: $(grep -c '^OB_CHECK' run_${t}_1.txt)  sha: $(sha256sum run_${t}_1.txt | cut -c1-16)"
done

if [ "$fail" -ne 0 ]; then echo "OB_B_RESULT,FAIL"; exit 1; fi
echo "OB_B_RESULT,PASS"
