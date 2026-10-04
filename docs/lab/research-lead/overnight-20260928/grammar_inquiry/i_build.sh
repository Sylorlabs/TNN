#!/bin/sh
# i_build.sh -- assemble and compile the grammar active-inquiry experiment.
# Pure shell + znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/grammar_inquiry"
cd "$D"
# pinned znc rejects duplicate fn definitions: strip base main (driver wins)
awk '/^fn main\(/{skip=1; next} /^fn /{skip=0} {if (!skip) print}' "$D/i_base.zag" > "$D/i_base_nomain.zag"
cat "$D/i_base_nomain.zag" "$D/i_patch.zag" "$D/i_driver.zag" > "$D/i_full.zag"
echo "dup check (expect 1 each):"
grep -c "^fn main(\|^fn t2_trial(\|^fn gi_trial_build(\|^fn gi_induce(" "$D/i_full.zag"
"$ZNC" "$D/i_full.zag" -o "$D/i_bin" > "$D/i_compile.txt" 2>&1
if [ $? -eq 0 ]; then echo "BUILT i_bin"; else echo "FAILED i_bin"; tail -30 "$D/i_compile.txt"; exit 1; fi
echo "build-done"
