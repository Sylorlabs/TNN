#!/usr/bin/env bash
# Trace-composition trial runner (Wave 3, slug: trace-composition).
# Compiles comp.zag, runs it, counts CL_CHECK lines, runs static
# program-law checks (no RNG/randomness/syscalls in system code), and
# verifies determinism by running the binary twice and diffing stdout.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
COMP="${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}"
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
E="$HERE/EVIDENCE_$STAMP"
BIN="$E/comp_trial"
mkdir -p "$E"
fail=0

"$COMP" "$HERE/comp.zag" \
  --no-zagd --no-analyze --no-foreground-cache -o "$BIN" \
  > "$E/compile.stdout" 2> "$E/compile.stderr"
if [[ ! -x "$BIN" ]]; then
  echo "COMPILE FAILED"; cat "$E/compile.stderr"; exit 1
fi

"$BIN" > "$E/run1.stdout" 2> "$E/run1.stderr"
ec1=$?
"$BIN" > "$E/run2.stdout" 2> "$E/run2.stderr"
ec2=$?
printf '%s %s' "$ec1" "$ec2" > "$E/run.exits"
if (( ec1 != 0 || ec2 != 0 )); then fail=$((fail+1)); echo "RUN EXIT NONZERO: $ec1 $ec2"; fi

total=$(grep -c '^CL_CHECK,' "$E/run1.stdout")
bad=$(awk -F, '/^CL_CHECK,/{if($3!=$4)print}' "$E/run1.stdout" | wc -l)
printf 'checks_total=%s\nchecks_failed=%s\n' "$total" "$bad" > "$E/summary.txt"
if (( bad != 0 )); then fail=$((fail+1)); fi
comp_line=$(grep '^COMP_FAILURES,' "$E/run1.stdout" | tail -1)
printf '%s\n' "$comp_line" >> "$E/summary.txt"

# Determinism: two runs of the binary must be byte-identical.
if cmp -s "$E/run1.stdout" "$E/run2.stdout"; then
  printf 'double_run_identical=true\n' >> "$E/summary.txt"
else
  printf 'double_run_identical=false\n' >> "$E/summary.txt"
  fail=$((fail+1))
fi

# Static program-law checks on the SYSTEM source (comp.zag only).
# Comments are stripped first so the check targets code, not prose.
# A2 — no RNG/randomness/time/raw-syscall anywhere in the system.
sed 's|//.*||' "$HERE/comp.zag" > "$E/comp.stripped.zag"
if grep -nEi '\brng\b|random|srand|rand\(|gettime|clock_gettime|_zag_raw_syscall' \
    "$E/comp.stripped.zag" > "$E/static.forbidden.txt"; then
  printf 'no_randomness=false\n' >> "$E/summary.txt"
  fail=$((fail+1))
else
  printf 'no_randomness=true\n' >> "$E/summary.txt"
fi
# No score tables / RL machinery in the design (banned mechanisms).
if grep -nEi 'score.?table|q_table|reward|policy_gradient' \
    "$HERE/comp.zag" > "$E/static.banned.txt"; then
  printf 'no_banned_mechanisms=false\n' >> "$E/summary.txt"
  fail=$((fail+1))
else
  printf 'no_banned_mechanisms=true\n' >> "$E/summary.txt"
fi

printf 'failures=%s\n' "$fail" > "$E/RECEIPT.txt"
printf 'platform=linux-x86_64\n' >> "$E/RECEIPT.txt"
printf 'prereg=%s/PREREG.md\n' "$HERE" >> "$E/RECEIPT.txt"
printf '%s\n' "$E"
cat "$E/summary.txt"
exit $(( fail != 0 ))
