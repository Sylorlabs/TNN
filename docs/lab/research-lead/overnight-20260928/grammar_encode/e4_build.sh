#!/bin/sh
# e4_build.sh -- assemble and compile the grammar encode-check experiment.
# Pure shell + znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/grammar_encode"
cd "$D"
# pinned znc rejects duplicate fn definitions: strip base main (driver wins)
awk '/^fn main\(/{skip=1; next} /^fn /{skip=0} {if (!skip) print}' "$D/e4_base.zag" > "$D/e4_base_nomain.zag"
cat "$D/e4_base_nomain.zag" "$D/e4_patch.zag" "$D/e4_driver.zag" > "$D/e4_full.zag"
echo "dup check (expect 1 each):"
grep -c "^fn main(\|^fn t2_trial(\|^fn gi_trial_build(\|^fn gi_induce(" "$D/e4_full.zag"
"$ZNC" "$D/e4_full.zag" -o "$D/e4_bin" > "$D/e4_compile.txt" 2>&1
if [ $? -eq 0 ]; then echo "BUILT e4_bin"; else echo "FAILED e4_bin"; tail -30 "$D/e4_compile.txt"; exit 1; fi
echo "build-done"
