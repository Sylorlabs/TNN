#!/bin/sh
# gi_build.sh -- assemble and compile the grammar-induction experiment.
# Pure shell + znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/grammar_induction"
cd "$D"
# pinned znc rejects duplicate fn definitions: strip base main (driver wins)
awk '/^fn main\(/{skip=1; next} /^fn /{skip=0} {if (!skip) print}' "$D/gi_base.zag" > "$D/gi_base_nomain.zag"
cat "$D/gi_base_nomain.zag" "$D/gi_patch.zag" "$D/gi_driver.zag" > "$D/gi_full.zag"
echo "dup check (expect 1 each):"
grep -c "^fn main(\|^fn t2_trial(\|^fn gi_trial_build(\|^fn gi_induce(" "$D/gi_full.zag"
"$ZNC" "$D/gi_full.zag" -o "$D/gi_bin" > "$D/gi_compile.txt" 2>&1
if [ $? -eq 0 ]; then echo "BUILT gi_bin"; else echo "FAILED gi_bin"; tail -30 "$D/gi_compile.txt"; exit 1; fi
echo "build-done"
