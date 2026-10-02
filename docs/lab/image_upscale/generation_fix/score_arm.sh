#!/bin/bash
# score_arm.sh <arm#> — runs arm binary twice on bridge+sky, SHA-compares, scores.
# Usage: score_arm.sh N   (N in 0 1 2 3)
set -u
N=$1
GF=~/workspace/selfpam_run/tnn-lab/docs/lab/image_upscale/generation_fix
GEN=~/workspace/selfpam_run/tnn-lab/docs/lab/image_upscale/generation
BIN=$GF/build/azgen_a$N
MET=$GEN/src/metrics.py
SCR=~/workspace/scratch_div/bs_$N

for img in bridge sky; do
  INDIR=$SCR/${img}_in
  mkdir -p $INDIR
  cp $GEN/run_${img}_1/input.bmp $GEN/run_${img}_1/gt.bmp $GEN/teach_out/vocab.bin $INDIR/
  for r in 1 2; do
    OUT=$SCR/${img}_out_$r
    mkdir -p $OUT
    $BIN $INDIR $OUT > $OUT/stdout.txt 2>&1 || { echo "FAIL arm$N $img run$r"; exit 1; }
  done
  echo "== arm$N $img: SHA compare run1 vs run2 =="
  for f in upscale_gen.bmp upscale_bicubic.bmp labels_raw.bin labelmap.bmp GEN_TRACE.txt; do
    s1=$(sha256sum $SCR/${img}_out_1/$f | cut -d' ' -f1)
    s2=$(sha256sum $SCR/${img}_out_2/$f | cut -d' ' -f1)
    if [ "$s1" == "$s2" ]; then st=IDENTICAL; else st=DIFFER; fi
    echo "  $f $st ${s1:0:16}"
  done
  echo "== arm$N $img: scores (run1) =="
  python3 $MET $INDIR/gt.bmp $SCR/${img}_out_1/upscale_gen.bmp $SCR/${img}_out_1/upscale_bicubic.bmp
  echo "== arm$N $img: trace =="
  grep -E "SHAPES G|order:" $SCR/${img}_out_1/GEN_TRACE.txt | head -3
done
echo "DONE arm$N"
