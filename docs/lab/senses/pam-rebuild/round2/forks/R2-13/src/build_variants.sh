#!/bin/bash
# build_variants.sh — compile the R2-13 eval binaries from enrolled tables.
# Must be run from the src/ directory (znc resolves @imports relative to cwd).
# Produces: fsf_fullbin (modes full/noclause), fsf_coarsebin (mode coarse).
set -e
SRC="$(cd "$(dirname "$0")" && pwd)"
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
TBL="$1"   # tables dir from enroll.py
cp "$TBL/tables_full.zag" "$SRC/tables.zag"
cp "$TBL/falsebank.zag"  "$SRC/bank.zag"
"$ZNC" build fsf.zag -o fsf_fullbin
cp "$TBL/tables_coarse.zag" "$SRC/tables.zag"
cp "$SRC/bank_stub.zag"     "$SRC/bank.zag"
"$ZNC" build fsf.zag -o fsf_coarsebin
ls -la "$SRC/fsf_fullbin" "$SRC/fsf_coarsebin"
