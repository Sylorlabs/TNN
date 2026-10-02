#!/usr/bin/env bash
# TWT-1 trial runner — compiles the teaching-without-tables trial natively,
# runs the binary twice (determinism: byte-identical stdout), and verifies
# every CL_CHECK line has actual==expected. Usage: ./run_twt.sh [ZNC]
set -u
BASE="$(cd "$(dirname "$0")" && pwd)"
ZNC="${1:-${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}}"
BIN="$BASE/twt_trial_linux"
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
E="$BASE/EVIDENCE_$STAMP"
mkdir -p "$E"

"$ZNC" "$BASE/twt_trial.zag" --no-zagd --no-analyze --no-foreground-cache -o "$BIN" \
  >"$E/compile.stdout" 2>"$E/compile.stderr"
ec=$?
echo "compile_exit=$ec"
if [ $ec -ne 0 ]; then echo "COMPILE FAILED"; tail -30 "$E/compile.stderr"; exit 1; fi

"$BIN" >"$E/run1.stdout" 2>"$E/run1.stderr"
ec1=$?
"$BIN" >"$E/run2.stdout" 2>"$E/run2.stderr"
ec2=$?
echo "run1_exit=$ec1 run2_exit=$ec2"
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
grep -E '^TWT_FAILURES,' "$E/run1.stdout" | tee "$E/summary.txt"
(cd "$E" && sha256sum run1.stdout run2.stdout > SHA256SUMS)
if [ "$bad" -ne 0 ] || [ "$ec1" -ne 0 ]; then echo "TRIAL FAILED"; exit 1; fi
echo "TRIAL PASSED"
