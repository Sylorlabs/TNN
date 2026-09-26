#!/bin/bash
# video-composer STEP 2 run script: determinism + deliberation evidence.
# Usage: ./run_all.sh   (run from ~/workspace/video-composer)
set -euo pipefail
cd "$(dirname "$0")"

BIN=./src/composer_bin
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
BUNNY_FRAMES=~/workspace/video-repro/runs/out_verbatim
PIG_FRAMES=~/workspace/video-combine/source/frames

if [ ! -x "$BIN" ]; then
  (cd src && "$ZNC" composer.zag -o composer_bin)
fi

rm -rf runs
mkdir -p runs instr

# instruction files
printf 'merge the pig and the bunny together' > instr/merge.txt
printf 'show the pig and the bunny side by side' > instr/side.txt
printf 'show the pig and the bunny one after the other' > instr/then.txt
printf 'merge the field and the bunny together' > instr/merge_field.txt

echo "== ingest (x2 each) =="
"$BIN" ingest bunny "$BUNNY_FRAMES" runs/ingest_bunny_A
"$BIN" ingest pig   "$PIG_FRAMES"   runs/ingest_pig_A
"$BIN" ingest bunny "$BUNNY_FRAMES" runs/ingest_bunny_B
"$BIN" ingest pig   "$PIG_FRAMES"   runs/ingest_pig_B
cmp runs/ingest_bunny_A/store.bin runs/ingest_bunny_B/store.bin && echo "bunny stores byte-identical"
cmp runs/ingest_pig_A/store.bin   runs/ingest_pig_B/store.bin   && echo "pig stores byte-identical"
cmp runs/ingest_bunny_A/trace_ingest.txt runs/ingest_bunny_B/trace_ingest.txt && echo "bunny traces byte-identical"
cmp runs/ingest_pig_A/trace_ingest.txt   runs/ingest_pig_B/trace_ingest.txt   && echo "pig traces byte-identical"

echo "== recall + bit-exact check =="
"$BIN" recall runs/ingest_bunny_A runs/recall_bunny
"$BIN" recall runs/ingest_pig_A   runs/recall_pig
for f in "$BUNNY_FRAMES"/frame_*.ppm; do
  b=$(basename "$f")
  cmp "$f" "runs/recall_bunny/$b" || { echo "BUNNY MISMATCH $b"; exit 1; }
done
echo "bunny 24/24 frames bit-exact"
for f in "$PIG_FRAMES"/frame_*.ppm; do
  b=$(basename "$f")
  cmp "$f" "runs/recall_pig/$b" || { echo "PIG MISMATCH $b"; exit 1; }
done
echo "pig 24/24 frames bit-exact"

echo "== still ingest/recall (x2) =="
"$BIN" stillingest photo "$BUNNY_FRAMES/frame_00.ppm" runs/still_A
"$BIN" stillrecall runs/still_A runs/stillrecall_A/still.ppm
"$BIN" stillingest photo "$BUNNY_FRAMES/frame_00.ppm" runs/still_B
"$BIN" stillrecall runs/still_B runs/stillrecall_B/still.ppm
sha256sum "$BUNNY_FRAMES/frame_00.ppm" | awk '{print "src     "$1}'
sha256sum runs/stillrecall_A/still.ppm | awk '{print "recallA "$1}'
sha256sum runs/stillrecall_B/still.ppm | awk '{print "recallB "$1}'
cmp "$BUNNY_FRAMES/frame_00.ppm" runs/stillrecall_A/still.ppm && echo "still A bit-exact"
cmp runs/stillrecall_A/still.ppm runs/stillrecall_B/still.ppm && echo "still A/B byte-identical"

echo "== compose MERGE (x2) =="
"$BIN" compose runs/ingest_bunny_A runs/ingest_pig_A instr/merge.txt runs/compose_merge_A
"$BIN" compose runs/ingest_bunny_A runs/ingest_pig_A instr/merge.txt runs/compose_merge_B
cmp runs/compose_merge_A/compose_trace.txt runs/compose_merge_B/compose_trace.txt && echo "merge traces byte-identical"
for i in $(seq -w 0 23); do
  cmp "runs/compose_merge_A/frame_$i.ppm" "runs/compose_merge_B/frame_$i.ppm" || { echo "MERGE MISMATCH frame_$i"; exit 1; }
done
echo "merge 24/24 frames byte-identical across runs"
grep -E "^(selected|RESULT)" runs/compose_merge_A/compose_trace.txt

echo "== compose SIDE =="
"$BIN" compose runs/ingest_bunny_A runs/ingest_pig_A instr/side.txt runs/compose_side
grep -E "^(selected|RESULT)" runs/compose_side/compose_trace.txt

echo "== compose THEN =="
"$BIN" compose runs/ingest_bunny_A runs/ingest_pig_A instr/then.txt runs/compose_then
grep -E "^(selected|RESULT)" runs/compose_then/compose_trace.txt

echo "== comparison renders (xfade idx17, split idx12) =="
"$BIN" render runs/ingest_bunny_A runs/ingest_pig_A 17 runs/render_xfade
"$BIN" render runs/ingest_bunny_A runs/ingest_pig_A 12 runs/render_split
echo "renders done"

echo "== content-sensitivity pair (field) =="
if [ -d runs/ingest_field_A ]; then
  "$BIN" compose runs/ingest_bunny_A runs/ingest_field_A instr/merge_field.txt runs/compose_merge_field
  grep -E "^(selected|RESULT)" runs/compose_merge_field/compose_trace.txt
else
  echo "field memory not present; skipping"
fi

echo "== hashes =="
sha256sum runs/compose_merge_A/compose_trace.txt
sha256sum runs/compose_merge_A/frame_00.ppm runs/compose_merge_A/frame_23.ppm
echo ALL_STEPS_OK
