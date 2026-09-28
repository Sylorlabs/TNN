#!/usr/bin/env bash
# MA4 trial runner — signed-value agency vs MA3 agency baseline (PREREG_MA4).
# Includes the program-law static check: no RNG in the trial's decision paths.
set -u
BASE="$(cd "$(dirname "$0")" && pwd)"
ZNC="${1:-${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}}"
BIN="$BASE/ma4_trial_linux"
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
E="$BASE/EVIDENCE_MA4_$STAMP"
mkdir -p "$E"

# Static check 1: no RNG token anywhere in the trial source's decision paths.
# (ma_common.zag ships an unused LCG helper; the trial must not reference it.)
if grep -nEi 'rng|rand\(|srand|random' "$BASE/ma4_trial.zag" | grep -vE '^[0-9]+:[[:space:]]*//'; then
  echo "STATIC CHECK FAILED: RNG token in ma4_trial.zag"
  exit 1
fi
echo "static_no_rng=pass"

"$ZNC" "$BASE/ma4_trial.zag" --no-zagd --no-analyze --no-foreground-cache -o "$BIN" \
  >"$E/compile.stdout" 2>"$E/compile.stderr"
ec=$?
echo "compile_exit=$ec"
if [ $ec -ne 0 ]; then echo "COMPILE FAILED"; tail -30 "$E/compile.stderr"; exit 1; fi

"$BIN" >"$E/run.stdout" 2>"$E/run.stderr"
ec=$?
echo "run_exit=$ec"
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
grep -E '^MA4_VERDICT,' "$E/run.stdout" | tee "$E/summary.txt"
if [ "$bad" -ne 0 ] || [ "$ec" -ne 0 ]; then echo "TRIAL FAILED"; exit 1; fi
echo "TRIAL PASSED"
