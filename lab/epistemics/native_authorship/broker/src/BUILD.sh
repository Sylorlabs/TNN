#!/bin/bash
# BUILD.sh — reassemble the broker drivers from frozen sources.
# Usage: ./BUILD.sh <workdir>   (extracts via git show; never touches the sparse worktree)
# Toolchain: ~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
#   SHA-256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
set -e
W="${1:?usage: BUILD.sh <workdir>}"
LAB=~/workspace/selfpam_run/tnn-lab
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
SRC="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$W"/{armL,armD}
cd "$LAB"
# Arm L: frozen lookup intake.zag (e74271015) + IO
git show e74271015:docs/lab/mg_chunking_promote/intake.zag > "$W/armL/intake.zag"
# Arm D: frozen chooser (ab79f1a5c7d)
git show ab79f1a5c7d:docs/lab/native_authorship/chooser/chooser.zag > "$W/armD/chooser.zag"
git show ab79f1a5c7d:docs/lab/native_authorship/chooser/dlib.zag    > "$W/armD/dlib.zag"
git show ab79f1a5c7d:docs/lab/native_authorship/chooser/R33_NATIVE_IO_V1.zag > "$W/armD/R33_NATIVE_IO_V1.zag"
# Sealed battery as the trap carrier (af629be25)
git show af629be25:docs/lab/native_authorship/battery/battery.zag > "$W/armD/carrier.zag"
git show af629be25:docs/lab/native_authorship/battery/battery.zag > "$W/armL/carrier.zag"
cp "$SRC"/drvL.zag "$W/armL/"
cp "$SRC"/drvD.zag "$SRC"/drvD_feat.zag "$SRC"/drvD_def.zag "$SRC"/drvD_trace.zag "$W/armD/"
# Neuters: apply NEUTER_PATCHES.md to copies of chooser.zag, wire driver mains to them
# (mechanical: see NEUTER_PATCHES.md; the committed evidence used these builds)
echo "extracted; apply NEUTER_PATCHES.md, then build, e.g.:"
echo "  cd $W/armD && $ZNC drvD.zag -o drvD_bin"
