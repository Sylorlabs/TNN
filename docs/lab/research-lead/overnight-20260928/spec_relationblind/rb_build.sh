#!/bin/bash
# rb_build.sh -- SPEC-RELATIONBLIND minimal repro: build + run + verify.
# Usage: ./rb_build.sh  (run from this directory)
# safebin PATH is mandatory; the pinned znc builds rb_bin; the binary
# runs 3x; sha256/cmp equality across the three runs is checked; the
# frozen kill bars from PREREG.md are adjudicated.
export PATH="$HOME/safebin"
set -u
D="$(cd "$(dirname "$0")" && pwd)"
DA="$D/../disagreement_attribution"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
cd "$D" || exit 1

# K2 toolchain guard record
echo "PATH=$PATH"
echo "python3: $(which python3 || echo MISSING)"
echo "python:  $(which python  || echo MISSING)"
which znc

fail() { echo "BUILD-FAIL: $1"; exit 1; }

[ -f "$ZNC" ] || fail "pinned znc missing at $ZNC"
[ -f "$DA/da_base.zag" ] || fail "da_base.zag missing in $DA"

# assemble: real da_base + lane world + real da_module + real da_learn
# + lane fix variants + lane harness main
cat "$DA/da_base.zag" rb_world.zag "$DA/da_module.zag" "$DA/da_learn.zag" rb_fix.zag rb_main.zag > rb_full.zag
[ "$(grep -c '^fn main(' rb_full.zag)" = "1" ] || fail "expected exactly one fn main in rb_full.zag"
grep -q "901\|902" rb_fix.zag && fail "rb_fix.zag contains world literals"

"$ZNC" build rb_full.zag -o rb_bin > rb_compile.txt 2>&1 || fail "znc build of rb_full.zag failed"
grep -q ": error" rb_compile.txt && fail "compiler reported an error (see rb_compile.txt)"

# run 3x
for i in 1 2 3; do
  ./rb_bin > "rb_run$i.txt" 2> "rb_run$i.err"; echo "rb_bin run$i exit=$?"
done

# K7 determinism: byte-identical across the 3 runs
cmp rb_run1.txt rb_run2.txt || fail "K7: rb_run1/rb_run2 differ"
cmp rb_run1.txt rb_run3.txt || fail "K7: rb_run1/rb_run3 differ"

# K3 stderr must be empty (exits printed above must be 0)
for f in rb_run1.err rb_run2.err rb_run3.err; do
  [ -s "$f" ] && fail "K3: non-empty stderr: $f"
done

echo "--- output ---"
cat rb_run1.txt
echo "--- kill bars ---"

agree_of() { grep "^$1 " rb_run1.txt | grep -o 'agree=[01]' | head -1; }
kbs_of()   { grep "^$1 " rb_run1.txt | grep -o 'kbs=[0-9]*' | head -1; }
chk() { # $1 = line label, $2 = expected agree value
  local got
  got="$(agree_of "$1")"
  [ "$got" = "agree=$2" ] || fail "agree bar: $1 expected agree=$2, got [$got]"
  echo "PASS: $1 agree=$2"
}

# K4 control: all agree pre-drift
chk D0RET 1; chk D0CNT 1; chk D0VFY 1
# K5 core repro: ret/cnt diverge on relation-only drift, vfy immune
chk D1RET 0; chk D1CNT 0; chk D1VFY 1
# K6 fix: variants restore agreement; t14 analog diverges unfixed, agrees fixed
chk D2RETFIX 1; chk D2CNTFIX 1
chk D3RET 0; chk D3CNT 0; chk D3RETFIX 1; chk D3CNTFIX 1

# K8 cost: identical kb iteration counts between spec and fix variants
[ "$(kbs_of D1RET)" = "$(kbs_of D2RETFIX)" ] || fail "K8: ret kb mismatch"
[ "$(kbs_of D1CNT)" = "$(kbs_of D2CNTFIX)" ] || fail "K8: cnt kb mismatch"
echo "PASS: K8 kb counts identical ($(kbs_of D1RET) / $(kbs_of D1CNT))"

# Post-freeze diagnostic (not a frozen kill bar): fix variants must match
# the originals exactly on the pristine world (rules out degenerate
# always-zero transcription of the fix).
chk D0RETFIX 1; chk D0CNTFIX 1
[ "$(grep '^D0RETFIX ' rb_run1.txt | grep -o 'spec=[0-9]*')" = "$(grep '^D0RET ' rb_run1.txt | grep -o 'spec=[0-9]*')" ] || fail "diagnostic: D0RETFIX spec != D0RET spec"
[ "$(grep '^D0CNTFIX ' rb_run1.txt | grep -o 'spec=[0-9]*')" = "$(grep '^D0CNT ' rb_run1.txt | grep -o 'spec=[0-9]*')" ] || fail "diagnostic: D0CNTFIX spec != D0CNT spec"
echo "PASS: diagnostic fix==original on pristine world"

# K9 hygiene: no non-ASCII bytes (covers em/en dashes) in lane sources
if LC_ALL=C grep -l '[^[:print:][:space:]]' PREREG.md NAMECHECK.md rb_world.zag rb_fix.zag rb_main.zag rb_build.sh 2>/dev/null; then
  fail "K9: non-ASCII byte found"
fi
echo "PASS: K9 ASCII-only, no world literals in rb_fix.zag, one fn main"

echo "ALL KILL BARS PASS"
