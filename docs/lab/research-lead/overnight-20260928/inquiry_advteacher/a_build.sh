#!/bin/sh
# a_build.sh -- assemble and compile the adversarial-teacher inquiry experiment.
# Pure shell + znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/inquiry_advteacher"
cd "$D"
# pinned znc rejects duplicate fn definitions: strip base main (driver wins)
awk '/^fn main\(/{skip=1; next} /^fn /{skip=0} {if (!skip) print}' "$D/a_base.zag" > "$D/a_base_nomain.zag"
cat "$D/a_base_nomain.zag" "$D/a_patch.zag" "$D/a_driver.zag" > "$D/a_full.zag"
echo "dup check (expect 1 each):"
grep -c "^fn main(\|^fn adv_world(\|^fn gi_induce(" "$D/a_full.zag"
"$ZNC" "$D/a_full.zag" -o "$D/a_bin" > "$D/a_compile.txt" 2>&1
if [ $? -eq 0 ]; then echo "BUILT a_bin"; else echo "FAILED a_bin"; tail -30 "$D/a_compile.txt"; exit 1; fi
echo "build-done"
