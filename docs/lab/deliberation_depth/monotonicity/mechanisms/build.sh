#!/bin/bash
# Build mech.zag with the PINNED znc toolchain. Compile twice and prove
# byte-identical binaries (determinism gate).
set -e
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
SRC=~/workspace/tnn-lab/deliberation_depth/monotonicity/mechanisms
cd "$SRC/src"
"$ZNC" mech.zag --no-zagd --no-analyze --no-foreground-cache -o "$SRC/mech_bin_a"
"$ZNC" mech.zag --no-zagd --no-analyze --no-foreground-cache -o "$SRC/mech_bin_b"
if cmp -s "$SRC/mech_bin_a" "$SRC/mech_bin_b"; then
  echo "DETERMINISTIC BUILD: mech_bin_a == mech_bin_b"
else
  echo "BUILD NON-DETERMINISTIC: a and b differ"
  exit 1
fi
sha256sum "$SRC/mech_bin_a"
