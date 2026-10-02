#!/bin/sh
# g3_build.sh -- assemble and compile the grammar-third-system experiment.
# Pure shell + znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/grammar_third"
cd "$D"
# pinned znc rejects duplicate fn definitions: strip base main (driver wins)
awk '/^fn main\(/{skip=1; next} /^fn /{skip=0} {if (!skip) print}' "$D/g3_base.zag" > "$D/g3_base_nomain.zag"
cat "$D/g3_base_nomain.zag" "$D/g3_patch.zag" "$D/g3_driver.zag" > "$D/g3_full.zag"
echo "dup check (expect 1 each):"
grep -c "^fn main(\|^fn t2_trial(\|^fn gi_trial_build(\|^fn gi_induce(" "$D/g3_full.zag"
"$ZNC" "$D/g3_full.zag" -o "$D/g3_bin" > "$D/g3_compile.txt" 2>&1
if [ $? -eq 0 ]; then echo "BUILT g3_bin"; else echo "FAILED g3_bin"; tail -30 "$D/g3_compile.txt"; exit 1; fi
echo "build-done"
