#!/bin/bash
# Contender D full battery (frozen PREREG_PAR_DIVE.md section 2).
# Rebuilds both schemes with the pinned toolchain, renders, and runs every
# battery leg. Analysis helpers are Python; the renderers are pure Zag.
set -u
D="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$D/src"; RUNS="$D/runs"; RES="$D/results"; TESTS="$D/tests"
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
FIX=~/workspace/bytegen/fixture/plan_v1.txt
GATE=~/workspace/bytegen/tests/gate_bin
CHOP=~/workspace/aud_v10/chop.py
PARBIN=~/workspace/bytegen/fork_par/src/render_par
EDGEPLAN=~/workspace/bytegen/tests/plan_edge_cut.txt
LONGPLAN=~/workspace/bytegen/tests/plan_long.txt
MULTIPLAN=~/workspace/bytegen/hybrid/tests/plan_long_multi.txt
NEARPLAN="$D/plans/plan_long_near.txt"
mkdir -p "$RUNS" "$RES"

echo "== build =="
"$ZNC" build "$SRC/render_d1.zag" -o "$SRC/render_d1" 2>&1 | grep -i "error" || true
"$ZNC" build "$SRC/render_d2.zag" -o "$SRC/render_d2" 2>&1 | grep -i "error" || true
sha256sum "$SRC/render_d1.zag" "$SRC/render_d2.zag" > "$RES/sources.sha256"
cat "$RES/sources.sha256"

echo "== reference PAR clean mix =="
"$PARBIN" "$FIX" "$RUNS/par_clean.mix" "seq+mix" > /dev/null 2>&1
"$PARBIN" "$EDGEPLAN" "$RUNS/par_edge.wav" seq > /dev/null 2>&1
"$PARBIN" "$LONGPLAN" "$RUNS/par_rtlong.wav" seq > /dev/null 2>&1

########## D1 ##########
echo "########## D1 MR-BIDI ##########"
echo "== D1 clean =="
"$SRC/render_d1" "$FIX" "$RUNS/d1_clean.wav" seq > "$RUNS/d1_clean.trace" 2>&1
"$SRC/render_d1" "$FIX" "$RUNS/d1_clean.mix" "seq+mix" > /dev/null 2>&1
cmp "$RUNS/d1_clean.mix" "$RUNS/par_clean.mix" && echo "D1-C1: mix bit-identical to PAR"
cmp "$RUNS/d1_clean.wav" ~/workspace/bytegen/fork_par/src/par_seq1.wav && echo "D1-C1: wav bit-identical to PAR"

echo "== D1 determinism =="
for i in 1 2 3; do "$SRC/render_d1" "$FIX" "$RUNS/d1_rerun$i.wav" seq > /dev/null 2>&1; done
sha256sum "$RUNS/d1_clean.wav" "$RUNS"/d1_rerun*.wav | tee "$RES/d1_determinism.sha256"

echo "== D1 quality =="
"$GATE" "$RUNS/d1_clean.wav" | tee "$RES/d1_gate.txt"
python3 "$CHOP" "$RUNS/d1_clean.wav" "$TESTS/events_full.txt" | tee "$RES/d1_chop.txt"

echo "== D1 coherence =="
python3 "$TESTS/coherence_full.py" "$RUNS/d1_clean.wav" | tee "$RES/d1_coherence.txt"

echo "== D1 cost =="
/usr/bin/time -v "$SRC/render_d1" "$FIX" "$RUNS/d1_cost.wav" seq > /dev/null 2> "$RES/d1_cost.txt" || \
  { echo "(no /usr/bin/time)"; time "$SRC/render_d1" "$FIX" "$RUNS/d1_cost.wav" seq > /dev/null 2> "$RES/d1_cost.txt"; }
grep -E "Elapsed|Maximum resident" "$RES/d1_cost.txt" || tail -3 "$RES/d1_cost.txt"

echo "== D1 RT-LONG (PAR semantics: renders nominal) =="
"$SRC/render_d1" "$LONGPLAN" "$RUNS/d1_rtlong.wav" seq > "$RUNS/d1_rtlong.trace" 2>&1
python3 "$TESTS/measure_zcr.py" "$RUNS/d1_rtlong.wav" 28.1 28.9 880 | tee "$RES/d1_rtlong.txt"
echo "D1 renders the nominal (880): 1200c error, same as PAR/NATIVE - documented tie"

echo "== D1 RT-CASCADE =="
"$SRC/render_d1" "$FIX" "$RUNS/d1_fault.mix" "seq+faultmix" > /dev/null 2>&1
python3 "$TESTS/postcut_diff.py" "$RUNS/d1_clean.mix" "$RUNS/d1_fault.mix" 3.0015 | tee "$RES/d1_cascade.txt"

echo "== D1 RT-EDGE (frozen) =="
"$SRC/render_d1" "$EDGEPLAN" "$RUNS/d1_edge.wav" seq > "$RUNS/d1_edge.trace" 2>&1
cmp "$RUNS/d1_edge.wav" "$RUNS/par_edge.wav" && echo "D1-C2frozen: edge wav bit-identical to PAR"
python3 "$CHOP" "$RUNS/d1_edge.wav" | head -2 | tee "$RES/d1_edge.txt"

echo "== D1 RT-EDGE extension (15 s render-window cut, unclipped plan) =="
"$SRC/render_d1" "$FIX" "$RUNS/d1_w15.wav" seq 15 > "$RUNS/d1_w15.trace" 2>&1
"$SRC/render_d1" "$FIX" "$RUNS/d1_w15_nofade.wav" seq 15 nofade > /dev/null 2>&1
grep -c "hardstop=1" "$RUNS/d1_w15.trace"
python3 "$CHOP" "$RUNS/d1_w15.wav" | head -1 | tee "$RES/d1_edge15.txt"
python3 "$CHOP" "$RUNS/d1_w15_nofade.wav" | head -1 | tee -a "$RES/d1_edge15.txt"

echo "== D1 order permutation =="
"$SRC/render_d1" "$FIX" "$RUNS/d1_rev.wav" rev > /dev/null 2>&1
cmp "$RUNS/d1_clean.wav" "$RUNS/d1_rev.wav" && echo "D1-C4: seq == rev bit-identical"

########## D2 ##########
echo "########## D2 PLANREF ##########"
echo "== D2 clean =="
"$SRC/render_d2" "$FIX" "$RUNS/d2_clean.wav" seq > "$RUNS/d2_clean.trace" 2>&1
"$SRC/render_d2" "$FIX" "$RUNS/d2_clean.mix" "seq+mix" > /dev/null 2>&1
cmp "$RUNS/d2_clean.mix" "$RUNS/par_clean.mix" && echo "D2-C1: mix bit-identical to PAR"
cmp "$RUNS/d2_clean.wav" ~/workspace/bytegen/fork_par/src/par_seq1.wav && echo "D2-C1: wav bit-identical to PAR"

echo "== D2 determinism =="
for i in 1 2 3; do "$SRC/render_d2" "$FIX" "$RUNS/d2_rerun$i.wav" seq > /dev/null 2>&1; done
sha256sum "$RUNS/d2_clean.wav" "$RUNS"/d2_rerun*.wav | tee "$RES/d2_determinism.sha256"

echo "== D2 quality =="
"$GATE" "$RUNS/d2_clean.wav" | tee "$RES/d2_gate.txt"
python3 "$CHOP" "$RUNS/d2_clean.wav" "$TESTS/events_full.txt" | tee "$RES/d2_chop.txt"

echo "== D2 coherence =="
python3 "$TESTS/coherence_full.py" "$RUNS/d2_clean.wav" | tee "$RES/d2_coherence.txt"

echo "== D2 cost =="
/usr/bin/time -v "$SRC/render_d2" "$FIX" "$RUNS/d2_cost.wav" seq > /dev/null 2> "$RES/d2_cost.txt" || \
  { echo "(no /usr/bin/time)"; time "$SRC/render_d2" "$FIX" "$RUNS/d2_cost.wav" seq > /dev/null 2> "$RES/d2_cost.txt"; }
grep -E "Elapsed|Maximum resident" "$RES/d2_cost.txt" || tail -3 "$RES/d2_cost.txt"

echo "== D2 RT-LONG original =="
"$SRC/render_d2" "$LONGPLAN" "$RUNS/d2_rtlong.wav" seq > "$RUNS/d2_rtlong.trace" 2>&1
grep "D2 RESPOND" "$RUNS/d2_rtlong.trace" | tee "$RES/d2_rtlong.txt"
echo "construction: f0q=28835840 = 440*65536 exact -> 0c error (D2-C2)"
python3 "$TESTS/measure_zcr.py" "$RUNS/d2_rtlong.wav" 28.1 28.9 440 | tee -a "$RES/d2_rtlong.txt"
sha256sum "$RUNS/d2_rtlong.wav" > "$RES/d2_rtlong.sha256"
"$SRC/render_d2" "$LONGPLAN" "$RUNS/d2_rtlong_b.wav" seq > /dev/null 2>&1
sha256sum "$RUNS/d2_rtlong_b.wav" >> "$RES/d2_rtlong.sha256"

echo "== D2 RT-LONG near-miss (nominal 460) =="
"$SRC/render_d2" "$NEARPLAN" "$RUNS/d2_rtlong_near.wav" seq > "$RUNS/d2_rtlong_near.trace" 2>&1
grep "D2 RESPOND" "$RUNS/d2_rtlong_near.trace" | tee "$RES/d2_rtlong_near.txt"
echo "construction: f0q=28835840 = 440 exact -> 0c error (D2-C3; hybrid abstains -> 75c; NATIVE 75c)"
python3 "$TESTS/measure_zcr.py" "$RUNS/d2_rtlong_near.wav" 28.1 28.9 440 | tee -a "$RES/d2_rtlong_near.txt"

echo "== D2 RT-LONG multi-trap =="
"$SRC/render_d2" "$MULTIPLAN" "$RUNS/d2_rtmulti.wav" seq > "$RUNS/d2_rtmulti.trace" 2>&1
grep "D2 RESPOND" "$RUNS/d2_rtmulti.trace" | tee "$RES/d2_rtmulti.txt"

echo "== D2 RT-CASCADE (fixture) =="
"$SRC/render_d2" "$FIX" "$RUNS/d2_fault.mix" "faultmix" > /dev/null 2>&1
python3 "$TESTS/postcut_diff.py" "$RUNS/d2_clean.mix" "$RUNS/d2_fault.mix" 3.0015 | tee "$RES/d2_cascade.txt"
echo "== D2 RT-CASCADE (plan_long: latch must still fire, window pre-cut clean) =="
"$SRC/render_d2" "$LONGPLAN" "$RUNS/d2_rtlong_fault.mix" "faultmix" > "$RUNS/d2_rtlong_fault.trace" 2>&1
grep "D2 RESPOND" "$RUNS/d2_rtlong_fault.trace" | tee -a "$RES/d2_cascade.txt"

echo "== D2 RT-EDGE (frozen) =="
"$SRC/render_d2" "$EDGEPLAN" "$RUNS/d2_edge.wav" seq > /dev/null 2>&1
cmp "$RUNS/d2_edge.wav" "$RUNS/par_edge.wav" && echo "D2: edge wav bit-identical to PAR"

echo "== D2 order permutation =="
"$SRC/render_d2" "$FIX" "$RUNS/d2_rev.wav" rev > /dev/null 2>&1
cmp "$RUNS/d2_clean.wav" "$RUNS/d2_rev.wav" && echo "D2: seq == rev bit-identical"

echo "== D2 red team: sustained 1292-block corruption =="
"$SRC/render_d2" "$LONGPLAN" "$RUNS/d2_sus.mix" "susfaultmix" > "$RUNS/d2_sus.trace" 2>&1
grep -E "D2 RESPOND|sustained" "$RUNS/d2_sus.trace" | tee "$RES/d2_sustained.txt"
echo "(expect ABSTAIN code=3: cue window != plan-pure; no pitch hallucination)"

echo "== done =="
