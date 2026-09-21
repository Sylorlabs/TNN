#!/bin/bash
# run_smoke.sh — M8 smoke gate for the R0 core.
# Builds r0_smoke once, runs 5 adversarial perturbation modes per leg (N=5),
# and requires byte-identical stdout within each leg. Any diff = FAIL.
set -u
CORE_DIR="$(cd "$(dirname "$0")" && pwd)"
ZNC="${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}"
BIN=/tmp/r0_smoke_m8
OUTD=/tmp/r0_m8_out
rm -rf "$OUTD"; mkdir -p "$OUTD"

echo "== build =="
"$ZNC" "$CORE_DIR/r0_smoke.zag" --no-zagd --no-analyze --no-foreground-cache -o "$BIN" || exit 1

fail=0
for leg in 0 1; do
  for p in 0 1 2 3 4; do
    "$BIN" "$leg" "$p" > "$OUTD/leg${leg}_p${p}.txt" 2>"$OUTD/leg${leg}_p${p}.err"
    ec=$?
    # normalize the perturb field before diffing (mode is the perturbation, not output)
    sed 's/,perturb=[0-9]/,perturb=N/' "$OUTD/leg${leg}_p${p}.txt" > "$OUTD/leg${leg}_p${p}.norm"
    if [ $ec -ne 0 ]; then echo "RUN FAIL leg=$leg perturb=$p exit=$ec"; fail=1; fi
    if [ -s "$OUTD/leg${leg}_p${p}.err" ]; then echo "STDERR leg=$leg perturb=$p:"; cat "$OUTD/leg${leg}_p${p}.err"; fail=1; fi
  done
  base="$OUTD/leg${leg}_p0.norm"
  for p in 1 2 3 4; do
    if ! diff -q "$base" "$OUTD/leg${leg}_p${p}.norm" >/dev/null; then
      echo "M8 DIFF FAIL leg=$leg perturb=$p vs perturb=0"
      diff "$base" "$OUTD/leg${leg}_p${p}.norm" | head -20
      fail=1
    fi
  done
  # repeat perturb=0 for run-to-run stability
  "$BIN" "$leg" 0 > "$OUTD/leg${leg}_p0b.txt"
  sed 's/,perturb=[0-9]/,perturb=N/' "$OUTD/leg${leg}_p0b.txt" > "$OUTD/leg${leg}_p0b.norm"
  if ! diff -q "$base" "$OUTD/leg${leg}_p0b.norm" >/dev/null; then
    echo "M8 RERUN DIFF FAIL leg=$leg"; fail=1
  fi
done

echo "== canonical output (leg 0, perturb 0) =="
cat "$OUTD/leg0_p0.txt"
echo "== canonical output (leg 1, perturb 0) =="
cat "$OUTD/leg1_p0.txt"

if [ $fail -eq 0 ]; then echo "M8_SMOKE_PASS"; else echo "M8_SMOKE_FAIL"; fi
exit $fail
