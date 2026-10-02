#!/bin/sh
# cogop_invention build.sh
# Step 0: toolchain guard re-verification.
export PATH="$HOME/safebin"
echo "toolchain guard:"
which python3 python 2>/dev/null; echo "guard-check-done"
L="docs/lab/research-lead/overnight-20260928/cogop_invention"
cd "$HOME/workspace/tnn-rsi" || exit 1
echo "--- K-COGOP-2 source checks ---"
echo -n "isa op forms (expect 1 2 3 4 5 6): "
grep -o 'op==[0-9]' "$L/cogop.zag" | sort -u | tr '\n' ' '; echo ""
echo -n "mode/bridge/handler hits (expect 0): "
grep -ciE 'mode|bridge|handler' "$L/cogop.zag"
echo -n "as *i32 hits (expect 0): "
grep -c 'as \*i32' "$L/cogop.zag"
echo -n "_zag_print hits (expect 0): "
grep -c '_zag_print' "$L/cogop.zag"
echo -n "python hits (expect 0): "
grep -ci 'python' "$L/cogop.zag"
echo -n "world_ in learner section (expect 0): "
sed -n '1,/=== DRIVER ===/p' "$L/cogop.zag" | grep -c 'world_'
echo -n "as []f64 / as []i64 hits (expect 0): "
grep -cE 'as \[\](f64|i64)' "$L/cogop.zag"
echo "--- compile ---"
znc "$L/cogop.zag" -o "$L/cogop" || exit 1
echo "BUILD-PASS cogop"
echo "--- run 1 ---"
"$L/cogop" > "$L/run1.txt" || exit 1
echo "--- run 2 ---"
"$L/cogop" > "$L/run2.txt" || exit 1
echo "--- run 3 ---"
"$L/cogop" > "$L/run3.txt" || exit 1
echo "--- determinism ---"
sha256sum "$L/run1.txt" "$L/run2.txt" "$L/run3.txt"
cmp "$L/run1.txt" "$L/run2.txt" && cmp "$L/run2.txt" "$L/run3.txt" && echo "3/3 DETERMINISTIC byte-identical"
sha256sum "$L/cogop"
