export PATH="$HOME/safebin"
cd ~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/meta_applicability
ZNC=~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1
# Treat: gate=1, phase1=1 (driver as written)
cat ma_base.zag ma_patch.zag ma_driver.zag > ma_full_treat.zag
# Fresh: gate=1, phase1=0
sed 's/fn ma_do_phase1()i32 { return 1; }/fn ma_do_phase1()i32 { return 0; }/' ma_driver.zag > ma_driver_fresh.zag
cat ma_base.zag ma_patch.zag ma_driver_fresh.zag > ma_full_fresh.zag
# Naive: gate=0, phase1=1
sed 's/fn ma_use_gate()i32 { return 1; }/fn ma_use_gate()i32 { return 0; }/' ma_driver.zag > ma_driver_naive.zag
cat ma_base.zag ma_patch.zag ma_driver_naive.zag > ma_full_naive.zag
echo "=== hook verification ==="
grep -h "^fn ma_use_gate\|^fn ma_do_phase1" ma_full_treat.zag ma_full_fresh.zag ma_full_naive.zag
echo "=== structural checks (expect 1/1/0 per file) ==="
for f in ma_full_treat.zag ma_full_fresh.zag ma_full_naive.zag; do
  echo "$f main=$(grep -c '^fn main' $f) evq=$(grep -c '^fn ev_query' $f) maq=$(grep -c '^fn ma_query' $f)"
done
echo "=== compile ==="
$ZNC ma_full_treat.zag -o ma_treat_bin > treat_compile.txt 2>&1
$ZNC ma_full_fresh.zag -o ma_fresh_bin > fresh_compile.txt 2>&1
$ZNC ma_full_naive.zag -o ma_naive_bin > naive_compile.txt 2>&1
grep -h "wrote native\|^znc: error" treat_compile.txt fresh_compile.txt naive_compile.txt
ls -la ma_treat_bin ma_fresh_bin ma_naive_bin
