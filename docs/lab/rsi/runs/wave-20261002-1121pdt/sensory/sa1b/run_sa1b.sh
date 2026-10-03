#!/bin/bash
# run_sa1b.sh -- SA1b sealed evaluation battery (frozen PREREG_SA1b.md).
# Pure Zag, safebin only. No Python. No em-dashes in logs.
export PATH="$HOME/safebin"
set -u
cd "$(dirname "$0")"
BIN=src/bin
CORP=../../../../../audio_longhorizon/corpus
ATOM=../../../../../audio_longhorizon/desynth/fixtures/atoms
OUT=out
EV=evidence
mkdir -p "$OUT" "$EV"

echo "which python3: [$(which python3)]"
echo "which znc: [$(which znc)]"

sha256sum $BIN/sa1b_isolate $BIN/sa1b_check $BIN/sa1b_render $BIN/sa1b_meter $BIN/desynth_render_base | tee $EV/bin.sha256

for atom in child speech; do
  case $atom in
    child) WAV=$CORP/child/child-fsd50k-171101.wav; AT=$ATOM/atom0_child.bin; F0=393176 ;;
    speech) WAV=$CORP/speech/speech-e22-000.wav; AT=$ATOM/atom1_speech.bin; F0=466296 ;;
  esac
  # isolator 1x + 2 determinism reruns
  S=$(date +%s%N); $BIN/sa1b_isolate "$WAV" $OUT/$atom.evt > $EV/isolate_$atom.log 2>&1; E=$(date +%s%N)
  echo "$atom isolate_wall_ms=$(( (E-S)/1000000 ))"
  $BIN/sa1b_isolate "$WAV" $OUT/$atom.r2.evt > /dev/null 2>&1
  $BIN/sa1b_isolate "$WAV" $OUT/$atom.r3.evt > /dev/null 2>&1
  sha256sum $OUT/$atom.evt $OUT/$atom.r2.evt $OUT/$atom.r3.evt | tee $EV/evt_$atom.sha256
  cmp $OUT/$atom.evt $OUT/$atom.r2.evt && cmp $OUT/$atom.evt $OUT/$atom.r3.evt && echo "$atom EVT determinism: BYTE-IDENTICAL x3"
  # baseline render 3x (atom only): committed renderer argv contract
  for r in 1 2 3; do $BIN/desynth_render_base "$AT" $OUT/$atom.base.$r.wav "$F0" 0 x 1000000 > /dev/null 2>&1; done
  sha256sum $OUT/$atom.base.1.wav $OUT/$atom.base.2.wav $OUT/$atom.base.3.wav | tee $EV/basewav_$atom.sha256
  cmp $OUT/$atom.base.1.wav $OUT/$atom.base.2.wav && cmp $OUT/$atom.base.1.wav $OUT/$atom.base.3.wav && echo "$atom baseline render: BYTE-IDENTICAL x3"
  # variant render 3x (atom + events via argv 7, SA1 frozen contract)
  for r in 1 2 3; do $BIN/sa1b_render "$AT" $OUT/$atom.var.$r.wav "$F0" 0 x 1000000 $OUT/$atom.evt > $EV/render_${atom}_$r.log 2>&1; done
  sha256sum $OUT/$atom.var.1.wav $OUT/$atom.var.2.wav $OUT/$atom.var.3.wav | tee $EV/varwav_$atom.sha256
  cmp $OUT/$atom.var.1.wav $OUT/$atom.var.2.wav && cmp $OUT/$atom.var.1.wav $OUT/$atom.var.3.wav && echo "$atom variant render: BYTE-IDENTICAL x3"
  # checker
  $BIN/sa1b_check "$WAV" $OUT/$atom.evt | tee $EV/check_$atom.txt
  # meters: baseline vs variant
  $BIN/sa1b_meter "$WAV" $OUT/$atom.base.1.wav | tee $EV/meter_${atom}_base.txt
  $BIN/sa1b_meter "$WAV" $OUT/$atom.var.1.wav | tee $EV/meter_${atom}_var.txt
done
echo "BATTERY DONE"
