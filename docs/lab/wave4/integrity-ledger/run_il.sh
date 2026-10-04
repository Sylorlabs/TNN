#!/usr/bin/env bash
# integrity-ledger trial runner — compiles natively, runs the binary twice
# (determinism: byte-identical stdout), verifies every CL_CHECK line.
set -u
BASE="$(cd "$(dirname "$0")" && pwd)"
ZNC="${1:-${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}}"
BIN="$BASE/il_trial_linux"
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
E="$BASE/EVIDENCE_$STAMP"
mkdir -p "$E"

"$ZNC" "$BASE/il_trial.zag" --no-zagd --no-analyze --no-foreground-cache -o "$BIN" \
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
sha256sum "$E/run1.stdout" | tee "$E/sha256.txt"
cat "$E/run1.stdout"

bad=0; total=0
while IFS=, read -r tag name actual expected; do
  total=$((total+1))
  if [ "$actual" != "$expected" ]; then
    echo "MISMATCH: $name actual=$actual expected=$expected"
    bad=$((bad+1))
  fi
done < <(grep '^CL_CHECK,' "$E/run1.stdout")
echo "checks=$total mismatches=$bad"
fails=$(grep -o 'IL_FAILURES,[0-9]*' "$E/run1.stdout" | cut -d, -f2)
echo "IL_FAILURES=$fails"
{
  echo "stamp=$STAMP"
  echo "compile_exit=$ec run1_exit=$ec1 run2_exit=$ec2"
  echo "determinism=byte-identical"
  echo "checks=$total mismatches=$bad IL_FAILURES=$fails"
} > "$E/summary.txt"
[ "$bad" -eq 0 ] && [ "$fails" = "0" ] && echo "TRIAL PASS" || { echo "TRIAL FAIL"; exit 1; }
