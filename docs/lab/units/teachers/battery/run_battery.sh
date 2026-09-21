#!/bin/bash
# run_battery.sh — Track B battery (Crew 6) self-test runner.
# 1. static no-RNG / no-wallclock scan (comments stripped first)
# 2. compiles tb_selftest.zag to a temp binary
# 3. runs it 3x; outputs must be byte-identical
# 4. every CL_CHECK must have actual==expected
# 5. TB_STAT / TB_SCORECARD / TB_HEAD2HEAD lines must match hand-computed values
# 6. TB_FAILURES,0 and exit code 0
# Pure Zag, zero RNG. Exits nonzero on any failure.
set -u
DIR="$(cd "$(dirname "$0")" && pwd)"
ZNC="$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1"
BIN="$(mktemp /tmp/tb_battery_bin.XXXXXX)"
OUT1="$(mktemp /tmp/tb_battery_out1.XXXXXX)"
OUT2="$(mktemp /tmp/tb_battery_out2.XXXXXX)"
OUT3="$(mktemp /tmp/tb_battery_out3.XXXXXX)"
fail=0
say(){ echo "BTRY: $*"; }
die(){ say "FAIL: $*"; fail=1; }

# ---- 1. static scans ----
say "static no-RNG / no-wallclock scan"
hits="$(for f in "$DIR"/tb_*.zag; do sed 's|//.*||' "$f"; done | grep -inE 'rand|srand|random|_zag_time|wallclock|gettime|clock_gettime|rdtsc|/dev/urandom|[^a-z_]seed[^a-z_]' || true)"
if [ -n "$hits" ]; then die "forbidden token found: $hits"; else say "clean"; fi

# forbidden build artifacts must not exist in the source dir
for pat in '*.zagd' '.zag-cache' 'tb_selftest_bin' 'battery_bin'; do
  if ls "$DIR"/$pat >/dev/null 2>&1; then die "forbidden artifact present: $pat"; fi
done

# ---- 2. compile ----
say "compiling"
if ! "$ZNC" "$DIR/tb_selftest.zag" --no-zagd --no-analyze --no-foreground-cache -o "$BIN" > /tmp/tb_compile.log 2>&1; then
  die "compile failed"; cat /tmp/tb_compile.log; rm -f "$BIN" "$OUT1" "$OUT2" "$OUT3"; exit 1
fi
say "compiled ok"

# ---- 3. run 3x, byte-identical ----
say "running 3x"
"$BIN" > "$OUT1" 2>&1; c1=$?
"$BIN" > "$OUT2" 2>&1; c2=$?
"$BIN" > "$OUT3" 2>&1; c3=$?
[ "$c1" = 0 ] || die "run1 exit=$c1"
[ "$c2" = 0 ] || die "run2 exit=$c2"
[ "$c3" = 0 ] || die "run3 exit=$c3"
cmp -s "$OUT1" "$OUT2" || die "run1/run2 differ"
cmp -s "$OUT1" "$OUT3" || die "run1/run3 differ"
say "byte-identical across 3 runs"

# ---- 4. CL_CHECK actual==expected ----
bad="$(awk -F, '/^CL_CHECK/{if($3!=$4) print}' "$OUT1" || true)"
nchk="$(grep -c '^CL_CHECK' "$OUT1")"
if [ -n "$bad" ]; then die "CL_CHECK mismatches: $bad"; else say "CL_CHECK $nchk/$nchk actual==expected"; fi

# ---- 5. hand-computed expectations ----
expect_grep(){ # $1 = fixed string expected exactly once
  if ! grep -qxF "$1" "$OUT1"; then die "missing/incorrect line: $1"; fi
}
expect_grep "TB_STAT,flawA,110,1"
expect_grep "TB_STAT,flawB,75,0,80,65"
expect_grep "TB_STAT,leakC,1,0"
expect_grep "TB_STAT,dcD1,0,996,0"
expect_grep "TB_STAT,dcD2,3"
expect_grep "TB_STAT,dcD3,2"
expect_grep "TB_STAT,dcD4,1"
expect_grep "TB_STAT,redteam,14,0,1,1,1,1,0,0,1"
expect_grep "TB_STAT,tripneg,0"
expect_grep "TB_STAT,m8det,1"
expect_grep "TB_STAT,m8nondet,0"
expect_grep "TB_SCORECARD,1,0,99.5,91.7,100.0,95.0,100.0,97.3,PASS,CLEAR"
expect_grep "TB_SCORECARD,3,0,98.0,54.2,100.0,90.0,90.9,86.0,PASS,CLEAR"
expect_grep "TB_SCORECARD,4,0,99.0,83.3,100.0,92.0,100.0,94.7,PASS,CLEAR"
expect_grep "TB_SCORECARD,5,0,97.0,75.0,92.8,88.0,66.6,86.5,PASS,CLEAR"
expect_grep "TB_SCORECARD,9,0,99.0,91.7,0.0,90.0,100.0,71.6,PASS,KILL-III"
expect_grep "TB_SCORECARD,8,0,99.0,91.7,0.0,90.0,100.0,71.6,PASS,KILL-IV"
expect_grep "TB_SCORECARD,7,0,99.5,91.7,100.0,95.0,100.0,97.3,PASS,INVALID"
expect_grep "TB_HEAD2HEAD,weighted_winner,1,97.3"
expect_grep "TB_HEAD2HEAD,leg_champion,M,1,99.5"
expect_grep "TB_HEAD2HEAD,leg_champion,R,1,91.7"
expect_grep "TB_HEAD2HEAD,leg_champion,I,1,100.0"
expect_grep "TB_HEAD2HEAD,leg_champion,Ret,1,95.0"
expect_grep "TB_HEAD2HEAD,leg_champion,C,1,100.0"
expect_grep "TB_FAILURES,0"
say "all hand-computed expectations match"

rm -f "$BIN" "$OUT1" "$OUT2" "$OUT3"
if [ "$fail" = 0 ]; then say "BATTERY SELF-TEST PASS"; else say "BATTERY SELF-TEST FAIL"; fi
exit "$fail"
