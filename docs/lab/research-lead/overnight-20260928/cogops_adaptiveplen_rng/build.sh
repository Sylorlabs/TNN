#!/bin/sh
# build.sh -- cogops_adaptiveplen_rng: guards (MR4), compile, 3 runs.
# Pure shell + pinned znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi-gpi3/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi-gpi3/docs/lab/research-lead/overnight-20260928/cogops_adaptiveplen_rng"
cd "$D"

fail() { echo "GUARD-FAIL: $1"; exit 1; }

echo "== MR4 guards =="
grep -c "python" rng.zag | grep -q "^0$" || fail "python token in rng.zag"
grep -c "as \*i32" rng.zag | grep -q "^0$" || fail "as *i32 in rng.zag"
grep -c "_MODE" rng.zag | grep -q "^0$" || fail "_MODE token in rng.zag"
grep -c "opc==9" rng.zag | grep -q "^0$" || fail "opcode 9 in rng.zag"
[ "$(grep -o "opc==[0-9]" rng.zag | sort -u | tr '\n' ' ')" = "opc==1 opc==2 opc==3 opc==4 opc==5 opc==6 opc==7 opc==8 " ] || fail "opcode dispatch not exactly 1..8"
grep -n "while.*!(" rng.zag | grep -q . && fail "negated condition in while"
[ "$(grep -c "^fn main(" rng.zag)" = "1" ] || fail "main count != 1"
echo "MR4 guards PASS"

echo "== compile =="
"$ZNC" rng.zag -o rng_bin > rng_compile.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT rng_bin"; else echo "COMPILE-FAILED"; tail -30 rng_compile.txt; exit 1; fi

echo "== 3 runs =="
./rng_bin > rng_run1.txt 2>rng_err1.txt
./rng_bin > rng_run2.txt 2>rng_err2.txt
./rng_bin > rng_run3.txt 2>rng_err3.txt
sha256sum rng_run1.txt rng_run2.txt rng_run3.txt | tee rng_sha.txt
cmp rng_run1.txt rng_run2.txt || fail "run1 != run2"
cmp rng_run2.txt rng_run3.txt || fail "run2 != run3"
echo "3/3 byte-identical: MR3 PASS"
echo "== summary =="
grep -h "REVISE-RESULT" rng_run1.txt
echo "RNG-MATCH lines: $(grep -c 'RNG-MATCH' rng_run1.txt)"
grep -h "RNG-MISMATCH" rng_run1.txt | head -3
grep -h "SEEDCUR" rng_run1.txt
echo "build-done"
