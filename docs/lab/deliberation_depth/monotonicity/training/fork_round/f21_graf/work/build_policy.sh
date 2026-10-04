#!/bin/bash
# F21 GRAF policy build: per-build trees with frozen trained params;
# build each tree twice (A/B), byte-compare.
set -u
T=~/workspace/tnn-lab/deliberation_depth/monotonicity/training/fork_round/f21_graf
SRC=$T/src
W=$T/work
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
for ab in a b; do
  d="$W/polbuild_$ab"
  rm -rf "$d"; mkdir -p "$d"
  cp "$SRC/R33_NATIVE_SHA256_V2.zag" "$SRC/R33_NATIVE_IO_V1.zag" \
     "$SRC/dlb_util.zag" "$SRC/dlb_json.zag" "$SRC/dlb_cfg.zag" \
     "$SRC/dlb_ledger.zag" "$SRC/dlb_delib.zag" "$SRC/policy.zag" "$d/"
  cp "$T/params/mt21_params.zag" "$d/mt_params.zag"
  cp "$SRC/mt_gate.zag" "$d/mt_gate.zag"
  (cd "$d" && "$ZNC" policy.zag --no-zagd --no-analyze --no-foreground-cache -o policy_bin)
  rc=$?
  if [ $rc -ne 0 ]; then echo "BUILD-FAIL $ab rc=$rc"; exit 1; fi
  cp "$d/policy_bin" "$W/policy_bin_$ab"
done
if cmp -s "$W/policy_bin_a" "$W/policy_bin_b"; then
  echo "POLICY-BYTE-IDENTICAL"
else
  echo "POLICY-MISMATCH"; exit 1
fi
cp "$W/policy_bin_a" "$W/policy_bin"
echo "policy sha256: $(sha256sum "$W/policy_bin" | cut -d' ' -f1)"
