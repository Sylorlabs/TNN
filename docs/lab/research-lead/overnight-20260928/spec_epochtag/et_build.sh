#!/bin/bash
# et_build.sh -- SPEC-EPOCHTAG: build + run + verify.
# Usage: ./et_build.sh  (run from this directory)
# safebin PATH is mandatory; the pinned znc builds et_bin; the binary
# runs 3x; sha256/cmp equality across the three runs is checked; the
# frozen kill bars from PREREG.md are adjudicated.
export PATH="$HOME/safebin"
set -u
D="$(cd "$(dirname "$0")" && pwd)"
DA="$D/../disagreement_attribution"
RB="$D/../spec_relationblind"
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
[ -f "$RB/rb_world.zag" ] || fail "rb_world.zag missing in $RB"
[ -f "$RB/rb_fix.zag" ] || fail "rb_fix.zag missing in $RB"

# assemble: real da_base + relationblind world + lane epoch/world +
# real da_module + real da_learn + relationblind fix variants (unmodified)
# + lane epoch specs + lane harness main. da_learn.zag is NOT modified.
cat "$DA/da_base.zag" "$RB/rb_world.zag" et_world.zag "$DA/da_module.zag" "$DA/da_learn.zag" "$RB/rb_fix.zag" et_spec.zag et_main.zag > et_full.zag
[ "$(grep -c '^fn main(' et_full.zag)" = "1" ] || fail "expected exactly one fn main in et_full.zag"
grep -q "901\|902" et_spec.zag && fail "et_spec.zag contains world literals"
grep -q "901\|902" et_main.zag && fail "et_main.zag contains world literals"

"$ZNC" build et_full.zag -o et_bin > et_compile.txt 2>&1 || fail "znc build of et_full.zag failed"
grep -q ": error" et_compile.txt && fail "compiler reported an error (see et_compile.txt)"

# run 3x
for i in 1 2 3; do
  ./et_bin > "et_run$i.txt" 2> "et_run$i.err"; echo "et_bin run$i exit=$?"
done

# K7 determinism: byte-identical across the 3 runs
cmp et_run1.txt et_run2.txt || fail "K7: et_run1/et_run2 differ"
cmp et_run1.txt et_run3.txt || fail "K7: et_run1/et_run3 differ"

# K3 stderr must be empty (exits printed above must be 0)
for f in et_run1.err et_run2.err et_run3.err; do
  [ -s "$f" ] && fail "K3: non-empty stderr: $f"
done

echo "--- output ---"
cat et_run1.txt
echo "--- kill bars ---"

agree_of()  { grep "^$1 " et_run1.txt | grep -o 'agree=[01]' | head -1; }
spec_of()   { grep "^$1 " et_run1.txt | grep -o 'spec=[0-9]*' | head -1; }
kbs_of()    { grep "^$1 " et_run1.txt | grep -o 'kbs=[0-9]*' | head -1; }
refuse_of() { grep "^$1 " et_run1.txt | grep -o 'refuse=[01]' | head -1; }
chk() { # $1 = line label, $2 = field, $3 = expected value
  local got
  case "$2" in
    agree)  got="$(agree_of "$1")" ;;
    spec)   got="$(spec_of "$1")" ;;
    kbs)    got="$(kbs_of "$1")" ;;
    refuse) got="$(refuse_of "$1")" ;;
  esac
  [ "$got" = "$2=$3" ] || fail "bar: $1 expected $2=$3, got [$got]"
  echo "PASS: $1 $2=$3"
}

# K4 control: et behaves exactly like the originals on the pristine world
chk E0RET agree 1; chk E0CNT agree 1; chk E0VFY agree 1
chk E0RET_ET spec 1; chk E0RET_ET agree 1; chk E0RET_ET refuse 0
chk E0CNT_ET spec 1; chk E0CNT_ET agree 1; chk E0CNT_ET refuse 0
chk E0VFY_ET spec 1; chk E0VFY_ET agree 1; chk E0VFY_ET refuse 0

# K5 relation drift: phantom in originals, silent miss in fix, REFUSE in et
chk E2RET spec 1; chk E2RET agree 0
chk E2RET_FIX spec 0; chk E2RET_FIX agree 1
chk E2RET_ET spec 0; chk E2RET_ET refuse 1; chk E2RET_ET kbs 0
chk E2CNT spec 1; chk E2CNT agree 0
chk E2CNT_FIX spec 0; chk E2CNT_FIX agree 1
chk E2CNT_ET spec 0; chk E2CNT_ET refuse 1; chk E2CNT_ET kbs 0
chk E2VFY agree 1
chk E2VFY_ET spec 0; chk E2VFY_ET refuse 1

# K6 deletion drift (t14 analog): diverge in originals, silent in fix, REFUSE in et
chk E3RET spec 1; chk E3RET agree 0
chk E3RET_FIX spec 0; chk E3RET_FIX agree 1
chk E3RET_ET spec 0; chk E3RET_ET refuse 1; chk E3RET_ET kbs 0
chk E3CNT spec 1; chk E3CNT agree 0
chk E3CNT_FIX spec 0; chk E3CNT_FIX agree 1
chk E3CNT_ET spec 0; chk E3CNT_ET refuse 1; chk E3CNT_ET kbs 0
chk E3VFY_ET spec 0; chk E3VFY_ET refuse 1

# K8 cost: identical kb iteration counts between original spec and et spec on E0
[ "$(kbs_of E0RET)" = "$(kbs_of E0RET_ET)" ] || fail "K8: ret kb mismatch"
[ "$(kbs_of E0CNT)" = "$(kbs_of E0CNT_ET)" ] || fail "K8: cnt kb mismatch"
echo "PASS: K8 kb counts identical ($(kbs_of E0RET) / $(kbs_of E0CNT)); epoch check is 2 get32 + 1 compare per call (source inspection)"

# K10 conservative cost: unrelated drift leaves fix correct, et refuses
chk E1RET agree 1
chk E1RET_FIX spec 1; chk E1RET_FIX agree 1
chk E1RET_ET spec 0; chk E1RET_ET refuse 1
chk E1CNT agree 1
chk E1CNT_FIX spec 1; chk E1CNT_FIX agree 1
chk E1CNT_ET spec 0; chk E1CNT_ET refuse 1

# K9 hygiene: no non-ASCII bytes (covers em/en dashes) in lane sources
if LC_ALL=C grep -l '[^[:print:][:space:]]' PREREG.md NAMECHECK.md et_world.zag et_spec.zag et_main.zag et_build.sh 2>/dev/null; then
  fail "K9: non-ASCII byte found"
fi
echo "PASS: K9 ASCII-only, no world literals in et_spec.zag/et_main.zag, one fn main"

echo "ALL KILL BARS PASS"
