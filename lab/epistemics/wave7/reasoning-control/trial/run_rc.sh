#!/usr/bin/env bash
# RC1 trial runner — native reasoning control.
# Compiles rc_trial.zag, runs twice (byte-identical required), verifies
# every CL_CHECK actual==expected, checks determinism + no-RNG.
set -u
BASE="$(cd "$(dirname "$0")" && pwd)"
ZNC="${1:-${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}}"
BIN="$BASE/rc_trial_linux"
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
E="$BASE/EVIDENCE_$STAMP"
mkdir -p "$E"

# Program law: no RNG anywhere in the SYSTEM's decision paths.
if sed 's|//.*||' "$BASE/rc_trial.zag" | grep -niE '\brng\b|\brand\b|srand|rand\(\)|random' >"$E/rng_grep.txt" 2>&1; then
  echo "RNG CHECK FAILED:"; cat "$E/rng_grep.txt"; exit 1
fi
echo "rng_check=clean"

"$ZNC" "$BASE/rc_trial.zag" --no-zagd --no-analyze --no-foreground-cache -o "$BIN" \
  >"$E/compile.stdout" 2>"$E/compile.stderr"
ec=$?; echo "compile_exit=$ec"
if [ $ec -ne 0 ]; then echo "COMPILE FAILED"; tail -40 "$E/compile.stderr"; exit 1; fi

"$BIN" >"$E/run1.stdout" 2>"$E/run1.stderr"; ec1=$?
"$BIN" >"$E/run2.stdout" 2>"$E/run2.stderr"; ec2=$?
echo "run_exit=$ec1,$ec2"
if [ $ec1 -ne 0 ] || [ $ec2 -ne 0 ]; then echo "RUN FAILED"; exit 1; fi

h1=$(sha256sum "$E/run1.stdout" | cut -d' ' -f1)
h2=$(sha256sum "$E/run2.stdout" | cut -d' ' -f1)
echo "sha1=$h1"; echo "sha2=$h2"
if [ "$h1" != "$h2" ]; then echo "NONDETERMINISM"; exit 1; fi
echo "determinism=byte-identical"

cat "$E/run1.stdout"

bad=0; total=0
while IFS=, read -r tag name actual expected; do
  total=$((total+1))
  if [ "$actual" != "$expected" ]; then
    echo "MISMATCH: $name actual=$actual expected=$expected"; bad=$((bad+1))
  fi
done < <(grep '^CL_CHECK,' "$E/run1.stdout")
echo "checks_total=$total checks_bad=$bad"
grep -E '^RC_FAILURES,' "$E/run1.stdout" | tee "$E/summary.txt"
if [ "$bad" -ne 0 ]; then echo "TRIAL FAILED"; exit 1; fi
echo "TRIAL PASSED"
