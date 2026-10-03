#!/bin/sh
# e8_run.sh -- BATTERY-E8 runner. Shell only: hash checks, fresh-state runs
# of the frozen binary, manifest. No transcript transformation, no logic
# keyed on world ids, subjects, relations, or CHOICE values; the section 3
# decision rule is applied as a byte comparison of the CHOICE lines.
# Usage: sh e8_run.sh
set -u
LANE=docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-E8
SHIM=docs/lab/research-lead/overnight-20260928/core_freeze_tnn2_shim/freeze_shim2_bin
TNN2=docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag
SHIM_WANT=9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954
TNN2_WANT=a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd
PREREG=docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-E8/PREREG_E8.md
PREREG_WANT=aa5f09a9d02902c482d1108bc2c53ac9abf82bb916c203c5a6e7b184448d071b

check_hash() {
  got=$(sha256sum "$1" | cut -d' ' -f1)
  if [ "$got" != "$2" ]; then
    echo "HASH-MISMATCH $1 want=$2 got=$got"
    exit 1
  fi
  echo "HASH-OK $1"
}

echo "== E8-K1 prereg hash =="
check_hash "$PREREG" "$PREREG_WANT"
echo "== E8-K3 pre-run frozen binary check =="
check_hash "$SHIM" "$SHIM_WANT"
check_hash "$TNN2" "$TNN2_WANT"
echo "== E8-K6 anti-smuggling (frozen sources, E8 id set) =="
if grep -r "84001\|84101\|84011\|84002\|84102\|84012\|84003\|84103\|84013\|84004\|84104\|84014\|84005\|84105\|84015\|84021\|84121\|84031" \
    docs/lab/research-lead/overnight-20260928/tnn2_build/ \
    docs/lab/research-lead/overnight-20260928/core_freeze_tnn2_shim/ 2>/dev/null; then
  echo "LEAK-FOUND"; exit 1
fi
echo "E8-K6 PASS (zero matches)"
echo "== E8-K4 manifest =="
(cd "$LANE" && sha256sum e8_worlds/e8_a_world.txt e8_worlds/e8_b_world.txt \
  e8_worlds/e8_c0_world.txt e8_worlds/e8_c1_world.txt > e8_worlds/E8_MANIFEST.sha256 && cat e8_worlds/E8_MANIFEST.sha256)
echo "== runs (3 fresh-state runs per world) =="
for w in a b c0 c1; do
  for n in 1 2 3; do
    st="$LANE/e8_runs/e8_${w}_r${n}.bin"
    tr="$LANE/e8_runs/e8_${w}_r${n}.trans"
    rm -f "$st"
    "./$SHIM" "$LANE/e8_worlds/e8_${w}_world.txt" "$st" > "$tr"
    rc=$?
    if [ $rc -ne 0 ]; then echo "RUN-FAILED $w r$n rc=$rc"; exit 1; fi
    echo "RUN-OK e8_${w}_r${n} exit=0"
  done
done
echo "== E8-K3 post-run frozen binary check =="
check_hash "$SHIM" "$SHIM_WANT"
check_hash "$TNN2" "$TNN2_WANT"
echo "== transcript hashes (E8-K2) =="
(cd "$LANE/e8_runs" && sha256sum e8_a_r1.trans e8_a_r2.trans e8_a_r3.trans \
  e8_b_r1.trans e8_b_r2.trans e8_b_r3.trans \
  e8_c0_r1.trans e8_c0_r2.trans e8_c0_r3.trans \
  e8_c1_r1.trans e8_c1_r2.trans e8_c1_r3.trans | tee E8_TRANS_SHA256.txt)
echo "== CHOICE lines per run =="
for w in a b c0 c1; do
  for n in 1 2 3; do
    printf "e8_%s_r%s: " "$w" "$n"
    grep '^CHOICE ' "$LANE/e8_runs/e8_${w}_r${n}.trans" | tr '\n' ';'
    printf '\n'
  done
done
echo "== E8-K2 within-world byte identity and single CHOICE line =="
for w in a b c0 c1; do
  if cmp -s "$LANE/e8_runs/e8_${w}_r1.trans" "$LANE/e8_runs/e8_${w}_r2.trans" && \
     cmp -s "$LANE/e8_runs/e8_${w}_r1.trans" "$LANE/e8_runs/e8_${w}_r3.trans"; then
    echo "E8-K2 PASS e8_$w (3/3 byte-identical)"
  else
    echo "E8-K2 FAIL e8_$w"; exit 1
  fi
  nl=$(grep -c '^CHOICE ' "$LANE/e8_runs/e8_${w}_r1.trans")
  if [ "$nl" = "1" ]; then
    echo "E8-K2 PASS e8_$w (exactly one CHOICE line)"
  else
    echo "E8-K2 FAIL e8_$w (CHOICE lines: $nl)"; exit 1
  fi
done
echo "== section 3 decision rule (byte comparison of CHOICE lines) =="
ca=$(grep '^CHOICE ' "$LANE/e8_runs/e8_a_r1.trans")
cb=$(grep '^CHOICE ' "$LANE/e8_runs/e8_b_r1.trans")
cc0=$(grep '^CHOICE ' "$LANE/e8_runs/e8_c0_r1.trans")
cc1=$(grep '^CHOICE ' "$LANE/e8_runs/e8_c1_r1.trans")
echo "E8-A CHOICE: [$ca]"
echo "E8-B CHOICE: [$cb]"
echo "E8-C0 CHOICE: [$cc0]"
echo "E8-C1 CHOICE: [$cc1]"
if [ "$ca" != "$cb" ]; then
  echo "SIGNATURE-BANDWIDTH-SUFFICIENT (CHOICE lines differ)"
else
  echo "SIGNATURE-STILL-BLIND (CHOICE lines byte-identical)"
fi
echo "== E8-K5 block calibration =="
k5=0
if [ "$cc0" = "CHOICE 0" ]; then echo "E8-K5 PASS e8_c0 (CHOICE 0)"; else echo "E8-K5 FAIL e8_c0 [$cc0]"; k5=1; fi
if [ "$cc1" = "CHOICE 0" ]; then echo "E8-K5 PASS e8_c1 (CHOICE 0)"; else echo "E8-K5 FAIL e8_c1 [$cc1]"; k5=1; fi
if [ "$ca" = "CHOICE 30" ]; then echo "E8-K5 PASS e8_a (CHOICE 30)"; else echo "E8-K5 FAIL e8_a [$ca]"; k5=1; fi
if [ "$k5" != "0" ]; then echo "E8-K5 CALIBRATION FAILED: comparison void"; exit 1; fi
echo E8-RUN-DONE
