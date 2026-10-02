#!/usr/bin/env bash
# RT-1 trial runner — RL-as-red-team harness trial (PREREG.md).
# Compiles natively, runs the binary twice (determinism: byte-identical
# stdout), and verifies every CL_CHECK line has actual==expected.
# Usage: ./run_red.sh [ZNC]
set -u
BASE="$(cd "$(dirname "$0")" && pwd)"
ZNC="${1:-${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}}"
BIN="$BASE/red_trial_linux"
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
E="$BASE/../evidence/EVIDENCE_RT1_$STAMP"
mkdir -p "$E"

# Static check: no RNG token anywhere in the trial's decision paths.
# Program law: zero RNG in anything the system decides. Fails closed.
if grep -nEi 'rng|rand\(|srand|random' "$BASE"/red_*.zag | grep -vE ':[0-9]+:[[:space:]]*//'; then
  echo "STATIC CHECK FAILED: RNG token in trial source"
  exit 1
fi
echo "static_no_rng=pass"
cp "$BASE"/red_*.zag "$E/"

"$ZNC" "$BASE/red_trial.zag" --no-zagd --no-analyze --no-foreground-cache -o "$BIN" \
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

bad=0; total=0
while IFS=, read -r tag name actual expected; do
  total=$((total+1))
  if [ "$actual" != "$expected" ]; then
    echo "MISMATCH: $name actual=$actual expected=$expected"
    bad=$((bad+1))
  fi
done < <(grep '^CL_CHECK,' "$E/run1.stdout")
# threshold checks: CL_CHECKGE requires actual>=min, CL_CHECKLE actual<=max
while IFS=, read -r tag name actual bound; do
  total=$((total+1))
  if [ "$actual" -lt "$bound" ]; then
    echo "MISMATCH(GE): $name actual=$actual min=$bound"
    bad=$((bad+1))
  fi
done < <(grep '^CL_CHECKGE,' "$E/run1.stdout")
while IFS=, read -r tag name actual bound; do
  total=$((total+1))
  if [ "$actual" -gt "$bound" ]; then
    echo "MISMATCH(LE): $name actual=$actual max=$bound"
    bad=$((bad+1))
  fi
done < <(grep '^CL_CHECKLE,' "$E/run1.stdout")
echo "checks_total=$total checks_bad=$bad"
grep -E '^RT_VERDICT,' "$E/run1.stdout" | tee "$E/summary.txt"
(cd "$E" && sha256sum run1.stdout run2.stdout red_*.zag > SHA256SUMS)
if [ "$bad" -ne 0 ] || [ "$ec1" -ne 0 ]; then echo "TRIAL FAILED"; exit 1; fi
echo "TRIAL PASSED"
