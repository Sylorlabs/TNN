#!/bin/bash
# build.sh — production intake build + full verification (learned policy v2).
# The learned chunking policy (frozen, derived from 9 chunkers x 57 questions)
# is now the live text-intake path. Fixed C/W/S arms are NOT in this build;
# they survive only in negcontrol.zag as retired negative controls.
#
# Usage: ./build.sh            (build battery1_bin, run once -> evidence/RUN_LIVE1.out)
#        ./build.sh verify     (rerun -> RUN_LIVE2.out, cmp; rebuild-from-source check)
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
  rm -f "evidence/$1.err"
}

if [ "$1" = "verify" ]; then
  run_once RUN_LIVE2.out
  echo "== byte-identical rerun check =="
  cmp evidence/RUN_LIVE1.out evidence/RUN_LIVE2.out && echo "RUN_LIVE1 == RUN_LIVE2: IDENTICAL"
  echo "== rebuild-from-source check =="
  rm -f battery1_bin
  $ZNC battery1.zag -o battery1_bin 2>build.log || { echo "REBUILD FAILED"; tail -30 build.log; exit 1; }
  ./battery1_bin > evidence/RUN_LIVE3.out 2>/dev/null
  cmp evidence/RUN_LIVE1.out evidence/RUN_LIVE3.out && echo "rebuild reproduces RUN_LIVE1: IDENTICAL"
  rm -f evidence/RUN_LIVE3.out
else
  run_once RUN_LIVE1.out
fi
echo "== production regression bars =="
python3 - <<'EOF'
import re
for line in open("evidence/RUN_LIVE1.out"):
    m = re.match(r"^# LIVE SUMMARY n=(\d+) correct=(\d+) native=(\d+) fallback=(\d+)", line)
    if m:
        n, c, nat, fb = map(int, m.groups())
        print(f"questions={n} correct={c} native={nat} fallbacks={fb}")
        assert (n, c, nat, fb) == (57, 57, 57, 0), "REGRESSION GATE FAILED"
        print("REGRESSION GATE: PASS (57/57 correct, 57/57 native, 0 fallbacks)")
        break
else:
    raise SystemExit("LIVE SUMMARY line missing: REGRESSION GATE FAILED")
EOF
