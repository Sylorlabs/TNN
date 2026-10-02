#!/bin/bash
# CREW D tournament battery — frozen PREREG_PAR_DIVE.md section 2.
# Rebuilds D1/D2/D3 + NATIVE reference with the pinned toolchain, then runs
# every battery leg per scheme. Analysis helpers are Python; renderers pure Zag.
set -u
D="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$D/src"; RUNS="$D/runs"; RES="$D/results"; TESTS="$D/tests"
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
OB=~/workspace/bytegen
FIX="$OB/fixture/plan_v1.txt"
GATE="$OB/tests/gate_bin"
CHOP=~/workspace/aud_v10/chop.py
EDGEPLAN="$OB/tests/plan_edge_cut.txt"
LONGPLAN="$OB/tests/plan_long.txt"
MULTIPLAN="$OB/hybrid/tests/plan_long_multi.txt"
NEARPLAN="$D/plans/plan_long_near.txt"
mkdir -p "$RUNS" "$RES"

echo "== build =="
"$ZNC" build "$SRC/render_d1.zag" -o "$SRC/render_d1" 2>&1 | grep -i "error" || true
"$ZNC" build "$SRC/render_d2.zag" -o "$SRC/render_d2" 2>&1 | grep -i "error" || true
"$ZNC" build "$SRC/render_d3.zag" -o "$SRC/render_d3" 2>&1 | grep -i "error" || true
"$ZNC" build "$SRC/render_native.zag" -o "$SRC/render_native" 2>&1 | grep -i "error" || true
sha256sum "$SRC/render_d1.zag" "$SRC/render_d2.zag" "$SRC/render_d3.zag" "$SRC/render_native.zag" | tee "$RES/sources.sha256"

echo "== NATIVE references =="
"$SRC/render_native" "$FIX" "$RUNS/native_clean.mix" "seq+mix" > /dev/null 2>&1
"$SRC/render_native" "$FIX" "$RUNS/native_clean.wav" seq > /dev/null 2>&1
"$SRC/render_native" "$EDGEPLAN" "$RUNS/native_edge.wav" seq > /dev/null 2>&1
"$SRC/render_native" "$LONGPLAN" "$RUNS/native_rtlong.wav" seq > /dev/null 2>&1
"$SRC/render_native" "$NEARPLAN" "$RUNS/native_rtlong_near.wav" seq > /dev/null 2>&1

run_scheme() {
  local S="$1" BIN="$2" FAULTMODE="$3"  # e.g. d1 $SRC/render_d1 seq+faultmix
  echo "########## $S ##########"
  echo "== $S clean =="
  "$BIN" "$FIX" "$RUNS/${S}_clean.wav" seq > "$RUNS/${S}_clean.trace" 2>&1
  "$BIN" "$FIX" "$RUNS/${S}_clean.mix" "seq+mix" > /dev/null 2>&1
  cmp "$RUNS/${S}_clean.mix" "$RUNS/native_clean.mix" && echo "$S-C1: mix bit-identical to NATIVE"
  cmp "$RUNS/${S}_clean.wav" "$RUNS/native_clean.wav" && echo "$S-C1: wav bit-identical to NATIVE"
  echo "== $S determinism =="
  for i in 1 2 3; do "$BIN" "$FIX" "$RUNS/${S}_rerun$i.wav" seq > /dev/null 2>&1; done
  sha256sum "$RUNS/${S}_clean.wav" "$RUNS"/${S}_rerun*.wav | tee "$RES/${S}_determinism.sha256"
  echo "== $S quality =="
  "$GATE" "$RUNS/${S}_clean.wav" | tee "$RES/${S}_gate.txt"
  python3 "$CHOP" "$RUNS/${S}_clean.wav" "$TESTS/events_full.txt" | tee "$RES/${S}_chop.txt"
  echo "== $S coherence =="
  python3 "$TESTS/coherence_full.py" "$RUNS/${S}_clean.wav" | tee "$RES/${S}_coherence.txt"
  echo "== $S RT-LONG (PAR semantics note) =="
  "$BIN" "$LONGPLAN" "$RUNS/${S}_rtlong.wav" seq > "$RUNS/${S}_rtlong.trace" 2>&1
  grep -E "D2 RESPOND" "$RUNS/${S}_rtlong.trace" | tee "$RES/${S}_rtlong.txt" || true
  python3 "$TESTS/measure_zcr.py" "$RUNS/${S}_rtlong.wav" 28.1 28.9 880 | tee -a "$RES/${S}_rtlong.txt"
  echo "== $S RT-CASCADE (frozen) =="
  "$BIN" "$FIX" "$RUNS/${S}_fault.mix" "$FAULTMODE" > /dev/null 2>&1
  python3 "$TESTS/postcut_diff.py" "$RUNS/${S}_clean.mix" "$RUNS/${S}_fault.mix" 3.0015 | tee "$RES/${S}_cascade.txt"
  echo "== $S RT-EDGE (frozen) =="
  "$BIN" "$EDGEPLAN" "$RUNS/${S}_edge.wav" seq > /dev/null 2>&1
  cmp "$RUNS/${S}_edge.wav" "$RUNS/native_edge.wav" && echo "$S: edge wav bit-identical to NATIVE"
  echo "== $S order permutation =="
  "$BIN" "$FIX" "$RUNS/${S}_rev.wav" rev > /dev/null 2>&1
  cmp "$RUNS/${S}_clean.wav" "$RUNS/${S}_rev.wav" && echo "$S: seq == rev bit-identical"
}

run_scheme d1 "$SRC/render_d1" "seq+faultmix"
run_scheme d2 "$SRC/render_d2" "faultmix"
run_scheme d3 "$SRC/render_d3" "seq+faultmix"

echo "########## D2 RT-LONG extras ##########"
"$SRC/render_d2" "$NEARPLAN" "$RUNS/d2_rtlong_near.wav" seq > "$RUNS/d2_rtlong_near.trace" 2>&1
grep "D2 RESPOND" "$RUNS/d2_rtlong_near.trace" | tee "$RES/d2_rtlong_near.txt"
python3 "$TESTS/measure_zcr.py" "$RUNS/d2_rtlong_near.wav" 28.1 28.9 440 | tee -a "$RES/d2_rtlong_near.txt"
"$SRC/render_d2" "$MULTIPLAN" "$RUNS/d2_rtmulti.wav" seq > "$RUNS/d2_rtmulti.trace" 2>&1
grep "D2 RESPOND" "$RUNS/d2_rtmulti.trace" | tee "$RES/d2_rtmulti.txt"
echo "== D2 RT-CASCADE on plan_long (latch must still fire) =="
"$SRC/render_d2" "$LONGPLAN" "$RUNS/d2_rtlong_fault.mix" "faultmix" > "$RUNS/d2_rtlong_fault.trace" 2>&1
grep "D2 RESPOND" "$RUNS/d2_rtlong_fault.trace" | tee -a "$RES/d2_cascade.txt"
echo "== D2 sustained 1292-block corruption =="
"$SRC/render_d2" "$LONGPLAN" "$RUNS/d2_sus.mix" "susfaultmix" > "$RUNS/d2_sus.trace" 2>&1
grep -E "D2 RESPOND|sustained" "$RUNS/d2_sus.trace" | tee "$RES/d2_sustained.txt"

echo "########## D1 extension: 15 s window-cut A/B ##########"
"$SRC/render_d1" "$FIX" "$RUNS/d1_w15.wav" seq 15 > "$RUNS/d1_w15.trace" 2>&1
"$SRC/render_d1" "$FIX" "$RUNS/d1_w15_nofade.wav" seq 15 nofade > /dev/null 2>&1
grep -c "hardstop=1" "$RUNS/d1_w15.trace" | tee "$RES/d1_edge15.txt"
python3 "$CHOP" "$RUNS/d1_w15.wav" | head -1 | tee -a "$RES/d1_edge15.txt"
python3 "$CHOP" "$RUNS/d1_w15_nofade.wav" | head -1 | tee -a "$RES/d1_edge15.txt"
"$SRC/render_d1" "$FIX" "$RUNS/d1_w15.mix" "seq+mix" 15 > /dev/null 2>&1
"$SRC/render_d1" "$FIX" "$RUNS/d1_w15_nofade.mix" "seq+mix" 15 nofade > /dev/null 2>&1

echo "########## D3 extended RT-CASCADE ##########"
: > "$RES/d3_cascade_ext.txt"
for m in burst dropout dcshift susfaultmix; do
  "$SRC/render_d3" "$FIX" "$RUNS/d3_$m.mix" "seq+$m" > "$RUNS/d3_$m.trace" 2>&1
  grep -E "injected|repaired" "$RUNS/d3_$m.trace" | tee -a "$RES/d3_cascade_ext.txt"
  python3 "$TESTS/postcut_diff.py" "$RUNS/d3_clean.mix" "$RUNS/d3_$m.mix" 3.0015 | tee -a "$RES/d3_cascade_ext.txt"
done
echo "== D1 sustained (confinement baseline for D3 comparison) =="
"$SRC/render_d1" "$FIX" "$RUNS/d1_sus.mix" "seq+susfaultmix" > /dev/null 2>&1
python3 "$TESTS/postcut_diff.py" "$RUNS/d1_clean.mix" "$RUNS/d1_sus.mix" 3.0015 | tee "$RES/d1_sustained.txt"

echo "########## NATIVE RT-LONG (gap-closing measurement) ##########"
python3 "$TESTS/measure_zcr.py" "$RUNS/native_rtlong.wav" 28.1 28.9 880 | tee "$RES/native_rtlong.txt"
python3 "$TESTS/measure_zcr.py" "$RUNS/native_rtlong_near.wav" 28.1 28.9 460 | tee "$RES/native_rtlong_near.txt"
python3 -c "
import math
print('NATIVE original: renders nominal 880 -> honest error vs true cue 440 = %.2fc (octave error)' % (1200*math.log2(880/440)))
print('NATIVE near-miss: renders nominal 460 -> honest error vs true cue 440 = %.2fc (pitch error, no octave error)' % (1200*math.log2(460/440)))
print('D2 both cases: latches cue-declared 440 -> 0c by construction')
" | tee -a "$RES/native_rtlong.txt"

echo "########## COST (interleaved, peakrss.py) ##########"
: > "$RES/cost_interleaved.txt"
for i in 1 2 3; do
  for b in render_native render_d1 render_d2 render_d3; do
    python3 "$TESTS/peakrss.py" "$SRC/$b" "$FIX" "$RUNS/cost_$b.wav" seq | tee -a "$RES/cost_interleaved.txt"
  done
done

echo "== done =="
