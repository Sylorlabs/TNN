#!/usr/bin/env bash
# TC1 trial runner — compiles the trainer-console trial natively and
# verifies every CL_CHECK line has actual==expected, plus run-to-run
# byte-identical output (determinism check: no RNG anywhere in the system).
set -u
BASE="$(cd "$(dirname "$0")" && pwd)"
ZNC="${1:-${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}}"
BIN="$BASE/tc_trial_linux"
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
E="$BASE/EVIDENCE_$STAMP"
mkdir -p "$E"

# Program law: zero RNG in anything the system decides. Fail closed.
if grep -rniE '\brand|srand|random' "$BASE"/*.zag >/dev/null 2>&1; then
  echo "RNG TOKEN FOUND IN TRIAL SOURCES"; grep -rniE '\brand|srand|random' "$BASE"/*.zag; exit 1
fi
echo "no_rng=OK"

"$ZNC" "$BASE/tc_trial.zag" --no-zagd --no-analyze --no-foreground-cache -o "$BIN" \
  >"$E/compile.stdout" 2>"$E/compile.stderr"
ec=$?
echo "compile_exit=$ec"
if [ $ec -ne 0 ]; then echo "COMPILE FAILED"; tail -30 "$E/compile.stderr"; exit 1; fi

# Two runs: determinism requires byte-identical stdout.
"$BIN" >"$E/run1.stdout" 2>"$E/run1.stderr"; ec1=$?
"$BIN" >"$E/run2.stdout" 2>"$E/run2.stderr"; ec2=$?
echo "run1_exit=$ec1 run2_exit=$ec2"
if [ $ec1 -ne 0 ] || [ $ec2 -ne 0 ]; then echo "RUN FAILED"; exit 1; fi
if ! cmp -s "$E/run1.stdout" "$E/run2.stdout"; then
  echo "NONDETERMINISM: run1 != run2"; diff "$E/run1.stdout" "$E/run2.stdout" | head -20; exit 1
fi
echo "determinism=OK (run1 == run2 byte-identical)"

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
grep -E '^TC_FAILURES,' "$E/run1.stdout" | tee "$E/summary.txt"
grep -E '^TC_FINGERPRINT,' "$E/run1.stdout" | tee -a "$E/summary.txt"
if [ "$bad" -ne 0 ]; then echo "TRIAL FAILED"; exit 1; fi
echo "TRIAL PASSED"
