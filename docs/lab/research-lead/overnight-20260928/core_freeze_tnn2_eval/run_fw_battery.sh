#!/bin/sh
# FW1-FW9 battery for CORE-FREEZE-TNN2 evaluation.
# POSIX shell only. No Python. Uses sha256sum, grep, awk, cmp, cp.
# Usage: run_fw_battery.sh <rundir>
# Runs FW1-FW9 sequentially with persistent state carried across worlds.
# FW6 uses the two-stage responder contract (treatment + control + b-annex).
# Binary hash verified before every world (VOID exit 10 on mismatch).
set -u
EVALDIR="$HOME/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/core_freeze_tnn2_eval"
SHIMDIR="$HOME/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/core_freeze_tnn2_shim"
WORLDS="$HOME/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/freeze_worlds_v2/worlds"
BIN="$SHIMDIR/freeze_shim2_bin"
FROZEN_BIN_HASH="9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954"
RUNDIR="$1"
mkdir -p "$RUNDIR"
STATE="$RUNDIR/state.bin"
rm -f "$STATE"

check_bin() {
  H=$(sha256sum "$BIN" | awk '{print $1}')
  if [ "$H" != "$FROZEN_BIN_HASH" ]; then
    echo "VOID: binary hash mismatch" >&2
    echo "  got      $H" >&2
    exit 10
  fi
}

# run_one <worldfile> <statefile> <outprefix>
run_one() {
  W="$1"; ST="$2"; OUT="$3"
  check_bin
  "$BIN" "$W" "$ST" > "$OUT.out" 2> "$OUT.stderr"
  RC=$?
  echo "$RC" > "$OUT.rc"
  sha256sum "$OUT.out" | awk '{print $1}' > "$OUT.hash"
  if [ -f "$ST" ]; then sha256sum "$ST" | awk '{print $1}' > "$OUT.statehash"; fi
  if [ "$RC" != "0" ]; then echo "WORLD-RC-NONZERO $W rc=$RC" >&2; fi
}

# responder <transcript> <diag_line> <releaseB> <releaseC>
# Releases releaseB iff some transcript line is exactly diag_line AND a line
# exactly "CHOICE 0" occurs after it; otherwise releaseC.
responder() {
  T="$1"; DIAG="$2"; RB="$3"; RC="$4"
  DL=$(grep -n -x -F "$DIAG" "$T" | head -1 | cut -d: -f1)
  if [ -n "$DL" ]; then
    if awk -v dl="$DL" 'NR>dl && $0=="CHOICE 0"{f=1} END{exit !f}' "$T"; then
      echo "$RB"; return 0
    fi
  fi
  echo "$RC"; return 0
}

# ---- FW1 ----
run_one "$WORLDS/fw1_world.txt" "$STATE" "$RUNDIR/fw1"
cp "$STATE" "$RUNDIR/fw1_state.bin"
# ---- FW2 ----
run_one "$WORLDS/fw2_world.txt" "$STATE" "$RUNDIR/fw2"
cp "$STATE" "$RUNDIR/fw2_state.bin"
# ---- FW3 ----
run_one "$WORLDS/fw3_world.txt" "$STATE" "$RUNDIR/fw3"
cp "$STATE" "$RUNDIR/fw3_state.bin"
# ---- FW4 ----
run_one "$WORLDS/fw4_world.txt" "$STATE" "$RUNDIR/fw4"
cp "$STATE" "$RUNDIR/fw4_state.bin"
# ---- FW5 ----
run_one "$WORLDS/fw5_world.txt" "$STATE" "$RUNDIR/fw5"
cp "$STATE" "$RUNDIR/fw5_state.bin"
# ---- FW6 treatment (battery state) ----
cp "$STATE" "$RUNDIR/fw6_pre.bin"
run_one "$WORLDS/fw6_phaseA1.txt" "$STATE" "$RUNDIR/fw6_A1"
REL1=$(responder "$RUNDIR/fw6_A1.out" "ANSWER 35001 35501 -2" "fw6_phaseB1.txt" "fw6_controlB.txt")
echo "$REL1" > "$RUNDIR/fw6_rel1.txt"
run_one "$WORLDS/$REL1" "$STATE" "$RUNDIR/fw6_B1"
REL2=$(responder "$RUNDIR/fw6_B1.out" "ANSWER 35002 35502 -2" "fw6_phaseB2.txt" "fw6_controlB2.txt")
echo "$REL2" > "$RUNDIR/fw6_rel2.txt"
run_one "$WORLDS/$REL2" "$STATE" "$RUNDIR/fw6_B2"
cp "$STATE" "$RUNDIR/fw6_state.bin"
# ---- FW6 control arm (from pre-FW6 state copy; discarded after) ----
# Fixed sequence controlA->controlB->controlB2 (no responder; the control
# is the no-treatment baseline). Battery state continues from treatment.
CSTATE="$RUNDIR/fw6_ctrl_state.bin"
cp "$RUNDIR/fw6_pre.bin" "$CSTATE"
run_one "$WORLDS/fw6_controlA.txt" "$CSTATE" "$RUNDIR/fw6c_A"
run_one "$WORLDS/fw6_controlB.txt" "$CSTATE" "$RUNDIR/fw6c_B"
run_one "$WORLDS/fw6_controlB2.txt" "$CSTATE" "$RUNDIR/fw6c_B2"
# ---- FW6b misinformation annex (diagnostic; from pre-FW6 state copy) ----
BSTATE="$RUNDIR/fw6b_state.bin"
cp "$RUNDIR/fw6_pre.bin" "$BSTATE"
run_one "$WORLDS/fw6b_phaseA1.txt" "$BSTATE" "$RUNDIR/fw6b_A1"
BREL1=$(responder "$RUNDIR/fw6b_A1.out" "ANSWER 35001 35501 -2" "fw6_phaseB1.txt" "fw6_controlB.txt")
echo "$BREL1" > "$RUNDIR/fw6b_rel1.txt"
run_one "$WORLDS/$BREL1" "$BSTATE" "$RUNDIR/fw6b_B1"
BREL2=$(responder "$RUNDIR/fw6b_B1.out" "ANSWER 35002 35502 -2" "fw6_phaseB2.txt" "fw6_controlB2.txt")
echo "$BREL2" > "$RUNDIR/fw6b_rel2.txt"
run_one "$WORLDS/$BREL2" "$BSTATE" "$RUNDIR/fw6b_B2"
# ---- FW7 ----
run_one "$WORLDS/fw7_world.txt" "$STATE" "$RUNDIR/fw7"
cp "$STATE" "$RUNDIR/fw7_state.bin"
# ---- FW8 ----
run_one "$WORLDS/fw8_world.txt" "$STATE" "$RUNDIR/fw8"
cp "$STATE" "$RUNDIR/fw8_state.bin"
# ---- FW9 ----
run_one "$WORLDS/fw9_dagA.txt" "$STATE" "$RUNDIR/fw9a"
run_one "$WORLDS/fw9_dagB.txt" "$STATE" "$RUNDIR/fw9b"
cp "$STATE" "$RUNDIR/fw9_state.bin"

echo "FW-BATTERY-COMPLETE $RUNDIR"
