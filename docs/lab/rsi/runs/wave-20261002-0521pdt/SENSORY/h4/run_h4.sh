#!/bin/bash
# run_h4.sh - H4 sealed evaluation pipeline (frozen PREREG_SENSORY_H4.md).
# Pure Zag binaries + bash only. Run from the h4/ directory.
set -u
export PATH="$HOME/safebin"
H4DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$H4DIR"
echo "=== H4 sealed run, $(date -u +%FT%TZ) ==="

echo "--- baseline gate: 2x 1024 renders must be byte-identical ---"
mkdir -p out/base1 out/base2
S1=$(date +%s); ./bin/r11_baseline out/base1 1024 > evidence/render_base1.log 2>&1; E1=$(date +%s)
S2=$(date +%s); ./bin/r11_baseline out/base2 1024 > evidence/render_base2.log 2>&1; E2=$(date +%s)
echo "base1_wall_s=$((E1-S1))" | tee -a evidence/render_base1.log
echo "base2_wall_s=$((E2-S2))" | tee -a evidence/render_base2.log
sha256sum out/base1/r11_alien_1024.bmp out/base2/r11_alien_1024.bmp | tee evidence/sha_base12.txt
if ! cmp -s out/base1/r11_alien_1024.bmp out/base2/r11_alien_1024.bmp; then
  echo "BASELINE GATE FAILED: renders differ"; exit 1
fi
echo "baseline gate PASSED"

echo "--- geometric validator on rebuilt baseline ---"
./bin/h4_verify out/base1 r11_alien_1024.bmp none | tee evidence/validator.log
if ! grep -q "VALIDATOR: PASS" evidence/validator.log; then
  echo "VALIDATOR FAILED"; exit 1
fi
echo "validator PASSED"

echo "--- H4 variant: 3x 1024 renders (H4-KB1) ---"
mkdir -p out/h4a out/h4b out/h4c
S1=$(date +%s); ./bin/h4_terrain out/h4a 1024 > evidence/render_h4a.log 2>&1; E1=$(date +%s)
S2=$(date +%s); ./bin/h4_terrain out/h4b 1024 > evidence/render_h4b.log 2>&1; E2=$(date +%s)
S3=$(date +%s); ./bin/h4_terrain out/h4c 1024 > evidence/render_h4c.log 2>&1; E3=$(date +%s)
echo "h4a_wall_s=$((E1-S1))" | tee -a evidence/render_h4a.log
echo "h4b_wall_s=$((E2-S2))" | tee -a evidence/render_h4b.log
echo "h4c_wall_s=$((E3-S3))" | tee -a evidence/render_h4c.log
sha256sum out/h4a/r11_alien_1024.bmp out/h4b/r11_alien_1024.bmp out/h4c/r11_alien_1024.bmp | tee evidence/sha_h4.txt
if ! cmp -s out/h4a/r11_alien_1024.bmp out/h4b/r11_alien_1024.bmp; then
  echo "H4-KB1 FAILED: h4a != h4b"; exit 1
fi
if ! cmp -s out/h4b/r11_alien_1024.bmp out/h4c/r11_alien_1024.bmp; then
  echo "H4-KB1 FAILED: h4b != h4c"; exit 1
fi
echo "H4-KB1 PASSED: 3/3 byte-identical"

echo "--- H4 kill bars (base1 vs h4a) ---"
mkdir -p out/kb
cp out/base1/r11_alien_1024.bmp out/kb/base.bmp
cp out/h4a/r11_alien_1024.bmp out/kb/h4.bmp
./bin/h4_verify out/kb base.bmp h4.bmp | tee evidence/killbars.log
echo "=== H4 sealed run complete ==="
