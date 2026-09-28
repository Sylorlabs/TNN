#!/usr/bin/env bash
# EXP-1 Phase 1 run pipeline: builds + instrumented re-runs + chain linkage.
# Heavy compute runs ONLY when 1-min load < 2.5, everything under nice -n 10.
set -u
W="$HOME/workspace/tnn-lab/wave10/int-c7s100/work"
ZNC="$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1"
EXPECTED_BIN="e673bae2c889b117db7656a4b77c11c4974bf6cd4823f05c50b806894c25acf0"
LOG="$W/run.log"
OUT="$W/logs_inst"
OUTG="$W/logs_gate"

exec > >(tee -a "$LOG") 2>&1
echo "=== EXP-1 Phase 1 run pipeline starting $(date -u +%FT%TZ) ==="
wall() { # $1=t0 $2=t1 -> seconds
  awk -v a="$1" -v b="$2" 'BEGIN{printf "%.2f", b-a}'
}

# --- load gate ---
while true; do
  L1=$(awk '{print $1}' /proc/loadavg)
  OK=$(awk -v l="$L1" 'BEGIN{print (l<2.5)?1:0}')
  if [ "$OK" = "1" ]; then echo "load gate passed: 1-min load $L1 < 2.5"; break; fi
  echo "waiting: 1-min load $L1 >= 2.5 (sleep 60)"
  sleep 60
done

build() { # $1=srcdir $2=outbin
  echo "--- build $1 -> $2 ---"
  nice -n 10 "$ZNC" "$1/main.zag" -o "$2"
  echo "build_exit:$?"
  sha256sum "$2"
}

# --- 1. pristine rebuild -> must be byte-identical to committed trial binary ---
build "$W/src0" "$W/bin0"
H0=$(sha256sum "$W/bin0" | awk '{print $1}')
if [ "$H0" = "$EXPECTED_BIN" ]; then
  echo "PRISTINE REBUILD: BYTE-IDENTICAL ($H0)"
else
  echo "PRISTINE REBUILD: MISMATCH got=$H0 want=$EXPECTED_BIN"
  exit 11
fi

# --- 2. instrumented intact build ---
build "$W/src_inst" "$W/bin_inst"

# --- 3. instrumented stages s2..s5, paired, timed ---
mkdir -p "$OUT"
: > "$W/stage_timing.txt"
for s in 2 3 4 5; do
  for rep in a b; do
    T0=$(date +%s.%N)
    (cd "$W/src_inst" && nice -n 10 "$W/bin_inst" "s$s" > "$OUT/s${s}_${rep}.log" 2>&1)
    echo "s${s}_${rep}:$?" >> "$OUT/stage.exits"
    T1=$(date +%s.%N)
    echo "s${s}_${rep} wall_s=$(wall $T0 $T1)" | tee -a "$W/stage_timing.txt"
  done
  if cmp -s "$OUT/s${s}_a.log" "$OUT/s${s}_b.log"; then
    echo "s$s:IDENTICAL" | tee -a "$OUT/determinism.txt"
  else
    echo "s$s:DIFFER" | tee -a "$OUT/determinism.txt"
  fi
done

# --- 4. instrumented controls (intact) ---
T0=$(date +%s.%N)
(cd "$W/src_inst" && nice -n 10 "$W/bin_inst" controls > "$OUT/controls.log" 2>&1)
echo "controls:$? (intact)" >> "$OUT/stage.exits"
T1=$(date +%s.%N)
echo "controls_intact wall_s=$(wall $T0 $T1)" | tee -a "$W/stage_timing.txt"

# --- 5. chain linkage on intact logs ---
python3 "$W/link_chains.py" "$OUT" intact | tee "$OUT/link_report.txt"

# --- 6. gate-less calibration variant: build + controls ---
build "$W/src_gateless" "$W/bin_gate"
mkdir -p "$OUTG"
T0=$(date +%s.%N)
(cd "$W/src_gateless" && nice -n 10 "$W/bin_gate" controls > "$OUTG/controls.log" 2>&1)
echo "controls:$? (gateless; c5_lesion=1 expected)" >> "$OUTG/stage.exits"
T1=$(date +%s.%N)
echo "controls_gateless wall_s=$(wall $T0 $T1)" | tee -a "$W/stage_timing.txt"
python3 "$W/link_chains.py" "$OUTG" gateless | tee "$OUTG/link_report.txt"

echo "=== pipeline done $(date -u +%FT%TZ) ==="
