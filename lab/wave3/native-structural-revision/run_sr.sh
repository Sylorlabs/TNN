#!/usr/bin/env bash
# NSR trial runner — compiles the native structural-revision trial, runs the
# binary twice (determinism: byte-identical stdout), verifies every CL_CHECK
# line has actual==expected, and enforces the program-law static proofs:
#   (a) sr_core.zag contains no RNG symbols (no RNG in the system);
#   (b) sr_core.zag imports no world/checkpoint substrate (isolation).
# Usage: ./run_sr.sh [ZNC]
set -u
BASE="$(cd "$(dirname "$0")" && pwd)"
ZNC="${1:-${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}}"
BIN="$BASE/sr_trial_linux"
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
E="$BASE/EVIDENCE_$STAMP"
mkdir -p "$E"

echo "== static: no RNG in the system =="
if grep -nE "1103515245|1000003|\* *997 *\+ *7919|sr_lcg_next|ht_next" "$BASE/sr_core.zag"; then
  echo "STATIC FAILED: RNG symbols in sr_core.zag"; exit 1
fi
echo "system_rng_symbols=none"
echo "== static: core isolation =="
if grep -nE "@import\([^)]*(world\.zag|checkpoint\.zag)" "$BASE/sr_core.zag"; then
  echo "STATIC FAILED: world/checkpoint import in sr_core.zag"; exit 1
fi
echo "core_isolation=ok"
cp "$BASE/sr_core.zag" "$BASE/trial_sr.zag" "$E/"

T0=$(date +%s%N)
"$ZNC" "$BASE/trial_sr.zag" --no-zagd --no-analyze --no-foreground-cache -o "$BIN" \
  >"$E/compile.stdout" 2>"$E/compile.stderr"
ec=$?
T1=$(date +%s%N)
echo "compile_exit=$ec compile_wall_ms=$(( (T1-T0)/1000000 ))"
if [ $ec -ne 0 ]; then echo "COMPILE FAILED"; tail -30 "$E/compile.stderr"; exit 1; fi

T2=$(date +%s%N)
"$BIN" >"$E/run1.stdout" 2>"$E/run1.stderr"
ec1=$?
T3=$(date +%s%N)
"$BIN" >"$E/run2.stdout" 2>"$E/run2.stderr"
ec2=$?
T4=$(date +%s%N)
echo "run1_exit=$ec1 run2_exit=$ec2 run_wall_ms=$(( (T3-T2)/1000000 ))"
if ! cmp -s "$E/run1.stdout" "$E/run2.stdout"; then
  echo "DETERMINISM FAILED: run outputs differ"; exit 1
fi
echo "determinism=byte-identical"
cat "$E/run1.stdout"

# verify: every CL_CHECK line must have actual==expected
bad=0; total=0
while IFS=, read -r tag name actual expected; do
  total=$((total+1))
  if [ "$actual" != "$expected" ]; then
    echo "MISMATCH: $name actual=$actual expected=$expected"
    bad=$((bad+1))
  fi
done < <(grep '^CL_CHECK,' "$E/run1.stdout")
echo "checks_total=$total checks_bad=$bad"
grep -E '^SR_FAILURES,' "$E/run1.stdout" | tee "$E/summary.txt"
{
  echo "stamp=$STAMP"
  echo "compile_wall_ms=$(( (T1-T0)/1000000 ))"
  echo "run_wall_ms=$(( (T3-T2)/1000000 ))"
  echo "determinism=byte-identical"
  echo "system_rng_symbols=none"
  echo "core_isolation=ok"
  echo "checks_total=$total checks_bad=$bad run1_exit=$ec1 run2_exit=$ec2"
} > "$E/RECEIPT.txt"
(cd "$E" && sha256sum run1.stdout run2.stdout sr_core.zag trial_sr.zag > SHA256SUMS)
if [ "$bad" -ne 0 ] || [ "$ec1" -ne 0 ]; then echo "TRIAL FAILED"; exit 1; fi
echo "TRIAL PASSED"
