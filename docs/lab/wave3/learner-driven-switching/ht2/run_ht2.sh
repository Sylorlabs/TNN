#!/usr/bin/env bash
# HT2 trial runner — compiles the educated-guess switching trial natively,
# enforces program-law static checks (no RNG / no clock in the learner's
# decision path; mechanism byte-identical to HT1's), runs the binary twice
# (determinism: byte-identical stdout), and verifies every CL_CHECK line.
# Usage: ./run_ht2.sh [ZNC]
set -u
BASE="$(cd "$(dirname "$0")" && pwd)"
ZNC="${1:-${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}}"
BIN="$BASE/ht2_trial_linux"
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
E="$BASE/EVIDENCE_$STAMP"
mkdir -p "$E"

# --- program-law static checks ---
# 1. No randomness source anywhere in the learner's decision path.
if grep -qiE 'rng|ht_next|srand|rand\(|random' "$BASE/ht2_learner.zag"; then
  echo "STATIC FAIL: randomness source in ht2_learner.zag"
  grep -qiE 'rng|ht_next|srand|rand\(|random' "$BASE/ht2_learner.zag" | head -5
  exit 1
fi
# 2. No time source in the learner's decision path (decisions are functions
#    of (hypothesis state, recorded evidence) only — never the clock).
if grep -qiE '\bepisode\b|\bclock\b|gettimeofday|time\(' "$BASE/ht2_learner.zag"; then
  echo "STATIC FAIL: time source in ht2_learner.zag"
  exit 1
fi
# 3. Mechanism fidelity: the switching mechanism is HT1's, byte-identical.
ORIG="$BASE/../../../wave2/posttable/ctx"
cmp -s "$BASE/ctx_core.zag" "$ORIG/ctx_core.zag" || { echo "FIDELITY FAIL: ctx_core.zag differs from HT1's"; exit 1; }
cmp -s "$BASE/toy_core.zag" "$ORIG/toy_core.zag" || { echo "FIDELITY FAIL: toy_core.zag differs from HT1's"; exit 1; }
diff -rq "$BASE/substrate" "$ORIG/substrate" >/dev/null || { echo "FIDELITY FAIL: substrate differs from HT1's"; exit 1; }
echo "static_checks=pass (learner has no RNG source, no clock source; mechanism byte-identical to HT1)"

# --- compile ---
"$ZNC" "$BASE/trial_ht2.zag" --no-zagd --no-analyze --no-foreground-cache -o "$BIN" \
  >"$E/compile.stdout" 2>"$E/compile.stderr"
ec=$?
echo "compile_exit=$ec"
if [ $ec -ne 0 ]; then echo "COMPILE FAILED"; tail -30 "$E/compile.stderr"; exit 1; fi

# --- run twice: the system is deterministic given the curriculum ---
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

# --- verify: every CL_CHECK line must have actual==expected ---
bad=0; total=0
while IFS=, read -r tag name actual expected; do
  total=$((total+1))
  if [ "$actual" != "$expected" ]; then
    echo "MISMATCH: $name actual=$actual expected=$expected"
    bad=$((bad+1))
  fi
done < <(grep '^CL_CHECK,' "$E/run1.stdout")
echo "checks_total=$total checks_bad=$bad"
grep -E '^HT2_FAILURES,' "$E/run1.stdout" | tee "$E/summary.txt"
(cd "$E" && sha256sum run1.stdout run2.stdout > SHA256SUMS)
if [ "$bad" -ne 0 ] || [ "$ec1" -ne 0 ]; then echo "TRIAL FAILED"; exit 1; fi
echo "TRIAL PASSED"
