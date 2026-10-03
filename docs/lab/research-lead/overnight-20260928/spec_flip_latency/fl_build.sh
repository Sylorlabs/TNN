#!/bin/bash
# fl_build.sh -- SPEC-FLIP-LATENCY: build + run + verify.
# Usage: ./fl_build.sh  (run from this directory)
# safebin PATH is mandatory; the pinned znc builds fl_bin; fl_bin runs
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
PCS="$D/../spec_cold_start"
PCSRUN="$PCS/cs_run1.txt"
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
         fl_spec.zag fl_main.zag; do
  [ -f "$f" ] || fail "missing source: $f"
done
# K10 (part): reused sources byte-unmodified (no unstaged diff vs HEAD).
# The 9 grandparent sources; the cold-start lane's cs_spec.zag is
# superseded here by copy-plus-delta (fl_spec.zag), never edited.
for f in "$DA/da_base.zag" "$DA/da_module.zag" "$DA/da_learn.zag" \
         "$RB/rb_world.zag" "$RB/rb_fix.zag" \
         "$ET/et_world.zag" "$ET/et_spec.zag" \
         "$RR/rr_spec.zag" "$LD/ld_spec.zag"; do
  /usr/bin/git diff --quiet -- "$f" || fail "K10: reused source modified: $f"
done
# K10 (part): da_learn.zag explicitly unmodified (separate lane only)
/usr/bin/git diff --quiet -- "$DA/da_learn.zag" || fail "K10: da_learn.zag modified"
# K5a needs the parent's frozen run intact
[ "$(sha256sum "$PCSRUN" | cut -d' ' -f1)" = "59e04ecd5e0a33fddc1a8daed2f879098150b74b1683aabea98f1af6fdd01c6d" ] \
  || fail "K5a: parent frozen run sha256 mismatch"

# assemble experiment binary: all reused sources byte-unmodified +
# flip-latency policy layer + harness main. cs_spec.zag is NOT
# assembled (superseded by fl_spec.zag); assembling both would
# duplicate fn definitions.
cat "$DA/da_base.zag" "$RB/rb_world.zag" "$ET/et_world.zag" "$DA/da_module.zag" \
    "$DA/da_learn.zag" "$RB/rb_fix.zag" "$ET/et_spec.zag" "$RR/rr_spec.zag" \
    "$LD/ld_spec.zag" fl_spec.zag fl_main.zag > fl_full.zag
[ "$(grep -c '^fn main(' fl_full.zag)" = "1" ] || fail "expected exactly one fn main in fl_full.zag"
# K10 (part): no world literals in new lane sources
for f in fl_spec.zag fl_main.zag; do
  grep -q "901\|902" "$f" && fail "K10: $f contains world literals"
done

"$ZNC" build fl_full.zag -o fl_bin > fl_compile.txt 2>&1 || fail "znc build of fl_full.zag failed"
grep -q ": error" fl_compile.txt && fail "compiler reported an error (see fl_compile.txt)"

# run experiment 3x
for i in 1 2 3; do
  ./fl_bin > "fl_run$i.txt" 2> "fl_run$i.err"; echo "fl_bin run$i exit=$?"
done

# K3 determinism: byte-identical across the 3 runs
cmp fl_run1.txt fl_run2.txt || fail "K3: fl_run1/fl_run2 differ"
cmp fl_run1.txt fl_run3.txt || fail "K3: fl_run1/fl_run3 differ"
sha256sum fl_run1.txt

# K3 stderr must be empty
for f in fl_run1.err fl_run2.err fl_run3.err; do
  [ -s "$f" ] && fail "K3: non-empty stderr: $f"
done

# K3: exactly 72 CELL lines (4 cells x 18 arms)
[ "$(grep -c '^CELL ' fl_run1.txt)" = "72" ] || fail "K3: expected 72 CELL lines"

echo "--- kill bars ---"

field() { # $1=R $2=P-pattern $3=L $4=field -> value
  grep "^CELL R=$1 " fl_run1.txt | grep " P=$2 " | grep " L=$3 " \
    | grep -o " $4=[0-9-]*" | head -1 | cut -d= -f2
}
fixed_field() { field "$1" "$2" "-1" "$3"; }
adapt_field() { field "$1" "adapt" "$2" "$3"; }
guard_field() { field "$1" "guard" "$2" "$3"; }
fastchk_field() { field "$1" "fastchk" "$2" "$3"; }
fastewma_field() { field "$1" "fastewma" "$2" "$3"; }
j_val() { # $1=R $2=P $3=L -> J = rb + rf*L
  rb=$(field "$1" "$2" "$3" rebuilds); rf=$(field "$1" "$2" "$3" refusals)
  echo $(( rb + rf * $3 ))
}

# arm list for anchoring: P:L pairs (18 per cell)
ARMS="lazy:-1 eager:-1 adapt:1 adapt:3 adapt:7 adapt:10 adapt:15 adapt:20 adapt:30 guard:3 guard:7 guard:10 fastchk:1 fastchk:7 fastchk:10 fastewma:1 fastewma:7 fastewma:10"
ADAPTIVE="adapt:1 adapt:3 adapt:7 adapt:10 adapt:15 adapt:20 adapt:30 guard:3 guard:7 guard:10 fastchk:1 fastchk:7 fastchk:10 fastewma:1 fastewma:7 fastewma:10"

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
  for pl in $ARMS; do
    P="${pl%%:*}"; L="${pl##*:}"
    [ "$P" = "lazy" ] && continue
    [ "$P" = "eager" ] && continue
    da=$(field $R $P $L D); qa=$(field $R $P $L Q)
    { [ "$da" = "$dd" ] && [ "$qa" = "$qd" ]; } \
      || fail "K4a: R=$R P=$P L=$L (D,Q)=($da,$qa) != lazy ($dd,$qd)"
  done
done
echo "PASS: K4a fixed arms anchor; cross-arm (D,Q) identical on all 4 cells (18 arms)"

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

# K4c: structural accounting on all 64 adaptive lines.
for R in 21 60 82 120; do
  rod=$(fixed_field $R lazy rebuilds); rrf=$(fixed_field $R lazy refusals)
  for pl in $ADAPTIVE; do
    P="${pl%%:*}"; L="${pl##*:}"
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
echo "PASS: K4c structural accounting on all 64 adaptive lines; lc=0 everywhere"

# K5a: exact replication of the parent's frozen lines (rename-only delta check).
echo "K5a FINDING replication lines:"
for R in 21 60 82 120; do
  for pl in "adapt 1" "adapt 3" "adapt 7" "guard 3" "guard 7"; do
    set -- $pl
    pline=$(grep "^CELL R=$R " "$PCSRUN" | grep " P=$1 " | grep " L=$2 ")
    nline=$(grep "^CELL R=$R " fl_run1.txt | grep " P=$1 " | grep " L=$2 ")
    [ -n "$pline" ] || fail "K5a: parent line missing R=$R P=$1 L=$2"
    [ "$pline" = "$nline" ] || fail "K5a: R=$R P=$1 L=$2 line differs from parent frozen run"
  done
done
echo "PASS: K5a 20 adapt/guard lines byte-identical to parent frozen run (delta is surgical)"

# K5b: quirk fires identically in the new arms (pre-shift path unchanged).
for R in 21 60 82; do
  for P in fastchk fastewma; do
    for L in 1 7 10; do
      tc=$(field $R $P $L tc); cm=$(field $R $P $L cm); Dc=$(field $R $P $L Dc)
      { [ "$tc" = "32" ] && [ "$cm" = "2" ] && [ "$Dc" = "0" ]; } \
        || fail "K5b: R=$R P=$P L=$L quirk not identical (tc=$tc cm=$cm Dc=$Dc)"
    done
  done
done
echo "PASS: K5b quirk fires identically (tc=32, cm=2, Dc=0) in fastchk/fastewma on D32=0 cells"

# K5c: monotone latency within each adaptive arm on R=60 (theorem).
check_mono() { # $1=P $2=La $3=Lb
  fla=$(field 60 $1 $2 flips); tfa=$(field 60 $1 $2 tf1)
  flb=$(field 60 $1 $3 flips); tfb=$(field 60 $1 $3 tf1)
  if [ "$flb" -ge 1 ]; then
    { [ "$fla" -ge 1 ] && [ "$tfa" -le "$tfb" ]; } \
      || fail "K5c: P=$1 La=$2 (flips=$fla tf1=$tfa) vs Lb=$3 (flips=$flb tf1=$tfb): latency not monotone"
  fi
}
for pair in "1 3" "3 7" "7 10" "10 15" "15 20" "20 30"; do
  set -- $pair; check_mono adapt $1 $2
done
for pair in "3 7" "7 10"; do
  set -- $pair; check_mono guard $1 $2
done
for pair in "1 7" "7 10"; do
  set -- $pair; check_mono fastchk $1 $2; check_mono fastewma $1 $2
done
echo "PASS: K5c latency monotone non-decreasing in L within every adaptive arm (R=60)"

# K6a: too-late replication: J_adapt(7) = 142 > 133 = J_eager on R=60.
ja7=$(j_val 60 adapt 7); je=$(j_val 60 eager -1)
echo "K6a R=60: J_adapt(7)=$ja7 J_eager=$je"
{ [ "$ja7" = "142" ] && [ "$je" = "133" ]; } \
  || fail "K6a: R=60 J_adapt(7)=$ja7 (want 142) J_eager=$je (want 133)"
echo "PASS: K6a too-late finding replicated: adapt(7)=142 > eager=133"

# K6b: too-late extension: J_adapt(10) > J_eager (theorem).
ja10=$(j_val 60 adapt 10)
echo "K6b R=60: J_adapt(10)=$ja10 J_eager=$je"
[ "$ja10" -gt "$je" ] || fail "K6b: R=60 J_adapt(10)=$ja10 not > J_eager=$je"
echo "PASS: K6b too-late boundary extends: adapt(10)=$ja10 > eager=$je"

# K7: quirk exonerated -- guard flip ticks identical to adapt (R=60).
for L in 3 7 10; do
  tfa=$(adapt_field 60 $L tf1); fla=$(adapt_field 60 $L flips); fda=$(adapt_field 60 $L fdir)
  tfg=$(guard_field 60 $L tf1); flg=$(guard_field 60 $L flips); fdg=$(guard_field 60 $L fdir)
  echo "  L=$L: adapt(tf1=$tfa flips=$fla fdir=$fda) guard(tf1=$tfg flips=$flg fdir=$fdg)"
  { [ "$tfa" = "$tfg" ] && [ "$fla" = "$flg" ] && [ "$fda" = "$fdg" ]; } \
    || fail "K7: L=$L guard/adapt flip ticks differ (quirk affects latency)"
done
echo "PASS: K7 guard flip ticks identical to adapt: latency is a flip-rule property, not a quirk property"

# K8: cadence -- fastchk never later than adapt (R=60).
for L in 1 7 10; do
  tfa=$(adapt_field 60 $L tf1); fla=$(adapt_field 60 $L flips)
  tff=$(fastchk_field 60 $L tf1); flf=$(fastchk_field 60 $L flips)
  echo "  L=$L: adapt(tf1=$tfa flips=$fla) fastchk(tf1=$tff flips=$flf)"
  [ "$tff" -le "$tfa" ] || fail "K8a: L=$L fastchk tf1=$tff > adapt tf1=$tfa"
  if [ "$fla" -ge 1 ]; then
    [ "$flf" -ge 1 ] || fail "K8b: L=$L adapt flipped but fastchk did not"
  fi
  if [ "$flf" -ge 1 ]; then
    [ "$tff" -ge 136 ] || fail "K8c: L=$L fastchk tf1=$tff < 136 (first post-shift 8-checkpoint)"
  fi
done
echo "PASS: K8 fastchk never later than adapt; flips whenever adapt flips; tf1>=136"

# K9a: fastewma still rescues at L=1 (R=60).
fl1=$(fastewma_field 60 1 flips); tf1=$(fastewma_field 60 1 tf1)
echo "K9a R=60 fastewma L=1: flips=$fl1 tf1=$tf1"
[ "$fl1" -ge 1 ] || fail "K9a: R=60 fastewma L=1 did not flip"
echo "PASS: K9a fastewma rescues at L=1"

# K10 hygiene: ASCII-only lane sources
if LC_ALL=C grep -l '[^[:print:][:space:]]' PREREG.md NAMECHECK.md fl_spec.zag fl_main.zag fl_build.sh 2>/dev/null; then
  fail "K10: non-ASCII byte found"
fi
echo "PASS: K10 ASCII-only, no world literals, one fn main per binary, reused sources unmodified, da_learn.zag untouched"

echo "ALL KILL BARS PASS"
