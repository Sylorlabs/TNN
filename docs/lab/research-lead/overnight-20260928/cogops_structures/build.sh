export PATH="$HOME/safebin"
cd ~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/cogops_structures
~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1 cogops.zag -o cogops_bin > compile.log 2>&1
echo "build exit=$?"
./cogops_bin > run1.txt 2>&1; echo "run1 exit=$?"
./cogops_bin > run2.txt 2>&1; echo "run2 exit=$?"
./cogops_bin > run3.txt 2>&1; echo "run3 exit=$?"
sha256sum run1.txt run2.txt run3.txt
cmp run1.txt run2.txt && cmp run2.txt run3.txt && echo "BYTE-IDENTICAL 3/3"
