#!/usr/bin/env bash
# RT-2 trial runner — sensor-spoofing red-team vs the REAL deliberate learner.
# Compiles natively, runs the binary twice (determinism: byte-identical
# stdout), and verifies every RT2_CHECK line has actual==expected.
# Usage: ./run_rt2.sh [ZNC]
set -u
BASE="$(cd "$(dirname "$0")" && pwd)"
ZNC="${1:-${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}}"
BIN="$BASE/rt2_trial_linux"
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
E="$BASE/../evidence/EVIDENCE_RT2_$STAMP"
mkdir -p "$E"

# Static check 1: no RNG token anywhere in the trial's decision paths.
# Program law: zero RNG in anything the system decides. Fails closed.
if grep -nEi 'rng|rand\(|srand|random' "$BASE"/*.zag | grep -vE ':[0-9]+:[[:space:]]*//'; then
  echo "STATIC CHECK FAILED: RNG token in trial source"
  exit 1
fi
echo "static_no_rng=pass"

# Static check 2: the SUT is the REAL learner, unmodified.
# trial/sr.zag must be byte-identical to wave4/scaffold-release/sr.zag.
if ! cmp -s "$BASE/sr.zag" "$HOME/workspace/tnn-lab/wave4/scaffold-release/sr.zag"; then
  echo "STATIC CHECK FAILED: trial/sr.zag differs from wave4/scaffold-release/sr.zag"
  echo "the SUT must be the real learner, unmodified"
  exit 1
fi
echo "static_real_learner=pass (sr.zag byte-identical to wave4)"

cp "$BASE"/*.zag "$E/"

"$ZNC" "$BASE/rt2_trial.zag" --no-zagd --no-analyze --no-foreground-cache -o "$BIN" \
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
done < <(grep '^RT2_CHECK,' "$E/run1.stdout")
echo "checks_total=$total checks_bad=$bad"
grep -E '^RT2_VERDICT,' "$E/run1.stdout" | tee "$E/summary.txt"
(cd "$E" && sha256sum run1.stdout run2.stdout *.zag > SHA256SUMS)
if [ "$bad" -ne 0 ] || [ "$ec1" -ne 0 ]; then echo "TRIAL FAILED"; exit 1; fi
echo "TRIAL PASSED"
