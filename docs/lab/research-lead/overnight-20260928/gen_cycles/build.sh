#!/bin/sh
# build.sh -- GEN-CYCLES frozen build/run/audit (PREREG Sections 6-7).
# Fail-closed: any audit failure aborts (set -e).
set -e
export PATH="$HOME/safebin"
cd ~/workspace/docs/lab/research-lead/overnight-20260928/gen_cycles

echo "== audit C7: opacity (no domain-story tokens in built sources) =="
if grep -i -E 'hypothesis|refine|evaluat|domain|plan|causal|navigat|arithmet|grammar|language|audio|interven|belie|goal|agent' gc_base.zag gc_uni.zag cyc_nomain.zag gc_main.zag gc_redmain.zag uni_nomain.zag; then
  echo "C7 BANNED TOKEN FOUND"; exit 1
fi
echo "C7 ok"

echo "== audit C8: no cycle-specific handler (fixpoint only in comments) =="
FPLINES=$(grep -n -i 'fixpoint' gc_uni.zag || true)
echo "$FPLINES"
echo "$FPLINES" | while IFS= read -r line; do
  case "$line" in
    *'//'*fixpoint*|*'//'*Fixpoint*|*'//'*FIXPOINT*) ;;
    "") ;;
    *) echo "C8 NON-COMMENT FIXPOINT: $line"; exit 1 ;;
  esac
done
echo "C8 ok (uniform v==prev halt; see REPORT for the read-audit)"

echo "== audit: frozen region copies =="
cmp gc_base.zag ~/workspace/docs/lab/research-lead/overnight-20260928/compose_cycles/cyc_base.zag
sed '/^fn main/,$d' ref_uc_uni.zag | cmp - uni_nomain.zag
sed '/^fn main/,$d' ref_cyc_new.zag | cmp - cyc_nomain.zag
echo "regions ok"

echo "== assemble gc_full.zag =="
cat gc_base.zag uni_nomain.zag gc_uni.zag cyc_nomain.zag gc_main.zag > gc_full.zag
S1=$(wc -c < gc_base.zag); S2=$(wc -c < uni_nomain.zag); S3=$(wc -c < gc_uni.zag)
S4=$(wc -c < cyc_nomain.zag); S5=$(wc -c < gc_main.zag)
head -c "$S1" gc_full.zag | cmp - gc_base.zag
tail -c +"$((S1+1))" gc_full.zag | head -c "$S2" | cmp - uni_nomain.zag
tail -c +"$((S1+S2+1))" gc_full.zag | head -c "$S3" | cmp - gc_uni.zag
tail -c +"$((S1+S2+S3+1))" gc_full.zag | head -c "$S4" | cmp - cyc_nomain.zag
tail -c "$S5" gc_full.zag | cmp - gc_main.zag
echo "gc_full regions ok"

echo "== assemble gc_redfull.zag =="
cat gc_base.zag uni_nomain.zag gc_uni.zag cyc_nomain.zag gc_redmain.zag > gc_redfull.zag
SR=$(wc -c < gc_redmain.zag)
tail -c "$SR" gc_redfull.zag | cmp - gc_redmain.zag
head -c "$((S1+S2+S3+S4))" gc_redfull.zag > /tmp/red_prefix.bin
head -c "$((S1+S2+S3+S4))" gc_full.zag > /tmp/main_prefix.bin
cmp /tmp/red_prefix.bin /tmp/main_prefix.bin
echo "gc_redfull regions ok (shared prefix identical, driver differs)"

echo "== compile with pinned safebin znc =="
znc gc_full.zag -o gc_bin
znc gc_redfull.zag -o gc_redbin
ls -la gc_bin gc_redbin

echo "== run gc_bin 3x (C2) =="
./gc_bin > gc_run1.txt
./gc_bin > gc_run2.txt
./gc_bin > gc_run3.txt
cmp gc_run1.txt gc_run2.txt && cmp gc_run2.txt gc_run3.txt
echo "3/3 byte-identical (C2)"
sha256sum gc_run1.txt gc_run2.txt gc_run3.txt

echo "== C4: cycle workload must PASS =="
grep 'ARM=GC PROB=QC ANS=1005 TRIES=23' gc_run1.txt
if grep -q 'WIDEN=2' gc_run1.txt; then echo "C4 UNEXPECTED WIDEN=2"; exit 1; fi
echo "C4 ok: ANS=1005 TRIES=23, no WIDEN=2"

echo "== C5: U 5-pair regression (seqmax=8 must match frozen U) =="
QCLINE=$(grep -n 'ARM=GC PROB=QC' gc_run1.txt | cut -d: -f1)
tail -n +"$((QCLINE+5))" gc_run1.txt | sed 's/ARM=GC/ARM=UNI/' > /tmp/gc_pairs8.txt
cmp /tmp/gc_pairs8.txt ref_u_out.txt
echo "C5 ok: 5 pairs byte-identical to frozen U (up to ARM label)"

echo "== run gc_redbin 3x =="
./gc_redbin > gc_red1.txt
./gc_redbin > gc_red2.txt
./gc_redbin > gc_red3.txt
cmp gc_red1.txt gc_red2.txt && cmp gc_red2.txt gc_red3.txt
echo "reduction 3/3 byte-identical"

echo "== C3: reduction to U (seqmax=2 must BE U) =="
cat ref_cyc_out.txt ref_u_out.txt > /tmp/red_expected.txt
cmp gc_red1.txt /tmp/red_expected.txt
echo "C3 ok: seqmax=2 output byte-identical to frozen U (cycle + 5 pairs)"

echo "== GEN regression assemblies =="
cat genreg_base.zag genreg_gen.zag genreg_dmain.zag > genreg_dfull.zag
cat genreg_base.zag genreg_gen.zag genreg_gg.zag > genreg_gfull.zag
G1=$(wc -c < genreg_base.zag); G2=$(wc -c < genreg_gen.zag)
head -c "$G1" genreg_dfull.zag | cmp - genreg_base.zag
tail -c +"$((G1+1))" genreg_dfull.zag | head -c "$G2" | cmp - genreg_gen.zag
echo "genreg regions ok"
znc genreg_dfull.zag -o genreg_dbin
znc genreg_gfull.zag -o genreg_gbin

echo "== C6: GEN diamond + generality regressions =="
./genreg_dbin > genreg_d1.txt; ./genreg_dbin > genreg_d2.txt; ./genreg_dbin > genreg_d3.txt
cmp genreg_d1.txt genreg_d2.txt && cmp genreg_d2.txt genreg_d3.txt
cmp genreg_d1.txt ref_diamond_out.txt
echo "diamond ok: byte-identical to recorded GEN output"
./genreg_gbin > genreg_g1.txt; ./genreg_gbin > genreg_g2.txt; ./genreg_gbin > genreg_g3.txt
cmp genreg_g1.txt genreg_g2.txt && cmp genreg_g2.txt genreg_g3.txt
cmp genreg_g1.txt ref_gg_out.txt
echo "generality ok: byte-identical to recorded GEN output (fan-in/DAG-4/chain-3/partial)"

echo "== digests =="
sha256sum gc_bin gc_redbin genreg_dbin genreg_gbin
sha256sum gc_run1.txt gc_red1.txt genreg_d1.txt genreg_g1.txt
echo "BUILD DONE"
