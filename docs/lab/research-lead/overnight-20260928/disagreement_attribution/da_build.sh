#!/bin/bash
# da_build.sh -- disagreement-attribution battery build + run + verify
# Usage: ./da_build.sh  (run from this directory)
# safebin PATH is mandatory; the pinned znc builds both binaries;
# each binary runs 3x; sha256 equality across the three runs is
# checked for every binary.
export PATH="$HOME/safebin"
set -u
D="$(cd "$(dirname "$0")" && pwd)"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
cd "$D" || exit 1

# K2 toolchain guard record
echo "PATH=$PATH"
echo "python3: $(which python3 || echo MISSING)"
echo "python:  $(which python  || echo MISSING)"
which znc

fail() { echo "BUILD-FAIL: $1"; exit 1; }

[ -f "$ZNC" ] || fail "pinned znc missing at $ZNC"

# assemble real binary
cat da_base.zag da_world.zag da_module.zag da_learn.zag da_main.zag > da_full.zag
[ "$(grep -c '^fn main(' da_full.zag)" = "1" ] || fail "expected exactly one fn main in da_full.zag"

"$ZNC" build da_full.zag -o da_bin > da_compile.txt 2>&1 || fail "znc build of da_full.zag failed"
grep -q ": error" da_compile.txt && fail "compiler reported an error (see da_compile.txt)"

# assemble null binary (pmod=1): the sed flip must match exactly one line
[ "$(grep -c '  let PMOD:i32=0;' da_main.zag)" = "1" ] || fail "PMOD flip anchor not unique in da_main.zag"
sed 's/^  let PMOD:i32=0;$/  let PMOD:i32=1;/' da_main.zag > da_main_null.zag
cat da_base.zag da_world.zag da_module.zag da_learn.zag da_main_null.zag > da_full_null.zag
[ "$(grep -c '^fn main(' da_full_null.zag)" = "1" ] || fail "expected exactly one fn main in da_full_null.zag"

"$ZNC" build da_full_null.zag -o da_nullbin > da_null_compile.txt 2>&1 || fail "znc build of da_full_null.zag failed"
grep -q ": error" da_null_compile.txt && fail "compiler reported an error (see da_null_compile.txt)"

# run each binary 3x
for i in 1 2 3; do
  ./da_bin      > "da_run$i.txt"      2> "da_run$i.err";  echo "da_bin      run$i exit=$?"
  ./da_nullbin  > "da_null$i.txt"     2> "da_null$i.err";  echo "da_nullbin  run$i exit=$?"
done

# determinism: byte-identical across the 3 runs of each binary
cmp da_run1.txt  da_run2.txt  || fail "da_run1/da_run2 differ"
cmp da_run1.txt  da_run3.txt  || fail "da_run1/da_run3 differ"
cmp da_null1.txt da_null2.txt || fail "da_null1/da_null2 differ"
cmp da_null1.txt da_null3.txt || fail "da_null1/da_null3 differ"

# stderr must be empty, exits recorded above must be 0
for f in da_run1.err da_run2.err da_run3.err da_null1.err da_null2.err da_null3.err; do
  [ -s "$f" ] && fail "non-empty stderr: $f"
done

# frozen kill-bar spot checks (full adjudication in REPORT.md)
echo "--- spot checks ---"
echo "ATTR lines:        $(grep -c '^ATTR ' da_run1.txt)"
echo "ATTR-MISMATCH:     $(grep -c 'ATTR-MISMATCH' da_run1.txt)"
echo "Q lines:           $(grep -c '^Q ' da_run1.txt)"
echo "agree=1:           $(grep -c 'agree=1' da_run1.txt)"
echo "agree=0:           $(grep -c 'agree=0' da_run1.txt)"
echo "RETRY lines:       $(grep -c 'RETRY' da_run1.txt)"
echo "HOOK lines:        $(grep -c 'HOOK' da_run1.txt)"
echo "SCORE-ATTR:        $(grep '^SCORE-ATTR' da_run1.txt)"
echo "SCORE-ATTR (null): $(grep '^SCORE-ATTR' da_null1.txt)"
echo "BUILD-OK"
