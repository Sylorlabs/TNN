#!/bin/bash
# run_amort.sh: build and measure the learned-procedure amortization test.
# Pure bash + znc + gcc. No Python.
set -u
ZNC=/home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc
D=docs/lab/research-lead/overnight-20260928/proc_amort
cd ~/workspace/tnn-rsi || exit 1

"$ZNC" "$D/amort.zag" -o "$D/amort_bin" 2> "$D/build_zag.err"
if [ ! -x "$D/amort_bin" ]; then echo "zag build failed"; exit 1; fi
gcc -O2 -o "$D/amort_c" "$D/amort.c" 2> "$D/build_c.err"
if [ ! -x "$D/amort_c" ]; then echo "c build failed"; exit 1; fi

for r in 1 2 3; do
  ./"$D/amort_bin" > "$D/AMORT_RAW_$r.txt" 2> "$D/AMORT_RAW_$r.err"
  ./"$D/amort_c" > "$D/AMORT_C_RAW_$r.txt" 2> "$D/AMORT_C_RAW_$r.err"
done

# normalized byte comparison for Zag stdout (timings excluded per prereg K4)
for r in 1 2 3; do
  sed 's/ms=[0-9]*/ms=X/;s/rss=[0-9]*/rss=X/' "$D/AMORT_RAW_$r.txt" > "$D/AMORT_NORM_$r.txt"
  sed 's/ms=[0-9]*/ms=X/;s/rss=[0-9]*/rss=X/' "$D/AMORT_C_RAW_$r.txt" > "$D/AMORT_C_NORM_$r.txt"
done
echo "== zag normalized md5 =="
md5sum "$D"/AMORT_NORM_*.txt
echo "== c normalized md5 =="
md5sum "$D"/AMORT_C_NORM_*.txt
echo "== raw outputs =="
cat "$D"/AMORT_RAW_*.txt "$D"/AMORT_C_RAW_*.txt
