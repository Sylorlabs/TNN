#!/bin/bash
# run_h1.sh - H1 LIT CLOUD DECK wave pipeline (prereg H1-CLOUDS-1721).
# Pure Zag + bash only. Run from the h1/ directory with safebin PATH.
set -u
H1DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$H1DIR"
echo "=== H1 pipeline, $(date -u +%FT%TZ) ==="
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
./bin/h1_verify out/base1 r11_alien_1024.bmp none | tee evidence/validator.log
echo "--- H1 variant: 3x 1024 renders (KB1) ---"
mkdir -p out/h1a out/h1b out/h1c
S1=$(date +%s); ./bin/h1_clouds out/h1a 1024 > evidence/render_h1a.log 2>&1; E1=$(date +%s)
S2=$(date +%s); ./bin/h1_clouds out/h1b 1024 > evidence/render_h1b.log 2>&1; E2=$(date +%s)
S3=$(date +%s); ./bin/h1_clouds out/h1c 1024 > evidence/render_h1c.log 2>&1; E3=$(date +%s)
echo "h1a_wall=$((E1-S1))s" >> evidence/render_h1a.log
echo "h1b_wall=$((E2-S2))s" >> evidence/render_h1b.log
echo "h1c_wall=$((E3-S3))s" >> evidence/render_h1c.log
sha256sum out/h1a/h1_clouds_1024.bmp out/h1b/h1_clouds_1024.bmp out/h1c/h1_clouds_1024.bmp | tee evidence/sha_h1.txt
echo "--- kill bars KB2..KB8 ---"
cp out/base1/r11_alien_1024.bmp out/h1a/r11_alien_1024.bmp
./bin/h1_verify out/h1a r11_alien_1024.bmp h1_clouds_1024.bmp | tee evidence/killbars.log
echo "=== pipeline done ==="
