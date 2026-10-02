#!/bin/bash
# run_h3.sh - H3 SUN-ANCHORED SKY-DOME LUMINANCE GRADIENT wave pipeline
# (prereg SENSORY-H3, frozen bars KB1..KB11). Pure Zag + bash only.
# Run from the h3/ directory with safebin PATH. Lane:
# docs/lab/rsi/runs/wave-20261002-0221pdt/SENSORY/h3/
set -u
H3DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$H3DIR"
echo "=== H3 pipeline, $(date -u +%FT%TZ) ==="
echo "--- baseline gate: 2x 1024 renders must be byte-identical ---"
mkdir -p out/base1 out/base2
S1=$(date +%s); ./bin/r11_baseline out/base1 1024 > evidence/render_base1.log 2>&1; E1=$(date +%s)
S2=$(date +%s); ./bin/r11_baseline out/base2 1024 > evidence/render_base2.log 2>&1; E2=$(date +%s)
echo "base1_wall=$((E1-S1))s" >> evidence/render_base1.log
echo "base2_wall=$((E2-S2))s" >> evidence/render_base2.log
sha256sum out/base1/r11_alien_1024.bmp out/base2/r11_alien_1024.bmp | tee evidence/sha_base12.txt
if ! cmp -s out/base1/r11_alien_1024.bmp out/base2/r11_alien_1024.bmp; then
  echo "BASELINE GATE (b) FAILED: renders differ"; exit 1
fi
echo "baseline gate (b) PASSED"
echo "--- geometric validator on rebuilt baseline ---"
./bin/h3_verify out/base1 r11_alien_1024.bmp none | tee evidence/validator.log
echo "--- H3 variant: 3x 1024 renders (KB1) ---"
mkdir -p out/h3a out/h3b out/h3c
S1=$(date +%s); ./bin/h3_dome out/h3a 1024 > evidence/render_h3a.log 2>&1; E1=$(date +%s)
S2=$(date +%s); ./bin/h3_dome out/h3b 1024 > evidence/render_h3b.log 2>&1; E2=$(date +%s)
S3=$(date +%s); ./bin/h3_dome out/h3c 1024 > evidence/render_h3c.log 2>&1; E3=$(date +%s)
echo "h3a_wall=$((E1-S1))s" >> evidence/render_h3a.log
echo "h3b_wall=$((E2-S2))s" >> evidence/render_h3b.log
echo "h3c_wall=$((E3-S3))s" >> evidence/render_h3c.log
sha256sum out/h3a/r11_alien_1024.bmp out/h3b/r11_alien_1024.bmp out/h3c/r11_alien_1024.bmp | tee evidence/sha_h3.txt
if ! cmp -s out/h3a/r11_alien_1024.bmp out/h3b/r11_alien_1024.bmp; then
  echo "KB1-DET FAILED: h3a != h3b"; exit 1
fi
if ! cmp -s out/h3b/r11_alien_1024.bmp out/h3c/r11_alien_1024.bmp; then
  echo "KB1-DET FAILED: h3b != h3c"; exit 1
fi
echo "KB1-DET PASSED: 3/3 byte-identical"
echo "--- kill bars KB2..KB11 (base1 vs h3a) ---"
mkdir -p out/kb
cp out/base1/r11_alien_1024.bmp out/kb/base.bmp
cp out/h3a/r11_alien_1024.bmp out/kb/h3a.bmp
./bin/h3_verify out/kb base.bmp h3a.bmp | tee evidence/killbars.log
echo "=== pipeline done ==="
