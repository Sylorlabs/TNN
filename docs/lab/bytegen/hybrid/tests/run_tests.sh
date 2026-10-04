#!/bin/bash
# Hybrid v2 (three-piece) reproducible evidence run.
# Pure Zag renderer; analysis helpers are Python (the renderer itself is
# pure Zag — see src/render_hyb.zag). Pinned compiler, zero RNG.
set -e
TDIR="$(cd "$(dirname "$0")" && pwd)"
HYB="$TDIR/.."
SRC="$HYB/src"
RES="$HYB/results"
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
FIX=~/workspace/tnn-lab/bytegen/fixture/plan_v1.txt
PARWAV=~/workspace/tnn-lab/bytegen/fork_par/src/par_seq1.wav
BIN="$SRC/render_hyb"

echo "== build =="
"$ZNC" build "$SRC/render_hyb.zag" -o "$BIN" 2>&1 | grep -i error || true
sha256sum "$SRC/render_hyb.zag"

echo "== clean + PAR byte-identity =="
"$BIN" "$FIX" "$RES/clean.wav" seq > "$RES/clean_trace.txt" 2>&1
cmp "$RES/clean.wav" "$PARWAV" && echo "CLEAN == PAR (byte-identical)"

echo "== determinism: 3 reruns =="
for i in 1 2 3; do
  "$BIN" "$FIX" "$RES/rerun$i.wav" seq > "$RES/rerun$i.trace" 2>&1
done
sha256sum "$RES/rerun1.wav" "$RES/rerun2.wav" "$RES/rerun3.wav" "$RES/clean.wav"

echo "== coherence =="
python3 "$TDIR/coherence.py" "$RES/clean.wav"

echo "== mixes: clean / single-fault / dropout / sustained =="
"$BIN" "$FIX" "$RES/clean.mix" seqmix > /dev/null 2>&1
"$BIN" "$FIX" "$RES/fault.mix" faultmix > "$RES/fault_trace.txt" 2>&1
"$BIN" "$FIX" "$RES/fault_noheal.mix" faultmix noheal > "$RES/fault_noheal_trace.txt" 2>&1
"$BIN" "$FIX" "$RES/drop.mix" dropoutmix > "$RES/drop_trace.txt" 2>&1
"$BIN" "$FIX" "$RES/drop_noheal.mix" dropoutmix noheal > "$RES/drop_noheal_trace.txt" 2>&1
"$BIN" "$FIX" "$RES/sus.mix" susfaultmix > "$RES/sus_trace.txt" 2>&1
"$BIN" "$FIX" "$RES/sus_noheal.mix" susfaultmix noheal > "$RES/sus_noheal_trace.txt" 2>&1
for pair in "fault fault" "fault_noheal noheal-control" "drop dropout" "drop_noheal dropout-noheal-control" "sus sustained" "sus_noheal sustained-noheal-control"; do
  set -- $pair
  echo "--- $2: clean.mix vs $1.mix ---"
  python3 "$TDIR/diff_mix.py" "$RES/clean.mix" "$RES/$1.mix"
done
grep -h "faults=" "$RES/fault_trace.txt" "$RES/drop_trace.txt" "$RES/sus_trace.txt"

echo "== RT-LONG (original) =="
"$BIN" ~/workspace/tnn-lab/bytegen/tests/plan_long.txt "$RES/rtlong.wav" seq > "$RES/rtlong_trace.txt" 2>&1
grep "HYB RESPOND" "$RES/rtlong_trace.txt"
"$BIN" ~/workspace/tnn-lab/bytegen/tests/plan_long.txt "$RES/rtlong2.wav" seq > /dev/null 2>&1
sha256sum "$RES/rtlong.wav" "$RES/rtlong2.wav"

echo "== RT-LONG multi-trap =="
"$BIN" "$TDIR/plan_long_multi.txt" "$RES/rtmulti.wav" seq > "$RES/rtmulti_trace.txt" 2>&1
grep "HYB RESPOND" "$RES/rtmulti_trace.txt"

echo "== done =="
