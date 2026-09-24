#!/bin/bash
# Long-horizon laws verification runner — Phase 1 (repaired baseline)
# Runs each config 3x, checks byte-identical, verifies PASS.
# Usage: ./run_lh_phase1.sh [outdir]
set -u
SRC=~/workspace/ob_lawslh/src
OUT=${1:-~/workspace/ob_lawslh/runs/phase1}
mkdir -p "$OUT"

# Configs: "bundle scale leg"
CONFIGS=(
  # base: 7 bundles x 3 scales
  "b0 s1 base" "a1pin s1 base" "a4race s1 base" "a2fp s1 base" "a6contra s1 base" "lie s1 base" "monk s1 base"
  "b0 s10 base" "a1pin s10 base" "a4race s10 base" "a2fp s10 base" "a6contra s10 base" "lie s10 base" "monk s10 base"
  "b0 s100 base" "a1pin s100 base" "a4race s100 base" "a2fp s100 base" "a6contra s100 base" "lie s100 base" "monk s100 base"
  # depth: b0, lie x 3 scales
  "b0 s1 depth" "b0 s10 depth" "b0 s100 depth"
  "lie s1 depth" "lie s10 depth" "lie s100 depth"
  # attacks: dos, key, cycle, distrust x s10, s100
  "lie s10 dos" "lie s100 dos"
  "lie s10 key" "lie s100 key"
  "b0 s10 cycle" "b0 s100 cycle"
  "lie s10 distrust" "lie s100 distrust"
  # offgov, indep x s1
  "b0 s1 offgov"
  "lie s1 indep"
)

PASS=0; FAIL=0; FAILED_LIST=""
for cfg in "${CONFIGS[@]}"; do
  set -- $cfg
  tag="$1_$2_$3"
  ok=1
  for rep in 1 2 3; do
    "$SRC/ob_lh" "$1" "$2" "$3" > "$OUT/${tag}_r${rep}.log" 2>&1
    rc=$?
    if [ $rc -ne 0 ]; then
      echo "FAIL $tag rep$rep: exit $rc"
      ok=0
    fi
  done
  # byte-identical check
  if ! cmp -s "$OUT/${tag}_r1.log" "$OUT/${tag}_r2.log" || ! cmp -s "$OUT/${tag}_r1.log" "$OUT/${tag}_r3.log"; then
    echo "FAIL $tag: not byte-identical across 3 runs"
    ok=0
  fi
  # verdict check
  if ! grep -q "OB_VERDICT,$1,$2,$3,PASS" "$OUT/${tag}_r1.log"; then
    echo "FAIL $tag: verdict not PASS"
    ok=0
  fi
  if [ $ok -eq 1 ]; then
    echo "PASS $tag"
    PASS=$((PASS+1))
  else
    FAIL=$((FAIL+1))
    FAILED_LIST="$FAILED_LIST $tag"
  fi
done

echo "=========================================="
echo "Phase 1: $PASS passed, $FAIL failed"
if [ -n "$FAILED_LIST" ]; then
  echo "Failed:$FAILED_LIST"
fi
echo "Results in $OUT"
