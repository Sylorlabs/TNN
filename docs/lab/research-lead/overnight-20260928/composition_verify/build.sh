#!/bin/sh
# build.sh -- assemble, compile, and run the composition_verify binary 3x.
# Pure Zag. Safebin PATH required.
export PATH="$HOME/safebin"
set -u
L=docs/lab/research-lead/overnight-20260928/composition_verify
if [ "$(which python3 2>/dev/null)" != "" ]; then
  echo "GUARD-FAIL: python3 resolves in PATH"; exit 1
fi
if [ "$(which python 2>/dev/null)" != "" ]; then
  echo "GUARD-FAIL: python resolves in PATH"; exit 1
fi
echo "guard: python3/python absent, znc=$(which znc)"
cd "$HOME/workspace/tnn-rsi" || exit 1
cat "$L/iv_mech.zag" "$L/iv_main.zag" > "$L/iv_full.zag"
echo "--- kill-bar source checks (frozen prereg) ---"
echo "answerkey_occurrences_in_zag=$(grep -ci 'expected' "$L/iv_mech.zag" "$L/iv_main.zag")"
echo "gate_write_sites:"; grep -n 'set32(E,0' "$L/iv_mech.zag"
echo "learner_select_definitions=$(grep -c 'fn learner_select' "$L/iv_mech.zag")"
echo "learner_update_definitions=$(grep -c 'fn learner_update' "$L/iv_mech.zag")"
echo "--- compile ---"
znc "$L/iv_full.zag" -o "$L/iv_bin" > "$L/compile.txt" 2>&1
echo "compile exit=$?"
ls -la "$L/iv_bin"
echo "--- run 3x ---"
for r in 1 2 3; do
  "$L/iv_bin" > "$L/run$r.txt" 2>&1
  echo "run$r exit=$?"
done
sha256sum "$L/run1.txt" "$L/run2.txt" "$L/run3.txt" | tee "$L/sha256sums.txt"
cmp "$L/run1.txt" "$L/run2.txt" && cmp "$L/run2.txt" "$L/run3.txt" && echo "DETERMINISM-OK: 3/3 byte-identical"
echo "BUILD-DONE"
