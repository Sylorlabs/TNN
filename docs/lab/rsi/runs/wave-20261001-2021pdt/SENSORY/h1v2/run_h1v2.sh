#!/bin/bash
# run_h1v2.sh - H1v2 TRANSPORT-ANCHORED LIT CLOUD DECK wave pipeline
# (prereg SENSORY-H1V2, frozen bars KB1..KB11). Pure Zag + bash only.
# Run from the h1v2/ directory with safebin PATH. Lane:
# docs/lab/rsi/runs/wave-20261001-2021pdt/SENSORY/h1v2/
set -u
H1V2DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$H1V2DIR"
echo "=== H1v2 pipeline, $(date -u +%FT%TZ) ==="
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
./bin/h1v2_verify out/base1 r11_alien_1024.bmp none | tee evidence/validator.log
echo "--- H1v2 variant: 3x 1024 renders (KB1) ---"
mkdir -p out/h1v2a out/h1v2b out/h1v2c
S1=$(date +%s); ./bin/h1v2_clouds out/h1v2a 1024 > evidence/render_h1v2a.log 2>&1; E1=$(date +%s)
S2=$(date +%s); ./bin/h1v2_clouds out/h1v2b 1024 > evidence/render_h1v2b.log 2>&1; E2=$(date +%s)
S3=$(date +%s); ./bin/h1v2_clouds out/h1v2c 1024 > evidence/render_h1v2c.log 2>&1; E3=$(date +%s)
echo "h1v2a_wall=$((E1-S1))s" >> evidence/render_h1v2a.log
echo "h1v2b_wall=$((E2-S2))s" >> evidence/render_h1v2b.log
echo "h1v2c_wall=$((E3-S3))s" >> evidence/render_h1v2c.log
sha256sum out/h1v2a/h1v2_clouds_1024.bmp out/h1v2b/h1v2_clouds_1024.bmp out/h1v2c/h1v2_clouds_1024.bmp | tee evidence/sha_h1v2.txt
echo "--- kill bars KB2..KB11 ---"
cp out/base1/r11_alien_1024.bmp out/h1v2a/r11_alien_1024.bmp
./bin/h1v2_verify out/h1v2a r11_alien_1024.bmp h1v2_clouds_1024.bmp | tee evidence/killbars.log
echo "=== pipeline done ==="
