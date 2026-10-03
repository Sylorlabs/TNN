#!/bin/sh
# build.sh -- cogops_plen_granularity: guards (GF6), compile, 3 runs.
# Pure shell + pinned znc. No forbidden interpreters.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi-gpi3/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/cogops_plen_granularity"
cd "$D"

fail() { echo "GUARD-FAIL: $1"; exit 1; }

echo "== GF6 guards =="
command -v python3 >/dev/null 2>&1 && fail "python3 resolves in PATH"
command -v python >/dev/null 2>&1 && fail "python resolves in PATH"
[ "$PATH" = "$HOME/safebin" ] || fail "PATH is not safebin-only"
grep -c "python" gran.zag | grep -q "^0$" || fail "python token in gran.zag"
grep -c "as \*i32" gran.zag | grep -q "^0$" || fail "as *i32 in gran.zag"
grep -c "_MODE" gran.zag | grep -q "^0$" || fail "_MODE token in gran.zag"
grep -c "opc==9" gran.zag | grep -q "^0$" || fail "opcode 9 in gran.zag"
[ "$(grep -o "opc==[0-9]" gran.zag | sort -u | tr '\n' ' ')" = "opc==1 opc==2 opc==3 opc==4 opc==5 opc==6 opc==7 opc==8 " ] || fail "opcode dispatch not exactly 1..8"
grep -n "while.*!(" gran.zag | grep -q . && fail "negated condition in while"
[ "$(grep -c "^fn main(" gran.zag)" = "1" ] || fail "main count != 1"
echo "GF6 guards PASS"

echo "== compile =="
"$ZNC" gran.zag -o gran_bin > gran_compile.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT gran_bin"; else echo "COMPILE-FAILED"; tail -30 gran_compile.txt; exit 1; fi

echo "== 3 runs =="
./gran_bin > gran_run1.txt 2>gran_err1.txt
./gran_bin > gran_run2.txt 2>gran_err2.txt
./gran_bin > gran_run3.txt 2>gran_err3.txt
sha256sum gran_run1.txt gran_run2.txt gran_run3.txt | tee gran_sha.txt
cmp gran_run1.txt gran_run2.txt || fail "run1 != run2"
cmp gran_run2.txt gran_run3.txt || fail "run2 != run3"
echo "3/3 byte-identical: GF5 PASS"
echo "== summary =="
grep -h "REVISE-RESULT" gran_run1.txt
echo "RNG-MATCH lines: $(grep -c 'RNG-MATCH' gran_run1.txt) (expect 48)"
grep -h "RNG-MISMATCH" gran_run1.txt | head -3
grep -h "FLIP" gran_run1.txt
grep -h "PLEN-ADJ" gran_run1.txt | head -20
echo "build-done"
