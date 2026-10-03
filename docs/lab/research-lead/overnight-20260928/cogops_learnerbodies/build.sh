#!/bin/sh
# build.sh -- LB1 (cogops_learnerbodies): guards (K8), compile, 3 runs.
# Pure shell + pinned znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi-gpi3/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi-gpi3/docs/lab/research-lead/overnight-20260928/cogops_learnerbodies"
cd "$D"

fail() { echo "GUARD-FAIL: $1"; exit 1; }

echo "== K8 guards =="
# no python
grep -c "python" lb.zag | grep -q "^0$" || fail "python token in lb.zag"
# no forbidden *i32 slice construction
grep -c "as \*i32" lb.zag | grep -q "^0$" || fail "as *i32 in lb.zag"
# no cognitive-mode tokens (RETRIEVE/DERIVE/VERIFY/PREDICT/INQUIRE/CONSTRUCT as modes)
grep -c "_MODE" lb.zag | grep -q "^0$" || fail "_MODE token in lb.zag"
# interpreter dispatches exactly opcodes 1..8
grep -c "opc==9" lb.zag | grep -q "^0$" || fail "opcode 9 in lb.zag"
[ "$(grep -o "opc==[0-9]" lb.zag | sort -u | tr '\n' ' ')" = "opc==1 opc==2 opc==3 opc==4 opc==5 opc==6 opc==7 opc==8 " ] || fail "opcode dispatch not exactly 1..8"
# no negated conjunction in while conditions (znc defect #4)
grep -n "while.*!(" lb.zag | grep -q . && fail "negated condition in while"
# single main
[ "$(grep -c "^fn main(" lb.zag)" = "1" ] || fail "main count != 1"
echo "K8 guards PASS"

echo "== compile =="
"$ZNC" lb.zag -o lb_bin > lb_compile.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT lb_bin"; else echo "COMPILE-FAILED"; tail -30 lb_compile.txt; exit 1; fi

echo "== 3 runs =="
./lb_bin > lb_run1.txt 2>lb_err1.txt
./lb_bin > lb_run2.txt 2>lb_err2.txt
./lb_bin > lb_run3.txt 2>lb_err3.txt
sha256sum lb_run1.txt lb_run2.txt lb_run3.txt | tee lb_sha.txt
cmp lb_run1.txt lb_run2.txt || fail "run1 != run2"
cmp lb_run2.txt lb_run3.txt || fail "run2 != run3"
echo "3/3 byte-identical: K7 PASS"
echo "== verdicts =="
grep -h "OVERALL" lb_run1.txt
grep -h "VERDICT" lb_run1.txt
echo "build-done"
