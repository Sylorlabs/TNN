#!/usr/bin/env bash
# SM1 trial runner — compiles the self-observation-loop trial natively and
# verifies every CL_CHECK line has actual==expected. Usage: ./run_sm.sh [ZNC]
set -u
BASE="$(cd "$(dirname "$0")" && pwd)"
ZNC="${1:-${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}}"
BIN="$BASE/sm_trial_linux"
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
E="$BASE/EVIDENCE_$STAMP"
mkdir -p "$E"

# Program law: no RNG anywhere in the SYSTEM's decision paths.
# (strip // comments first so the check can't trip on documentation)
if sed 's|//.*||' "$BASE/sm_trial.zag" | grep -niE '\brng\b|\brand\b|srand|rand\(\)|random' >"$E/rng_grep.txt" 2>&1; then
  echo "RNG CHECK FAILED — matches in system code:"
  cat "$E/rng_grep.txt"
  exit 1
fi
echo "rng_check=clean (no RNG in system code)"

"$ZNC" "$BASE/sm_trial.zag" --no-zagd --no-analyze --no-foreground-cache -o "$BIN" \
  >"$E/compile.stdout" 2>"$E/compile.stderr"
ec=$?
echo "compile_exit=$ec"
if [ $ec -ne 0 ]; then echo "COMPILE FAILED"; tail -30 "$E/compile.stderr"; exit 1; fi

"$BIN" >"$E/run.stdout" 2>"$E/run.stderr"
ec=$?
echo "run_exit=$ec"
cat "$E/run.stdout"

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

# verify SM_STAT lines against prereg hand-computed expectations:
# A_phase1: attempts=10 refused=4 rate=400 fired=1 predicted=1
# B:        attempts=10 refused=1 rate=100 fired=0 predicted=-1
declare -A EXP_STAT=( ["A_phase1"]="10,4,400,1,1" ["B"]="10,1,100,0,-1" )
while IFS=, read -r tag name a r rt f p; do
  want="${EXP_STAT[$name]:-}"
  if [ -z "$want" ]; then echo "UNEXPECTED SM_STAT: $name"; bad=$((bad+1)); continue; fi
  if [ "$a,$r,$rt,$f,$p" != "$want" ]; then
    echo "SM_STAT MISMATCH: $name got=$a,$r,$rt,$f,$p want=$want"
    bad=$((bad+1))
  fi
done < <(grep '^SM_STAT,' "$E/run.stdout")
echo "stat_bad_included_above"

grep -E '^SM_FAILURES,' "$E/run.stdout" | tee "$E/summary.txt"
if [ "$bad" -ne 0 ] || [ "$ec" -ne 0 ]; then echo "TRIAL FAILED"; exit 1; fi
echo "TRIAL PASSED"
