#!/bin/sh
# build.sh -- cogops_adaptiveplen: guards (K8), compile, 3 runs.
# Pure shell + pinned znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi-gpi3/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi-gpi3/docs/lab/research-lead/overnight-20260928/cogops_adaptiveplen"
cd "$D"

fail() { echo "GUARD-FAIL: $1"; exit 1; }

echo "== K8 guards =="
# no python
grep -c "python" ap.zag | grep -q "^0$" || fail "python token in ap.zag"
# no forbidden *i32 slice construction
grep -c "as \*i32" ap.zag | grep -q "^0$" || fail "as *i32 in ap.zag"
# no cognitive-mode tokens
grep -c "_MODE" ap.zag | grep -q "^0$" || fail "_MODE token in ap.zag"
# interpreter dispatches exactly opcodes 1..8
grep -c "opc==9" ap.zag | grep -q "^0$" || fail "opcode 9 in ap.zag"
[ "$(grep -o "opc==[0-9]" ap.zag | sort -u | tr '\n' ' ')" = "opc==1 opc==2 opc==3 opc==4 opc==5 opc==6 opc==7 opc==8 " ] || fail "opcode dispatch not exactly 1..8"
# no negated conjunction in while conditions (znc defect #4)
grep -n "while.*!(" ap.zag | grep -q . && fail "negated condition in while"
# single main
[ "$(grep -c "^fn main(" ap.zag)" = "1" ] || fail "main count != 1"
echo "K8 guards PASS"

echo "== compile =="
"$ZNC" ap.zag -o ap_bin > ap_compile.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT ap_bin"; else echo "COMPILE-FAILED"; tail -30 ap_compile.txt; exit 1; fi

echo "== 3 runs =="
./ap_bin > ap_run1.txt 2>ap_err1.txt
./ap_bin > ap_run2.txt 2>ap_err2.txt
./ap_bin > ap_run3.txt 2>ap_err3.txt
sha256sum ap_run1.txt ap_run2.txt ap_run3.txt | tee ap_sha.txt
cmp ap_run1.txt ap_run2.txt || fail "run1 != run2"
cmp ap_run2.txt ap_run3.txt || fail "run2 != run3"
echo "3/3 byte-identical: K7 PASS"
echo "== verdicts =="
grep -h "OVERALL" ap_run1.txt
grep -h "TRADEOFF" ap_run1.txt
grep -h "ADAPTIVEPLEN-COMPLETE\|INCOMPLETE" ap_run1.txt
echo "== plen trajectory (arm 0) =="
grep -h "PLEN-ADJ" ap_run1.txt
echo "build-done"
