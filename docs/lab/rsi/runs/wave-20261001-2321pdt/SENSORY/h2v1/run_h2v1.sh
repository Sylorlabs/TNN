#!/bin/bash
# run_h2v1.sh - H2v1 FORWARD-SCATTER DECK FIELD wave pipeline
# (prereg SENSORY-H2V1, frozen bars KB1..KB11). Pure Zag + bash only.
# Run from the h2v1/ directory with safebin PATH. Lane:
# docs/lab/rsi/runs/wave-20261001-2321pdt/SENSORY/h2v1/
set -u
H2V1DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$H2V1DIR"
echo "=== H2v1 pipeline, $(date -u +%FT%TZ) ==="
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
./bin/h2v1_verify out/base1 r11_alien_1024.bmp none | tee evidence/validator.log
echo "--- H2v1 variant: 3x 1024 renders (KB1) ---"
mkdir -p out/h2v1a out/h2v1b out/h2v1c
S1=$(date +%s); ./bin/h2v1_clouds out/h2v1a 1024 > evidence/render_h2v1a.log 2>&1; E1=$(date +%s)
S2=$(date +%s); ./bin/h2v1_clouds out/h2v1b 1024 > evidence/render_h2v1b.log 2>&1; E2=$(date +%s)
S3=$(date +%s); ./bin/h2v1_clouds out/h2v1c 1024 > evidence/render_h2v1c.log 2>&1; E3=$(date +%s)
echo "h2v1a_wall=$((E1-S1))s" >> evidence/render_h2v1a.log
echo "h2v1b_wall=$((E2-S2))s" >> evidence/render_h2v1b.log
echo "h2v1c_wall=$((E3-S3))s" >> evidence/render_h2v1c.log
sha256sum out/h2v1a/h2v1_clouds_1024.bmp out/h2v1b/h2v1_clouds_1024.bmp out/h2v1c/h2v1_clouds_1024.bmp | tee evidence/sha_h2v1.txt
echo "--- kill bars KB2..KB11 ---"
cp out/base1/r11_alien_1024.bmp out/h2v1a/r11_alien_1024.bmp
./bin/h2v1_verify out/h2v1a r11_alien_1024.bmp h2v1_clouds_1024.bmp | tee evidence/killbars.log
echo "=== pipeline done ==="
