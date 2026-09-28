#!/usr/bin/env bash
# cheat-traps validation runner (PREREG_TRAPS.md).
# Static no-RNG check -> compile -> two runs -> byte-identical determinism
# check -> CL_CHECK verification -> replay check.
set -u
BASE="$(cd "$(dirname "$0")" && pwd)"
ZNC="${1:-${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}}"
BIN="$BASE/traps_trial_linux"
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
E="$BASE/EVIDENCE_$STAMP"
mkdir -p "$E"

# Static check: no RNG token in the trial source's decision paths.
if grep -nEi 'rng|rand\(|srand|random' "$BASE/traps_trial.zag" | grep -vE '^[0-9]+:[[:space:]]*//'; then
  echo "STATIC CHECK FAILED: RNG token in traps_trial.zag"
  exit 1
fi
echo "static_no_rng=pass"

"$ZNC" "$BASE/traps_trial.zag" --no-zagd --no-analyze --no-foreground-cache -o "$BIN" \
  >"$E/compile.stdout" 2>"$E/compile.stderr"
ec=$?
echo "compile_exit=$ec"
if [ $ec -ne 0 ]; then echo "COMPILE FAILED"; tail -30 "$E/compile.stderr"; exit 1; fi

"$BIN" >"$E/run1.stdout" 2>"$E/run1.stderr"
ec1=$?
"$BIN" >"$E/run2.stdout" 2>"$E/run2.stderr"
ec2=$?
echo "run1_exit=$ec1 run2_exit=$ec2"
if [ $ec1 -ne 0 ] || [ $ec2 -ne 0 ]; then echo "RUN FAILED"; exit 1; fi

# Determinism: byte-identical reruns (system determinism, reported separately
# from test adversity per program law).
if cmp -s "$E/run1.stdout" "$E/run2.stdout"; then
  echo "determinism=pass (byte-identical)"
else
  echo "determinism=FAIL"; diff "$E/run1.stdout" "$E/run2.stdout" | head; exit 1
fi
cp "$E/run1.stdout" "$E/run.stdout"
cat "$E/run.stdout"

bad=0; total=0
while IFS=, read -r tag name actual expected; do
  total=$((total+1))
  if [ "$actual" != "$expected" ]; then
    echo "MISMATCH: $name actual=$actual expected=$expected"
    bad=$((bad+1))
  fi
done < <(grep '^CL_CHECK,' "$E/run.stdout")
echo "checks_total=$total checks_bad=$bad"

replay=$(grep '^TRAP_REPLAY_OK,' "$E/run.stdout" | cut -d, -f2)
echo "replay_ok=$replay"
verdict=$(grep '^TRAP_VERDICT,' "$E/run.stdout" | cut -d, -f2)
echo "verdict=$verdict"

{
  echo "stamp=$STAMP"
  echo "static_no_rng=pass"
  echo "compile_exit=$ec"
  echo "determinism=pass"
  echo "checks_total=$total checks_bad=$bad"
  echo "replay_ok=$replay"
  echo "verdict=$verdict"
} > "$E/summary.txt"

if [ "$bad" -ne 0 ] || [ "$replay" != "1" ] || [ "$verdict" != "CONFIRM_SUITE_CONSISTENT" ]; then
  echo "TRIAL FAILED"; exit 1
fi
echo "TRIAL PASSED"
