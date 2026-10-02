#!/bin/sh
# Frozen fork battery harness, wave-20260924-0521pdt. Pure shell, no Python.
# Usage: harness.sh <label> <znc_path> <scratch_dir>
set -u
LABEL="$1"; ZNC="$2"; SCR="$3"
mkdir -p "$SCR"; cd "$SCR" || exit 99
LOG="$SCR/harness.log"; : > "$LOG"
say() { echo "$@" | tee -a "$LOG"; }
fail() { say "FAIL[$LABEL]: $*"; echo "FAIL: $*" >> "$SCR/VERDICT.txt"; exit 1; }

printf 'fn main()i32 {\n    _zag_print("FORKBATTERY-OK 42");\n    return 0;\n}\n' > forkbat_hello.zag
printf 'FORKBATTERY-OK 42' > expected.out

# B1 COMPILE+RUN
"$ZNC" forkbat_hello.zag --no-zagd --no-analyze --no-foreground-cache -o hello_bin > znc_compile.out 2> znc_compile.err
ce=$?; say "B1 compile exit=$ce"
[ "$ce" -eq 0 ] || fail "B1 compile exit $ce; err: $(cat znc_compile.err)"
./hello_bin > run1.out 2> run1.err
re=$?; say "B1 run exit=$re"
[ "$re" -eq 0 ] || fail "B1 run exit $re"
cmp run1.out expected.out > /dev/null 2>&1 || fail "B1 stdout differ: run1=$(sha256sum < run1.out | cut -d' ' -f1) expected=$(sha256sum < expected.out | cut -d' ' -f1)"
say "B1 PASS (stdout sha256 $(sha256sum < run1.out | cut -d' ' -f1))"

# B2 DETERMINISM
./hello_bin > run2.out 2>/dev/null
cmp run1.out run2.out > /dev/null 2>&1 || fail "B2 rerun stdout differ"
"$ZNC" forkbat_hello.zag --no-zagd --no-analyze --no-foreground-cache -o bin_a > /dev/null 2>&1
"$ZNC" forkbat_hello.zag --no-zagd --no-analyze --no-foreground-cache -o bin_b > /dev/null 2>&1
ha=$(sha256sum bin_a | cut -d" " -f1); hb=$(sha256sum bin_b | cut -d" " -f1)
say "B2 bin_a sha256 $ha"; say "B2 bin_b sha256 $hb"
[ "$ha" = "$hb" ] || fail "B2 two compiles differ"
[ "$ha" = "75b85d3cec684f6a156f4c01169551369e4b0e040b56ec1fd24749876eddffa2" ] || fail "B2 binary sha256 mismatch (expected pinned 75b85d3...)"
say "B2 PASS"

# B3 STRICT CHECK
"$ZNC" check forkbat_hello.zag --strict --no-zagd > check.out 2> check.err
cke=$?; say "B3 check exit=$cke stdout=$(cat check.out)"
[ "$cke" -eq 0 ] || fail "B3 check exit $cke: $(cat check.err)"

# NEG1: unterminated string must fail compile with E0002 and fail check
printf 'fn main()i32 {\n    _zag_print("oops);\n    return 0;\n}\n' > neg1.zag
"$ZNC" neg1.zag --no-zagd --no-analyze --no-foreground-cache -o neg1_bin > neg1_compile.out 2> neg1_compile.err
nce=$?
[ "$nce" -ne 0 ] || fail "NEG1 verdict logic broken: bad file compiled cleanly"
grep -q 'E0002' neg1_compile.err || fail "NEG1: compile failed but no E0002 (got: $(cat neg1_compile.err))"
"$ZNC" check neg1.zag --strict --no-zagd > neg1_check.out 2> neg1_check.err
[ "$?" -ne 0 ] || fail "NEG1 verdict logic broken: check passed on bad file"
say "NEG1 PASS (compile exit=$nce, E0002 confirmed, check nonzero)"

# NEG2: compiles and checks but wrong stdout; must fail at byte-compare
printf 'fn main()i32 {\n    _zag_print("WRONG OUTPUT");\n    return 0;\n}\n' > neg2.zag
"$ZNC" neg2.zag --no-zagd --no-analyze --no-foreground-cache -o neg2_bin > /dev/null 2>&1
[ "$?" -eq 0 ] || fail "NEG2: clean file failed to compile"
"$ZNC" check neg2.zag --strict --no-zagd > /dev/null 2>&1
[ "$?" -eq 0 ] || fail "NEG2: clean file failed strict check"
./neg2_bin > neg2.out 2>/dev/null
cmp neg2.out expected.out > /dev/null 2>&1 && fail "NEG2 verdict logic broken: wrong output byte-matched"
say "NEG2 PASS (cmp differ as required: $(cmp neg2.out expected.out 2>&1))"

echo "VERDICT=PASS" > "$SCR/VERDICT.txt"
say "VERDICT=PASS [$LABEL]"
exit 0
