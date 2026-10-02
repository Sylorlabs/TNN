#!/bin/bash
# TNN-2 transfer refreeze driver.
# Implements the frozen criterion protocol from TRANSFER_REFREEZE_PREREG.md.
# Bash sequences frozen shim invocations ONLY and parses ANSWER lines from
# shim stdout. All world generation and scoring is pure Zag.
# The frozen TNN-2 binary and shim are NEVER modified (hash-verified below).
# Usage: run_tnn2_transfer.sh <rundir>
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
SHIM=/home/hatch/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/core_freeze_tnn2_shim/freeze_shim2_bin
SHIM_SHA="9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954"
WORLDS="$HERE/worlds"
RUNDIR="${1:-$HERE/runs/run1}"
mkdir -p "$RUNDIR/logs"

echo "$SHIM_SHA  $SHIM" | sha256sum -c - || { echo "SHIM HASH MISMATCH"; exit 1; }

# run_phase <cond> <phase> <statefile> <use_criterion:1|0>
# use_criterion=1: interleaved consecutive/held-out protocol per prereg sec 5.
#   Prints "<examples> <met>" on stdout; full transcript in logs/.
# use_criterion=0: pure exposure, all 24 steps, no criterion check.
run_phase() {
  local cond=$1 phase=$2 state=$3 use_crit=$4
  local log="$RUNDIR/logs/${cond}_${phase}.log"
  : > "$log"
  local consec=0 k=0 examples=24 met=0
  while [ $k -lt 24 ]; do
    local wf="$WORLDS/${cond}_${phase}_train_${k}.txt"
    [ -f "$wf" ] || { echo "missing world file $wf"; exit 1; }
    local out
    out="$("$SHIM" "$wf" "$state")" || { echo "shim failed on $wf"; exit 1; }
    echo "== STEP $k ==" >> "$log"
    echo "$out" >> "$log"
    if [ "$use_crit" = "1" ]; then
      local ans target
      ans="$(echo "$out" | grep '^ANSWER' | awk '{print $4}')"
      target="$(grep '^QUERY' "$wf" | awk '{print $4}')"
      if [ -n "$ans" ] && [ "$ans" = "$target" ]; then
        consec=$((consec+1))
      else
        consec=0
      fi
      echo "STEP_RESULT k=$k ans=$ans target=$target consec=$consec" >> "$log"
      if [ $consec -eq 3 ]; then
        cp "$state" "${state}.chk" || { echo "checkpoint copy failed"; exit 1; }
        local correct=0 j=0
        while [ $j -lt 12 ]; do
          local hwf="$WORLDS/${cond}_${phase}_held_${j}.txt"
          [ -f "$hwf" ] || { echo "missing held-out file $hwf"; exit 1; }
          local hout hans htarget
          hout="$("$SHIM" "$hwf" "${state}.chk")" || { echo "shim failed on $hwf"; exit 1; }
          echo "== HELD $j ==" >> "$log"
          echo "$hout" >> "$log"
          hans="$(echo "$hout" | grep '^ANSWER' | awk '{print $4}')"
          htarget="$(grep '^QUERY' "$hwf" | awk '{print $4}')"
          if [ -n "$hans" ] && [ "$hans" = "$htarget" ]; then
            correct=$((correct+1))
          fi
          j=$((j+1))
        done
        rm -f "${state}.chk"
        echo "HELD_RESULT correct=$correct/12" >> "$log"
        if [ $correct -eq 12 ]; then
          examples=$((k+1)); met=1
          break
        else
          consec=0
        fi
      fi
    fi
    k=$((k+1))
  done
  echo "PHASE_RESULT cond=$cond phase=$phase examples=$examples met=$met" >> "$log"
  echo "$examples $met"
}

echo "== condition T: A phase (criterion), then B phase (criterion), persistent state =="
rm -f "$RUNDIR/state_T.bin"
read t_a t_a_met <<< "$(run_phase T A "$RUNDIR/state_T.bin" 1)"
read t_b t_b_met <<< "$(run_phase T B "$RUNDIR/state_T.bin" 1)"
echo "== condition F: B phase only, fresh state =="
rm -f "$RUNDIR/state_F.bin"
read f_b f_b_met <<< "$(run_phase F B "$RUNDIR/state_F.bin" 1)"
echo "== condition X: scrambled-A exposure, then B phase (criterion), persistent state =="
rm -f "$RUNDIR/state_X.bin"
run_phase X A "$RUNDIR/state_X.bin" 0 > /dev/null
read x_b x_b_met <<< "$(run_phase X B "$RUNDIR/state_X.bin" 1)"

{
  echo "T_A_examples=$t_a T_A_met=$t_a_met"
  echo "T_B_examples=$t_b T_B_met=$t_b_met"
  echo "F_B_examples=$f_b F_B_met=$f_b_met"
  echo "X_B_examples=$x_b X_B_met=$x_b_met"
} > "$RUNDIR/summary.txt"
echo "== summary =="
cat "$RUNDIR/summary.txt"
echo "RUN_DONE $RUNDIR"
