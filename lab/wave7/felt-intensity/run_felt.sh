#!/bin/bash
# Felt-intensity trial runner: static checks -> compile -> run 2x per cell ->
# determinism check -> preregistered-bar validation.
# Any FAIL aborts. No RNG anywhere; outputs must be byte-identical.
set -u
D=~/workspace/tnn-lab/wave7/felt-intensity
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
W5=~/workspace/tnn-lab/wave5/strength-trial-run/trial
W5SUB=~/workspace/tnn-lab/wave5/strength-trial-run/trial
cd "$D" || exit 1

fail(){ echo "RUNNER_FAIL,$1"; exit 1; }

echo "== static checks =="
# 1. no direct st_str writes outside st_memory_core (no st_str[ assignments in felt code/driver)
for f in felt.zag felt_trial.zag smoke.zag; do
  grep -n 'st_str\[' "$f" | grep -v 'as i32' | grep -v '\.st_str\[' >/dev/null 2>&1 && fail "direct st_str write in $f"
  grep -n '\.st_str\[.*\]\s*=' "$f" | grep -v 'as i32' >/dev/null 2>&1 && fail "direct st_str assign in $f"
done
# simpler: any occurrence of 'st_str[' followed by ']' then '=' on same line, excluding reads
grep -nE 'st_str\[[^]]*\]\s*=' felt.zag felt_trial.zag | grep -v 'st\.st_str\[s\] as i32' | grep -v 'st_i32' >/dev/null 2>&1 && fail "strength write outside substrate API"
# 2. no RNG tokens
grep -rniE 'rand|srand|random|getrandom|/dev/urandom|rdtsc' felt.zag felt_trial.zag smoke.zag >/dev/null 2>&1 && fail "RNG token found"
# 3. copied substrate byte-identical to Wave-5 originals
for f in st_memory_core.zag; do
  cmp -s "$D/$f" "$W5/$f" || fail "hash mismatch: $f"
done
cmp -s "$D/substrate/cl/common.zag" "$W5SUB/substrate/cl/common.zag" || fail "hash mismatch: common.zag"
cmp -s "$D/substrate/R33_NATIVE_SHA256_V2.zag" "$W5SUB/substrate/R33_NATIVE_SHA256_V2.zag" || fail "hash mismatch: sha256"
cmp -s "$D/substrate/R33_NATIVE_IO_V1.zag" "$W5SUB/substrate/R33_NATIVE_IO_V1.zag" || fail "hash mismatch: nativeio"
# 4. bare @import (not commented)
grep -q '^@import' felt.zag || fail "felt.zag import not bare"
grep -q '^@import' felt_trial.zag || fail "felt_trial.zag import not bare"
# 5. frozen curriculum formulas present verbatim
grep -q '(7\*m+13\*v+3)%10)<3' felt_trial.zag || fail "imp formula changed"
grep -q '(3\*m+7\*v+9)%10)<2' felt_trial.zag || fail "wrong formula changed"
grep -q 'm==0' felt_trial.zag || fail "implant schedule changed"
grep -q 'm==83' felt_trial.zag || fail "implant schedule changed"
grep -q 'm==166' felt_trial.zag || fail "implant schedule changed"
grep -q 'm==250' felt_trial.zag || fail "implant schedule changed"
grep -q 'm==333' felt_trial.zag || fail "implant schedule changed"
grep -q 'm==416' felt_trial.zag || fail "implant schedule changed"
echo "STATIC_OK"

echo "== compile =="
"$ZNC" felt_trial.zag --no-zagd --no-analyze --no-foreground-cache -o felt_bin || fail "compile"
echo "COMPILE_OK"

echo "== run cells (2x each) =="
for cell in F0 F1 F2 N0 N1 N2; do
  arm=${cell:0:1}; var=${cell:1:1}
  ./felt_bin "$arm" "$var" > "out_${cell}_a.txt" || fail "run ${cell} a"
  ./felt_bin "$arm" "$var" > "out_${cell}_b.txt" || fail "run ${cell} b"
  cmp -s "out_${cell}_a.txt" "out_${cell}_b.txt" || fail "nondeterministic ${cell}"
  grep -q '^FELT_DONE$' "out_${cell}_a.txt" || fail "incomplete ${cell}"
  echo "CELL_OK,${cell}"
done
echo "DETERMINISM_OK"

echo "== bar validation =="
check(){ # file metric expected_min expected_max
  local v; v=$(grep -E "^FELT_METRIC,${2}," "$1" | head -1 | awk -F, '{print $3}')
  [ -n "$v" ] || fail "metric $2 missing in $1"
  if [ "$v" -lt "$3" ] || [ "$v" -gt "$4" ]; then fail "bar $2=$v not in [$3,$4] ($1)"; fi
  echo "BAR_OK,$1,$2,$v"
}
for cell in F0 F1 F2 N0 N1 N2; do
  f="out_${cell}_a.txt"; arm=${cell:0:1}
  # offered counts (frozen curriculum: 50 right-important, 100 wrong nested inside imp)
  check "$f" offered_right_imp 50 50
  check "$f" offered_wrong 100 100
  r=$(grep -E '^FELT_CHECK,replay,' "$f" | awk -F, '{print $3}')
  [ "$r" = "0" ] || fail "replay rc=$r ($cell)"
  b=$(grep -E '^FELT_CHECK,recompute_bad,' "$f" | awk -F, '{print $3}')
  [ "$b" = "0" ] || fail "recompute_bad=$b ($cell)"
  d=$(grep -E '^FELT_METRIC,n_drops,' "$f" | awk -F, '{print $3}')
  [ "$d" = "0" ] || fail "n_drops=$d ($cell)"
  echo "BAR_OK,$cell,replay+recompute+drops"
  if [ "$arm" = "F" ]; then
    j=$(grep -E '^FELT_METRIC,junk_max,' "$f" | awk -F, '{print $3}')
    [ "$j" -le 50 ] || fail "junk_max=$j ($cell)"
    i=$(grep -E '^FELT_METRIC,impl_bad,' "$f" | awk -F, '{print $3}')
    [ "$i" = "0" ] || fail "impl_bad=$i ($cell)"
    n=$(grep -E '^FELT_METRIC,noev_bad,' "$f" | awk -F, '{print $3}')
    [ "$n" = "0" ] || fail "noev_bad=$n ($cell)"
    echo "BAR_OK,$cell,anti_inflation"
    # valuable retention >= 90% of admitted
    a=$(grep -E '^FELT_METRIC,admitted_right_imp,' "$f" | awk -F, '{print $3}')
    h=$(grep -E '^FELT_METRIC,held_right_imp,' "$f" | awk -F, '{print $3}')
    [ $(( h * 100 )) -ge $(( a * 90 )) ] || fail "retention $h/$a <90% ($cell)"
    echo "BAR_OK,$cell,retention,$h/$a"
    # wrong revision 100% (censored)
    aw=$(grep -E '^FELT_METRIC,admitted_wrong_cens,' "$f" | awk -F, '{print $3}')
    rw=$(grep -E '^FELT_METRIC,revised_wrong_cens,' "$f" | awk -F, '{print $3}')
    [ "$rw" = "$aw" ] || fail "wrong revision $rw/$aw ($cell)"
    echo "BAR_OK,$cell,wrong_revision,$rw/$aw"
    # trainer-designated wrong revised 100% (censored)
    at=$(grep -E '^FELT_METRIC,admitted_trainerwrong_cens,' "$f" | awk -F, '{print $3}')
    rt=$(grep -E '^FELT_METRIC,revised_trainerwrong_cens,' "$f" | awk -F, '{print $3}')
    [ "$rt" = "$at" ] || fail "trainerwrong revision $rt/$at ($cell)"
    echo "BAR_OK,$cell,trainerwrong_revision,$rt/$at"
  fi
done
echo "ALL_BARS_OK"
