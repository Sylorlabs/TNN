#!/bin/bash
# Reproduction: builds the fixed intake + both batteries, runs each twice,
# and checks byte-identical output + expected scores.
# Pure Zag, zero RNG. Binaries are built in a scratch dir (never committed).
set -u
ZNC="${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}"
HERE="$(cd "$(dirname "$0")" && pwd)"
SCRATCH="${SCRATCH:-$HOME/workspace/tmp_commit/chunking_repro}"
EXP_WALL="cd86da4355b6e059ea829c63ca41de63e4d7d0a0fea84773d661c1827f1be24b"
EXP_PROD="170bacd71ba5f57c79be20786978964bbb094117e452b1a00d5289cbca351a23"
EXP_DEGEN="42fcb2c5e9eb138dab2838c22dd57453024c095ba88704a33e23870dcf0387ed"
mkdir -p "$SCRATCH"
cp "$HERE/intake.zag" "$HERE/battery1.zag" "$HERE/battery2.zag" "$HERE/battery3.zag" \
   "$HERE/R33_NATIVE_IO_V1.zag" "$SCRATCH/"
cd "$SCRATCH" || exit 1
fail=0
check() { # name expected_sha f1 f2
  s1=$(sha256sum "$3" | cut -d' ' -f1); s2=$(sha256sum "$4" | cut -d' ' -f1)
  if [ "$s1" != "$2" ] || [ "$s2" != "$2" ]; then
    echo "FAIL $1: got $s1 / $s2, want $2"; fail=1
  else echo "OK $1 sha=$s1"; fi
}
"$ZNC" battery2.zag -o wall_bin || { echo "wall build failed"; exit 1; }
./wall_bin > W1.out; ./wall_bin > W2.out
check wall "$EXP_WALL" W1.out W2.out
wok=$(grep -c 'INTAKER.*correct=1' W1.out); wtot=$(grep -c 'INTAKER' W1.out)
[ "$wok" = 26 ] && [ "$wtot" = 26 ] && echo "OK wall score 26/26" \
  || { echo "FAIL wall score $wok/$wtot"; fail=1; }
"$ZNC" battery1.zag -o prod_bin || { echo "prod build failed"; exit 1; }
./prod_bin > P1.out; ./prod_bin > P2.out
check production "$EXP_PROD" P1.out P2.out
pok=$(grep -c 'INTAKER.*correct=1' P1.out); ptot=$(grep -c 'INTAKER' P1.out)
[ "$pok" = 57 ] && [ "$ptot" = 57 ] && echo "OK production score 57/57" \
  || { echo "FAIL production score $pok/$ptot"; fail=1; }
"$ZNC" battery3.zag -o degen_bin || { echo "degen build failed"; exit 1; }
./degen_bin > D1.out; ./degen_bin > D2.out
check degenerate "$EXP_DEGEN" D1.out D2.out
dok=$(grep -c 'INTAKER.*correct=1' D1.out); dtot=$(grep -c 'INTAKER' D1.out)
[ "$dok" = 41 ] && [ "$dtot" = 41 ] && echo "OK degenerate score 41/41 (zero panics)" \
  || { echo "FAIL degenerate score $dok/$dtot"; fail=1; }
[ "$fail" = 0 ] && echo "ALL CHECKS PASSED" || { echo "CHECKS FAILED"; exit 1; }
