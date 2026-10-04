#!/bin/bash
# run_step1d.sh — deterministic Step 1d evidence runner.
# Builds all harnesses from source (twice), runs the full instrument battery,
# and verifies byte-identical outputs across builds.
# Usage: ./run_step1d.sh [outdir]
# Pure deterministic: zero RNG, fixed seeds, lawful state machinery.
set -e
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
SRC=~/workspace/tnn-lab/wave12/step1d-phrasing
OUT=${1:-/tmp/step1d_evidence}
mkdir -p "$OUT"

build_all() {
    local tag=$1
    local d="$OUT/build_$tag"
    mkdir -p "$d"
    $ZNC "$SRC/cert.zag"    --no-zagd --no-analyze --no-foreground-cache -o "$d/cert" 2>/dev/null
    $ZNC "$SRC/trial.zag"   --no-zagd --no-analyze --no-foreground-cache -o "$d/trial" 2>/dev/null
    $ZNC "$SRC/nullrun.zag" --no-zagd --no-analyze --no-foreground-cache -o "$d/nullrun" 2>/dev/null
    $ZNC "$SRC/detect.zag"  --no-zagd --no-analyze --no-foreground-cache -o "$d/detect" 2>/dev/null
    $ZNC "$SRC/adapt.zag"   --no-zagd --no-analyze --no-foreground-cache -o "$d/adapt" 2>/dev/null
}

run_battery() {
    local tag=$1
    local d="$OUT/build_$tag"
    local r="$OUT/run_$tag"
    mkdir -p "$r"
    "$d/cert" certinv    > "$r/certinv.txt" 2>&1
    "$d/cert" certneg    > "$r/certneg.txt" 2>&1
    "$d/trial"          > "$r/trial.txt" 2>&1; echo "trial_exit=$?" >> "$r/trial.txt"
    "$d/nullrun" nullself     > "$r/nullself.txt" 2>&1
    "$d/nullrun" freezencheck > "$r/freezencheck.txt" 2>&1
    "$d/nullrun" armc         > "$r/armc.txt" 2>&1
    "$d/detect" pos  > "$r/det_pos.txt" 2>&1
    "$d/detect" neg  > "$r/det_neg.txt" 2>&1
    "$d/detect" real > "$r/det_real.txt" 2>&1
    "$d/adapt" pilot > "$r/adapt_pilot.txt" 2>&1
    "$d/adapt" full  > "$r/adapt_full.txt" 2>&1
    "$d/adapt" novel > "$r/adapt_novel.txt" 2>&1
}

echo "=== build A ==="; build_all A
echo "=== run A ===";   run_battery A
echo "=== build B ==="; build_all B
echo "=== run B ===";   run_battery B

echo "=== byte-compare runs ==="
fail=0
for f in certinv.txt certneg.txt trial.txt nullself.txt freezencheck.txt armc.txt \
         det_pos.txt det_neg.txt det_real.txt adapt_pilot.txt adapt_full.txt adapt_novel.txt; do
    if cmp -s "$OUT/run_A/$f" "$OUT/run_B/$f"; then
        echo "IDENTICAL $f"
    else
        echo "DIFFER $f"; fail=1
    fi
done
if [ $fail -eq 0 ]; then echo "ALL_RUNS_BYTE_IDENTICAL"; else echo "RUN_MISMATCH"; exit 1; fi
