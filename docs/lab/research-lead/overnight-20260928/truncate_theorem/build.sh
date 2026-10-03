#!/bin/sh
# build.sh -- assemble, compile, and run the truncate_theorem binary 3x.
# Pure Zag. Safebin PATH required.
export PATH="$HOME/safebin"
set -u
L=docs/lab/research-lead/overnight-20260928/truncate_theorem
SRC=docs/lab/research-lead/overnight-20260928/adapt_revision_ops
if [ "$(which python3 2>/dev/null)" != "" ]; then
  echo "GUARD-FAIL: python3 resolves in PATH"; exit 1
fi
if [ "$(which python 2>/dev/null)" != "" ]; then
  echo "GUARD-FAIL: python resolves in PATH"; exit 1
fi
echo "guard: python3/python absent, znc=$(which znc)"
cd "$HOME/workspace/tnn-rsi" || exit 1
echo "--- frozen-source copy + integrity (K-H2) ---"
for f in cc_base.zag un_patch.zag adapt_patch.zag revise_patch.zag ts_patch.zag; do
  cp "$SRC/$f" "$L/$f"
  a=$(sha256sum "$L/$f" | cut -d' ' -f1)
  b=$(sha256sum "$SRC/$f" | cut -d' ' -f1)
  if [ "$a" = "$b" ]; then echo "OK $f $a"; else echo "MISMATCH $f"; exit 1; fi
done
cat "$L/cc_base.zag" "$L/un_patch.zag" "$L/adapt_patch.zag" "$L/revise_patch.zag" "$L/ts_patch.zag" "$L/tt_patch.zag" "$L/tt_driver.zag" > "$L/tt_full.zag"
echo "--- kill-bar source checks ---"
echo "mode_bridge_handler_wholeword_occurrences=$(grep -ciw -e mode -e bridge -e handler "$L/tt_patch.zag" "$L/tt_driver.zag")"
echo "forbidden_slice_pattern=$(grep -c 'as \*i32' "$L/tt_patch.zag" "$L/tt_driver.zag")"
echo "--- compile ---"
znc "$L/tt_full.zag" -o "$L/tt_bin" > "$L/compile.txt" 2>&1
echo "compile exit=$?"
ls -la "$L/tt_bin"
echo "--- run 3x ---"
for r in 1 2 3; do
  "$L/tt_bin" > "$L/run$r.txt" 2>&1
  echo "run$r exit=$?"
done
sha256sum "$L/run1.txt" "$L/run2.txt" "$L/run3.txt" | tee "$L/sha256sums.txt"
cmp "$L/run1.txt" "$L/run2.txt" && cmp "$L/run2.txt" "$L/run3.txt" && echo "DETERMINISM-OK: 3/3 byte-identical"
echo "--- verdict lines ---"
grep -E "^(A|B|C|T)-.*=PASS|^(A|B|C|T)-.*=FAIL" "$L/run1.txt"
echo "--- K-H1 dash byte check (expect no output) ---"
grep -c $'\xe2\x80\x94' "$L/PREREG.md" "$L/REPORT.md" "$L/NAMECHECK.md" "$L/tt_patch.zag" "$L/tt_driver.zag" 2>/dev/null | grep -v ":0" || echo "no em dashes"
grep -c $'\xe2\x80\x93' "$L/PREREG.md" "$L/REPORT.md" "$L/NAMECHECK.md" "$L/tt_patch.zag" "$L/tt_driver.zag" 2>/dev/null | grep -v ":0" || echo "no en dashes"
echo "BUILD-DONE"
