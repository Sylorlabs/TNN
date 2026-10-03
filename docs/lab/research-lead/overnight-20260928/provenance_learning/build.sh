#!/bin/sh
# Build: provenance policy learning, treatment vs hardcoded-rank control.
export PATH="$HOME/safebin"
D=~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/provenance_learning
ZNC=~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1
cd "$D" || exit 1
# control patch: exactly one line differs (rank_fixed 0 -> 1)
sed 's/fn rank_fixed()i32 { return 0; }/fn rank_fixed()i32 { return 1; }/' pl_patch.zag > pl_patch_ctl.zag
echo "--- patch diff (must be exactly one line) ---"
diff pl_patch.zag pl_patch_ctl.zag
cat pl_nomain.zag pl_patch.zag pl_driver.zag > pl_full_trt.zag
cat pl_nomain.zag pl_patch_ctl.zag pl_driver.zag > pl_full_ctl.zag
"$ZNC" build pl_full_trt.zag -o pl_trt_bin 2>znc_trt_err.txt || { echo "TRT BUILD FAIL"; cat znc_trt_err.txt; exit 1; }
"$ZNC" build pl_full_ctl.zag -o pl_ctl_bin 2>znc_ctl_err.txt || { echo "CTL BUILD FAIL"; cat znc_ctl_err.txt; exit 1; }
echo "builds ok"
i=1
while [ $i -le 3 ]; do
  ./pl_trt_bin > pl_trt_run$i.txt 2>&1 || { echo "TRT RUN $i FAIL"; exit 1; }
  ./pl_ctl_bin > pl_ctl_run$i.txt 2>&1 || { echo "CTL RUN $i FAIL"; exit 1; }
  i=$((i+1))
done
echo "--- determinism ---"
sha256sum pl_trt_run1.txt pl_trt_run2.txt pl_trt_run3.txt | cut -c1-16
sha256sum pl_ctl_run1.txt pl_ctl_run2.txt pl_ctl_run3.txt | cut -c1-16
cmp pl_trt_run1.txt pl_trt_run2.txt && cmp pl_trt_run1.txt pl_trt_run3.txt && echo "TRT 3/3 identical"
cmp pl_ctl_run1.txt pl_ctl_run2.txt && cmp pl_ctl_run1.txt pl_ctl_run3.txt && echo "CTL 3/3 identical"
