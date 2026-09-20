#!/usr/bin/env bash
# Deliberate-recall trial runner — compiles natively, runs twice
# (byte-identity = determinism), verifies every CL_CHECK actual==expected,
# and statically asserts no RNG in the system or harness.
# Usage: ./run_recall.sh [ZNC]
set -u
BASE="$(cd "$(dirname "$0")" && pwd)"
ZNC="${1:-${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}}"
BIN="$BASE/recall_trial_linux"
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
E="$BASE/EVIDENCE_$STAMP"
mkdir -p "$E"

echo "== static: no RNG / argv in trial sources (code lines only) =="
if grep -rniE 'rng|random|seed|_zag_arg' "$BASE"/*.zag | grep -vE ':[0-9]+:\s*//'; then
  echo "STATIC CHECK FAILED: randomness/argv token found in code"; exit 1
fi
echo "static_ok=1"
# record input hashes for the evidence bundle
sha256sum "$BASE/recall_trial.zag" "$BASE/recall_core.zag" > "$E/inputs.sha256"
sha256sum "$HOME/workspace/tnn-lab/wave2/memoryagency/trial/memory_core.zag" >> "$E/inputs.sha256"
cat "$E/inputs.sha256"

echo "== compile =="
"$ZNC" "$BASE/recall_trial.zag" --no-zagd --no-analyze --no-foreground-cache -o "$BIN" \
  >"$E/compile.stdout" 2>"$E/compile.stderr"
ec=$?
echo "compile_exit=$ec"
if [ $ec -ne 0 ]; then echo "COMPILE FAILED"; tail -30 "$E/compile.stderr"; exit 1; fi

echo "== run 1 =="
"$BIN" >"$E/run1.stdout" 2>"$E/run1.stderr"
ec1=$?
echo "== run 2 (determinism) =="
"$BIN" >"$E/run2.stdout" 2>"$E/run2.stderr"
ec2=$?
echo "run_exit_1=$ec1 run_exit_2=$ec2"
if [ $ec1 -ne 0 ] || [ $ec2 -ne 0 ]; then
  echo "RUN FAILED"; tail -20 "$E/run1.stderr"; tail -20 "$E/run2.stderr"; exit 1
fi
if ! cmp -s "$E/run1.stdout" "$E/run2.stdout"; then
  echo "DETERMINISM FAILED: run1 != run2"; diff "$E/run1.stdout" "$E/run2.stdout" | head; exit 1
fi
echo "determinism=byte_identical"
cp "$E/run1.stdout" "$E/run.stdout"

echo "== verify CL_CHECK =="
bad=0; total=0
while IFS=, read -r tag name actual expected; do
  total=$((total+1))
  if [ "$actual" != "$expected" ]; then
    echo "MISMATCH: $name actual=$actual expected=$expected"
    bad=$((bad+1))
  fi
done < <(grep '^CL_CHECK,' "$E/run.stdout")
echo "checks_total=$total checks_bad=$bad"
grep -E -e '^DR_EP,' -e '^DR_MEAN,' -e '^DR_TAUROW,' -e '^DR_TAU,' -e '^DR_FAILURES,' "$E/run.stdout" | tee "$E/summary.txt"
if [ "$bad" -ne 0 ]; then echo "TRIAL FAILED"; exit 1; fi
echo "TRIAL PASSED"
