#!/bin/sh
# build.sh -- cogops_plen_advantage: guards (AH8), compile, 3 runs.
# Pure shell + pinned znc. No forbidden interpreters.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi-gpi3/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi-plenadv/docs/lab/research-lead/overnight-20260928/cogops_plen_advantage"
cd "$D"

fail() { echo "GUARD-FAIL: $1"; exit 1; }

echo "== AH8 guards =="
command -v python3 >/dev/null 2>&1 && fail "python3 resolves in PATH"
command -v python >/dev/null 2>&1 && fail "python resolves in PATH"
[ "$PATH" = "$HOME/safebin" ] || fail "PATH is not safebin-only"
grep -c "python" adv.zag | grep -q "^0$" || fail "python token in adv.zag"
grep -c "as \\*i32" adv.zag | grep -q "^0$" || fail "as *i32 in adv.zag"
grep -c "_MODE" adv.zag | grep -q "^0$" || fail "_MODE token in adv.zag"
grep -c "opc==9" adv.zag | grep -q "^0$" || fail "opcode 9 in adv.zag"
[ "$(grep -o "opc==[0-9]" adv.zag | sort -u | tr '\n' ' ')" = "opc==1 opc==2 opc==3 opc==4 opc==5 opc==6 opc==7 opc==8 " ] || fail "opcode dispatch not exactly 1..8"
grep -n "while.*!(" adv.zag | grep -q . && fail "negated condition in while"
[ "$(grep -c "^fn main(" adv.zag)" = "1" ] || fail "main count != 1"
echo "AH8 guards PASS"

echo "== compile =="
"$ZNC" adv.zag -o adv_bin > adv_compile.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT adv_bin"; else echo "COMPILE-FAILED"; tail -30 adv_compile.txt; exit 1; fi

echo "== 3 runs =="
./adv_bin > adv_run1.txt 2>adv_err1.txt
./adv_bin > adv_run2.txt 2>adv_err2.txt
./adv_bin > adv_run3.txt 2>adv_err3.txt
sha256sum adv_run1.txt adv_run2.txt adv_run3.txt | tee adv_sha.txt
cmp adv_run1.txt adv_run2.txt || fail "run1 != run2"
cmp adv_run2.txt adv_run3.txt || fail "run2 != run3"
echo "3/3 byte-identical: AH7 PASS"
echo "== summary =="
grep -h "REVISE-RESULT" adv_run1.txt
echo "RNG-MATCH lines: $(grep -c 'RNG-MATCH' adv_run1.txt) (expect 96)"
grep -h "RNG-MISMATCH" adv_run1.txt | head -3
echo "PLEN-ADJ count: $(grep -c 'PLEN-ADJ' adv_run1.txt)"
echo "build-done"
