#!/bin/sh
# go_build.sh -- assemble and compile the outlier-exclusion experiment.
# Pure shell + znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/grammar_outlier"
cd "$D"
# pinned znc rejects duplicate fn definitions: strip base main (driver wins)
awk '/^fn main\(/{skip=1; next} /^fn /{skip=0} {if (!skip) print}' "$D/go_base.zag" > "$D/go_base_nomain.zag"
cat "$D/go_base_nomain.zag" "$D/go_patch.zag" "$D/go_driver.zag" > "$D/go_full.zag"
echo "dup check (expect 1 each):"
grep -c "^fn main(\|^fn t2_trial(\|^fn gi_induce(\|^fn gi_induce2(" "$D/go_full.zag"
"$ZNC" "$D/go_full.zag" -o "$D/go_bin" > "$D/go_compile.txt" 2>&1
if [ $? -eq 0 ]; then echo "BUILT go_bin"; else echo "FAILED go_bin"; tail -30 "$D/go_compile.txt"; exit 1; fi
echo "build-done"
