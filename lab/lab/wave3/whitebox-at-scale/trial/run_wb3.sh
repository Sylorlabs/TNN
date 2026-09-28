#!/usr/bin/env bash
# WB3 trial runner — compiles the selective-audit trial natively and verifies
# every CL_CHECK line has actual==expected. Usage: ./run_wb3.sh [ZNC]
set -u
BASE="$(cd "$(dirname "$0")" && pwd)"
ZNC="${1:-${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}}"
BIN="$BASE/wb3_trial_linux"
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
E="$BASE/EVIDENCE_$STAMP"
mkdir -p "$E"

"$ZNC" "$BASE/trial_wb3.zag" --no-zagd --no-analyze --no-foreground-cache -o "$BIN" \
  >"$E/compile.stdout" 2>"$E/compile.stderr"
ec=$?
echo "compile_exit=$ec"
if [ $ec -ne 0 ]; then echo "COMPILE FAILED"; tail -30 "$E/compile.stderr"; exit 1; fi

"$BIN" >"$E/run.stdout" 2>"$E/run.stderr"
ec=$?
echo "run_exit=$ec"
grep -E '^(WB_PHASE|WB_STATS|WB_MANIFEST|WB_COVERAGE|WB_REPLAY|WB_FAILURES),' "$E/run.stdout"

# verify: every CL_CHECK line must have actual==expected
bad=0; total=0
while IFS=, read -r tag name actual expected; do
  total=$((total+1))
  if [ "$actual" != "$expected" ]; then
    echo "MISMATCH: $name actual=$actual expected=$expected"
    bad=$((bad+1))
  fi
done < <(grep '^CL_CHECK,' "$E/run.stdout")
echo "checks_total=$total checks_bad=$bad"
grep -E '^WB_FAILURES,' "$E/run.stdout" | tee "$E/summary.txt"
if [ "$bad" -ne 0 ] || [ "$ec" -ne 0 ]; then echo "TRIAL FAILED"; exit 1; fi
echo "TRIAL PASSED"
