#!/bin/bash
# run_h5.sh -- H5 sealed evaluation battery (frozen PREREG_H5.md).
# Pure Zag, safebin only. No Python.
export PATH="$HOME/safebin"
set -u
cd "$(dirname "$0")"
BIN=bin
OUT=out/battery
EV=evidence
mkdir -p "$OUT" "$EV" out/base1 out/base2 out/var1 out/var2 out/var3

echo "which python3: [$(which python3)]"
echo "which znc: [$(which znc)]"
sha256sum $BIN/r11_baseline $BIN/h5_terrain $BIN/h5_verify | tee $EV/bin.sha256
sha256sum r11_baseline.zag h5_terrain.zag h5_verify.zag h5_funcs_block.txt | tee $EV/src.sha256

# H5-KB1: baseline determinism gate, 2x1024 byte-identical
S=$(date +%s); ./$BIN/r11_baseline out/base1 1024 > $EV/render_base1.log 2>&1; E=$(date +%s)
BASE1_WALL=$((E-S)); echo "base1_wall_s=$BASE1_WALL"
S=$(date +%s); ./$BIN/r11_baseline out/base2 1024 > $EV/render_base2.log 2>&1; E=$(date +%s)
BASE2_WALL=$((E-S)); echo "base2_wall_s=$BASE2_WALL"
sha256sum out/base1/r11_alien_1024.bmp out/base2/r11_alien_1024.bmp | tee $EV/base.sha256
cmp out/base1/r11_alien_1024.bmp out/base2/r11_alien_1024.bmp && echo "H5KB1: BASELINE BYTE-IDENTICAL x2 PASS" || echo "H5KB1: FAIL"

# Geometric validator on the rebuilt baseline (no variant)
./$BIN/h5_verify out/base1 r11_alien_1024.bmp none | tee $EV/validator_base.txt
echo "validator_exit=$?"

# 3x1024 H5 variant renders
for r in 1 2 3; do
  S=$(date +%s); ./$BIN/h5_terrain out/var$r 1024 > $EV/render_var$r.log 2>&1; E=$(date +%s)
  echo "var${r}_wall_s=$((E-S))"
done
sha256sum out/var1/r11_alien_1024.bmp out/var2/r11_alien_1024.bmp out/var3/r11_alien_1024.bmp | tee $EV/var.sha256
cmp out/var1/r11_alien_1024.bmp out/var2/r11_alien_1024.bmp && cmp out/var1/r11_alien_1024.bmp out/var3/r11_alien_1024.bmp && echo "VARIANT BYTE-IDENTICAL x3" || echo "VARIANT NONDETERMINISM"

# Kill bars: base vs variant (use var1)
mkdir -p out/kbpair
cp out/base1/r11_alien_1024.bmp out/kbpair/base.bmp
cp out/var1/r11_alien_1024.bmp out/kbpair/var.bmp
./$BIN/h5_verify out/kbpair base.bmp var.bmp | tee $EV/killbars.txt
echo "killbars_exit=$?"
echo "BATTERY DONE"
