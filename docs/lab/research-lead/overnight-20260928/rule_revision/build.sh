#!/bin/sh
# build.sh -- assemble, compile, and run the rule_revision binary 3x.
# Pure Zag. Safebin PATH required.
export PATH="$HOME/safebin"
set -u
L=docs/lab/research-lead/overnight-20260928/rule_revision
if [ "$(which python3 2>/dev/null)" != "" ]; then
  echo "GUARD-FAIL: python3 resolves in PATH"; exit 1
fi
if [ "$(which python 2>/dev/null)" != "" ]; then
  echo "GUARD-FAIL: python resolves in PATH"; exit 1
fi
echo "guard: python3/python absent, znc=$(which znc)"
cd "$HOME/workspace/tnn-rsi" || exit 1
cat "$L/rr_mech.zag" "$L/rr_main.zag" > "$L/rr_full.zag"
echo "--- kill-bar source checks (frozen prereg) ---"
echo "answerkey_occurrences_in_zag=$(grep -ci 'expected' "$L/rr_mech.zag" "$L/rr_main.zag")"
echo "gate_write_sites:"; grep -n 'set32(E,0' "$L/rr_mech.zag"
echo "learner_refute_definitions=$(grep -c 'fn learner_refute' "$L/rr_mech.zag")"
echo "learner_refine_definitions=$(grep -c 'fn learner_refine' "$L/rr_mech.zag")"
echo "rule_induce_definitions=$(grep -c 'fn rule_induce' "$L/rr_mech.zag")"
echo "rule_pred_definitions=$(grep -c 'fn rule_pred' "$L/rr_mech.zag")"
echo "learner_update_definitions=$(grep -c 'fn learner_update' "$L/rr_mech.zag")"
echo "learner_select_definitions=$(grep -c 'fn learner_select' "$L/rr_mech.zag")"
echo "h1_finalize_definitions=$(grep -c 'fn h1_finalize' "$L/rr_mech.zag")"
echo "rule_cell_write_sites (must all sit inside rule_induce or learner_refine):"
grep -n 'ls(L,rb' "$L/rr_mech.zag"
total_rw=$(grep -c 'ls(L,rb' "$L/rr_mech.zag")
in_induce=$(sed -n '/^fn rule_induce/,/^}/p' "$L/rr_mech.zag" | grep -c 'ls(L,rb')
in_refine=$(sed -n '/^fn learner_refine/,/^}/p' "$L/rr_mech.zag" | grep -c 'ls(L,rb')
echo "rule_write_sites total=$total_rw induce=$in_induce refine=$in_refine (expect 6 2 4)"
echo "value_literals_inside_learner_refute (expect 0):"
sed -n '/^fn learner_refute/,/^}/p' "$L/rr_mech.zag" | grep -c '33\|34\|30'
echo "value_literals_inside_learner_refine (expect 0):"
sed -n '/^fn learner_refine/,/^}/p' "$L/rr_mech.zag" | grep -c '33\|34\|30'
echo "exception_machinery_occurrences=$(grep -ci 'exception' "$L/rr_mech.zag" "$L/rr_main.zag")"
echo "mode_bridge_handler_occurrences=$(grep -ci 'mode\|bridge\|handler' "$L/rr_mech.zag" "$L/rr_main.zag")"
echo "forbidden_slice_pattern=$(grep -c 'as \*i32' "$L/rr_mech.zag" "$L/rr_main.zag")"
echo "--- compile ---"
znc "$L/rr_full.zag" -o "$L/rr_bin" > "$L/compile.txt" 2>&1
echo "compile exit=$?"
ls -la "$L/rr_bin"
echo "--- run 3x ---"
for r in 1 2 3; do
  "$L/rr_bin" > "$L/run$r.txt" 2>&1
  echo "run$r exit=$?"
done
sha256sum "$L/run1.txt" "$L/run2.txt" "$L/run3.txt" | tee "$L/sha256sums.txt"
cmp "$L/run1.txt" "$L/run2.txt" && cmp "$L/run2.txt" "$L/run3.txt" && echo "DETERMINISM-OK: 3/3 byte-identical"
echo "--- K-RR-4 unseen-input check: OBS lines for 34/30 (expect 0) ---"
grep -c 'OBS D in=34\|OBS D in=30' "$L/run1.txt" || true
echo "BUILD-DONE"
