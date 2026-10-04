#!/bin/sh
# build.sh -- assemble, compile, and run the sequential_revision binary 3x.
# Pure Zag. Safebin PATH required.
export PATH="$HOME/safebin"
set -u
L=docs/lab/research-lead/overnight-20260928/sequential_revision
if [ "$(which python3 2>/dev/null)" != "" ]; then
  echo "GUARD-FAIL: python3 resolves in PATH"; exit 1
fi
if [ "$(which python 2>/dev/null)" != "" ]; then
  echo "GUARD-FAIL: python resolves in PATH"; exit 1
fi
echo "guard: python3/python absent, znc=$(which znc)"
cd "$HOME/workspace/tnn-rsi" || exit 1
cat "$L/sr_mech.zag" "$L/sr_main.zag" > "$L/sr_full.zag"
echo "--- kill-bar source checks (frozen prereg K-SR-4) ---"
echo "answerkey_occurrences_in_zag=$(grep -ci 'expected' "$L/sr_mech.zag" "$L/sr_main.zag")"
echo "gate_write_sites (world_init init + world_downstream consequence signal):"
grep -n 'set32(E,4' "$L/sr_mech.zag"
echo "learner_E_writes (expect 0: learner only reads the kind law via kind_probe):"
for f in learner_refute boundary_search learner_refine; do
  sed -n "/^fn $f/,/^}/p" "$L/sr_mech.zag" | grep -c 'set32(E'
done
echo "learner_fn_definitions (expect 1 each):"
echo "learner_refute=$(grep -c '^fn learner_refute' "$L/sr_mech.zag")"
echo "boundary_search=$(grep -c '^fn boundary_search' "$L/sr_mech.zag")"
echo "learner_refine=$(grep -c '^fn learner_refine' "$L/sr_mech.zag")"
echo "rule_induce=$(grep -c '^fn rule_induce' "$L/sr_mech.zag")"
echo "rule_pred=$(grep -c '^fn rule_pred' "$L/sr_mech.zag")"
total_nset=$(grep -c 'nset(' "$L/sr_mech.zag")
in_induce=$(sed -n '/^fn rule_induce/,/^}/p' "$L/sr_mech.zag" | grep -c 'nset(')
in_refine=$(sed -n '/^fn learner_refine/,/^}/p' "$L/sr_mech.zag" | grep -c 'nset(')
echo "node_cell_writes total=$total_nset induce=$in_induce refine=$in_refine (expect 11 2 8: 1 def + 10 calls, all inside induce/refine)"
echo "nset_in_driver (expect 0): $(grep -c 'nset(' "$L/sr_main.zag")"
for f in learner_refute boundary_search learner_refine; do
  n=$(sed -n "/^fn $f/,/^}/p" "$L/sr_mech.zag" | grep -wE -c '31|32|33|34|40|50|60|66|67|70|80')
  echo "value_literals_inside_$f (expect 0): $n"
done
echo "driver_calls_to_learner_operators (must pass no values):"
grep -n 'learner_refute(\|boundary_search(\|learner_refine(' "$L/sr_main.zag"
echo "exception_machinery_occurrences=$(grep -ci 'exception' "$L/sr_mech.zag" "$L/sr_main.zag")"
echo "mode_bridge_handler_occurrences=$(grep -ci 'mode\|bridge\|handler' "$L/sr_mech.zag" "$L/sr_main.zag")"
echo "forbidden_slice_pattern=$(grep -c 'as \*i32' "$L/sr_mech.zag" "$L/sr_main.zag")"
echo "--- compile ---"
znc "$L/sr_full.zag" -o "$L/sr_bin" > "$L/compile.txt" 2>&1
echo "compile exit=$?"
ls -la "$L/sr_bin"
echo "--- run 3x ---"
for r in 1 2 3; do
  "$L/sr_bin" > "$L/run$r.txt" 2>&1
  echo "run$r exit=$?"
done
sha256sum "$L/run1.txt" "$L/run2.txt" "$L/run3.txt" | tee "$L/sha256sums.txt"
cmp "$L/run1.txt" "$L/run2.txt" && cmp "$L/run2.txt" "$L/run3.txt" && echo "DETERMINISM-OK: 3/3 byte-identical"
echo "--- K-SR-3 preservation text checks ---"
echo "node0_desc_in_both_dumps (expect 2): $(grep -c '\[0:split T=33 L=1 R=2\]' "$L/run1.txt")"
echo "node1_desc_in_both_dumps (expect 2): $(grep -c '\[1:leaf NODE\]' "$L/run1.txt")"
echo "revise2_after_exact (expect 1): $(grep -c 'after=IF(in<33,NODE,IF(in<66,NUM,STR))' "$L/run1.txt")"
echo "--- K-SR-4 unseen-input check: probe lines mentioning 40/60/50/80 (expect 0) ---"
grep -E '^(OBS|REFUTE-[12] link|REVISE-[12] SEARCH)' "$L/run1.txt" | grep -cE '(^|[^0-9])(40|60|50|80)([^0-9]|$)'
echo "BUILD-DONE"
