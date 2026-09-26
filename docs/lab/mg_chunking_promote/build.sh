#!/bin/bash
# build.sh — Phase-1 promotion build + full verification.
# Usage: ./build.sh            (builds battery1_bin, runs once -> evidence/RUN_R1.out)
#        ./build.sh verify     (rerun -> RUN_R2.out, cmp; rebuild-from-source check)
set -e
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
cd "$(dirname "$0")"
mkdir -p evidence

echo "== build =="
$ZNC battery1.zag -o battery1_bin 2>build.log || { echo "BUILD FAILED"; tail -30 build.log; exit 1; }
echo "build ok"

run_once() {
  ./battery1_bin > "evidence/$1" 2>"evidence/$1.err"
  echo "run $1: $(sha256sum "evidence/$1" | cut -d' ' -f1)"
}

if [ "$1" = "verify" ]; then
  run_once RUN_R2.out
  echo "== byte-identical rerun check =="
  cmp evidence/RUN_R1.out evidence/RUN_R2.out && echo "R1 == R2: IDENTICAL"
  echo "== rebuild-from-source check =="
  rm -f battery1_bin
  $ZNC battery1.zag -o battery1_bin 2>build.log || { echo "REBUILD FAILED"; tail -30 build.log; exit 1; }
  ./battery1_bin > evidence/RUN_R3.out 2>evidence/RUN_R3.err
  cmp evidence/RUN_R1.out evidence/RUN_R3.out && echo "rebuild reproduces R1: IDENTICAL"
  rm -f evidence/RUN_R3.out evidence/RUN_R3.err
else
  run_once RUN_R1.out
fi
echo "== LIVE-path bars =="
grep -E '^LIVE ' evidence/RUN_R1.out | awk '{c+=$4~/correct=24/; n+=$6~/native=24/} END {}' || true
python3 - <<'EOF'
import re
tot_c = tot_n = 0
for line in open("evidence/RUN_R1.out"):
    m = re.match(r"^LIVE \S+ n=(\d+) correct=(\d+) native=(\d+)", line)
    if m:
        n, c, nat = map(int, m.groups())
        assert c == n and nat == n, "LIVE bar failed: " + line
        tot_c += c; tot_n += nat
print(f"LIVE: {tot_c}/24 correct, {tot_n}/24 native — PROMOTION BARS PASS")
EOF
