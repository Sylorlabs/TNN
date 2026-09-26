#!/bin/bash
# build_regress.sh — degenerate-input regression: build + verify.
# Runs regress_degen.zag (empty text x all 6 position kinds) through the LIVE
# production intake. Bars: 6/6 correct, 6/6 native, 0 fallbacks, rc=0,
# byte-identical reruns x2.
set -e
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
cd "$(dirname "$0")"
mkdir -p evidence

echo "== build =="
$ZNC regress_degen.zag -o regress_bin 2>build_regress.log || { echo "BUILD FAILED"; tail -30 build_regress.log; exit 1; }
echo "build ok"

run_once() {
  rc=0
  ./regress_bin > "evidence/$1" 2>"evidence/$1.err" || rc=$?
  echo "run $1: rc=$rc sha=$(sha256sum "evidence/$1" | cut -d' ' -f1)"
  if [ "$rc" -ne 0 ]; then echo "REGRESSION FAILED: nonzero rc (panic?)"; exit 1; fi
}

run_once DEGEN1.out
run_once DEGEN2.out
echo "== byte-identical rerun check =="
cmp evidence/DEGEN1.out evidence/DEGEN2.out && echo "DEGEN1 == DEGEN2: IDENTICAL"
echo "== regression bars =="
python3 - <<'EOF'
import re
txt = open("evidence/DEGEN1.out").read()
m = re.search(r"^# DEGEN SUMMARY n=(\d+) correct=(\d+) native=(\d+) fallback=(\d+)", txt, re.M)
assert m, "DEGEN SUMMARY missing"
n, c, nat, fb = map(int, m.groups())
assert (n, c, nat, fb) == (6, 6, 6, 0), f"REGRESSION FAILED: {m.group(0)}"
assert "panic" not in txt.lower(), "panic text in output"
print(f"DEGEN REGRESSION: PASS ({c}/{n} correct, {nat}/{n} native, {fb} fallbacks, no panic)")
EOF
