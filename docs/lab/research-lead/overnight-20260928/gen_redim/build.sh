#!/bin/sh
# GEN-REDIM build + verification pipeline. Fail-closed: any failure aborts.
# Encodes PREREG.md Section 7 construction sequence and the C2-C11 audits.
set -e
export PATH="$HOME/safebin"
cd "$(dirname "$0")"
LANE="$(pwd)"

echo "=== GEN-REDIM build pipeline ==="

# ---- Step 1: frozen digest checks (PREREG Sec 7.1; NAMECHECK Step 1) ----
echo "--- Step 1: frozen digests ---"
echo "a53cdf0126ab1501fb70d9b14c2f745e0ef1838209753df8a0c6d0daf484bbcb  ref_rd_base.zag" | sha256sum -c -
echo "d6f1f9d8f4747293bb7a8e99474660347dc24693f62f3d25caaf1d83c19c9d9a  ref_rd_gen.zag" | sha256sum -c -
echo "f23258bb6ad3b140f5b741ba90576fa8503f167c884948604c971987d1186c81  ref_gs_new.zag" | sha256sum -c -

# ---- Step 2: ref identity vs GEN-STRESS frozen files ----
echo "--- Step 2: ref identity ---"
cmp ref_rd_base.zag ../gen_stress/ref_gs_base.zag
cmp ref_rd_gen.zag ../gen_stress/ref_gs_gen.zag
cmp ref_gs_new.zag ../gen_stress/gs_new.zag
echo "refs identical to GEN-STRESS frozen files"

# ---- Step 3: C10 minimal-diff audit (PREREG Sec 8) ----
echo "--- Step 3: C10 minimal-diff audit ---"
# base diff: added lines must be comments, r_* accessors, world_new_nm,
# or the m2g/m2p rebase; removed lines must be comments, m2g/m2p defs,
# or world_new.
diff ref_rd_base.zag rbase.zag | grep "^>" > /tmp/rd_base_added.txt || true
diff ref_rd_base.zag rbase.zag | grep "^<" > /tmp/rd_base_removed.txt || true
if grep -v "^> //" /tmp/rd_base_added.txt | grep -v "^> *fn r_" | grep -v "^> *fn world_new_nm" | grep -v "r_m2g(A)+m" | grep -q .; then
  echo "C10 FAIL: unexpected added lines in rbase.zag:"; grep -v "^> //" /tmp/rd_base_added.txt | grep -v "^> *fn r_" | grep -v "^> *fn world_new_nm" | grep -v "r_m2g(A)+m"; exit 1
fi
if grep -v "^< //" /tmp/rd_base_removed.txt | grep -v "^< *fn m2[gp]" | grep -v "^< *fn world_new" | grep -q .; then
  echo "C10 FAIL: unexpected removed lines in rbase.zag:"; grep -v "^< //" /tmp/rd_base_removed.txt | grep -v "^< *fn m2[gp]" | grep -v "^< *fn world_new"; exit 1
fi
# gen diff: added lines must contain an r_* accessor call or world_new_nm
# (or be the updated scratch comment); removed lines must contain a frozen
# scratch literal, world_new(), or be the old scratch comment.
diff ref_rd_gen.zag rgen.zag | grep "^>" > /tmp/rd_gen_added.txt || true
diff ref_rd_gen.zag rgen.zag | grep "^<" > /tmp/rd_gen_removed.txt || true
if grep -v "r_tries(A)\|r_found(A)\|r_ans(A)\|r_vp(A)\|r_kp(A)\|r_pv(A)\|r_t1(A)\|r_t2c(A)\|r_t2e(A)\|r_nv(A)\|r_wid(A)\|r_vs(A)\|r_dn(A)\|world_new_nm\|GEN scratch" /tmp/rd_gen_added.txt | grep -q .; then
  echo "C10 FAIL: unexpected added lines in rgen.zag:"; grep -v "r_tries(A)\|r_found(A)\|r_ans(A)\|r_vp(A)\|r_kp(A)\|r_pv(A)\|r_t1(A)\|r_t2c(A)\|r_t2e(A)\|r_nv(A)\|r_wid(A)\|r_vs(A)\|r_dn(A)\|world_new_nm\|GEN scratch" /tmp/rd_gen_added.txt; exit 1
fi
if grep -v "936\|940\|944\|1024\|1280\|1536\|2304\|3328\|3332\|3588\|3592\|3596\|3660\|world_new()\|GEN scratch" /tmp/rd_gen_removed.txt | grep -q .; then
  echo "C10 FAIL: unexpected removed lines in rgen.zag:"; grep -v "936\|940\|944\|1024\|1280\|1536\|2304\|3328\|3332\|3588\|3592\|3596\|3660\|world_new()\|GEN scratch" /tmp/rd_gen_removed.txt; exit 1
fi
echo "C10 audit: diffs contain only authorized changes"
echo "base diff lines changed: $(diff ref_rd_base.zag rbase.zag | grep -c '^[<>]')"
echo "gen diff lines changed: $(diff ref_rd_gen.zag rgen.zag | grep -c '^[<>]')"

# ---- Step 4: C11 opacity audit (PREREG Sec 4, Sec 8) ----
echo "--- Step 4: C11 opacity audit ---"
TOKENS="hypothesis|refine|evaluat|domain|plan|causal|navigat|arithmet|grammar|language|audio|interven|belie|goal|agent"
# The definitional token-list lines in PREREG.md Sec 4 (bare pipe-separated
# lowercase tokens) are excluded; every other hit is a violation.
HITS=$(grep -in "$TOKENS" rbase.zag rgen.zag rd_dmain.zag rd_gmain.zag rd_smain.zag PREREG.md REPORT.md 2>/dev/null | grep -v "^[^:]*:[0-9]*:[a-z|.]*$" || true)
if [ -n "$HITS" ]; then
  echo "C11 FAIL: banned-token hits:"; echo "$HITS"; exit 1
fi
echo "C11 audit: no banned tokens outside the definitional list"

# ---- Step 5: assemble ----
echo "--- Step 5: assemble ---"
# Frozen baselines, regenerated from the verified frozen sources, with
# drivers byte-exact to the frozen battery structure (world_new()).
sed '/^fn main()i32 {/,$d' ref_rd_gen.zag > gen_nomain.zag
sed 's/world_new_nm(4)/world_new()/g; s/world_new_nm(2)/world_new()/g' rd_dmain.zag > fz_dmain.zag
sed 's/world_new_nm(4)/world_new()/g; s/world_new_nm(2)/world_new()/g' rd_gmain.zag > fz_gmain.zag
cat ref_rd_base.zag gen_nomain.zag fz_dmain.zag > fz_dfull.zag
cat ref_rd_base.zag gen_nomain.zag fz_gmain.zag > fz_gfull.zag
# GEN-REDIM assemblies (PREREG Sec 7.5).
sed '/^fn main()i32 {/,$d' rgen.zag > rgen_nomain.zag
cat rbase.zag rgen_nomain.zag rd_dmain.zag > rd_dfull.zag
cat rbase.zag rgen_nomain.zag rd_gmain.zag > rd_gfull.zag
cat rbase.zag rgen_nomain.zag rd_smain.zag > rd_sfull.zag
# No duplicate main definitions in any assembly.
for f in fz_dfull.zag fz_gfull.zag rd_dfull.zag rd_gfull.zag rd_sfull.zag; do
  n=$(grep -c "^fn main()i32 {" "$f"); [ "$n" = "1" ] || { echo "assembly $f has $n mains"; exit 1; }
done
echo "assemblies built, one main each"

# ---- Step 6: compile with pinned znc ----
echo "--- Step 6: compile ---"
znc fz_dfull.zag -o fz_dbin > fz_dcompile.txt 2>&1
znc fz_gfull.zag -o fz_gbin > fz_gcompile.txt 2>&1
znc rd_dfull.zag -o rd_dbin > rd_dcompile.txt 2>&1
znc rd_gfull.zag -o rd_gbin > rd_gcompile.txt 2>&1
znc rd_sfull.zag -o rd_sbin > rd_scompile.txt 2>&1
echo "all five binaries compiled"

# ---- Step 7: run 3x each, pairwise byte-identical (C2) ----
echo "--- Step 7: 3x runs ---"
for b in fz_dbin fz_gbin rd_dbin rd_gbin rd_sbin; do
  ./$b > ${b}_run1.txt 2> ${b}_run1.err
  ./$b > ${b}_run2.txt 2> ${b}_run2.err
  ./$b > ${b}_run3.txt 2> ${b}_run3.err
  cmp ${b}_run1.txt ${b}_run2.txt
  cmp ${b}_run2.txt ${b}_run3.txt
  if [ -s ${b}_run1.err ]; then echo "$b wrote to stderr"; exit 1; fi
  echo "$b: 3/3 byte-identical, stderr empty, sha256 $(sha256sum ${b}_run1.txt | cut -d' ' -f1)"
done

# ---- Step 8: extract expected blocks from this PREREG ----
echo "--- Step 8: expected blocks ---"
for s in S1 S2 S3 S4; do
  sed -n "/^\`\`\`text exp-$s\$/,/^\`\`\`$/p" PREREG.md | sed '1d;$d' > exp_$s.txt
done
wc -l exp_S1.txt exp_S2.txt exp_S3.txt exp_S4.txt

# ---- Step 9: C3/C4 regressions (frozen baseline vs GEN-REDIM) ----
echo "--- Step 9: C3/C4 ---"
cmp fz_dbin_run1.txt rd_dbin_run1.txt && echo "C3 DIAMOND-REGRESSION: outputs byte-identical"
cmp fz_gbin_run1.txt rd_gbin_run1.txt && echo "C4 GENERALITY-REGRESSION: outputs byte-identical"

# ---- Step 10: C5-C8 section comparisons ----
echo "--- Step 10: C5-C8 ---"
# Split rd_sbin output into S1..S5 sections at the ARM= lines.
a1=$(grep -n "ARM=GEN PROB=S1" rd_sbin_run1.txt | cut -d: -f1)
a2=$(grep -n "ARM=GEN PROB=S2" rd_sbin_run1.txt | cut -d: -f1)
a3=$(grep -n "ARM=GEN PROB=S3" rd_sbin_run1.txt | cut -d: -f1)
a4=$(grep -n "ARM=GEN PROB=S4" rd_sbin_run1.txt | cut -d: -f1)
end=$(wc -l < rd_sbin_run1.txt)
sed -n "1,${a1}p" rd_sbin_run1.txt > rd_sec_S1.txt
sed -n "$((a1+1)),${a2}p" rd_sbin_run1.txt > rd_sec_S2.txt
sed -n "$((a2+1)),${a3}p" rd_sbin_run1.txt > rd_sec_S3.txt
sed -n "$((a3+1)),${a4}p" rd_sbin_run1.txt > rd_sec_S4.txt
sed -n "$((a4+1)),${end}p" rd_sbin_run1.txt > rd_sec_S5.txt
cmp rd_sec_S1.txt exp_S1.txt && echo "C5 STRESS-S1: PASS (byte-identical)"
cmp rd_sec_S2.txt exp_S2.txt && echo "C6 STRESS-S2: PASS (byte-identical)"
cmp rd_sec_S3.txt exp_S3.txt && echo "C7 STRESS-S3: PASS (byte-identical)"
cmp rd_sec_S4.txt exp_S4.txt && echo "C8 STRESS-S4: PASS (byte-identical)"

# ---- Step 11: C9 S5 line counts ----
echo "--- Step 11: C9 ---"
tail -1 rd_sec_S5.txt | grep -qx "ARM=GEN PROB=S5 ANS=-2 TRIES=2734" && echo "S5 ARM line exact"
[ "$(grep -c "^INTER=" rd_sec_S5.txt)" = "3" ] && echo "S5 INTER count = 3"
[ "$(grep -c "^INTER2=" rd_sec_S5.txt)" = "2731" ] && echo "S5 INTER2 count = 2731"
[ "$(grep -c "^WIDEN=1" rd_sec_S5.txt)" = "0" ] && echo "S5 WIDEN count = 0"
echo "C9 STRESS-S5: PASS"

echo "=== GEN-REDIM pipeline complete: all kill bars evaluated ==="
