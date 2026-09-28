#!/bin/bash
# H2 full 1x battery runner. Sequential (load constraint). Logs to evidence/r1/.
set -u
H2=~/workspace/tnn-lab/units/arms/H2
CORP=~/workspace/tnn-lab/corpora/r1
EV=$H2/evidence/r1
mkdir -p "$EV"
BIN=$H2/work/h2
run() {  # $1 = mode, $2 = outdir, $3.. = extra args
  local mode="$1"; shift
  local out="$EV/$mode"
  mkdir -p "$out"
  echo "[$(date -u +%H:%M:%S)] START $mode" | tee -a "$EV/battery.log"
  ( cd "$H2" && "$BIN" "$mode" "$CORP" "$@" > "$out/stdout.txt" 2> "$out/stderr.txt" )
  local ec=$?
  echo "$ec" > "$out/exitcode"
  echo "[$(date -u +%H:%M:%S)] END $mode exit=$ec" | tee -a "$EV/battery.log"
}
run m1-1x-prose
run m1-1x-code
run m2-t1-prose
run m2-t1-code
run m2-t2-prose
run m2-t2-code
run m2-t3-1x
run m3-1x
run m4-1x-prose
run m4-1x-code
run m5-1x
run m6-p2c-1x
run m6-c2p-1x
run m7-1x
echo "[$(date -u +%H:%M:%S)] BATTERY (non-M8) DONE" | tee -a "$EV/battery.log"
