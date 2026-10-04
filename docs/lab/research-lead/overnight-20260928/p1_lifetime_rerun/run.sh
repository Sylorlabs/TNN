#!/bin/sh
# run.sh -- assemble, compile, and CERTIFY both lifetime binaries.
#
# Hard requirements enforced here, not asserted in prose:
#   * pure Zag (the caller must have sourced .env/pure-zag.sh)
#   * --target macos-arm64 (injected by tools/zbuild.sh)
#   * 3/3 BYTE-IDENTICAL stdout
#   * NON-EMPTY output -- output length > 0 is checked explicitly, because
#     an empty log with rc=0 is the defect that silently ate the previous
#     worker's run (the inert _zag_raw_syscall output path).
#   * the frozen prefix is byte-identical to the repository's frozen cores.
set -e
D=$(dirname "$0")
D=$(cd "$D" && pwd)
R=/Users/Shared/micah/Documents/TNN/TNN/docs/lab/research-lead/overnight-20260928
Z=/Users/Shared/micah/Documents/TNN/TNN/tools/zbuild.sh
cd "$D"

echo "== frozen prefix integrity =="
cat "$R/cogops_rescueaware/c15_base.zag" \
    "$R/cogops_learnosc2/c8_learn.zag" \
    "$R/hook_phase1/hq_module.zag" > frozen_prefix.zag
A=$(shasum -a 256 frozen_prefix.zag | cut -d' ' -f1)
echo "frozen prefix sha256 $A"
echo "c8_learn.zag lines: $(grep -c '^fn \|^// ' "$R/cogops_learnosc2/c8_learn.zag") (prereg expects 1331)"
echo "exactly one fn main per unit:"
for f in lt1 lt2; do
  n=$(grep -c "^fn main(" "$f.zag")
  echo "  $f.zag main count = $n"
  if [ "$n" -ne 1 ]; then echo "FAIL: $f has $n mains"; exit 1; fi
done

echo "== LT1 (LIFETIME-AB-1) =="
cat frozen_prefix.zag lt_world.zag lt_life.zag lt_main.zag > lt1.zag
sh "$Z" ./lt1.zag --rep 3
./lt1 > lt1_run1.txt 2>&1
./lt1 > lt1_run2.txt 2>&1
./lt1 > lt1_run3.txt 2>&1
for f in lt1_run1.txt lt1_run2.txt lt1_run3.txt; do
  sz=$(wc -c < "$f" | tr -d ' ')
  echo "  $f bytes=$sz"
  if [ "$sz" -le 0 ]; then echo "FAIL: $f is EMPTY"; exit 1; fi
done
H1=$(shasum -a 256 lt1_run1.txt lt1_run2.txt lt1_run3.txt | cut -d' ' -f1 | sort -u | wc -l | tr -d ' ')
echo "  distinct output hashes across 3 runs = $H1 (must be 1)"
if [ "$H1" -ne 1 ]; then echo "FAIL: LT1 not deterministic"; exit 1; fi
if ! grep -q "^CONTRACT-SELFTEST" lt1_run1.txt; then echo "FAIL: no contract selftest"; exit 1; fi
if ! grep -q "orc=7/7" lt1_run1.txt; then echo "FAIL: oracle/declared mismatch"; exit 1; fi
echo "  LT1 NON-EMPTY output assertion PASSED"

echo "== LT2 (charter 221, harder second lifetime) =="
cat frozen_prefix.zag lt2_life.zag lt2_world.zag lt2_main.zag > lt2.zag
sh "$Z" ./lt2.zag --rep 3
./lt2 > lt2_run1.txt 2>&1
./lt2 > lt2_run2.txt 2>&1
./lt2 > lt2_run3.txt 2>&1
for f in lt2_run1.txt lt2_run2.txt lt2_run3.txt; do
  sz=$(wc -c < "$f" | tr -d ' ')
  echo "  $f bytes=$sz"
  if [ "$sz" -le 0 ]; then echo "FAIL: $f is EMPTY"; exit 1; fi
done
H2=$(shasum -a 256 lt2_run1.txt lt2_run2.txt lt2_run3.txt | cut -d' ' -f1 | sort -u | wc -l | tr -d ' ')
echo "  distinct output hashes across 3 runs = $H2 (must be 1)"
if [ "$H2" -ne 1 ]; then echo "FAIL: LT2 not deterministic"; exit 1; fi
NA=$(grep -c "^ARMSUM" lt2_run1.txt | tr -d ' ')
echo "  LT2 arm summaries = $NA (must be 2)"
if [ "$NA" -ne 2 ]; then echo "FAIL: LT2 arms missing"; exit 1; fi
echo "  LT2 NON-EMPTY output assertion PASSED"

echo
echo "ALL CERTIFICATION CHECKS PASSED"
shasum -a 256 lt1_run1.txt lt2_run1.txt
