#!/bin/bash
# Wave-8 felt re-trial, Worker C (Arm T developmental + Phase C coupling).
# Static checks -> compile -> run each cell 2x -> byte-identical determinism
# check -> basic integrity checks (replay, recompute, FELT_DONE).
# Any FAIL aborts. No RNG anywhere. No git commits.
set -u
D=~/workspace/tnn-lab/wave8/felt-retrial/develop
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
W7=~/workspace/tnn-lab/wave7/felt-intensity
cd "$D" || exit 1

fail(){ echo "RUNNER_FAIL,$1"; exit 1; }

echo "== static checks =="
# 1. copied files byte-identical to Wave-7 frozen originals
cmp -s "$D/felt.zag" "$W7/felt.zag" || fail "felt.zag modified"
cmp -s "$D/st_memory_core.zag" "$W7/st_memory_core.zag" || fail "st_memory_core.zag modified"
cmp -s "$D/substrate/cl/common.zag" "$W7/substrate/cl/common.zag" || fail "common.zag modified"
cmp -s "$D/substrate/R33_NATIVE_SHA256_V2.zag" "$W7/substrate/R33_NATIVE_SHA256_V2.zag" || fail "sha256 modified"
cmp -s "$D/substrate/R33_NATIVE_IO_V1.zag" "$W7/substrate/R33_NATIVE_IO_V1.zag" || fail "nativeio modified"
# 2. no RNG tokens
grep -rniE 'rand|srand|random|getrandom|/dev/urandom|rdtsc' develop.zag felt.zag st_memory_core.zag >/dev/null 2>&1 && fail "RNG token found"
# 3. bare @import
grep -q '^@import' develop.zag || fail "develop.zag import not bare"
grep -q '^@import' felt.zag || fail "felt.zag import not bare"
# 4. frozen curriculum formulas present verbatim (T arm)
grep -q '(7\*m+13\*v+3)%10)<3' develop.zag || fail "imp formula changed"
grep -q '(3\*m+7\*v+9)%10)<2' develop.zag || fail "wrong formula changed"
grep -q 'm==83' develop.zag || fail "implant schedule changed"
grep -q 'm==416' develop.zag || fail "implant schedule changed"
# 5. felt constants 12/20/25 present (from felt.zag, frozen)
grep -q 'FT_W_CORROBORATE:i32=12' felt.zag || fail "felt constant 12 missing"
grep -q 'FT_W_CONTRADICT:i32=20' felt.zag || fail "felt constant 20 missing"
grep -q 'FT_W_TRAINER_MARK:i32=25' felt.zag || fail "felt constant 25 missing"
echo "STATIC_OK"

echo "== compile =="
"$ZNC" develop.zag --no-zagd --no-analyze --no-foreground-cache -o develop_bin || fail "compile"
echo "COMPILE_OK"

echo "== run cells (2x each) =="
# Arm T: 3 variants x 2 runs. Phase C cells are run separately once Worker B's
# D-harness mapping arrives; this script runs whatever cells are requested.
CELLS="${1:-T0 T1 T2}"
for cell in $CELLS; do
  mode=${cell:0:1}; var=${cell:1:1}
  ./develop_bin "$mode" "$var" > "out_${cell}_a.txt" || fail "run ${cell} a"
  ./develop_bin "$mode" "$var" > "out_${cell}_b.txt" || fail "run ${cell} b"
  cmp -s "out_${cell}_a.txt" "out_${cell}_b.txt" || fail "nondeterministic ${cell}"
  grep -q '^FELT_DONE$' "out_${cell}_a.txt" || fail "incomplete ${cell}"
  echo "CELL_OK,${cell}"
done
echo "DETERMINISM_OK"

echo "== integrity checks =="
check(){ # file metric
  local v; v=$(grep -E "^FELT_METRIC,${2}," "$1" | head -1 | awk -F, '{print $3}')
  [ -n "$v" ] || fail "metric $2 missing in $1"
  echo "METRIC,$1,$2,$v"
}
for cell in $CELLS; do
  f="out_${cell}_a.txt"
  r=$(grep -E '^FELT_CHECK,replay,' "$f" | awk -F, '{print $3}')
  [ "$r" = "0" ] || fail "replay rc=$r ($cell)"
  b=$(grep -E '^FELT_CHECK,recompute_bad,' "$f" | awk -F, '{print $3}')
  [ "$b" = "0" ] || fail "recompute_bad=$b ($cell)"
  check "$f" offered_ri
  check "$f" offered_wr
  check "$f" held_ri
  check "$f" n_drops
  check "$f" junk_max
  check "$f" impl_bad
  check "$f" noev_bad
  check "$f" r_final
  check "$f" delib_count
  check "$f" delib_fails
  check "$f" gate_t12
  check "$f" gate_t23
  check "$f" rparam_frozen
  echo "INTEGRITY_OK,$cell"
done
echo "ALL_OK"
