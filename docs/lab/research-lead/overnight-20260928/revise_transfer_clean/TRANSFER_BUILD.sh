#!/bin/sh
# TRANSFER_BUILD.sh -- F3 REVISE step-9 transfer clean re-run.
# Prereg: revise_transfer_clean/PREREG_REVISE_TRANSFER_CLEAN.md (frozen alone first).
# Pure Zag + shell + znc only. No Python. World files copied byte-verbatim
# from committed step-9 artifacts (c3c3e3bc8) via git show; nothing recomputed.
ZNC=/home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc
S=docs/lab/research-lead/overnight-20260928
D=$S/revise_transfer_clean
FROZEN=$D/f3_revise_frozen.zag
FROZEN_SHA=354236fb3071729fc8921489163f1454bb04d673655f2cb3d1f3c88cb771d392
set -e
cd ~/workspace/tnn-rsi

echo "=== frozen learner sha256 ==="
H=$(sha256sum "$FROZEN" | cut -d' ' -f1)
echo "$H"
if [ "$H" != "$FROZEN_SHA" ]; then
  echo "FROZEN LEARNER HASH MISMATCH"; exit 1
fi

build_run() {
  name="$1"; world="$2"
  cat "$FROZEN" "$D/$world" > "$D/run_$name.zag"
  "$ZNC" "$D/run_$name.zag" -o "$D/bin_$name" 2> "$D/build_$name.err" || (cat "$D/build_$name.err"; exit 1)
  i=1
  while [ $i -le 3 ]; do
    "$D/bin_$name" > "$D/raw_${name}_r$i.txt" 2> "$D/raw_${name}_r$i.err"
    i=$((i+1))
  done
  echo "$name built and run 3x"
}

case "$1" in
  stf)
    echo "=== Treatment: frozen REVISE + S-TRF (setup S1 then S2) ==="
    build_run "stf" "world_stf.zag"
    ;;
  sct)
    echo "=== Control: frozen REVISE + S-CTF (setup S2 directly) ==="
    build_run "sct" "world_sct.zag"
    ;;
  all)
    "$0" stf
    "$0" sct
    ;;
  *)
    echo "usage: $0 {stf|sct|all}"; exit 1 ;;
esac

echo "=== md5 of raw outputs ==="
md5sum "$D"/raw_"$1"*_r*.txt 2>/dev/null
echo "=== stderr sizes (must all be 0) ==="
wc -c "$D"/raw_"$1"*_r*.err 2>/dev/null
