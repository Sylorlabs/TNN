#!/bin/bash
# C5 flaw-score re-run driver (Track B closeout).
# Unblocked by the W5 pcodec rebuild (frozen §B.3): the REAL learner ingresses
# the REAL arm-1 teacher wires with the REAL p_decode — no integration shim.
# Full session harness still blocked (session_close skips TAPE_FOOTER, replay
# honest-FAIL; harness files owned by another crew, untouched) — sessions are
# fixture-framed TST-1 tapes per the W8 driver pattern (see flawrun_frozen.zag).
#
# N=5 byte-identical runs per slice + adversarial wire perturbations (P-a..P-d).
set -u
cd "$(dirname "$0")/../.." || exit 1   # -> units/teachers
HERE="$(pwd)"
VF="$HERE/curriculum/verify_flawscore"
C5="$VF/logs/c5"
ZNC="${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}"
mkdir -p "$C5"

echo "== build flawrun_frozen =="
"$ZNC" "$VF/flawrun_frozen.zag" --no-zagd --no-analyze --no-foreground-cache \
  -o "$VF/flawrun_frozen_bin" 2>&1 | tail -2
echo "== build flawscore_run (frozen battery, unmodified source) =="
"$ZNC" "$VF/flawscore_run.zag" --no-zagd --no-analyze --no-foreground-cache \
  -o "$VF/flawscore_bin" 2>&1 | tail -2
[ -x "$VF/flawrun_frozen_bin" ] || { echo "BUILD_FAIL flawrun_frozen"; exit 1; }
[ -x "$VF/flawscore_bin" ] || { echo "BUILD_FAIL flawscore"; exit 1; }

LOG="$C5/c5_run.log"
: > "$LOG"
echo "== C5 flaw re-run: $(date -u +%FT%TZ) ==" | tee -a "$LOG"

# Stage inputs (verified byte-identical to arm1/wired/expected + wired slices).
for k in 0 1 2 3 4 5 6 7; do
  cp "$HERE/arm1/wired/slice_S$k.bin" "$C5/slice_S$k.bin"
  cp "$HERE/arm1/wired/expected/S$k.bin" "$C5/wires_S$k.bin"
done

for k in 0 1 2 3 4 5 6 7; do
  echo "--- slice S$k ---" | tee -a "$LOG"
  for n in 1 2 3 4 5; do
    "$VF/flawrun_frozen_bin" "$k" "$C5" "wires_S$k.bin" "slice_S$k.bin" "tape_S${k}_n$n.bin" \
      > "$C5/dec_S${k}_n$n.bin" 2>>"$LOG"
    rc=$?
    [ $rc -ne 0 ] && echo "C5_RUN_FAIL S$k run$n rc=$rc" | tee -a "$LOG"
  done
  H1=$(sha256sum "$C5/dec_S${k}_n1.bin" | cut -d' ' -f1)
  T1=$(sha256sum "$C5/tape_S${k}_n1.bin" | cut -d' ' -f1)
  DET=1
  TDET=1
  for n in 2 3 4 5; do
    Hn=$(sha256sum "$C5/dec_S${k}_n$n.bin" | cut -d' ' -f1)
    [ "$Hn" != "$H1" ] && DET=0
    Tn=$(sha256sum "$C5/tape_S${k}_n$n.bin" | cut -d' ' -f1)
    [ "$Tn" != "$T1" ] && TDET=0
  done
  [ $DET -eq 1 ] && echo "DET S$k: decisions byte-identical x5 ($H1)" | tee -a "$LOG" \
                   || echo "DET S$k: DECISION MISMATCH" | tee -a "$LOG"
  [ $TDET -eq 1 ] && echo "TDET S$k: tapes byte-identical x5 ($T1)" | tee -a "$LOG" \
                   || echo "TDET S$k: TAPE MISMATCH" | tee -a "$LOG"
  # Cross-check: no-shim decisions must equal W7's shim decisions
  # (proves the codec swap preserved deliberation behavior).
  HW7=$(sha256sum "$VF/logs/decisions_S$k.bin" | cut -d' ' -f1)
  [ "$H1" = "$HW7" ] && echo "SHIMCHECK S$k: byte-identical to W7 shim decisions" | tee -a "$LOG" \
                      || echo "SHIMCHECK S$k: DIFFERS from W7 (investigate)" | tee -a "$LOG"
  cp "$C5/dec_S${k}_n1.bin" "$C5/decisions_S$k.bin"
  cp "$C5/tape_S${k}_n1.bin" "$C5/tape_S$k.bin"
  "$VF/flawscore_bin" "$k" "$C5" "wires_S$k.bin" "decisions_S$k.bin" \
    > "$C5/verdict_S$k.txt" 2>>"$LOG"
  rc=$?
  [ $rc -ne 0 ] && echo "SCORE_FAIL S$k rc=$rc" | tee -a "$LOG"
  grep -E "^W7_STAT" "$C5/verdict_S$k.txt" | tee -a "$LOG"
done
echo "== baseline done ==" | tee -a "$LOG"
