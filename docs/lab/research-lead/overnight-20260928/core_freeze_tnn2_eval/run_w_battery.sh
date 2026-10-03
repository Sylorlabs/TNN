#!/bin/sh
# W1-W9 battery for CORE-FREEZE-TNN2 evaluation (supplementary regression).
# POSIX shell only. No Python. Uses sha256sum, grep, awk, cmp, cp.
# Usage: run_w_battery.sh <rundir>
# Runs W1-W9 sequentially with persistent state carried across worlds.
# W6 uses the responder contract (treatment + control + w6b annex).
# Binary hash verified before every world (VOID exit 10 on mismatch).
set -u
EVALDIR="$HOME/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/core_freeze_tnn2_eval"
SHIMDIR="$HOME/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/core_freeze_tnn2_shim"
PRE="$HOME/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/core_freeze/worlds_prefreeze"
ADV="$HOME/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/core_freeze/worlds_adversary"
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

# ---- W1 ----
run_one "$PRE/W1_world.txt" "$STATE" "$RUNDIR/w1"
cp "$STATE" "$RUNDIR/w1_state.bin"
# ---- W2 ----
run_one "$PRE/W2_world.txt" "$STATE" "$RUNDIR/w2"
cp "$STATE" "$RUNDIR/w2_state.bin"
# ---- W3 ----
run_one "$PRE/W3_world.txt" "$STATE" "$RUNDIR/w3"
cp "$STATE" "$RUNDIR/w3_state.bin"
# ---- W4 ----
run_one "$PRE/W4_world.txt" "$STATE" "$RUNDIR/w4"
cp "$STATE" "$RUNDIR/w4_state.bin"
# ---- W5 ----
run_one "$PRE/W5_world.txt" "$STATE" "$RUNDIR/w5"
cp "$STATE" "$RUNDIR/w5_state.bin"
# ---- W6 treatment (battery state) ----
cp "$STATE" "$RUNDIR/w6_pre.bin"
run_one "$ADV/w6_phaseA.txt" "$STATE" "$RUNDIR/w6_A"
W6REL=$(responder "$RUNDIR/w6_A.out" "ANSWER 22001 22101 -2" "$ADV/w6_phaseB.txt" "$ADV/w6_controlB.txt")
echo "$W6REL" > "$RUNDIR/w6_rel.txt"
run_one "$W6REL" "$STATE" "$RUNDIR/w6_B"
cp "$STATE" "$RUNDIR/w6_state.bin"
# ---- W6 control arm (from pre-W6 state copy; discarded after) ----
WCSTATE="$RUNDIR/w6_ctrl_state.bin"
cp "$RUNDIR/w6_pre.bin" "$WCSTATE"
run_one "$ADV/w6_controlA.txt" "$WCSTATE" "$RUNDIR/w6c_A"
run_one "$ADV/w6_controlB.txt" "$WCSTATE" "$RUNDIR/w6c_B"
# ---- W6b annex (diagnostic; from pre-W6 state copy) ----
WBSTATE="$RUNDIR/w6b_state.bin"
cp "$RUNDIR/w6_pre.bin" "$WBSTATE"
run_one "$ADV/w6b_phaseA.txt" "$WBSTATE" "$RUNDIR/w6b_A"
W6BREL=$(responder "$RUNDIR/w6b_A.out" "ANSWER 22001 22101 -2" "$ADV/w6b_phaseB.txt" "$ADV/w6_controlB.txt")
echo "$W6BREL" > "$RUNDIR/w6b_rel.txt"
run_one "$W6BREL" "$WBSTATE" "$RUNDIR/w6b_B"
# ---- W7 ----
run_one "$PRE/W7_world.txt" "$STATE" "$RUNDIR/w7"
cp "$STATE" "$RUNDIR/w7_state.bin"
# ---- W8 ----
run_one "$PRE/W8_world.txt" "$STATE" "$RUNDIR/w8"
cp "$STATE" "$RUNDIR/w8_state.bin"
# ---- W9 ----
run_one "$ADV/w9_treeA.txt" "$STATE" "$RUNDIR/w9a"
run_one "$ADV/w9_treeB.txt" "$STATE" "$RUNDIR/w9b"
cp "$STATE" "$RUNDIR/w9_state.bin"

echo "W-BATTERY-COMPLETE $RUNDIR"
