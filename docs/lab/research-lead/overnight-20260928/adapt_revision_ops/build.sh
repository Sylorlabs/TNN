#!/bin/sh
# build.sh -- assemble, compile, and run the adapt_revision_ops binary 3x.
# Pure Zag. Safebin PATH required.
export PATH="$HOME/safebin"
set -u
L=docs/lab/research-lead/overnight-20260928/adapt_revision_ops
if [ "$(which python3 2>/dev/null)" != "" ]; then
  echo "GUARD-FAIL: python3 resolves in PATH"; exit 1
fi
if [ "$(which python 2>/dev/null)" != "" ]; then
  echo "GUARD-FAIL: python resolves in PATH"; exit 1
fi
echo "guard: python3/python absent, znc=$(which znc)"
cd "$HOME/workspace/tnn-rsi" || exit 1
echo "--- frozen-source integrity (K-H2) ---"
echo "cc_base_copy=$(sha256sum $L/cc_base.zag | cut -d' ' -f1)"
echo "cc_base_orig=$(sha256sum docs/lab/research-lead/overnight-20260928/composition_C/cc_base.zag | cut -d' ' -f1)"
echo "un_patch_copy=$(sha256sum $L/un_patch.zag | cut -d' ' -f1)"
echo "un_patch_orig=$(sha256sum docs/lab/research-lead/overnight-20260928/composition_adapt/un_patch.zag | cut -d' ' -f1)"
echo "adapt_patch_copy=$(sha256sum $L/adapt_patch.zag | cut -d' ' -f1)"
echo "adapt_patch_orig=$(sha256sum docs/lab/research-lead/overnight-20260928/composition_adapt/adapt_patch.zag | cut -d' ' -f1)"
echo "revise_patch_copy=$(sha256sum $L/revise_patch.zag | cut -d' ' -f1)"
echo "revise_patch_orig=$(sha256sum docs/lab/research-lead/overnight-20260928/adapt_revision/revise_patch.zag | cut -d' ' -f1)"
cat "$L/cc_base.zag" "$L/un_patch.zag" "$L/adapt_patch.zag" "$L/revise_patch.zag" "$L/ts_patch.zag" "$L/ts_driver.zag" > "$L/ts_full.zag"
echo "--- kill-bar source checks ---"
echo "mode_bridge_handler_occurrences=$(grep -ci 'mode\|bridge\|handler' "$L/ts_patch.zag" "$L/ts_driver.zag")"
echo "forbidden_slice_pattern=$(grep -c 'as \*i32' "$L/ts_patch.zag" "$L/ts_driver.zag")"
echo "--- compile ---"
znc "$L/ts_full.zag" -o "$L/ts_bin" > "$L/compile.txt" 2>&1
echo "compile exit=$?"
ls -la "$L/ts_bin"
echo "--- run 3x ---"
for r in 1 2 3; do
  "$L/ts_bin" > "$L/run$r.txt" 2>&1
  echo "run$r exit=$?"
done
sha256sum "$L/run1.txt" "$L/run2.txt" "$L/run3.txt" | tee "$L/sha256sums.txt"
cmp "$L/run1.txt" "$L/run2.txt" && cmp "$L/run2.txt" "$L/run3.txt" && echo "DETERMINISM-OK: 3/3 byte-identical"
echo "--- verdict lines ---"
grep -E "^(T1|T2|S1|S2|S3)-.*=PASS|^(T1|T2|S1|S2|S3)-.*=FAIL" "$L/run1.txt"
echo "--- K-H1 dash byte check (expect 0 0) ---"
grep -c $'\xe2\x80\x94' "$L/PREREG.md" "$L/PREREG_AMENDMENT1.md" "$L/ts_patch.zag" "$L/ts_driver.zag" 2>/dev/null | grep -v ":0" || echo "no em dashes"
grep -c $'\xe2\x80\x93' "$L/PREREG.md" "$L/PREREG_AMENDMENT1.md" "$L/ts_patch.zag" "$L/ts_driver.zag" 2>/dev/null | grep -v ":0" || echo "no en dashes"
echo "BUILD-DONE"
