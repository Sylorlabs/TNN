#!/bin/sh
# asm_adv.sh -- assemble, compile (3x byte-identical), and run (3x
# byte-identical) the ADV-A adversarial battery for the frozen satisfy
# operation. Pure Zag. Safebin PATH required.
export PATH="$HOME/safebin"
set -u
L=docs/lab/rsi/runs/wave-20261002-1121pdt/comp
SRC52=docs/lab/rsi/runs/wave-20261002-0521pdt/COMP
if [ "$(which python3 2>/dev/null)" != "" ]; then
  echo "GUARD-FAIL: python3 resolves in PATH"; exit 1
fi
echo "guard: python3 absent, znc=$(which znc)"

# --- assemble: frozen mechanism region (0521 full_d.zag lines 1..2027)
# --- + new shim + new driver. No mechanism edits.
head -n 2027 "$SRC52/full_d.zag" > "$L/full_adv.zag"
cat "$L/shim_adv.zag" "$L/driver_adv.zag" >> "$L/full_adv.zag"
echo "--- KB2 region check ---"
head -n 2027 "$L/full_adv.zag" | sha256sum
echo "expect 627ff98a691b0bd02e26d16b99d4b61fc064750eead9b3e6c1f45f7ca873ba81"
echo "--- KB2/KB5a grep: zero 'compose' code occurrences in mechanism region ---"
head -n 2027 "$L/full_adv.zag" | grep -n "compose" | grep -v "^[0-9]*://" || echo "OK: no 'compose' outside comments in mechanism region"
head -n 2027 "$L/full_adv.zag" | grep -c "compose_try\|compose_on" || echo "OK: zero compose_try/compose_on hits"

# --- timed binary: same mechanism, driver main runs only B1,B2,B7 ---
sed '/^fn main()i32 {$/,/^}$/d' "$L/driver_adv.zag" > "$L/driver_timed.zag"
cat >> "$L/driver_timed.zag" <<'ZEOF'
fn main()i32 {
  emit("TIMED-START\n");
  let W:[]u8=z_alloc(110656); tnn2_init(W); t_b1(W);
  W=z_alloc(110656); tnn2_init(W); t_b2(W);
  W=z_alloc(110656); tnn2_init(W); t_b7(W);
  emit("TIMED-END\n");
  return 0;
}
ZEOF
head -n 2027 "$SRC52/full_d.zag" > "$L/full_timed.zag"
cat "$L/shim_adv.zag" "$L/driver_timed.zag" >> "$L/full_timed.zag"

# --- compile 3x each, require byte-identical builds ---
for m in adv timed; do
  for b in 1 2 3; do
    znc "$L/full_$m.zag" -o "$L/bin_${m}_$b" > "$L/compile_${m}_$b.txt" 2>&1
    echo "compile $m build$b exit=$?"
  done
  sha256sum "$L/bin_${m}_1" "$L/bin_${m}_2" "$L/bin_${m}_3"
done
cp "$L/bin_adv_1" "$L/bin_adv"
cp "$L/bin_timed_1" "$L/bin_timed"

# --- run 3x each, sha256 ---
for m in adv timed; do
  for r in 1 2 3; do
    "$L/bin_$m" > "$L/run_${m}${r}.txt" 2>&1
    echo "run $m$r exit=$?"
  done
  sha256sum "$L/run_${m}1.txt" "$L/run_${m}2.txt" "$L/run_${m}3.txt"
done
echo "ASM-ADV-DONE"
