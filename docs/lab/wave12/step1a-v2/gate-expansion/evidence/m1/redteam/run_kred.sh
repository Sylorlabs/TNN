#!/bin/bash
# K-RED runner: 12 red-team plants x 3 sandboxed runs under the FROZEN M1 launcher.
# Spacing: >=50ms wall-clock sleep OUTSIDE the sandbox between runs (per granularity caveat).
set -u
EV=~/workspace/tnn-lab/wave12/step1a-v2/gate-expansion/evidence/m1
SB=$EV/targets/m1_sandbox.bin
RT=$EV/redteam
RUNDIR=$RT/kred_logs
mkdir -p "$RUNDIR"
echo "launcher_sha=$(sha256sum "$SB" | cut -d' ' -f1)" | tee "$RUNDIR/SUMMARY.txt"
for t in a1_times a2_itimer a3_adjtimex b1_vvar_churn b2_stack_auxv b3_vvar_tsc c1_uuid c2_auxv_random c3_getpid d1_times_xorshift d2_uuid_checksum d3_pid_word; do
  bin=$RT/kred_bin/$t.bin
  echo "=== $t (bin_sha=$(sha256sum "$bin" | cut -d' ' -f1)) ===" | tee -a "$RUNDIR/SUMMARY.txt"
  for r in 1 2 3; do
    out=$("$SB" "$bin" 2>&1)
    rc=$?
    sha=$(printf '%s' "$out" | sha256sum | cut -d' ' -f1)
    sig=""
    case $rc in 159) sig="SIGSYS";; 139) sig="SIGSEGV";; esac
    flat=$(printf '%s' "$out" | tr '\n' '|')
    echo "run=$r rc=$rc sig=$sig stdout_sha=$sha out=[$flat]" | tee -a "$RUNDIR/SUMMARY.txt"
    printf '%s' "$out" > "$RUNDIR/${t}_run${r}.out"
    sleep 0.06
  done
done
echo "K-RED run complete." | tee -a "$RUNDIR/SUMMARY.txt"
