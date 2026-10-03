#!/bin/sh
# e2_run.sh -- BATTERY-E2 runner. Shell only: hash checks, fresh-state runs
# of the frozen binary, manifest. No transcript transformation, no logic
# keyed on world ids, subjects, relations, or CHOICE values; the section 3
# decision rule is applied as a byte comparison of the CHOICE lines.
# Usage: sh e2_run.sh
set -u
LANE=docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-E2
SHIM=docs/lab/research-lead/overnight-20260928/core_freeze_tnn2_shim/freeze_shim2_bin
TNN2=docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag
SHIM_WANT=9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954
TNN2_WANT=a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd
PREREG=docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-E2/PREREG_E2.md

check_hash() {
  got=$(sha256sum "$1" | cut -d' ' -f1)
  if [ "$got" != "$2" ]; then
    echo "HASH-MISMATCH $1 want=$2 got=$got"
    exit 1
  fi
  echo "HASH-OK $1"
}

echo "== E2-K1 prereg hash =="
sha256sum "$PREREG"
echo "== E2-K3 pre-run frozen binary check =="
check_hash "$SHIM" "$SHIM_WANT"
check_hash "$TNN2" "$TNN2_WANT"
echo "== E2-K6 anti-smuggling (frozen sources, E2 id set) =="
if grep -r "81001\|81101\|81011\|82001\|82002\|82101\|82102\|82011\|82012" \
    docs/lab/research-lead/overnight-20260928/tnn2_build/ \
    docs/lab/research-lead/overnight-20260928/core_freeze_tnn2_shim/ 2>/dev/null; then
  echo "LEAK-FOUND"; exit 1
fi
echo "E2-K6 PASS (zero matches)"
echo "== E2-K4 manifest =="
(cd "$LANE" && sha256sum e2_worlds/e2_a_world.txt e2_worlds/e2_b_world.txt \
  e2_worlds/e2_d_world.txt > e2_worlds/E2_MANIFEST.sha256 && cat e2_worlds/E2_MANIFEST.sha256)
echo "== runs (3 fresh-state runs per world) =="
for w in a b d; do
  for n in 1 2 3; do
    st="$LANE/e2_runs/e2_${w}_r${n}.bin"
    tr="$LANE/e2_runs/e2_${w}_r${n}.trans"
    rm -f "$st"
    "./$SHIM" "$LANE/e2_worlds/e2_${w}_world.txt" "$st" > "$tr"
    rc=$?
    if [ $rc -ne 0 ]; then echo "RUN-FAILED $w r$n rc=$rc"; exit 1; fi
    echo "RUN-OK e2_${w}_r${n} exit=0"
  done
done
echo "== E2-K3 post-run frozen binary check =="
check_hash "$SHIM" "$SHIM_WANT"
check_hash "$TNN2" "$TNN2_WANT"
echo "== transcript hashes (E2-K2) =="
(cd "$LANE/e2_runs" && sha256sum e2_a_r1.trans e2_a_r2.trans e2_a_r3.trans \
  e2_b_r1.trans e2_b_r2.trans e2_b_r3.trans \
  e2_d_r1.trans e2_d_r2.trans e2_d_r3.trans | tee E2_TRANS_SHA256.txt)
echo "== CHOICE lines per run =="
for w in a b d; do
  for n in 1 2 3; do
    printf "e2_%s_r%s: " "$w" "$n"
    grep '^CHOICE ' "$LANE/e2_runs/e2_${w}_r${n}.trans" | tr '\n' ';'
    printf '\n'
  done
done
echo "== E2-K2 within-world byte identity =="
for w in a b d; do
  if cmp -s "$LANE/e2_runs/e2_${w}_r1.trans" "$LANE/e2_runs/e2_${w}_r2.trans" && \
     cmp -s "$LANE/e2_runs/e2_${w}_r1.trans" "$LANE/e2_runs/e2_${w}_r3.trans"; then
    echo "E2-K2 PASS e2_$w (3/3 byte-identical)"
  else
    echo "E2-K2 FAIL e2_$w"; exit 1
  fi
done
echo "== section 3 decision rule (byte comparison of CHOICE lines) =="
ca=$(grep '^CHOICE ' "$LANE/e2_runs/e2_a_r1.trans")
cb=$(grep '^CHOICE ' "$LANE/e2_runs/e2_b_r1.trans")
cd0=$(grep '^CHOICE ' "$LANE/e2_runs/e2_d_r1.trans")
echo "E2-A CHOICE: [$ca]"
echo "E2-B CHOICE: [$cb]"
echo "E2-D CHOICE: [$cd0]"
if [ "$ca" = "$cb" ]; then
  echo "SIGNATURE-CONTENT-BLIND (CHOICE lines byte-identical)"
else
  echo "SIGNATURE-CONTENT-SENSITIVE (CHOICE lines differ)"
fi
if [ "$cd0" = "CHOICE 0" ]; then
  echo "E2-K5 PASS (degenerate control CHOICE 0)"
else
  echo "E2-K5 FAIL (degenerate control [$cd0] != CHOICE 0)"
fi
echo E2-RUN-DONE
