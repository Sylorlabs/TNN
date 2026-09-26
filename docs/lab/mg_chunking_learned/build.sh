#!/bin/bash
# build.sh — Phase-2 learned chunking: generate base, build, derive, verify.
# Usage: ./build.sh            (generate + build + run -> evidence/RUN_D1.out)
#        ./build.sh verify     (rerun -> RUN_D2.out, cmp; rebuild-from-source check)
set -e
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
cd "$(dirname "$0")"
mkdir -p evidence

echo "== generate base.zag from frozen fork =="
python3 gen_phase2.py

echo "== build =="
$ZNC derive.zag -o derive_bin 2>build.log || { echo "BUILD FAILED"; tail -30 build.log; exit 1; }
echo "build ok"

run_once() {
  ./derive_bin > "evidence/$1" 2>"evidence/$1.err"
  echo "run $1: $(sha256sum "evidence/$1" | cut -d' ' -f1)"
}

if [ "$1" = "verify" ]; then
  run_once RUN_D2.out
  echo "== byte-identical rerun check =="
  cmp evidence/RUN_D1.out evidence/RUN_D2.out && echo "R1 == R2: IDENTICAL"
  echo "== rebuild-from-source check =="
  rm -f derive_bin
  python3 gen_phase2.py
  $ZNC derive.zag -o derive_bin 2>build.log || { echo "REBUILD FAILED"; tail -30 build.log; exit 1; }
  ./derive_bin > evidence/RUN_D3.out 2>evidence/RUN_D3.out.err
  cmp evidence/RUN_D1.out evidence/RUN_D3.out && echo "rebuild reproduces R1: IDENTICAL"
  rm -f evidence/RUN_D3.out evidence/RUN_D3.out.err
else
  run_once RUN_D1.out
fi
echo "== learned-intake bars =="
python3 - <<'EOF'
import re
txt = open("evidence/RUN_D1.out").read()
m = re.search(r"^# LIVE SUMMARY n=(\d+) correct=(\d+) native=(\d+) fallback=(\d+)", txt, re.M)
assert m, "no LIVE SUMMARY"
n, c, nat, fb = map(int, m.groups())
assert c == n and nat == n and fb == 0, f"bars failed: {m.group(0)}"
v = re.search(r"^# VERDICT (.*)", txt, re.M)
print(f"LEARNED INTAKE: {c}/{n} correct, {nat}/{n} native, {fb} fallbacks — {v.group(1)}")
EOF
