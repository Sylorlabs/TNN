#!/bin/sh
# adv_build.sh -- assemble and compile the inquiry adversary experiment.
# Pure shell + znc. No Python. The hardened mechanism
# (h_base_nomain.zag + h_patch.zag) is linked UNMODIFIED; only the
# adversary driver (adv_driver.zag) is new.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/inquiry_adversary"
cd "$D"
cat "$D/h_base_nomain.zag" "$D/h_patch.zag" "$D/adv_driver.zag" > "$D/adv_full.zag"
echo "dup check (expect 1 each):"
grep -c "^fn main(\|^fn a2_world(\|^fn gi_induce(\|^fn gi_inquiry_accept(" "$D/adv_full.zag"
"$ZNC" "$D/adv_full.zag" -o "$D/adv_bin" > "$D/adv_compile.txt" 2>&1
if [ $? -eq 0 ]; then echo "BUILT adv_bin"; else echo "FAILED adv_bin"; tail -30 "$D/adv_compile.txt"; exit 1; fi
echo "build-done"
