#!/bin/sh
# c_build.sh -- assemble and compile the grammar codec-induction experiment.
# Pure shell + znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/grammar_codec"
cd "$D"
# pinned znc rejects duplicate fn definitions: strip base main (driver wins)
awk '/^fn main\(/{skip=1; next} /^fn /{skip=0} {if (!skip) print}' "$D/c_base.zag" > "$D/c_base_nomain.zag"
cat "$D/c_base_nomain.zag" "$D/c_patch.zag" "$D/c_driver.zag" > "$D/c_full.zag"
echo "dup check (expect 1 each):"
grep -c "^fn main(\|^fn t2_trial(\|^fn gi_trial_build(\|^fn gi_induce(" "$D/c_full.zag"
"$ZNC" "$D/c_full.zag" -o "$D/c_bin" > "$D/c_compile.txt" 2>&1
if [ $? -eq 0 ]; then echo "BUILT c_bin"; else echo "FAILED c_bin"; tail -30 "$D/c_compile.txt"; exit 1; fi
echo "build-done"
