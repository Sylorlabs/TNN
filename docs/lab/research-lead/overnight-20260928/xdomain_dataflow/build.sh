#!/bin/sh
export PATH="$HOME/safebin"
D=~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/xdomain_dataflow
C=~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/composition_C
ZNC=~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1
cat $C/cc_base.zag $D/df_patch.zag $D/df_driver.zag > $D/df_full.zag
cat $C/cc_base.zag $D/df_patch_nodf.zag $D/df_driver.zag > $D/df_full_nodf.zag
$ZNC $D/df_full.zag -o $D/df_bin 2> $D/df_compile.txt; echo "treat build exit=$?"
$ZNC $D/df_full_nodf.zag -o $D/df_nodf_bin 2> $D/df_compile_nodf.txt; echo "nodf build exit=$?"
