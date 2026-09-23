#!/usr/bin/env bash
# White-box test suite runner (Agent D, wave 2).
# Compiles wb_whitebox_tests.zag, runs it, and runs the learner-core
# isolation static check. Everything executes on this machine.
set -u
R34V3="$(cd "$(dirname "$0")/../../toolchain/r34v3" && pwd)"
COMP="${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}"
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
E="$(cd "$(dirname "$0")" && pwd)/EVIDENCE_$STAMP"
BIN="$E/wb_tests"
mkdir -p "$E"
fail=0

"$COMP" "$R34V3/wb_whitebox_tests.zag" \
  --no-zagd --no-analyze --no-foreground-cache -o "$BIN" \
  > "$E/compile.stdout" 2> "$E/compile.stderr"
if [[ ! -x "$BIN" ]]; then
  echo "COMPILE FAILED"; cat "$E/compile.stderr"; exit 1
fi

"$BIN" > "$E/run.stdout" 2> "$E/run.stderr"
ec=$?
printf '%s' "$ec" > "$E/run.exit"
if (( ec != 0 )); then fail=$((fail+1)); fi

# Count checks: every CL_CHECK line must have actual == expected.
total=$(grep -c '^CL_CHECK,' "$E/run.stdout")
bad=$(awk -F, '/^CL_CHECK,/{if($3!=$4)print}' "$E/run.stdout" | wc -l)
printf 'checks_total=%s\nchecks_failed=%s\n' "$total" "$bad" > "$E/summary.txt"
if (( bad != 0 )); then fail=$((fail+1)); fi
wb_line=$(grep '^WB_FAILURES,' "$E/run.stdout" | tail -1)
printf '%s\n' "$wb_line" >> "$E/summary.txt"

# Learner-core isolation: static check, same rule as the R34 runner.
if grep -nE '@import\([^)]*(world\.zag|checkpoint\.zag)|\bcw_|CWOutcome' \
    "$R34V3/r34_learner_core.zag" > "$E/isolation.forbidden.txt"; then
  printf 'learner_core_isolation=false\n' >> "$E/summary.txt"
  fail=$((fail+1))
else
  printf 'learner_core_isolation=true\n' >> "$E/summary.txt"
fi

printf 'failures=%s\n' "$fail" > "$E/RECEIPT.txt"
printf 'platform=linux-x86_64\n' >> "$E/RECEIPT.txt"
printf '%s\n' "$E"
cat "$E/summary.txt"
exit $(( fail != 0 ))
