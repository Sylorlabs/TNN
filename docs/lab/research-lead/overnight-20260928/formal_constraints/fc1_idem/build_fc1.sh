#!/bin/sh
# build_fc1.sh: compile fc1.zag with pinned safebin znc, run 3x,
# verify K-FC-6 (3/3 byte-identical, exit 0, zero FAIL lines).
# Pure shell. No Python. Binary lives in /tmp (never committed).
export PATH="$HOME/safebin"
D="$HOME/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/formal_constraints/fc1_idem"
cd "$HOME/workspace/tnn-rsi" || exit 1
echo "toolchain: znc=$(which znc) python3=[$(which python3)]"
znc -o /tmp/fc1_bin "$D/fc1.zag" || exit 1
/tmp/fc1_bin > "$D/fc1_run1.txt"; c1=$?
/tmp/fc1_bin > "$D/fc1_run2.txt"; c2=$?
/tmp/fc1_bin > "$D/fc1_run3.txt"; c3=$?
echo "exit codes: $c1 $c2 $c3"
if cmp -s "$D/fc1_run1.txt" "$D/fc1_run2.txt" && cmp -s "$D/fc1_run2.txt" "$D/fc1_run3.txt"; then
  echo "byte-identical: yes"
  cm=0
else
  echo "byte-identical: NO"
  cm=1
fi
sha256sum "$D/fc1_run1.txt" | tee "$D/fc1_sha256.txt"
fails=$(grep -c FAIL "$D/fc1_run1.txt")
echo "FAIL lines: $fails"
if [ "$c1" -eq 0 ] && [ "$c2" -eq 0 ] && [ "$c3" -eq 0 ] && [ "$cm" -eq 0 ] && [ "$fails" -eq 0 ]; then
  echo "K-FC-6 PASS" | tee "$D/fc1_kfc6.txt"
else
  echo "K-FC-6 FAIL" | tee "$D/fc1_kfc6.txt"
  exit 1
fi
