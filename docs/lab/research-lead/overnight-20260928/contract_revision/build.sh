#!/bin/sh
# build.sh -- assemble, compile, and run the contract_revision binary 3x.
# Pure Zag. Safebin PATH required.
export PATH="$HOME/safebin"
set -u
L=docs/lab/research-lead/overnight-20260928/contract_revision
if [ "$(which python3 2>/dev/null)" != "" ]; then
  echo "GUARD-FAIL: python3 resolves in PATH"; exit 1
fi
if [ "$(which python 2>/dev/null)" != "" ]; then
  echo "GUARD-FAIL: python resolves in PATH"; exit 1
fi
echo "guard: python3/python absent, znc=$(which znc)"
cd "$HOME/workspace/tnn-rsi" || exit 1
cat "$L/cr_mech.zag" "$L/cr_main.zag" > "$L/cr_full.zag"
echo "--- kill-bar source checks (frozen prereg) ---"
echo "answerkey_occurrences_in_zag=$(grep -ci 'expected' "$L/cr_mech.zag" "$L/cr_main.zag")"
echo "gate_write_sites:"; grep -n 'set32(E,0' "$L/cr_mech.zag"
echo "learner_refute_definitions=$(grep -c 'fn learner_refute' "$L/cr_mech.zag")"
echo "learner_revise_definitions=$(grep -c 'fn learner_revise' "$L/cr_mech.zag")"
echo "learner_update_definitions=$(grep -c 'fn learner_update' "$L/cr_mech.zag")"
echo "learner_select_definitions=$(grep -c 'fn learner_select' "$L/cr_mech.zag")"
echo "h1_finalize_definitions=$(grep -c 'fn h1_finalize' "$L/cr_mech.zag")"
echo "signature_cell_writes_outside_finalize:"
grep -n 'ls(L,base+4\|ls(L,base+5' "$L/cr_mech.zag"
echo "exception_cell_write_sites (must all sit inside learner_revise):"
grep -n 'ls(L,xb' "$L/cr_mech.zag"
echo "value_literals_inside_learner_refute (expect 0):"
sed -n '/^fn learner_refute/,/^}/p' "$L/cr_mech.zag" | grep -c '33\|34'
echo "value_literals_inside_learner_revise (expect 0):"
sed -n '/^fn learner_revise/,/^}/p' "$L/cr_mech.zag" | grep -c '33\|34'
echo "mode_bridge_handler_occurrences=$(grep -ci 'mode\|bridge\|handler' "$L/cr_mech.zag" "$L/cr_main.zag")"
echo "forbidden_slice_pattern=$(grep -c 'as \*i32' "$L/cr_mech.zag" "$L/cr_main.zag")"
echo "--- compile ---"
znc "$L/cr_full.zag" -o "$L/cr_bin" > "$L/compile.txt" 2>&1
echo "compile exit=$?"
ls -la "$L/cr_bin"
echo "--- run 3x ---"
for r in 1 2 3; do
  "$L/cr_bin" > "$L/run$r.txt" 2>&1
  echo "run$r exit=$?"
done
sha256sum "$L/run1.txt" "$L/run2.txt" "$L/run3.txt" | tee "$L/sha256sums.txt"
cmp "$L/run1.txt" "$L/run2.txt" && cmp "$L/run2.txt" "$L/run3.txt" && echo "DETERMINISM-OK: 3/3 byte-identical"
echo "BUILD-DONE"
