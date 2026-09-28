#!/bin/bash
# build.sh — next-wall fresh battery build + verification.
# battery2.zag runs 26 NEVER-SEEN traps through the FROZEN production intake
# (../mg_chunking_promote/intake.zag). The policy was NOT re-derived or tuned
# for this battery: every oracle was fixed by the generator before the first run.
# Usage: ./build.sh            (build wall_bin, run once -> evidence/WALL1.out)
#        ./build.sh verify     (rerun -> WALL2.out, cmp byte-identical)
set -e
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
cd "$(dirname "$0")"
mkdir -p evidence

echo "== build =="
$ZNC battery2.zag -o wall_bin 2>build.log || { echo "BUILD FAILED"; tail -30 build.log; exit 1; }
echo "build ok"

run_once() {
  rc=0
  ./wall_bin > "evidence/$1" 2>"evidence/$1.err" || rc=$?
  echo "run $1: rc=$rc sha=$(sha256sum "evidence/$1" | cut -d' ' -f1)"
  if [ "$rc" -ne 0 ]; then echo "(nonzero rc is the known deterministic W25 panic; see VERDICT.md)"; fi
}

if [ "$1" = "verify" ]; then
  run_once WALL2.out
  echo "== byte-identical rerun check =="
  cmp evidence/WALL1.out evidence/WALL2.out && echo "WALL1 == WALL2: IDENTICAL"
else
  run_once WALL1.out
fi
echo "== wall score =="
python3 - <<'EOF'
import re
txt = open("evidence/WALL1.out").read()
oks = len(re.findall(r'^INTAKER .*correct=1', txt, re.M))
tot = len(re.findall(r'^INTAKER ', txt, re.M))
print(f"answered={tot} correct={oks}")
EOF
