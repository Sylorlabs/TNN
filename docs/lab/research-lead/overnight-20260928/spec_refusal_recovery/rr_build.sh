#!/bin/bash
# rr_build.sh -- SPEC-REFUSAL-RECOVERY: build + run + verify.
# Usage: ./rr_build.sh  (run from this directory)
# safebin PATH is mandatory; the pinned znc builds rr_bin; the binary
# runs 3x; sha256/cmp equality across the three runs is checked; the
# frozen kill bars from PREREG.md are adjudicated.
export PATH="$HOME/safebin"
set -u
D="$(cd "$(dirname "$0")" && pwd)"
DA="$D/../disagreement_attribution"
RB="$D/../spec_relationblind"
ET="$D/../spec_epochtag"
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
[ -f "$ET/et_world.zag" ] || fail "et_world.zag missing in $ET"
[ -f "$ET/et_spec.zag" ] || fail "et_spec.zag missing in $ET"

# assemble: real da_base + relationblind world + epochtag epoch machinery +
# real da_module + real da_learn (NOT modified) + relationblind fix variants
# + epochtag epoch specs (all unmodified) + lane recovery wrappers + lane
# harness main.
cat "$DA/da_base.zag" "$RB/rb_world.zag" "$ET/et_world.zag" "$DA/da_module.zag" "$DA/da_learn.zag" "$RB/rb_fix.zag" "$ET/et_spec.zag" rr_spec.zag rr_main.zag > rr_full.zag
[ "$(grep -c '^fn main(' rr_full.zag)" = "1" ] || fail "expected exactly one fn main in rr_full.zag"
grep -q "901\|902" rr_spec.zag && fail "rr_spec.zag contains world literals"
grep -q "901\|902" rr_main.zag && fail "rr_main.zag contains world literals"

"$ZNC" build rr_full.zag -o rr_bin > rr_compile.txt 2>&1 || fail "znc build of rr_full.zag failed"
grep -q ": error" rr_compile.txt && fail "compiler reported an error (see rr_compile.txt)"

# run 3x
for i in 1 2 3; do
  ./rr_bin > "rr_run$i.txt" 2> "rr_run$i.err"; echo "rr_bin run$i exit=$?"
done

# K10 determinism: byte-identical across the 3 runs
cmp rr_run1.txt rr_run2.txt || fail "K10: rr_run1/rr_run2 differ"
cmp rr_run1.txt rr_run3.txt || fail "K10: rr_run1/rr_run3 differ"

# K3 stderr must be empty (exits printed above must be 0)
for f in rr_run1.err rr_run2.err rr_run3.err; do
  [ -s "$f" ] && fail "K3: non-empty stderr: $f"
done

echo "--- output ---"
cat rr_run1.txt
echo "--- kill bars ---"

field_of() { grep "^$1 " rr_run1.txt | grep -o "$2=[0-9]*" | head -1; }
chk() { # $1 = line label, $2 = field, $3 = expected value
  local got
  got="$(field_of "$1" "$2")"
  [ "$got" = "$2=$3" ] || fail "bar: $1 expected $2=$3, got [$got]"
  echo "PASS: $1 $2=$3"
}
chk_gt() { # $1 = line label, $2 = field, $3 = strict lower bound
  local got val
  got="$(field_of "$1" "$2")"
  val="${got#$2=}"
  [ -n "$val" ] && [ "$val" -gt "$3" ] || fail "bar: $1 expected $2>$3, got [$got]"
  echo "PASS: $1 $2=$val > $3"
}
chk_eq2() { # $1/$2 = line labels, $3 = field: equal values
  local a b
  a="$(field_of "$1" "$3")"; b="$(field_of "$2" "$3")"
  [ "$a" = "$b" ] || fail "bar: $3 mismatch: $1=[$a] $2=[$b]"
  echo "PASS: $1 $2 share $3=[$a]"
}

# K4 E1 recovery restores correctness (answers unchanged by unrelated drift)
chk E1RET_RR spec 1; chk E1RET_RR gen 1; chk E1RET_RR agree 1
chk E1RET_RR refuse 1; chk E1RET_RR resp 1
chk E1CNT_RR spec 1; chk E1CNT_RR gen 1; chk E1CNT_RR agree 1
chk E1CNT_RR refuse 1; chk E1CNT_RR resp 1
chk E1VFY_RR spec 1; chk E1VFY_RR gen 1; chk E1VFY_RR agree 1
chk E1VFY_RR refuse 1; chk E1VFY_RR resp 1

# K5 E2 recovery restores agreement after answer-changing drift
# (correctness = agree with gen, NOT spec=1)
chk E2RET_RR spec 0; chk E2RET_RR gen 0; chk E2RET_RR agree 1
chk E2RET_RR refuse 1; chk E2RET_RR resp 1; chk_gt E2RET_RR kbs 0
chk E2CNT_RR spec 0; chk E2CNT_RR gen 0; chk E2CNT_RR agree 1
chk E2CNT_RR refuse 1; chk E2CNT_RR resp 1; chk_gt E2CNT_RR kbs 0
chk E2VFY_RR spec 0; chk E2VFY_RR gen 0; chk E2VFY_RR agree 1
chk E2VFY_RR refuse 1; chk E2VFY_RR resp 1; chk_gt E2VFY_RR kbs 0

# K6 decision rule: silent miss with matching epoch triggers NO recovery
chk E0MISS_ET spec 0; chk E0MISS_ET refuse 0
chk E0MISS_RR spec 0; chk E0MISS_RR refuse 0; chk E0MISS_RR resp 0
chk_eq2 E0MISS_ET E0MISS_RR kbs

# K7 repeatability: E3 refuses again after E2's restamp, then recovers again
# (per A1: E3's rebuilt 901 buckets are legitimately empty, so the real-work
# evidence here is resp=1 + agree=1, not kbs>0)
chk E3RET_ET spec 0; chk E3RET_ET refuse 1; chk E3RET_ET kbs 0
chk E3RET_RR spec 0; chk E3RET_RR gen 0; chk E3RET_RR agree 1
chk E3RET_RR refuse 1; chk E3RET_RR resp 1
chk E3CNT_RR spec 0; chk E3CNT_RR gen 0; chk E3CNT_RR agree 1
chk E3CNT_RR refuse 1; chk E3CNT_RR resp 1
chk E3VFY_RR spec 0; chk E3VFY_RR gen 0; chk E3VFY_RR agree 1
chk E3VFY_RR refuse 1; chk E3VFY_RR resp 1

# K8 one-time cost: post-recovery calls hit with no new refuse / re-specialize
chk E1RET_RR2 spec 1; chk E1RET_RR2 agree 1
chk E1RET_RR2 refuse 0; chk E1RET_RR2 resp 0
chk E2RET_RR2 spec 0; chk E2RET_RR2 agree 1
chk E2RET_RR2 refuse 0; chk E2RET_RR2 resp 0

# K9 recovery does real work: retry scans the bucket, refuse-only does not.
# (As amended by A1: kbs>0 applies to the non-empty-bucket E1/E2 lines;
# E3's rebuilt 901 buckets are legitimately empty, covered by K7 resp/agree.)
chk_gt E1RET_RR kbs 0; chk_gt E1CNT_RR kbs 0; chk_gt E1VFY_RR kbs 0
chk_gt E2RET_RR kbs 0; chk_gt E2CNT_RR kbs 0; chk_gt E2VFY_RR kbs 0
chk E1RET_ET spec 0; chk E1RET_ET refuse 1; chk E1RET_ET kbs 0
chk E2RET_ET spec 0; chk E2RET_ET refuse 1; chk E2RET_ET kbs 0
chk E3RET_ET spec 0; chk E3RET_ET refuse 1; chk E3RET_ET kbs 0

# K11 hygiene: no non-ASCII bytes (covers em/en dashes) in lane sources
if LC_ALL=C grep -l '[^[:print:][:space:]]' PREREG.md NAMECHECK.md rr_spec.zag rr_main.zag rr_build.sh 2>/dev/null; then
  fail "K11: non-ASCII byte found"
fi
echo "PASS: K11 ASCII-only, no world literals in rr_spec.zag/rr_main.zag, one fn main"

echo "ALL KILL BARS PASS"
