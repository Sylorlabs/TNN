#!/bin/sh
# fu_build.sh -- assemble and compile the formal-understanding experiment.
# Pure shell + znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/formal_understanding"
cd "$D"
# pinned znc rejects duplicate fn definitions: strip base main (driver wins)
awk '/^fn main\(/{skip=1; next} /^fn /{skip=0} {if (!skip) print}' "$D/fu_base.zag" > "$D/fu_base_nomain.zag"
cat "$D/fu_base_nomain.zag" "$D/fu_patch.zag" "$D/fu_driver.zag" > "$D/fu_full.zag"
echo "dup check (expect 1 each):"
grep -c "^fn main(\|^fn t2_trial(\|^fn fu_trial_build(" "$D/fu_full.zag"
"$ZNC" "$D/fu_full.zag" -o "$D/fu_bin" > "$D/fu_compile.txt" 2>&1
if [ $? -eq 0 ]; then echo "BUILT fu_bin"; else echo "FAILED fu_bin"; tail -30 "$D/fu_compile.txt"; exit 1; fi
echo "build-done"
