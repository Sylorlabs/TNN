#!/bin/bash
# Build script for Node2-v2 generalization tests.
# Pure shell + znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
DIR="$HOME/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/node2_generalization"
cd "$DIR"

# Core source is lines 1-1020 of gen_base.zag (before test battery).
# For multi-policy tests, use gen_multi.zag lines 1-1020 (same split; verify).

build_one() {
  local src="$1"   # gen_base.zag or gen_multi.zag
  local drv="$2"   # driver file
  local out="$3"   # output binary name
  local nlines="$4" # core source lines (before test battery)
  head -n "$nlines" "$src" > "/tmp/${out}_full.zag"
  cat "$drv" >> "/tmp/${out}_full.zag"
  "$ZNC" "/tmp/${out}_full.zag" -o "$DIR/$out"
  if [ $? -eq 0 ]; then
    echo "BUILT $out"
  else
    echo "FAILED $out"
    return 1
  fi
}

build_one gen_base.zag gen_test1_threshold.zag gen_test1_bin 1020
build_one gen_base.zag gen_test4_revision.zag gen_test4_bin 1020
build_one gen_base.zag gen_test5_noise.zag gen_test5_bin 1020
build_one gen_multi.zag gen_test2_multi.zag gen_test2_bin 1082
build_one gen_multi.zag gen_test3_ctxdep.zag gen_test3_bin 1082

echo "build-done"
