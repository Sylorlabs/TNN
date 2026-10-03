#!/bin/sh
# tx_build.sh -- assemble and compile the TX1 experiment.
# Pure shell + znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/formal_richer"
cd "$D"
# pinned znc rejects duplicate fn definitions: strip base main (driver wins)
awk '/^fn main\(/{skip=1; next} /^fn /{skip=0} {if (!skip) print}' "$D/tx_base.zag" > "$D/tx_base_nomain.zag"
cat "$D/tx_base_nomain.zag" "$D/tx_patch.zag" "$D/tx_driver.zag" > "$D/tx_full.zag"
echo "dup check (expect 1 each):"
grep -c "^fn main(\|^fn t2_trial(\|^fn tx_induce(\|^fn tx_trial_build(" "$D/tx_full.zag"
"$ZNC" "$D/tx_full.zag" -o "$D/tx_bin" > "$D/tx_compile.txt" 2>&1
if [ $? -eq 0 ]; then echo "BUILT tx_bin"; else echo "FAILED tx_bin"; tail -30 "$D/tx_compile.txt"; exit 1; fi
echo "build-done"
