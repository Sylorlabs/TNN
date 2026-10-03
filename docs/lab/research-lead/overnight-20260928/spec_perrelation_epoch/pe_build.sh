#!/bin/bash
# pe_build.sh -- SPEC-PERRELATION-EPOCH: build + run + verify.
# Usage: ./pe_build.sh  (run from this directory)
# safebin PATH is mandatory; the pinned znc builds pe_bin; the binary
# runs 3x; sha256/cmp equality across the three runs is checked; the
# frozen kill bars from PREREG.md are adjudicated.
export PATH="$HOME/safebin"
set -u
D="$(cd "$(dirname "$0")" && pwd)"
DA="$D/../disagreement_attribution"
RB="$D/../spec_relationblind"
ET="$D/../spec_epochtag"
RR="$D/../spec_refusal_recovery"
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
[ -f "$RR/rr_spec.zag" ] || fail "rr_spec.zag missing in $RR"

# assemble: real da_base + relationblind world + epochtag epoch machinery +
# real da_module + real da_learn (NOT modified) + relationblind fix variants
# + epochtag epoch specs + refusal-recovery wrappers (all unmodified) +
# lane per-relation epoch table/drifts + lane per-relation specs +
# lane per-relation recovery wrappers + lane harness main.
cat "$DA/da_base.zag" "$RB/rb_world.zag" "$ET/et_world.zag" "$DA/da_module.zag" "$DA/da_learn.zag" "$RB/rb_fix.zag" "$ET/et_spec.zag" "$RR/rr_spec.zag" pe_world.zag pe_spec.zag pe_rr.zag pe_main.zag > pe_full.zag
[ "$(grep -c '^fn main(' pe_full.zag)" = "1" ] || fail "expected exactly one fn main in pe_full.zag"
grep -q "901\|902" pe_world.zag && fail "pe_world.zag contains world literals"
grep -q "901\|902" pe_spec.zag && fail "pe_spec.zag contains world literals"
grep -q "901\|902" pe_rr.zag && fail "pe_rr.zag contains world literals"
grep -q "901\|902" pe_main.zag && fail "pe_main.zag contains world literals"

"$ZNC" build pe_full.zag -o pe_bin > pe_compile.txt 2>&1 || fail "znc build of pe_full.zag failed"
grep -q ": error" pe_compile.txt && fail "compiler reported an error (see pe_compile.txt)"

# run 3x
for i in 1 2 3; do
  ./pe_bin > "pe_run$i.txt" 2> "pe_run$i.err"; echo "pe_bin run$i exit=$?"
done

# K11 determinism: byte-identical across the 3 runs
cmp pe_run1.txt pe_run2.txt || fail "K11: pe_run1/pe_run2 differ"
cmp pe_run1.txt pe_run3.txt || fail "K11: pe_run1/pe_run3 differ"

# K3 stderr must be empty (exits printed above must be 0)
for f in pe_run1.err pe_run2.err pe_run3.err; do
  [ -s "$f" ] && fail "K3: non-empty stderr: $f"
done

echo "--- output ---"
cat pe_run1.txt
echo "--- kill bars ---"

field_of() { grep "^$1 " pe_run1.txt | grep -o "$2=[0-9]*" | head -1; }
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

# K9 healthy-world parity: per-relation tagging changes nothing on E0
chk E0RET_ETC spec 1; chk E0RET_ETC refuse 0
chk E0RET_PERR spec 1; chk E0RET_PERR gen 1; chk E0RET_PERR agree 1
chk E0RET_PERR refuse 0; chk E0RET_PERR resp 0
chk_eq2 E0RET_ETC E0RET_PERR kbs
chk E0CNT_PERR spec 1; chk E0CNT_PERR gen 1; chk E0CNT_PERR agree 1
chk E0CNT_PERR refuse 0; chk E0CNT_PERR resp 0
chk E0VFY_PERR spec 1; chk E0VFY_PERR gen 1; chk E0VFY_PERR agree 1
chk E0VFY_PERR refuse 0; chk E0VFY_PERR resp 0

# K8 decision rule: silent miss with matching relation epoch -> no recovery
chk E0MISS_PEET spec 0; chk E0MISS_PEET refuse 0
chk E0MISS_PERR spec 0; chk E0MISS_PERR refuse 0; chk E0MISS_PERR resp 0
chk_eq2 E0MISS_PEET E0MISS_PERR kbs

# K4 E1: coarse scheme prices the rebuild; per-relation scheme pays none
chk E1RET_ETC spec 0; chk E1RET_ETC refuse 1; chk E1RET_ETC kbs 0
chk E1RET_RRC spec 1; chk E1RET_RRC gen 1; chk E1RET_RRC agree 1
chk E1RET_RRC refuse 1; chk E1RET_RRC resp 1
chk E1RET_PEET spec 1; chk E1RET_PEET refuse 0
chk E1RET_PERR spec 1; chk E1RET_PERR gen 1; chk E1RET_PERR agree 1
chk E1RET_PERR refuse 0; chk E1RET_PERR resp 0
chk E1CNT_PERR spec 1; chk E1CNT_PERR gen 1; chk E1CNT_PERR agree 1
chk E1CNT_PERR refuse 0; chk E1CNT_PERR resp 0
chk E1VFY_PERR spec 1; chk E1VFY_PERR gen 1; chk E1VFY_PERR agree 1
chk E1VFY_PERR refuse 0; chk E1VFY_PERR resp 0

# K5 gate not degenerate: the drifted relation still refuses and recovers
chk E1B_PEET spec 0; chk E1B_PEET refuse 1; chk E1B_PEET kbs 0
chk E1B_PERR spec 0; chk E1B_PERR gen 0; chk E1B_PERR agree 1
chk E1B_PERR refuse 1; chk E1B_PERR resp 1; chk_gt E1B_PERR kbs 0

# K10 epoch table: exactly the touched relations, right epochs
chk EPOCHS_E1 era 0; chk EPOCHS_E1 erb 1; chk EPOCHS_E1 n 1
chk EPOCHS_E2 era 1; chk EPOCHS_E2 erb 2; chk EPOCHS_E2 n 2
chk EPOCHS_E3 era 2; chk EPOCHS_E3 erb 3; chk EPOCHS_E3 n 2

# K6 E2: answer-changing drift on the queried relation refuses + recovers
chk E2RET_PEET spec 0; chk E2RET_PEET refuse 1; chk E2RET_PEET kbs 0
chk E2RET_PERR spec 0; chk E2RET_PERR gen 0; chk E2RET_PERR agree 1
chk E2RET_PERR refuse 1; chk E2RET_PERR resp 1; chk_gt E2RET_PERR kbs 0
chk E2CNT_PERR spec 0; chk E2CNT_PERR gen 0; chk E2CNT_PERR agree 1
chk E2CNT_PERR refuse 1; chk E2CNT_PERR resp 1; chk_gt E2CNT_PERR kbs 0
chk E2VFY_PERR spec 0; chk E2VFY_PERR gen 0; chk E2VFY_PERR agree 1
chk E2VFY_PERR refuse 1; chk E2VFY_PERR resp 1; chk_gt E2VFY_PERR kbs 0

# K7 repeatability + one-time cost; E3 refuses again and recovers again
chk E2RET_PERR2 spec 0; chk E2RET_PERR2 agree 1
chk E2RET_PERR2 refuse 0; chk E2RET_PERR2 resp 0
chk E3RET_PEET spec 0; chk E3RET_PEET refuse 1; chk E3RET_PEET kbs 0
chk E3RET_PERR spec 0; chk E3RET_PERR gen 0; chk E3RET_PERR agree 1
chk E3RET_PERR refuse 1; chk E3RET_PERR resp 1
chk E3CNT_PERR spec 0; chk E3CNT_PERR gen 0; chk E3CNT_PERR agree 1
chk E3CNT_PERR refuse 1; chk E3CNT_PERR resp 1
chk E3VFY_PERR spec 0; chk E3VFY_PERR gen 0; chk E3VFY_PERR agree 1
chk E3VFY_PERR refuse 1; chk E3VFY_PERR resp 1

# K12 hygiene: no non-ASCII bytes (covers em/en dashes) in lane sources
if LC_ALL=C grep -l '[^[:print:][:space:]]' PREREG.md NAMECHECK.md pe_world.zag pe_spec.zag pe_rr.zag pe_main.zag pe_build.sh 2>/dev/null; then
  fail "K12: non-ASCII byte found"
fi
echo "PASS: K12 ASCII-only, no world literals in pe_*.zag, one fn main"

echo "ALL KILL BARS PASS"
