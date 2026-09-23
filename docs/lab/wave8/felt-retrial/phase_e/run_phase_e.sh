#!/bin/bash
# Phase-E runner (wave-8 felt re-trial): static checks -> compile -> 54 runs
# (7 arms x 3 variants x 2 runs) -> determinism check -> integrity-bar validation.
# Integrity/INVALID-class FAIL aborts. Substantive falsification bars (F-INT-1/2/3)
# are evaluated in analysis (FAIL-with-evidence is a first-class result).
# No RNG anywhere; paired runs must be byte-identical.
set -u
D=~/workspace/tnn-lab/wave8/felt-retrial/phase_e
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
W7=~/workspace/tnn-lab/wave7/felt-intensity
cd "$D" || exit 1

fail(){ echo "RUNNER_FAIL,$1"; exit 1; }

echo "== static checks =="
# 1. I-7: felt.zag and substrate byte-identical to W7 originals
cmp -s "$D/felt.zag" "$W7/felt.zag" || fail "felt.zag differs from W7 original"
cmp -s "$D/st_memory_core.zag" "$W7/st_memory_core.zag" || fail "st_memory_core.zag differs from W7 original"
cmp -s "$D/substrate/cl/common.zag" "$W7/substrate/cl/common.zag" || fail "common.zag differs"
cmp -s "$D/substrate/R33_NATIVE_SHA256_V2.zag" "$W7/substrate/R33_NATIVE_SHA256_V2.zag" || fail "sha256 differs"
cmp -s "$D/substrate/R33_NATIVE_IO_V1.zag" "$W7/substrate/R33_NATIVE_IO_V1.zag" || fail "nativeio differs"
sha256sum -c "$D/hashes.sha256" || fail "hash file mismatch"
# 2. no direct st_str writes outside substrate API
grep -nE 'st_str\[[^]]*\]\s*=' felt.zag felt_phase_e.zag | grep -v 'st\.st_str\[s\] as i32' | grep -v 'st_i32' >/dev/null 2>&1 && fail "strength write outside substrate API"
# 3. I-4: no RNG tokens (case-insensitive) in felt module, driver, substrate copies
grep -rniE 'rand|srand|random|getrandom|/dev/urandom|rdtsc' felt.zag felt_phase_e.zag st_memory_core.zag substrate/ >/dev/null 2>&1 && fail "RNG token found"
# 4. bare @import (not commented)
grep -q '^@import' felt.zag || fail "felt.zag import not bare"
grep -q '^@import' felt_phase_e.zag || fail "driver import not bare"
# 5. frozen curriculum formulas present verbatim
grep -q '(7\*m+13\*v+3)%10)<3' felt_phase_e.zag || fail "imp formula changed"
grep -q '(3\*m+7\*v+9)%10)<2' felt_phase_e.zag || fail "wrong formula changed"
for mep in 'm==0' 'm==83' 'm==166' 'm==250' 'm==333' 'm==416'; do
  grep -q "$mep" felt_phase_e.zag || fail "implant schedule changed ($mep)"
done
# 6. I-7: felt.zag 12/20/25 constants unchanged from W7
grep -q 'FT_W_CORROBORATE:i32=12' felt.zag || fail "corroborate constant changed"
grep -q 'FT_W_CONTRADICT:i32=20' felt.zag || fail "contradict constant changed"
grep -q 'FT_W_TRAINER_MARK:i32=25' felt.zag || fail "trainer-mark constant changed"
# 7. felt read call sites restricted to the three W7 policy points
n=$(grep -cE 'do_read\((&w|w),' felt_phase_e.zag)
[ "$n" = "3" ] || fail "do_read call sites = $n, expected 3"
# 8. I-5: no R_PARAM / R write path anywhere in Phase E
grep -ni 'r_param' felt_phase_e.zag felt.zag st_memory_core.zag >/dev/null 2>&1 && fail "R_PARAM token found"
echo "STATIC_OK"

echo "== compile =="
"$ZNC" felt_phase_e.zag --no-zagd --no-analyze --no-foreground-cache -o felt_phase_e_bin || fail "compile"
echo "COMPILE_OK"

echo "== run cells (2x each) =="
for arm in F N; do
  for h in 1 2 3 4 5; do
    if [ "$arm" = "N" ] && [ "$h" != "1" ] && [ "$h" != "5" ]; then continue; fi
    for v in 0 1 2; do
      cell="${arm}_H${h}_${v}"
      ./felt_phase_e_bin "$arm" "$v" "$h" > "out_${cell}_a.txt" || fail "run ${cell} a"
      ./felt_phase_e_bin "$arm" "$v" "$h" > "out_${cell}_b.txt" || fail "run ${cell} b"
      cmp -s "out_${cell}_a.txt" "out_${cell}_b.txt" || fail "nondeterministic ${cell}"
      grep -q '^FELT_DONE$' "out_${cell}_a.txt" || fail "incomplete ${cell}"
      echo "CELL_OK,${cell}"
    done
  done
done
echo "DETERMINISM_OK"

echo "== integrity-bar validation =="
check(){ # file metric expected_min expected_max
  local v; v=$(grep -E "^FELT_METRIC,${2}," "$1" | head -1 | awk -F, '{print $3}')
  [ -n "$v" ] || fail "metric $2 missing in $1"
  if [ "$v" -lt "$3" ] || [ "$v" -gt "$4" ]; then fail "bar $2=$v not in [$3,$4] ($1)"; fi
}
for arm in F N; do
  for h in 1 2 3 4 5; do
    if [ "$arm" = "N" ] && [ "$h" != "1" ] && [ "$h" != "5" ]; then continue; fi
    for v in 0 1 2; do
      cell="${arm}_H${h}_${v}"; f="out_${cell}_a.txt"
      # frozen curriculum totals (verified by closed-form: v=0,1 -> 50/100;
      # v=2 -> 48/98 because implants at 166,416 override imp/wrong per the
      # precedence rule; matches W7's own out_F2_a.txt)
      if [ "$v" = "2" ]; then check "$f" offered_right_imp 48 48; else check "$f" offered_right_imp 50 50; fi
      if [ "$v" = "2" ]; then check "$f" offered_wrong 98 98; else check "$f" offered_wrong 100 100; fi
      check "$f" r_zone_entries 0 0
      r=$(grep -E '^FELT_CHECK,replay,' "$f" | awk -F, '{print $3}')
      [ "$r" = "0" ] || fail "replay rc=$r ($cell)"
      b=$(grep -E '^FELT_CHECK,recompute_bad,' "$f" | awk -F, '{print $3}')
      [ "$b" = "0" ] || fail "recompute_bad=$b ($cell)"
      af=$(grep -E '^FELT_METRIC,auc_full,' "$f" | awk -F, '{print $3}')
      [ "$af" = "0" ] || fail "auc histogram overflow ($cell)"
      tf=$(grep -E '^FELT_METRIC,wrong_traj_full,' "$f" | awk -F, '{print $3}')
      [ "$tf" = "0" ] || fail "wrong traj overflow ($cell)"
      if=$(grep -E '^FELT_METRIC,impl_traj_full,' "$f" | awk -F, '{print $3}')
      [ "$if" = "0" ] || fail "implant traj overflow ($cell)"
      echo "INTEGRITY_OK,$cell"
      if [ "$arm" = "F" ]; then
        j=$(grep -E '^FELT_METRIC,junk_max,' "$f" | awk -F, '{print $3}')
        [ "$j" -le 50 ] || fail "F4a junk_max=$j ($cell)"
        i2=$(grep -E '^FELT_METRIC,impl_bad,' "$f" | awk -F, '{print $3}')
        [ "$i2" = "0" ] || fail "F4b impl_bad=$i2 ($cell)"
        n2=$(grep -E '^FELT_METRIC,noev_bad,' "$f" | awk -F, '{print $3}')
        [ "$n2" = "0" ] || fail "F4c noev_bad=$n2 ($cell)"
        echo "ANTIINFLATION_OK,$cell"
      fi
    done
  done
done
echo "ALL_INTEGRITY_OK"
