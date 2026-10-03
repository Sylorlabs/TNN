#!/bin/sh
# build.sh -- cogops_parsimony: guards (K8), compile, 3 runs.
# Pure shell + pinned znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi-gpi3/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi-gpi3/docs/lab/research-lead/overnight-20260928/cogops_parsimony"
cd "$D"

fail() { echo "GUARD-FAIL: $1"; exit 1; }

echo "== K8 guards =="
# no python
grep -c "python" pp.zag | grep -q "^0$" || fail "python token in pp.zag"
# no forbidden *i32 slice construction
grep -c "as \*i32" pp.zag | grep -q "^0$" || fail "as *i32 in pp.zag"
# no cognitive-mode tokens
grep -c "_MODE" pp.zag | grep -q "^0$" || fail "_MODE token in pp.zag"
# interpreter dispatches exactly opcodes 1..8
grep -c "opc==9" pp.zag | grep -q "^0$" || fail "opcode 9 in pp.zag"
[ "$(grep -o "opc==[0-9]" pp.zag | sort -u | tr '\n' ' ')" = "opc==1 opc==2 opc==3 opc==4 opc==5 opc==6 opc==7 opc==8 " ] || fail "opcode dispatch not exactly 1..8"
# no negated conjunction in while conditions (znc defect #4)
grep -n "while.*!(" pp.zag | grep -q . && fail "negated condition in while"
# single main
[ "$(grep -c "^fn main(" pp.zag)" = "1" ] || fail "main count != 1"
echo "K8 guards PASS"

echo "== compile =="
"$ZNC" pp.zag -o pp_bin > pp_compile.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT pp_bin"; else echo "COMPILE-FAILED"; tail -30 pp_compile.txt; exit 1; fi

echo "== 3 runs =="
./pp_bin > pp_run1.txt 2>pp_err1.txt
./pp_bin > pp_run2.txt 2>pp_err2.txt
./pp_bin > pp_run3.txt 2>pp_err3.txt
sha256sum pp_run1.txt pp_run2.txt pp_run3.txt | tee pp_sha.txt
cmp pp_run1.txt pp_run2.txt || fail "run1 != run2"
cmp pp_run2.txt pp_run3.txt || fail "run2 != run3"
echo "3/3 byte-identical: K7 PASS"
echo "== verdicts =="
grep -h "OVERALL" pp_run1.txt
grep -h "TRADEOFF" pp_run1.txt
grep -h "PARSIMONY-COMPLETE\|INCOMPLETE" pp_run1.txt
echo "build-done"
