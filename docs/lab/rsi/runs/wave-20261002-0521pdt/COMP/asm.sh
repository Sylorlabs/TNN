#!/bin/sh
# asm.sh -- assemble, compile, and run the 5 COMP binaries (3x each).
# Pure Zag. Safebin PATH required.
export PATH="$HOME/safebin"
set -u
L=docs/lab/rsi/runs/wave-20261002-0521pdt/COMP
SRC=docs/lab/research-lead/overnight-20260928/composition_compare
if [ "$(which python3 2>/dev/null)" != "" ]; then
  echo "GUARD-FAIL: python3 resolves in PATH"; exit 1
fi
echo "guard: python3 absent, znc=$(which znc)"

# --- assemble ---
head -n 1860 "$SRC/cmp_full_a.zag" > "$L/full_a.zag"
cat "$L/shim_a.zag" "$L/driver.zag" >> "$L/full_a.zag"
head -n 1865 "$SRC/cmp_full_b.zag" > "$L/full_b.zag"
cat "$L/shim_b.zag" "$L/driver.zag" >> "$L/full_b.zag"
head -n 1985 "$SRC/cmp_full_c.zag" > "$L/full_c.zag"
cat "$L/shim_c.zag" "$L/driver.zag" >> "$L/full_c.zag"
# C0: one-line diff on the C mechanism (compose_on -> 0)
head -n 1985 "$SRC/cmp_full_c.zag" | sed 's/fn compose_on()i32 { return 1; }/fn compose_on()i32 { return 0; }/' > "$L/full_c0.zag"
cat "$L/shim_c.zag" "$L/driver_c0.zag" >> "$L/full_c0.zag"
grep -c 'fn compose_on()i32 { return 0; }' "$L/full_c0.zag"
# D: frozen substrate+rebind (lines 1-1677 of cmp_full_c) + patch_d
head -n 1677 "$SRC/cmp_full_c.zag" > "$L/full_d.zag"
cat "$L/patch_d.zag" "$L/shim_d.zag" "$L/driver.zag" >> "$L/full_d.zag"

# --- KB4a: D patch must contain zero code occurrences of "compose" ---
echo "--- KB4a grep (expect 0 code hits) ---"
grep -n "compose" "$L/patch_d.zag" | grep -v "^[0-9]*://" || echo "KB4a: no 'compose' outside comments (none found at all)"
grep -c "compose_try\|compose_on\|COMPOSE" "$L/patch_d.zag" || echo "KB4a: zero compose_try/compose_on/COMPOSE hits"

# --- compile ---
for m in a b c c0 d; do
  echo "--- compiling $m ---"
  znc "$L/full_$m.zag" -o "$L/bin_$m" > "$L/compile_$m.txt" 2>&1
  echo "compile_$m exit=$?"
  ls -la "$L/bin_$m"
done

# --- run 3x each, sha256 ---
for m in a b c c0 d; do
  for r in 1 2 3; do
    "$L/bin_$m" > "$L/run_${m}${r}.txt" 2>&1
    echo "run $m$r exit=$?"
  done
  sha256sum "$L/run_${m}1.txt" "$L/run_${m}2.txt" "$L/run_${m}3.txt"
done
echo "ASM-DONE"
