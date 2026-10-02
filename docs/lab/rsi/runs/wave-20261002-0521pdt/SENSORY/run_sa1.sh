#!/bin/bash
# run_sa1.sh - SA1 sealed evaluation pipeline (frozen PREREG_SA1.md, bars B1-B8).
# Pure Zag binaries + bash only. Run from the SENSORY/ lane directory.
set -u
export PATH="$HOME/safebin"
LANE="$(cd "$(dirname "$0")" && pwd)"
cd "$LANE"
BIN="$LANE/src/bin"
ATOMS="$LANE/../../../../audio_longhorizon/desynth/fixtures/atoms"
CORPUS="$LANE/../../../../audio_longhorizon/corpus"
mkdir -p out evidence

echo "=== SA1 sealed run, $(date -u +%FT%TZ) ==="

echo "--- 1. isolator: child (1x + 2 determinism reruns) ---"
S=$(date +%s%N); "$BIN/sa1_isolate" "$CORPUS/child/child-fsd50k-171101.wav" out/child.evt > evidence/isolate_child.log 2>&1; E=$(date +%s%N)
echo "isolate_child_wall_ms=$(( (E - S) / 1000000 ))" | tee -a evidence/isolate_child.log
"$BIN/sa1_isolate" "$CORPUS/child/child-fsd50k-171101.wav" out/child_r2.evt > evidence/isolate_child_r2.log 2>&1
"$BIN/sa1_isolate" "$CORPUS/child/child-fsd50k-171101.wav" out/child_r3.evt > evidence/isolate_child_r3.log 2>&1
sha256sum out/child.evt out/child_r2.evt out/child_r3.evt | tee evidence/sha_isolate_child.txt

echo "--- 2. isolator: speech (1x + 2 determinism reruns) ---"
S=$(date +%s%N); "$BIN/sa1_isolate" "$CORPUS/speech/speech-e22-000.wav" out/speech.evt > evidence/isolate_speech.log 2>&1; E=$(date +%s%N)
echo "isolate_speech_wall_ms=$(( (E - S) / 1000000 ))" | tee -a evidence/isolate_speech.log
"$BIN/sa1_isolate" "$CORPUS/speech/speech-e22-000.wav" out/speech_r2.evt > evidence/isolate_speech_r2.log 2>&1
"$BIN/sa1_isolate" "$CORPUS/speech/speech-e22-000.wav" out/speech_r3.evt > evidence/isolate_speech_r3.log 2>&1
sha256sum out/speech.evt out/speech_r2.evt out/speech_r3.evt | tee evidence/sha_isolate_speech.txt

echo "--- 3. baseline renders 3x per atom (committed renderer, unmodified) ---"
for atom in child speech; do
  if [ "$atom" = "child" ]; then AB="$ATOMS/atom0_child.bin"; F0=393176; else AB="$ATOMS/atom1_speech.bin"; F0=466296; fi
  for r in 1 2 3; do
    S=$(date +%s%N)
    "$BIN/desynth_render_base" "$AB" "out/base_${atom}_${r}.wav" "$F0" 0 x 1000000 > "evidence/render_base_${atom}_${r}.log" 2>&1
    E=$(date +%s%N)
    echo "base_${atom}_${r}_wall_ms=$(( (E - S) / 1000000 ))" | tee -a "evidence/render_base_${atom}_${r}.log"
  done
done
sha256sum out/base_child_*.wav out/base_speech_*.wav | tee evidence/sha_base.txt

echo "--- 4. variant renders 3x per atom ---"
for atom in child speech; do
  if [ "$atom" = "child" ]; then AB="$ATOMS/atom0_child.bin"; F0=393176; else AB="$ATOMS/atom1_speech.bin"; F0=466296; fi
  for r in 1 2 3; do
    S=$(date +%s%N)
    "$BIN/sa1_render" "$AB" "out/var_${atom}_${r}.wav" "$F0" 0 x 1000000 "out/${atom}.evt" > "evidence/render_var_${atom}_${r}.log" 2>&1
    E=$(date +%s%N)
    echo "var_${atom}_${r}_wall_ms=$(( (E - S) / 1000000 ))" | tee -a "evidence/render_var_${atom}_${r}.log"
  done
done
sha256sum out/var_child_*.wav out/var_speech_*.wav | tee evidence/sha_var.txt

echo "--- 5. meters ---"
{
  echo -e "label\tn\tpeak\trms\tdc\tclip\tH\tonset_rate\tf0_mhz"
  "$BIN/sa1_meter" "$CORPUS/child/child-fsd50k-171101.wav" src_child
  "$BIN/sa1_meter" "$CORPUS/speech/speech-e22-000.wav" src_speech
  "$BIN/sa1_meter" out/base_child_1.wav base_child
  "$BIN/sa1_meter" out/base_speech_1.wav base_speech
  "$BIN/sa1_meter" out/var_child_1.wav var_child
  "$BIN/sa1_meter" out/var_speech_1.wav var_speech
} | tee evidence/meters.tsv

echo "--- 6. event-file sizes ---"
ls -la out/child.evt out/speech.evt | tee evidence/evt_sizes.txt

echo "=== SA1 sealed run complete ==="
