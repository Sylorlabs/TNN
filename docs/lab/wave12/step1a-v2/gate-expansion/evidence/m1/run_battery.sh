#!/bin/bash
# M1 battery runner: runs all targets under the frozen launcher, records rc/signal/stdout.
# Usage: run_battery.sh <runid>   (creates runs/<runid>/, writes verdict vector to stdout+file)
set -u
EV=~/workspace/tnn-lab/wave12/step1a-v2/gate-expansion/evidence/m1
RUNID=${1:?runid}
RUNDIR=$EV/runs/$RUNID
SB=$EV/targets/m1_sandbox.bin
mkdir -p "$RUNDIR"
cd "$RUNDIR" || exit 1
# deterministic data file for C04 (pinned allowlist read)
python3 -c "
d = bytes([(i*37+11)&255 for i in range(64)])
open('c04_data.bin','wb').write(d)
"
TARGETS="p01 p02 p03 p04 p05 p06 p07 p08 p09 p10 p11 p12 c01 c02 c04 c05 c06"
{
echo "run=$RUNID launcher_sha=$(sha256sum "$SB" | cut -d' ' -f1)"
for t in $TARGETS; do
  bin=$EV/targets/t_$t.bin
  out=$("$SB" "$bin" 2>&1)
  rc=$?
  case $rc in
    0)   v=PASS ;;
    139) v=FAIL-SIGSEGV ;;
    159) v=FAIL-SIGSYS ;;
    *)   v=INCONCLUSIVE-rc$rc ;;
  esac
  # single-line the output for the log
  flat=$(printf '%s' "$out" | tr '\n' '|')
  echo "$t rc=$rc verdict=$v out=[$flat]"
done
} | tee "$EV/logs/battery_$RUNID.log"
