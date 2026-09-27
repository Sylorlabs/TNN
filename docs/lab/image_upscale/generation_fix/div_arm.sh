#!/bin/bash
# div_arm.sh <arm#> — diverse-set double run, low-disk profile:
# r1 -> save TSV + full SHAs -> rm r1 -> r2 -> SHA-compare vs r1 -> rm r2.
set -u
N=$1
GF=~/workspace/selfpam_run/tnn-lab/docs/lab/image_upscale/generation_fix
DS=~/workspace/selfpam_run/tnn-lab/docs/lab/image_upscale/diverse_set
SCR=~/workspace/scratch_div
BIN=$GF/build/azgen_a$N

cd $DS
echo "== arm$N diverse r1 =="
python3 eval_all.py --binary $BIN --outdir $SCR/a${N}_r1 > $SCR/a${N}_r1.log 2>&1 || { echo "FAIL arm$N r1"; tail -5 $SCR/a${N}_r1.log; exit 1; }
grep -E "^fabric|^woodgrain|^treebark|^calmwaters|^portrait|^car|^building|^cat|^market" $SCR/a${N}_r1.log
for f in $SCR/a${N}_r1/run_*/out/upscale_gen.bmp; do sha256sum $f; done | awk '{n=split($2,a,"/"); print a[n-2]" "$1}' | sort > $SCR/a${N}_r1_shas.txt
cp $SCR/a${N}_r1/RESULTS.tsv $GF/runs/scores_a${N}_diverse.tsv
cp $SCR/a${N}_r1_shas.txt $GF/runs/shas_a${N}_diverse_r1.txt
rm -rf $SCR/a${N}_r1
echo "== arm$N diverse r2 =="
python3 eval_all.py --binary $BIN --outdir $SCR/a${N}_r2 > $SCR/a${N}_r2.log 2>&1 || { echo "FAIL arm$N r2"; tail -5 $SCR/a${N}_r2.log; exit 1; }
for f in $SCR/a${N}_r2/run_*/out/upscale_gen.bmp; do sha256sum $f; done | awk '{n=split($2,a,"/"); print a[n-2]" "$1}' | sort > $SCR/a${N}_r2_shas.txt
echo "== arm$N diverse SHA r1 vs r2 =="
join -j 1 $SCR/a${N}_r1_shas.txt $SCR/a${N}_r2_shas.txt | \
  awk '{ s=($2==$3?"IDENTICAL":"DIFFER"); print s, $1 }'
rm -rf $SCR/a${N}_r2
df -h ~ | tail -1
echo "DONE div arm$N"
