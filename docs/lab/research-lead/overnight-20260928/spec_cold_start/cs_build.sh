#!/bin/bash
# cs_build.sh -- SPEC-COLD-START: build + run + verify.
# Usage: ./cs_build.sh  (run from this directory)
# safebin PATH is mandatory; the pinned znc builds cs_bin; cs_bin runs
# 3x; sha256/cmp equality across the three runs is checked; the frozen
# kill bars from PREREG.md are adjudicated.
export PATH="$HOME/safebin"
set -u
D="$(cd "$(dirname "$0")" && pwd)"
DA="$D/../disagreement_attribution"
RB="$D/../spec_relationblind"
ET="$D/../spec_epochtag"
RR="$D/../spec_refusal_recovery"
LD="$D/../spec_lazy_default"
PARENT="$D/../spec_abstention_trap"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
cd "$D" || exit 1

# K2 toolchain guard record
echo "PATH=$PATH"
echo "python3: $(which python3 || echo MISSING)"
echo "python:  $(which python  || echo MISSING)"
which znc
[ "$(sha256sum "$ZNC" | cut -d' ' -f1)" = "498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef" ] \
  || { echo "BUILD-FAIL: K2 pinned znc sha256 mismatch"; exit 1; }

fail() { echo "BUILD-FAIL: $1"; exit 1; }

[ -f "$ZNC" ] || fail "pinned znc missing at $ZNC"
for f in "$DA/da_base.zag" "$DA/da_module.zag" "$DA/da_learn.zag" \
         "$RB/rb_world.zag" "$RB/rb_fix.zag" \
         "$ET/et_world.zag" "$ET/et_spec.zag" \
         "$RR/rr_spec.zag" "$LD/ld_spec.zag" \
         "$PARENT/at_spec.zag" \
         cs_spec.zag cs_main.zag; do
  [ -f "$f" ] || fail "missing source: $f"
done
# K8 (part): reused sources byte-unmodified (no unstaged diff vs HEAD).
# The 9 grandparent sources plus the parent lane's at_spec.zag, which
# is superseded here by copy-plus-delta (cs_spec.zag), never edited.
for f in "$DA/da_base.zag" "$DA/da_module.zag" "$DA/da_learn.zag" \
         "$RB/rb_world.zag" "$RB/rb_fix.zag" \
         "$ET/et_world.zag" "$ET/et_spec.zag" \
         "$RR/rr_spec.zag" "$LD/ld_spec.zag" \
         "$PARENT/at_spec.zag"; do
  /usr/bin/git diff --quiet -- "$f" || fail "K8: reused source modified: $f"
done
# K8 (part): da_learn.zag explicitly unmodified (separate lane only)
/usr/bin/git diff --quiet -- "$DA/da_learn.zag" || fail "K8: da_learn.zag modified"

# assemble experiment binary: all reused sources byte-unmodified +
# cold-start policy layer + harness main. at_spec.zag is NOT
# assembled (superseded by cs_spec.zag); assembling both would
# duplicate fn definitions.
cat "$DA/da_base.zag" "$RB/rb_world.zag" "$ET/et_world.zag" "$DA/da_module.zag" \
    "$DA/da_learn.zag" "$RB/rb_fix.zag" "$ET/et_spec.zag" "$RR/rr_spec.zag" \
    "$LD/ld_spec.zag" cs_spec.zag cs_main.zag > cs_full.zag
[ "$(grep -c '^fn main(' cs_full.zag)" = "1" ] || fail "expected exactly one fn main in cs_full.zag"
# K8 (part): no world literals in new lane sources
for f in cs_spec.zag cs_main.zag probe.zag; do
  grep -q "901\|902" "$f" && fail "K8: $f contains world literals"
done

"$ZNC" build cs_full.zag -o cs_bin > cs_compile.txt 2>&1 || fail "znc build of cs_full.zag failed"
grep -q ": error" cs_compile.txt && fail "compiler reported an error (see cs_compile.txt)"

# run experiment 3x
for i in 1 2 3; do
  ./cs_bin > "cs_run$i.txt" 2> "cs_run$i.err"; echo "cs_bin run$i exit=$?"
done

# K3 determinism: byte-identical across the 3 runs
cmp cs_run1.txt cs_run2.txt || fail "K3: cs_run1/cs_run2 differ"
cmp cs_run1.txt cs_run3.txt || fail "K3: cs_run1/cs_run3 differ"
sha256sum cs_run1.txt

# K3 stderr must be empty
for f in cs_run1.err cs_run2.err cs_run3.err; do
  [ -s "$f" ] && fail "K3: non-empty stderr: $f"
done

# K3: exactly 40 CELL lines (4 cells x 10 arms)
[ "$(grep -c '^CELL ' cs_run1.txt)" = "40" ] || fail "K3: expected 40 CELL lines"

echo "--- kill bars ---"

field() { # $1=R $2=P-pattern $3=L $4=field -> value
  grep "^CELL R=$1 " cs_run1.txt | grep " P=$2 " | grep " L=$3 " \
    | grep -o " $4=[0-9-]*" | head -1 | cut -d= -f2
}
fixed_field() { field "$1" "$2" "-1" "$3"; }
adapt_field() { field "$1" "adapt" "$2" "$3"; }
guard_field() { field "$1" "guard" "$2" "$3"; }
j_val() { # $1=R $2=P $3=L -> J = rb + rf*L
  rb=$(field "$1" "$2" "$3" rebuilds); rf=$(field "$1" "$2" "$3" refusals)
  echo $(( rb + rf * $3 ))
}
line_nop() { # $1=R $2=P $3=L -> CELL line with the P= field stripped
  grep "^CELL R=$1 " cs_run1.txt | grep " P=$2 " | grep " L=$3 " | sed 's/ P=[a-z]*//'
}

# K4a: per-cell cross-arm (D,Q) identity + fixed-arm structural identities.
for R in 21 60 82 120; do
  dd=$(fixed_field $R lazy D);       qd=$(fixed_field $R lazy Q)
  rd=$(fixed_field $R lazy rebuilds); ad=$(fixed_field $R lazy answered)
  fd=$(fixed_field $R lazy refusals); kd=$(fixed_field $R lazy kb)
  de=$(fixed_field $R eager D);       qe=$(fixed_field $R eager Q)
  re=$(fixed_field $R eager rebuilds); ae=$(fixed_field $R eager answered)
  fe=$(fixed_field $R eager refusals); ke=$(fixed_field $R eager kb)
  if [ "$rd" -gt "$dd" ] || [ "$rd" -gt "$qd" ]; then
    fail "K4a: R=$R lazy rebuilds=$rd > min(D,Q)=($dd,$qd)"
  fi
  { [ "$ad" = "$qd" ] && [ "$fd" = "$rd" ] && [ "$kd" = "$(( qd * 2 ))" ]; } \
    || fail "K4a: R=$R lazy: answered=$ad refusals=$fd kb=$kd (Q=$qd)"
  { [ "$re" = "$de" ] && [ "$ae" = "$qe" ] && [ "$fe" = "0" ] && [ "$ke" = "$(( qe * 2 ))" ]; } \
    || fail "K4a: R=$R eager: rebuilds=$re answered=$ae refusals=$fe kb=$ke (D=$de Q=$qe)"
  { [ "$de" = "$dd" ] && [ "$qe" = "$qd" ]; } \
    || fail "K4a: R=$R eager (D,Q)=($de,$qe) != lazy ($dd,$qd)"
  for L in 0 1 3 7; do
    da=$(adapt_field $R $L D); qa=$(adapt_field $R $L Q)
    dg=$(guard_field $R $L D); qg=$(guard_field $R $L Q)
    { [ "$da" = "$dd" ] && [ "$qa" = "$qd" ] && \
      [ "$dg" = "$dd" ] && [ "$qg" = "$qd" ]; } \
      || fail "K4a: R=$R L=$L adapt/guard (D,Q) != lazy ($dd,$qd)"
  done
done
echo "PASS: K4a fixed arms anchor; cross-arm (D,Q) identical on all 4 cells"

# K4b: arrival splits show the shift (lazy arm).
for R in 60 120; do
  dpre=$(fixed_field $R lazy Dpre); qpre=$(fixed_field $R lazy Qpre)
  dpost=$(fixed_field $R lazy Dpost); qpost=$(fixed_field $R lazy Qpost)
  { [ "$dpost" = "128" ] && [ "$qpost" -lt 32 ] && \
    [ "$dpre" -lt 32 ] && [ "$qpre" -lt 32 ]; } \
    || fail "K4b: R=$R splits=($dpre,$qpre,$dpost,$qpost), want (<32,<32,128,<32)"
done
dpre82=$(fixed_field 82 lazy Dpre); qpre82=$(fixed_field 82 lazy Qpre)
dpost82=$(fixed_field 82 lazy Dpost); qpost82=$(fixed_field 82 lazy Qpost)
{ [ "$qpost82" = "128" ] && [ "$dpost82" -lt 32 ] && \
  [ "$dpre82" -lt 32 ] && [ "$qpre82" -lt 32 ]; } \
  || fail "K4b: R=82 splits=($dpre82,$qpre82,$dpost82,$qpost82), want (<32,<32,<32,128)"
dd21=$(fixed_field 21 lazy D); qd21=$(fixed_field 21 lazy Q)
{ [ "$dd21" -lt 48 ] && [ "$qd21" -lt 48 ]; } \
  || fail "K4b: R=21 sparse stationary (D,Q)=($dd21,$qd21), want <48 each"
echo "PASS: K4b regime splits: CS1/CS3 Dpost=128 pins, CS2 Qpost=128 pin, CS0 sparse"

# K4c: structural accounting on all 32 adapt + guard lines.
for R in 21 60 82 120; do
  rod=$(fixed_field $R lazy rebuilds); rrf=$(fixed_field $R lazy refusals)
  for P in adapt guard; do
    for L in 0 1 3 7; do
      cm=$(field $R $P $L cm); tc=$(field $R $P $L tc)
      flips=$(field $R $P $L flips); pflips=$(field $R $P $L pflips)
      tf1=$(field $R $P $L tf1); fdir=$(field $R $P $L fdir)
      tf2=$(field $R $P $L tf2); rb=$(field $R $P $L rebuilds)
      an=$(field $R $P $L answered); rf=$(field $R $P $L refusals)
      kb=$(field $R $P $L kb); qq=$(field $R $P $L Q)
      od=$(field $R $P $L od); rs=$(field $R $P $L rs)
      dd=$(field $R $P $L D); Dc=$(field $R $P $L Dc)
      Qc=$(field $R $P $L Qc); lc=$(field $R $P $L lc)
      dpre=$(field $R $P $L Dpre); dpost=$(field $R $P $L Dpost)
      qpre=$(field $R $P $L Qpre); qpost=$(field $R $P $L Qpost)
      tag="R=$R P=$P L=$L"
      [ "$lc" = "0" ] || fail "K4c: $tag lc=$lc != 0 (pol 3 dormant in this lane)"
      { [ "$(( dpre + dpost ))" = "$dd" ] && [ "$(( qpre + qpost ))" = "$qq" ]; } \
        || fail "K4c: $tag arrival splits do not sum to (D,Q)"
      { [ "$an" = "$qq" ] && [ "$kb" = "$(( qq * 2 ))" ] && \
        [ "$rb" = "$(( od + rs ))" ] && [ "$rf" = "$od" ]; } \
        || fail "K4c: $tag an/kb/rb/rf identity broken"
      { { [ "$pflips" = "0" ] && [ "$tf1" = "0" ] && [ "$fdir" = "0" ]; } || \
        { [ "$pflips" != "0" ] && [ "$tf1" != "0" ] && [ "$fdir" != "0" ]; }; } \
        || fail "K4c: $tag pflips/tf1/fdir inconsistent ($pflips/$tf1/$fdir)"
      if [ "$pflips" != "0" ]; then
        { [ "$tf1" -gt 128 ] && [ "$tf1" -le 256 ]; } \
          || fail "K4c: $tag post-shift flip tick tf1=$tf1 not in (128,256]"
      fi
      if [ "$tf2" != "0" ]; then
        { [ "$tf2" -ge "$tf1" ] && [ "$tf2" -le 256 ]; } \
          || fail "K4c: $tag tf2=$tf2 inconsistent with tf1=$tf1"
      fi
      [ "$flips" -ge "$pflips" ] || fail "K4c: $tag flips=$flips < pflips=$pflips"
      if [ "$flips" = "0" ]; then
        if [ "$cm" = "0" ] || [ "$cm" = "1" ]; then
          { [ "$od" = "$rod" ] && [ "$rf" = "$rrf" ] && [ "$rs" = "0" ]; } \
            || fail "K4c: $tag cm=$cm not field-equal to lazy twin"
        fi
        if [ "$cm" = "2" ]; then
          exprs=$(( 1 + dd - Dc ))
          [ "$rs" = "$exprs" ] \
            || fail "K4c: $tag cm=2 rs=$rs != 1+(D-Dc)=$exprs"
          { [ "$od" -le "$Dc" ] && [ "$od" -le "$Qc" ]; } \
            || fail "K4c: $tag cm=2 od=$od > min(Dc,Qc)=($Dc,$Qc)"
        fi
      fi
    done
  done
done
echo "PASS: K4c structural accounting on all 32 adapt+guard lines; lc=0 everywhere"

# K5: quirk characterization. On D32==0 cells, adapt L>=1 must show
# the exact disclosed degenerate commit; L=0 never eager anywhere.
echo "K5 FINDING quirk commits (adapt):"
for R in 21 60 82; do
  for L in 1 3 7; do
    tc=$(adapt_field $R $L tc); cm=$(adapt_field $R $L cm)
    sel=$(adapt_field $R $L sel); Dc=$(adapt_field $R $L Dc)
    dh=$(adapt_field $R $L dh); dlo=$(adapt_field $R $L dlo)
    dhi=$(adapt_field $R $L dhi); pnum=$(adapt_field $R $L pnum)
    phin=$(adapt_field $R $L phin); phid=$(adapt_field $R $L phid)
    echo "  R=$R L=$L: tc=$tc cm=$cm sel=$sel Dc=$Dc dh=$dh dlo=$dlo dhi=$dhi pnum=$pnum phin=$phin phid=$phid"
    { [ "$tc" = "32" ] && [ "$cm" = "2" ] && [ "$sel" = "1" ] && \
      [ "$Dc" = "0" ] && [ "$dh" = "0" ] && [ "$dlo" = "0" ] && \
      [ "$dhi" = "0" ] && [ "$pnum" = "0" ] && [ "$phin" = "0" ] && \
      [ "$phid" -ge 1 ]; } \
      || fail "K5: R=$R adapt L=$L not the disclosed zero-data eager commit"
  done
done
for R in 21 60 82 120; do
  s0=$(adapt_field $R 0 sel); c0=$(adapt_field $R 0 cm)
  { [ "$s0" = "0" ] && [ "$c0" != "2" ]; } \
    || fail "K5: R=$R adapt L=0 sel=$s0 cm=$c0 (eager at L=0)"
done
echo "PASS: K5 quirk fires exactly as disclosed on all D32==0 cells; L=0 never eager"

# K6a: guard blocks every degenerate eager commit.
for R in 21 60 82; do
  for L in 1 3 7; do
    cm=$(guard_field $R $L cm); tc=$(guard_field $R $L tc)
    Dc=$(guard_field $R $L Dc); sel=$(guard_field $R $L sel)
    echo "  guard R=$R L=$L: tc=$tc cm=$cm sel=$sel Dc=$Dc"
    { [ "$cm" != "2" ] || [ "$tc" != "32" ]; } \
      || fail "K6a: R=$R guard L=$L eager commit at tc=32 (degenerate commit not blocked)"
    if [ "$cm" = "2" ]; then
      [ "$Dc" -ge 1 ] || fail "K6a: R=$R guard L=$L cm=2 with Dc=0 (zero-data eager commit)"
    fi
  done
done
echo "PASS: K6a guard blocks every degenerate eager commit; all guard eager commits have Dc>=1"

# K6b: L=0 guard field-equal adapt (guard never binds at L=0).
for R in 21 60 82 120; do
  [ "$(line_nop $R adapt 0)" = "$(line_nop $R guard 0)" ] \
    || fail "K6b: R=$R L=0 guard not field-equal to adapt"
done
echo "PASS: K6b L=0 guard field-equal adapt on all 4 cells"

# K6c: CS3 (D32>=1) guard field-equal adapt at every L.
for L in 0 1 3 7; do
  [ "$(line_nop 120 adapt $L)" = "$(line_nop 120 guard $L)" ] \
    || fail "K6c: R=120 L=$L guard not field-equal to adapt (guard fired where data exists)"
done
echo "PASS: K6c CS3 guard field-equal adapt (guard is a pure degenerate-case intervention)"

# K7a: harm mechanism -- CS1 adapt's zero-data eager commit was
# wrong-direction: rescued by the flip rule (flips>=1, ends lazy).
echo "K7a FINDING CS1 adapt flips/sel:"
for L in 1 3 7; do
  fl=$(adapt_field 60 $L flips); sel=$(adapt_field 60 $L sel)
  tf1=$(adapt_field 60 $L tf1); fdir=$(adapt_field 60 $L fdir)
  echo "  R=60 L=$L: flips=$fl sel=$sel tf1=$tf1 fdir=$fdir"
  { [ "$fl" -ge 1 ] && [ "$sel" = "0" ]; } \
    || fail "K7a: R=60 adapt L=$L flips=$fl sel=$sel (zero-data commit not wrong-direction)"
done
echo "PASS: K7a CS1 zero-data eager commits were wrong-direction, rescued by flips"

# K7b/c/d: economics. J = rb + rf*L.
ja60=$(j_val 60 adapt 1); jg60=$(j_val 60 guard 1)
echo "K7b R=60 L=1: J_adapt=$ja60 J_guard=$jg60"
[ "$jg60" -lt "$ja60" ] || fail "K7b: R=60 L=1 J_guard=$jg60 not < J_adapt=$ja60 (no measured harm)"
echo "PASS: K7b measured harm of the quirk on the lazy-optimal cell"
ja82=$(j_val 82 adapt 1); jg82=$(j_val 82 guard 1)
echo "K7c R=82 L=1: J_adapt=$ja82 J_guard=$jg82"
[ "$ja82" -lt "$jg82" ] || fail "K7c: R=82 L=1 J_adapt=$ja82 not < J_guard=$jg82 (no measured benefit)"
echo "PASS: K7c quirk's early eager commit wins where the world is eager-optimal"
for L in 3 7; do
  ja21=$(j_val 21 adapt $L); jg21=$(j_val 21 guard $L)
  echo "K7d R=21 L=$L: J_adapt=$ja21 J_guard=$jg21"
  [ "$ja21" -lt "$jg21" ] || fail "K7d: R=21 L=$L J_adapt=$ja21 not < J_guard=$jg21"
done
echo "PASS: K7d zero-data eager is the cheaper default under genuine sparsity"

# K8 hygiene: ASCII-only lane sources
if LC_ALL=C grep -l '[^[:print:][:space:]]' PREREG.md NAMECHECK.md cs_spec.zag cs_main.zag cs_build.sh probe.zag 2>/dev/null; then
  fail "K8: non-ASCII byte found"
fi
echo "PASS: K8 ASCII-only, no world literals, one fn main per binary, reused sources unmodified, da_learn.zag untouched"

echo "ALL KILL BARS PASS"
