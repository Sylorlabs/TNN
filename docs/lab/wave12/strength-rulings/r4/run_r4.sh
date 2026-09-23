#!/bin/bash
# Ruling 4 runner: static checks -> compile -> positions a/b/c x2 runs.
# Every binary run must be byte-identical across the two runs (diffed).
set -u
R=~/workspace/tnn-lab/wave12/strength-rulings/r4
T=$R/trial
OUT=$R/evidence
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
mkdir -p "$OUT"
LOG="$OUT/runner.log"
: > "$LOG"
note(){ echo "$1" | tee -a "$LOG"; }
fail(){ note "RUNNER_FAIL,$1"; exit 1; }
pass=0; fail_n=0

note "== static checks =="
cd "$T" || exit 1
if grep -rniE 'rand\(|srand|getrandom|/dev/urandom|rdtsc' \
    strength_core.zag strength_checker.zag "$R/r4_overwrite.zag" >/dev/null 2>&1; then
  fail "RNG token found"
fi
for f in "$R/r4_overwrite.zag"; do
  if grep -q '^@import' "$f"; then :; else fail "$f import not bare"; fi
done
# strength-write sites: the four legal judgment paths + restore + kill-clear
# + overwrite's add path + the R4 position-(a) test hook st_overwrite_direct.
grep -n "st_write_strength(" strength_core.zag > /tmp/r4_sw_calls.txt
awk '
/^fn /{fn=$2; sub(/\(.*/,"",fn)}
/st_write_strength\(s,/{print fn}
' strength_core.zag | sort | uniq -c > /tmp/r4_sw_fns.txt
allowed="st_write_strength st_add_into_slot st_redeclare st_trainer_declare st_restore st_clear_strength st_add_core st_overwrite st_overwrite_direct"
ok=1
while read -r count fn; do
  case " $allowed " in
    *" $fn "*) ;;
    *) note "BAD strength-write caller: $fn"; ok=0;;
  esac
done < /tmp/r4_sw_fns.txt
if [ "$ok" = 1 ]; then note "PASS strength_write_sites"; pass=$((pass+1));
else fail "strength_write_sites"; fi
# the (a) hook must exist and be marked as test-only
grep -q "R4 POSITION (a) TEST HOOK" strength_core.zag || fail "hook marker missing"
note "STATIC_OK"; pass=$((pass+1))

note "== compile =="
"$ZNC" "$R/r4_overwrite.zag" --no-zagd --no-analyze --no-foreground-cache \
  -o "$R/r4_bin" || fail "compile"
note "COMPILE_OK"; pass=$((pass+1))

note "== positions a/b/c =="
for pos in a b c; do
  for run in 1 2; do
    "$R/r4_bin" "$pos" > "$OUT/pos_${pos}_r${run}.log" 2>&1
    ec=$?
    if [ $ec -ne 0 ]; then note "FAIL pos_${pos}_r${run} exit=$ec"; fail_n=$((fail_n+1)); fi
  done
  if cmp -s "$OUT/pos_${pos}_r1.log" "$OUT/pos_${pos}_r2.log"; then
    note "PASS pos_${pos}_deterministic"
  else note "FAIL pos_${pos}_deterministic"; fail_n=$((fail_n+1)); fi
  if ! grep -q "^R4_DONE$" "$OUT/pos_${pos}_r1.log"; then
    note "FAIL pos_${pos}_nodone"; fail_n=$((fail_n+1)); fi
done

note "== done =="
note "pass=$pass fail_n=$fail_n"
if [ "$fail_n" = 0 ]; then echo "R4_COMPLETE" > "$OUT/VERDICT.txt"; else echo "R4_FAILED" > "$OUT/VERDICT.txt"; fi
