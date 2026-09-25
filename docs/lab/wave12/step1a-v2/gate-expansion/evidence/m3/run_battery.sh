#!/bin/bash
# run_battery.sh — M3 fixed battery: clean-heap vs dirtied-heap pairs + checker.
# Usage: run_battery.sh <rundir>
# Env: M3_FLAG=7 always set (p05 plant realism). B runs add M3_PAD + "dirty" mode.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
RUNDIR="${1:-$HERE/runs/battery1}"
CHECKER="$HERE/checker/m3_checker"
mkdir -p "$RUNDIR"
PAD="$(python3 -c 'print("P"*5000)')"
PASS=0; FAILN=0
declare -A EXPECT=( [sample]=PASS [c01]=PASS [c02]=PASS [c04]=PASS [c05]=PASS [c06]=PASS
  [p01]=FAIL [p02]=FAIL [p03]=FAIL [p04]=FAIL [p05]=FAIL [p06]=FAIL [p07]=FAIL
  [p08]=FAIL [p09]=PASS [p10]=FAIL [p11]=FAIL [p12]=FAIL )
for m in sample c01 c02 c04 c05 c06 p01 p02 p03 p04 p05 p06 p07 p08 p09 p10 p11 p12; do
  BIN="$HERE/runs/$m"
  PRE=""
  if [ "$m" = "p07" ]; then PRE="LD_LIBRARY_PATH=$HERE/runs"; fi
  # A: clean heap, small environ
  env M3_FLAG=7 $PRE setarch -R "$BIN" "$RUNDIR/${m}_A.trace" clean >/dev/null 2>&1
  rca=$?
  # B: predirtied heap, shifted environ
  env M3_FLAG=7 M3_PAD="$PAD" $PRE setarch -R "$BIN" "$RUNDIR/${m}_B.trace" dirty >/dev/null 2>&1
  rcb=$?
  out="$($CHECKER "$RUNDIR/${m}_A.trace" "$RUNDIR/${m}_B.trace" "$HERE/maps/$m.map" "$HERE/m3_allowlist.txt" 2>&1)"
  verdict="$(echo "$out" | grep '^VERDICT' | head -1)"
  exp="${EXPECT[$m]}"
  got="FAIL"
  if [ "$verdict" = "VERDICT PASS" ]; then got="PASS"; fi
  mark="OK"
  if [ "$got" != "$exp" ]; then mark="MISMATCH"; fi
  echo "$mark $m expect=$exp got=$got rc=$rca/$rcb :: $verdict"
  if [ "$mark" = "OK" ]; then PASS=$((PASS+1)); else FAILN=$((FAILN+1)); fi
done
echo "BATTERY $RUNDIR: $PASS ok, $FAILN mismatch"
