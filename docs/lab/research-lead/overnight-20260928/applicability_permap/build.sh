export PATH="$HOME/safebin"
cd ~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/applicability_permap
ZNC=~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1
# Permap: per-candidate gate, phase1=1 (driver as written)
cat ma_base.zag ma_patch_permap.zag ma_driver_pm.zag > pm_full_permap.zag
# Treat: problem-level gate, phase1=1 (rerun sources verbatim)
cat ma_base.zag ma_patch.zag ma_driver.zag > pm_full_treat.zag
# Fresh: problem-level gate, phase1=0
sed 's/fn ma_do_phase1()i32 { return 1; }/fn ma_do_phase1()i32 { return 0; }/' ma_driver.zag > ma_driver_fresh.zag
cat ma_base.zag ma_patch.zag ma_driver_fresh.zag > pm_full_fresh.zag
# Naive: no gate, phase1=1
sed 's/fn ma_use_gate()i32 { return 1; }/fn ma_use_gate()i32 { return 0; }/' ma_driver.zag > ma_driver_naive.zag
cat ma_base.zag ma_patch.zag ma_driver_naive.zag > pm_full_naive.zag
echo "=== hook verification ==="
grep -h "^fn ma_use_gate\|^fn ma_do_phase1" pm_full_permap.zag pm_full_treat.zag pm_full_fresh.zag pm_full_naive.zag
echo "=== structural checks (expect 1/1/0 per file) ==="
for f in pm_full_permap.zag pm_full_treat.zag pm_full_fresh.zag pm_full_naive.zag; do
  echo "$f main=$(grep -c '^fn main' $f) evq=$(grep -c '^fn ev_query' $f) maq=$(grep -c '^fn ma_query' $f)"
done
echo "=== compile ==="
$ZNC pm_full_permap.zag -o pm_permap_bin > permap_compile.txt 2>&1
$ZNC pm_full_treat.zag -o pm_treat_bin > treat_compile.txt 2>&1
$ZNC pm_full_fresh.zag -o pm_fresh_bin > fresh_compile.txt 2>&1
$ZNC pm_full_naive.zag -o pm_naive_bin > naive_compile.txt 2>&1
grep -h "wrote native\|^znc: error" permap_compile.txt treat_compile.txt fresh_compile.txt naive_compile.txt
ls -la pm_permap_bin pm_treat_bin pm_fresh_bin pm_naive_bin
