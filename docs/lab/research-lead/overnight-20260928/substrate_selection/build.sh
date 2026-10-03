export PATH="$HOME/safebin"
cd ~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/substrate_selection
cat ss_core.zag ss_patch.zag ss_driver.zag > ss_full.zag
echo "=== main count (expect 1) ==="
grep -c "^fn main" ss_full.zag
~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1 ss_full.zag -o ss_bin > compile.log 2>&1
echo "build exit=$?"
./ss_bin > ss_run1.txt 2>&1; echo "run1 exit=$?"
./ss_bin > ss_run2.txt 2>&1; echo "run2 exit=$?"
./ss_bin > ss_run3.txt 2>&1; echo "run3 exit=$?"
sha256sum ss_run1.txt ss_run2.txt ss_run3.txt
cmp ss_run1.txt ss_run2.txt && cmp ss_run2.txt ss_run3.txt && echo "BYTE-IDENTICAL 3/3"
