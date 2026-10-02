#!/bin/bash
# run_dr_leg.sh — Wave-6 Investigation 1 deliberative-refusal ablation leg.
# Preregistered (PREREG_ABLATION.md §8): intact dr.zag 10x vs DR_VARIANT=1
# (myopic) 10x, two runs each, byte-identical reruns required. Take counts
# are read from the DR_SUMMARY lines. The original dr.zag is never edited:
# the variant is a sed-patched copy in /tmp, like the wave-5 harness.
set -u
D="$HOME/workspace/tnn-lab/wave5/deliberative-refusal"
W="$HOME/workspace/tnn-lab/wave6/attribution-ablation"
ZNC="$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1"
EV="$W/logs/dr_leg"
mkdir -p "$EV"
cd "$D"

fail(){ echo "GATE_FAIL: $1" | tee -a "$EV/run.log"; exit 1; }
pass(){ echo "GATE_PASS: $1" | tee -a "$EV/run.log"; }
: > "$EV/run.log"

# --- Gate 0: dr.zag unmodified vs the preregistered hash ---
DRH=$(sha256sum "$D/dr.zag" | cut -d' ' -f1)
[ "$DRH" = "11a972cc99ded769694a45adab1a53c9e76de83c5dd70d9c798e3e20a8b4cfe4" ] \
  || fail "dr.zag modified: $DRH"
pass "dr.zag matches prereg hash"

# --- Gate 1: no RNG in the DR decision path ---
sed 's|//.*||' "$D/dr.zag" | grep -nEi 'rand|srand|random|entropy|/dev/urandom|getrandom|rdtsc|time\(|clock\(' \
  && fail "RNG token in dr.zag" || pass "no RNG tokens in dr.zag"

# --- Gate 2: compile intact + myopic (patched copy), run each twice ---
"$ZNC" "$D/dr.zag" -O3 -o "$EV/dr_intact.bin" > "$EV/compile_intact.log" 2>&1 \
  || { tail -20 "$EV/compile_intact.log"; fail "intact compile failed"; }
sed "s/const DR_VARIANT:i32=0;/const DR_VARIANT:i32=1;/" "$D/dr.zag" > /tmp/dr_myopic.zag
"$ZNC" /tmp/dr_myopic.zag -O3 -o "$EV/dr_myopic.bin" > "$EV/compile_myopic.log" 2>&1 \
  || { tail -20 "$EV/compile_myopic.log"; fail "myopic compile failed"; }
pass "both variants compiled"

for v in intact myopic; do
  "$EV/dr_${v}.bin" 10x > "$EV/dr_${v}_a.log" 2>&1; ra=$?
  "$EV/dr_${v}.bin" 10x > "$EV/dr_${v}_b.log" 2>&1; rb=$?
  # Prereg §8: the variant's exit code is informational — myopic is
  # EXPECTED to fail its own internal checks (takes>0). Only the intact
  # leg must exit 0; both legs must be byte-identical across reruns.
  echo "DR_EXIT,$v,a,$ra,b,$rb" | tee -a "$EV/run.log"
  if [ "$v" = "intact" ]; then
    [ $ra -eq 0 ] || fail "$v run a exited $ra"
    [ $rb -eq 0 ] || fail "$v run b exited $rb"
  fi
  ha=$(sha256sum "$EV/dr_${v}_a.log" | cut -d' ' -f1)
  hb=$(sha256sum "$EV/dr_${v}_b.log" | cut -d' ' -f1)
  [ "$ha" = "$hb" ] || fail "$v runs differ"
  pass "$v 10x byte-identical reruns: $ha"
done

# --- Gate 3: extract take counts from DR_SUMMARY ---
for v in intact myopic; do
  s=$(grep '^DR_SUMMARY' "$EV/dr_${v}_a.log" | head -1)
  echo "DR_TAKES,$v,$s" | tee -a "$EV/run.log"
done
echo "ALL GATES PASSED" | tee -a "$EV/run.log"
