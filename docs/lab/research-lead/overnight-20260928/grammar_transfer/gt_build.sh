#!/bin/sh
# gt_build.sh -- assemble and compile the grammar-transfer experiment.
# Pure shell + znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/grammar_transfer"
cd "$D"
# pinned znc rejects duplicate fn definitions: strip base main (driver wins)
awk '/^fn main\(/{skip=1; next} /^fn /{skip=0} {if (!skip) print}' "$D/gt_base.zag" > "$D/gt_base_nomain.zag"
cat "$D/gt_base_nomain.zag" "$D/gt_patch.zag" "$D/gt_driver.zag" > "$D/gt_full.zag"
echo "dup check (expect 1 each):"
grep -c "^fn main(\|^fn t2_trial(\|^fn gi_trial_build(\|^fn gi_induce(" "$D/gt_full.zag"
"$ZNC" "$D/gt_full.zag" -o "$D/gt_bin" > "$D/gt_compile.txt" 2>&1
if [ $? -eq 0 ]; then echo "BUILT gt_bin"; else echo "FAILED gt_bin"; tail -30 "$D/gt_compile.txt"; exit 1; fi
echo "build-done"
