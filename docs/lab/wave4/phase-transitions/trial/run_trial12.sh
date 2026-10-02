#!/usr/bin/env bash
# PT-12 trial runner — compiles the 1->2 transition trial natively and
# verifies every CL_CHECK line has actual==expected.
# Usage: ./run_trial12.sh [ZNC]
set -u
BASE="$(cd "$(dirname "$0")" && pwd)"
ZNC="${1:-${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}}"
BIN="$BASE/trial12_linux"
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
E="$BASE/EVIDENCE_$STAMP"
mkdir -p "$E"

# Program law: no RNG anywhere in the SYSTEM's decision paths.
if sed 's|//.*||' "$BASE/trial12.zag" | grep -niE '\brng\b|\brand\b|srand|rand\(\)|random' >"$E/rng_grep.txt" 2>&1; then
  echo "RNG CHECK FAILED — matches in system code:"
  cat "$E/rng_grep.txt"
  exit 1
fi
echo "rng_check=clean (no RNG in system code)"

"$ZNC" "$BASE/trial12.zag" --no-zagd --no-analyze --no-foreground-cache -o "$BIN" \
  >"$E/compile.stdout" 2>"$E/compile.stderr"
ec=$?
echo "compile_exit=$ec"
if [ $ec -ne 0 ]; then echo "COMPILE FAILED"; tail -30 "$E/compile.stderr"; exit 1; fi

"$BIN" >"$E/run1.stdout" 2>"$E/run1.stderr"
ec=$?
echo "run1_exit=$ec"
"$BIN" >"$E/run2.stdout" 2>"$E/run2.stderr"
echo "run2_exit=$?"
cat "$E/run1.stdout"

# determinism: byte-identical reruns
if ! cmp -s "$E/run1.stdout" "$E/run2.stdout"; then
  echo "DETERMINISM FAILED — run1 and run2 differ"
  exit 1
fi
echo "determinism=byte-identical (2 runs)"

# verify: every CL_CHECK line must have actual==expected
bad=0; total=0
while IFS=, read -r tag name actual expected; do
  total=$((total+1))
  if [ "$actual" != "$expected" ]; then
    echo "MISMATCH: $name actual=$actual expected=$expected"
    bad=$((bad+1))
  fi
done < <(grep '^CL_CHECK,' "$E/run1.stdout")
echo "checks_total=$total checks_bad=$bad"

# verify PT_STAT lines against prereg hand-computed expectations:
# name: phase,grant_rc,attempts,refused,destruction,lessons,petitions
declare -A EXP_STAT=(
  ["A"]="2,0,3,3,0,4,1"
  ["B"]="1,203,3,1,2,4,1"
  ["C"]="1,202,3,3,0,2,1"
  ["D"]="1,204,3,3,0,4,1"
  ["E"]="1,201,3,3,0,4,0"
)
while IFS=, read -r tag name phase rc a r d l p; do
  want="${EXP_STAT[$name]:-}"
  if [ -z "$want" ]; then echo "UNEXPECTED PT_STAT: $name"; bad=$((bad+1)); continue; fi
  if [ "$phase,$rc,$a,$r,$d,$l,$p" != "$want" ]; then
    echo "PT_STAT MISMATCH: $name got=$phase,$rc,$a,$r,$d,$l,$p want=$want"
    bad=$((bad+1))
  fi
done < <(grep '^PT_STAT,' "$E/run1.stdout")
echo "stat_check_done"

grep -E '^PT_FAILURES,' "$E/run1.stdout" | tee "$E/summary.txt"
if [ "$bad" -ne 0 ] || [ "$ec" -ne 0 ]; then echo "TRIAL FAILED"; exit 1; fi
echo "TRIAL PASSED"
