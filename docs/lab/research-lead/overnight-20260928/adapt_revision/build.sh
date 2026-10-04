#!/bin/sh
# build.sh -- assemble, compile, and run the adapt_revision binary 3x.
# Pure Zag. Safebin PATH required.
export PATH="$HOME/safebin"
set -u
L=docs/lab/research-lead/overnight-20260928/adapt_revision
if [ "$(which python3 2>/dev/null)" != "" ]; then
  echo "GUARD-FAIL: python3 resolves in PATH"; exit 1
fi
if [ "$(which python 2>/dev/null)" != "" ]; then
  echo "GUARD-FAIL: python resolves in PATH"; exit 1
fi
echo "guard: python3/python absent, znc=$(which znc)"
cd "$HOME/workspace/tnn-rsi" || exit 1
echo "--- frozen-source integrity (K7) ---"
echo "cc_base_copy=$(sha256sum $L/cc_base.zag | cut -d' ' -f1)"
echo "cc_base_orig=$(sha256sum docs/lab/research-lead/overnight-20260928/composition_C/cc_base.zag | cut -d' ' -f1)"
echo "un_patch_copy=$(sha256sum $L/un_patch.zag | cut -d' ' -f1)"
echo "un_patch_orig=$(sha256sum docs/lab/research-lead/overnight-20260928/composition_adapt/un_patch.zag | cut -d' ' -f1)"
echo "adapt_patch_copy=$(sha256sum $L/adapt_patch.zag | cut -d' ' -f1)"
echo "adapt_patch_orig=$(sha256sum docs/lab/research-lead/overnight-20260928/composition_adapt/adapt_patch.zag | cut -d' ' -f1)"
cat "$L/cc_base.zag" "$L/un_patch.zag" "$L/adapt_patch.zag" "$L/revise_patch.zag" "$L/rv_driver.zag" > "$L/rv_full.zag"
echo "--- kill-bar source checks ---"
echo "mode_bridge_handler_occurrences=$(grep -ci 'mode\|bridge\|handler' "$L/revise_patch.zag" "$L/rv_driver.zag")"
echo "forbidden_slice_pattern=$(grep -c 'as \*i32' "$L/revise_patch.zag" "$L/rv_driver.zag")"
echo "task_label_dispatch=$(grep -ci 'task' "$L/revise_patch.zag")"
echo "--- compile ---"
znc "$L/rv_full.zag" -o "$L/rv_bin" > "$L/compile.txt" 2>&1
echo "compile exit=$?"
ls -la "$L/rv_bin"
echo "--- run 3x ---"
for r in 1 2 3; do
  "$L/rv_bin" > "$L/run$r.txt" 2>&1
  echo "run$r exit=$?"
done
sha256sum "$L/run1.txt" "$L/run2.txt" "$L/run3.txt" | tee "$L/sha256sums.txt"
cmp "$L/run1.txt" "$L/run2.txt" && cmp "$L/run2.txt" "$L/run3.txt" && echo "DETERMINISM-OK: 3/3 byte-identical"
echo "--- verdict lines ---"
grep -E "^R[1234]-.*=PASS|^R[1234]-.*=FAIL" "$L/run1.txt"
echo "--- K6 dash byte check (expect 0 0) ---"
grep -c $'\xe2\x80\x94' "$L/PREREG.md" "$L/revise_patch.zag" "$L/rv_driver.zag" 2>/dev/null | grep -v ":0" || echo "no em dashes"
grep -c $'\xe2\x80\x93' "$L/PREREG.md" "$L/revise_patch.zag" "$L/rv_driver.zag" 2>/dev/null | grep -v ":0" || echo "no en dashes"
echo "BUILD-DONE"
