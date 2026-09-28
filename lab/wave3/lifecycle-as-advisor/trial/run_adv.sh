#!/usr/bin/env bash
# ADV trial runner — lifecycle estimator as advisor (PREREG.md).
# Static checks: advisor isolation (no imports, no store/op references),
# no RNG in the system sources. Then gate white-box test, then the trial.
set -u
BASE="$(cd "$(dirname "$0")" && pwd)"
ZNC="${1:-${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}}"
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
E="$BASE/EVIDENCE_ADV_$STAMP"
mkdir -p "$E"

echo "== static: advisor isolation =="
if grep -nE '@import|MaStore|ma_' "$BASE/adv_advisor.zag" >"$E/isolation.grep"; then
  echo "ISOLATION CHECK FAILED"; cat "$E/isolation.grep"; exit 1
fi
echo "advisor_isolation=pass"

echo "== static: no RNG in system sources =="
if grep -nE 'rng_next|_rand\(|random\(|srand\(' \
    "$BASE/adv_trial.zag" "$BASE/adv_advisor.zag" "$BASE/adv_gate_test.zag" >"$E/norng.grep"; then
  echo "NO-RNG CHECK FAILED"; cat "$E/norng.grep"; exit 1
fi
echo "no_rng_in_system=pass"

echo "== compile: gate test =="
"$ZNC" "$BASE/adv_gate_test.zag" --no-zagd --no-analyze --no-foreground-cache \
  -o "$BASE/adv_gate_test_linux" >"$E/gate.compile.stdout" 2>"$E/gate.compile.stderr"
ec=$?; echo "gate_compile_exit=$ec"
if [ $ec -ne 0 ]; then echo "GATE COMPILE FAILED"; tail -30 "$E/gate.compile.stderr"; exit 1; fi

echo "== run: gate test =="
"$BASE/adv_gate_test_linux" >"$E/gate.run.stdout" 2>"$E/gate.run.stderr"
ec=$?; echo "gate_run_exit=$ec"; cat "$E/gate.run.stdout"
if [ $ec -ne 0 ]; then echo "GATE TEST FAILED"; exit 1; fi

echo "== compile: trial =="
"$ZNC" "$BASE/adv_trial.zag" --no-zagd --no-analyze --no-foreground-cache \
  -o "$BASE/adv_trial_linux" >"$E/compile.stdout" 2>"$E/compile.stderr"
ec=$?; echo "compile_exit=$ec"
if [ $ec -ne 0 ]; then echo "COMPILE FAILED"; tail -30 "$E/compile.stderr"; exit 1; fi

echo "== run: trial =="
"$BASE/adv_trial_linux" >"$E/run.stdout" 2>"$E/run.stderr"
ec=$?; echo "run_exit=$ec"
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
grep -E '^ADV_VERDICT,' "$E/run.stdout" | tee "$E/summary.txt"
if [ "$bad" -ne 0 ] || [ "$ec" -ne 0 ]; then echo "TRIAL FAILED"; exit 1; fi
echo "TRIAL PASSED"
