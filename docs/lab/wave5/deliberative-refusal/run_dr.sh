#!/bin/bash
# Wave-5 deliberative-refusal trial runner.
# Preregistered battery (see PREREG.md): static checks, native compile,
# 10x + 100x main legs (2x each, byte-identical), four variants,
# four negative controls. Evidence bundle under evidence/.
set -u
D="$HOME/workspace/tnn-lab/wave5/deliberative-refusal"
ZNC="$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1"
EV="$D/evidence"
mkdir -p "$EV"
FAIL=0
note() { echo "[run_dr] $*"; }
bad()  { echo "[run_dr] FAIL: $*"; FAIL=1; }

# ---- 1. static: no RNG anywhere in the AI decision path ----
if grep -nEi 'rand\(|srand|seed\(|entropy|random\(|/dev/urandom|getrandom|rdtsc' "$D/dr.zag"; then
  bad "RNG/entropy source found in dr.zag"
else note "no-RNG static check clean"; fi

# ---- 2. static: the deep-audit schedule lives only in the harness region ----
MARK=$(grep -n "HARNESS REGION" "$D/dr.zag" | head -1 | cut -d: -f1)
if [ -z "$MARK" ]; then bad "harness marker not found"; fi
for id in DR_DEEP_K DR_DEEP_W; do
  if head -n $((MARK-1)) "$D/dr.zag" | grep -Eq "(^|[^A-Za-z0-9_])$id([^A-Za-z0-9_]|$)"; then
    bad "scope leak: $id referenced before the harness region"
  fi
done
# dr_deep_audit may be defined once (harness region) and called once, from main
DEFC=$(grep -c "^fn dr_deep_audit" "$D/dr.zag")
CALLS=$(grep -n "dr_deep_audit(" "$D/dr.zag" | grep -v "fn dr_deep_audit" | grep -v "^\s*//")
NCC=$(echo "$CALLS" | grep -c .)
if [ "$DEFC" != "1" ] || [ "$NCC" != "1" ]; then bad "dr_deep_audit def/call sites unexpected: def=$DEFC calls=$NCC"; fi
CALLCTX=$(echo "$CALLS" | head -1 | cut -d: -f1)
MAINLN=$(grep -n "^fn main" "$D/dr.zag" | head -1 | cut -d: -f1)
if [ "$CALLCTX" -lt "$MAINLN" ]; then bad "dr_deep_audit called outside main"; fi
note "scope check clean (deep audit defined once, called once, from main)"

# ---- 3. native compile ----
"$ZNC" --no-zagd --no-analyze --no-foreground-cache "$D/dr.zag" -o "$D/dr" \
  > "$EV/compile.log" 2>&1 || bad "native compile failed (see evidence/compile.log)"
note "compiled: $(wc -c < "$D/dr") bytes"

sha256sum "$D/dr.zag" > "$EV/sha256sums.txt"

# ---- 4. main legs: 10x and 100x, two runs each, byte-identical ----
for leg in 10x 100x; do
  "$D/dr" "$leg" > "$EV/dr_${leg}_a.log" 2>&1; ra=$?
  "$D/dr" "$leg" > "$EV/dr_${leg}_b.log" 2>&1; rb=$?
  if [ $ra -ne 0 ] || [ $rb -ne 0 ]; then bad "main leg $leg nonzero exit ($ra/$rb)"; fi
  if ! cmp -s "$EV/dr_${leg}_a.log" "$EV/dr_${leg}_b.log"; then
    bad "main leg $leg not byte-identical across runs"
  fi
  sha256sum "$EV/dr_${leg}_a.log" >> "$EV/sha256sums.txt"
  note "main leg $leg: exit $ra/$rb, byte-identical, $(grep -c DR_CURVE "$EV/dr_${leg}_a.log") curve points"
done

# ---- 5. variants: patched copies in /tmp, 100x leg ----
# v1 myopic: takes expected. v2 pressure: takes expected. v3 sens140: takes
# expected (late). v4 sens160: zero takes expected.
declare -A VARIANT_SED=( [1]="s/const DR_VARIANT:i32=0;/const DR_VARIANT:i32=1;/"
                         [2]="s/const DR_VARIANT:i32=0;/const DR_VARIANT:i32=2;/"
                         [3]="s/const DR_VARIANT:i32=0;/const DR_VARIANT:i32=3;/;s/const DR_SMAX:i32=150;/const DR_SMAX:i32=140;/"
                         [4]="s/const DR_VARIANT:i32=0;/const DR_VARIANT:i32=4;/;s/const DR_SMAX:i32=150;/const DR_SMAX:i32=160;/" )
for v in 1 2 3 4; do
  sed "${VARIANT_SED[$v]}" "$D/dr.zag" > /tmp/dr_v$v.zag
  "$ZNC" --no-zagd --no-analyze --no-foreground-cache /tmp/dr_v$v.zag -o /tmp/dr_v$v \
    > "$EV/compile_v$v.log" 2>&1 || bad "variant $v compile failed"
  /tmp/dr_v$v 100x > "$EV/dr_variant${v}_100x.log" 2>&1; rv=$?
  sha256sum "$EV/dr_variant${v}_100x.log" >> "$EV/sha256sums.txt"
  note "variant $v (100x): exit $rv :: $(grep DR_VARIANT_SUMMARY "$EV/dr_variant${v}_100x.log" | head -1)"
done

# ---- 6. negative controls: patched copies in /tmp ----
# NC-DR1: forced T1 take at block 602 -> 100x leg, expect DR_RULE_FAIL.
# NC-DR2/3/4: 10x legs, expect DR_CITE_FAIL,strength / DR_COMPLETE_FAIL / DR_CITE_FAIL.
for nc in 1 2 3 4; do
  sed "s/const DR_SABOTAGE:i32=0;/const DR_SABOTAGE:i32=$nc;/" "$D/dr.zag" > /tmp/dr_nc$nc.zag
  "$ZNC" --no-zagd --no-analyze --no-foreground-cache /tmp/dr_nc$nc.zag -o /tmp/dr_nc$nc \
    > "$EV/compile_nc$nc.log" 2>&1 || bad "NC-DR$nc compile failed"
done
/tmp/dr_nc1 100x > "$EV/dr_nc1_100x.log" 2>&1; r1=$?
/tmp/dr_nc2 10x  > "$EV/dr_nc2_10x.log" 2>&1; r2=$?
/tmp/dr_nc3 10x  > "$EV/dr_nc3_10x.log" 2>&1; r3=$?
/tmp/dr_nc4 10x  > "$EV/dr_nc4_10x.log" 2>&1; r4=$?
for i in 1 2 3 4; do eval "r=\$r$i"; sha256sum "$EV"/dr_nc${i}_*.log >> "$EV/sha256sums.txt"; done
[ $r1 -eq 0 ] && bad "NC-DR1 not detected (exit 0)"
grep -q "DR_RULE_FAIL" "$EV/dr_nc1_100x.log" || bad "NC-DR1 missing DR_RULE_FAIL"
[ $r2 -eq 0 ] && bad "NC-DR2 not detected (exit 0)"
grep -q "DR_CITE_FAIL,strength" "$EV/dr_nc2_10x.log" || bad "NC-DR2 missing DR_CITE_FAIL,strength"
[ $r3 -eq 0 ] && bad "NC-DR3 not detected (exit 0)"
grep -q "DR_COMPLETE_FAIL" "$EV/dr_nc3_10x.log" || bad "NC-DR3 missing DR_COMPLETE_FAIL"
[ $r4 -eq 0 ] && bad "NC-DR4 not detected (exit 0)"
grep -q "DR_CITE_FAIL" "$EV/dr_nc4_10x.log" || bad "NC-DR4 missing DR_CITE_FAIL"
note "NC exits: $r1 $r2 $r3 $r4 (all nonzero = detected)"

# ---- 7. trajectory extraction ----
for leg in 10x 100x; do
  grep "^DR_CURVE" "$EV/dr_${leg}_a.log" > "$EV/curve_${leg}.csv"
done
grep "^DR_SUMMARY" "$EV"/dr_*.log > "$EV/summaries.txt"

if [ $FAIL -eq 0 ]; then note "ALL RUNNER CHECKS PASSED"; else note "RUNNER FAILURES PRESENT"; fi
exit $FAIL
