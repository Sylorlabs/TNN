#!/bin/bash
# build.sh — Arm D build + K5/K6 verification (native-authorship trial 1).
#
# Usage: ./build.sh            (build battery_d_bin, run once -> evidence/RUN_D1.out)
#        ./build.sh verify     (rerun -> RUN_D2.out, cmp; rebuild-from-source check)
set -e
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
cd "$(dirname "$0")"
mkdir -p evidence

echo "== build =="
$ZNC battery_d.zag -o battery_d_bin 2>build.log || { echo "BUILD FAILED"; tail -30 build.log; exit 1; }
echo "build ok"

run_once() {
  ./battery_d_bin > "evidence/$1" 2>"evidence/$1.err"
  echo "run $1: $(sha256sum "evidence/$1" | cut -d' ' -f1)"
  rm -f "evidence/$1.err"
}

if [ "$1" = "verify" ]; then
  run_once RUN_D2.out
  echo "== byte-identical rerun check =="
  cmp evidence/RUN_D1.out evidence/RUN_D2.out && echo "RUN_D1 == RUN_D2: IDENTICAL"
  echo "== rebuild-from-source check =="
  rm -f battery_d_bin
  $ZNC battery_d.zag -o battery_d_bin 2>build.log || { echo "REBUILD FAILED"; tail -30 build.log; exit 1; }
  ./battery_d_bin > evidence/RUN_D3.out 2>/dev/null
  cmp evidence/RUN_D1.out evidence/RUN_D3.out && echo "rebuild reproduces RUN_D1: IDENTICAL"
  rm -f evidence/RUN_D3.out
else
  run_once RUN_D1.out
fi
echo "== K5 regression bar (57/57 correct) =="
python3 - <<'EOF'
import re
for line in open("evidence/RUN_D1.out"):
    m = re.match(r"^# LIVE SUMMARY n=(\d+) correct=(\d+) native=(\d+) fallback=(\d+)", line)
    if m:
        n, c, nat, fb = map(int, m.groups())
        print(f"questions={n} correct={c} native={nat} fallbacks={fb}")
        assert (n, c) == (57, 57), "K5 FAILED"
        print("K5: PASS (57/57 correct on the frozen battery)")
        break
else:
    raise SystemExit("LIVE SUMMARY line missing: K5 FAILED")
EOF
