#!/bin/sh
# h_build.sh -- assemble and compile the hardened inquiry experiment.
# Pure shell + znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/inquiry_hardened"
cd "$D"
# pinned znc rejects duplicate fn definitions: strip base main (driver wins)
awk '/^fn main\(/{skip=1; next} /^fn /{skip=0} {if (!skip) print}' "$D/h_base.zag" > "$D/h_base_nomain.zag"
cat "$D/h_base_nomain.zag" "$D/h_patch.zag" "$D/h_driver.zag" > "$D/h_full.zag"
echo "dup check (expect 1 each):"
grep -c "^fn main(\|^fn h_world(\|^fn gi_induce(\|^fn gi_inquiry_accept(" "$D/h_full.zag"
"$ZNC" "$D/h_full.zag" -o "$D/h_bin" > "$D/h_compile.txt" 2>&1
if [ $? -eq 0 ]; then echo "BUILT h_bin"; else echo "FAILED h_bin"; tail -30 "$D/h_compile.txt"; exit 1; fi
echo "build-done"
