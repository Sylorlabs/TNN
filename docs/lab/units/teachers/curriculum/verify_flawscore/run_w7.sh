#!/bin/bash
# W7 flaw-manifest verification runner (Track B).
# Builds flawrun (learner-side) + flawscore_run (scorer-side), runs the
# learner over all 8 arm-1 teacher flaw slices (N=5 byte-identical check),
# scores against the sealed manifest, and writes evidence logs.
#
# The per-slice flaw scores below are INFORMATIONAL (integration-shim
# measurement; see flawrun.zag header and the W7 verdict sheet). They are
# NOT §B.4 sessions and do not apply the ≥10/12 pass bar as a verdict.
set -u
cd "$(dirname "$0")/../.." || exit 1   # -> units/teachers
HERE="$(pwd)"
VF="$HERE/curriculum/verify_flawscore"
W="$HERE/../../scratch_w7"
ZNC="${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}"
mkdir -p "$VF/logs"

echo "== build flawrun =="
"$ZNC" "$VF/flawrun.zag" --no-zagd --no-analyze --no-foreground-cache \
  -o "$VF/flawrun_bin" 2>&1 | tail -3
echo "== build flawscore_run =="
"$ZNC" "$VF/flawscore_run.zag" --no-zagd --no-analyze --no-foreground-cache \
  -o "$VF/flawscore_bin" 2>&1 | tail -3
[ -x "$VF/flawrun_bin" ] || { echo "BUILD_FAIL flawrun"; exit 1; }
[ -x "$VF/flawscore_bin" ] || { echo "BUILD_FAIL flawscore_run"; exit 1; }

LOG="$VF/logs/w7_flaw_run.log"
: > "$LOG"
echo "== W7 flaw probe run: $(date -u +%FT%TZ) ==" | tee -a "$LOG"
for k in 0 1 2 3 4 5 6 7; do
  echo "--- slice S$k ---" | tee -a "$LOG"
  cp "$HERE/arm1/wired/slice_S$k.bin" "$VF/logs/slice_S$k.bin"
  cp "$W/wires_S$k.bin" "$VF/logs/wires_S$k.bin"
  # N=5 byte-identical learner runs (inputs staged in $VF/logs)
  for n in 1 2 3 4 5; do
    "$VF/flawrun_bin" "$VF/logs" "wires_S$k.bin" "slice_S$k.bin" > "$VF/logs/dec_S${k}_n$n.bin" 2>>"$LOG"
    rc=$?
    [ $rc -ne 0 ] && echo "FLAWRUN_FAIL S$k run$n rc=$rc" | tee -a "$LOG"
  done
  H1=$(sha256sum "$VF/logs/dec_S${k}_n1.bin" | cut -d' ' -f1)
  DET=1
  for n in 2 3 4 5; do
    Hn=$(sha256sum "$VF/logs/dec_S${k}_n$n.bin" | cut -d' ' -f1)
    [ "$Hn" != "$H1" ] && DET=0
  done
  [ $DET -eq 1 ] && echo "DET S$k: byte-identical x5 ($H1)" | tee -a "$LOG" \
                   || echo "DET S$k: MISMATCH" | tee -a "$LOG"
  cp "$VF/logs/dec_S${k}_n1.bin" "$VF/logs/decisions_S$k.bin"
  # Score (scorer-side dir: $VF/logs, holding wires + decisions)
  "$VF/flawscore_bin" "$k" "$VF/logs" "wires_S$k.bin" "decisions_S$k.bin" \
    > "$VF/logs/verdict_S$k.txt" 2>>"$LOG"
  rc=$?
  [ $rc -ne 0 ] && echo "SCORE_FAIL S$k rc=$rc" | tee -a "$LOG"
  grep -E "^W7_STAT" "$VF/logs/verdict_S$k.txt" | tee -a "$LOG"
done
echo "== done ==" | tee -a "$LOG"
