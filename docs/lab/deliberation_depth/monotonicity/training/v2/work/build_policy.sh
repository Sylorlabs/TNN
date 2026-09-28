#!/bin/bash
# v2 policy build: per-tag build trees with frozen trained params;
# build each tree twice (A/B), byte-compare.
set -u
T=~/workspace/tnn-lab/deliberation_depth/monotonicity/training/v2
SRC=$T/src
W=$T/work
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
build_tree() { # tag (uses params/mt2_params_<tag>.zag + trivial mt_gate.zag)
  local tag=$1
  for ab in a b; do
    local d="$W/polbuild_${tag}_${ab}"
    rm -rf "$d"; mkdir -p "$d"
    cp "$SRC/R33_NATIVE_SHA256_V2.zag" "$SRC/R33_NATIVE_IO_V1.zag" \
       "$SRC/dlb_util.zag" "$SRC/dlb_json.zag" "$SRC/dlb_cfg.zag" \
       "$SRC/dlb_ledger.zag" "$SRC/dlb_delib.zag" "$SRC/policy.zag" "$d/"
    cp "$T/params/mt2_params_${tag}.zag" "$d/mt_params.zag"
    cp "$SRC/mt_gate.zag" "$d/mt_gate.zag"
    (cd "$d" && "$ZNC" policy.zag --no-zagd --no-analyze --no-foreground-cache -o policy_bin)
    local rc=$?
    if [ $rc -ne 0 ]; then echo "BUILD-FAIL $tag $ab rc=$rc"; return 1; fi
    cp "$d/policy_bin" "$W/policy_bin_${tag}_${ab}"
  done
  if cmp -s "$W/policy_bin_${tag}_a" "$W/policy_bin_${tag}_b"; then
    echo "POLICY-BYTE-IDENTICAL $tag"
  else
    echo "POLICY-MISMATCH $tag"; return 1
  fi
  cp "$W/policy_bin_${tag}_a" "$W/policy_bin_${tag}"
  return 0
}
build_tree 10x
build_tree 100x
echo "POLICY-BUILD-DONE"
