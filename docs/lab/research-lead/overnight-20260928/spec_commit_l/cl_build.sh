#!/bin/bash
# cl_build.sh -- SPEC-COMMIT-L: build + run + verify.
# Usage: ./cl_build.sh  (run from this directory)
# safebin PATH is mandatory; the pinned znc builds cl_bin; cl_bin runs
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
PAR="$D/../spec_l_discipline"
PARRUN="$PAR/ld_run1.txt"
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
         cl_spec.zag cl_main.zag; do
  [ -f "$f" ] || fail "missing source: $f"
done
# K9 (part): reused sources byte-unmodified (no unstaged diff vs HEAD).
# The 9 grandparent sources; the parent lane's ld_spec.zag/ld_main.zag
# are superseded here by copy-plus-delta (cl_spec.zag), never edited.
for f in "$DA/da_base.zag" "$DA/da_module.zag" "$DA/da_learn.zag" \
         "$RB/rb_world.zag" "$RB/rb_fix.zag" \
         "$ET/et_world.zag" "$ET/et_spec.zag" \
         "$RR/rr_spec.zag" "$LD/ld_spec.zag" \
         "$PAR/ld_spec.zag" "$PAR/ld_main.zag"; do
  /usr/bin/git diff --quiet -- "$f" || fail "K9: reused source modified: $f"
done
# K9 (part): da_learn.zag explicitly unmodified (separate lane only)
/usr/bin/git diff --quiet -- "$DA/da_learn.zag" || fail "K9: da_learn.zag modified"
# K4d needs the parent's frozen run intact
[ "$(sha256sum "$PARRUN" | cut -d' ' -f1)" = "36d63552f3e3ec5bfd664bc9b40a1043c47c89ce181881bd5c94726fc0781b4b" ] \
  || fail "K4d: parent frozen run sha256 mismatch"

# assemble experiment binary: all reused sources byte-unmodified +
# commit-rule policy layer + harness main. The parent lane's ld_spec.zag
# is NOT assembled (superseded by cl_spec.zag); assembling both would
# duplicate fn definitions.
cat "$DA/da_base.zag" "$RB/rb_world.zag" "$ET/et_world.zag" "$DA/da_module.zag" \
    "$DA/da_learn.zag" "$RB/rb_fix.zag" "$ET/et_spec.zag" "$RR/rr_spec.zag" \
    "$LD/ld_spec.zag" cl_spec.zag cl_main.zag > cl_full.zag
[ "$(grep -c '^fn main(' cl_full.zag)" = "1" ] || fail "expected exactly one fn main in cl_full.zag"
# K9 (part): no world literals in new lane sources
for f in cl_spec.zag cl_main.zag; do
  grep -q "901\|902" "$f" && fail "K9: $f contains world literals"
done

"$ZNC" build cl_full.zag -o cl_bin > cl_compile.txt 2>&1 || fail "znc build of cl_full.zag failed"
grep -q ": error" cl_compile.txt && fail "compiler reported an error (see cl_compile.txt)"

# run experiment 3x
for i in 1 2 3; do
  ./cl_bin > "cl_run$i.txt" 2> "cl_run$i.err"; echo "cl_bin run$i exit=$?"
done

# K3 determinism: byte-identical across the 3 runs
cmp cl_run1.txt cl_run2.txt || fail "K3: cl_run1/cl_run2 differ"
cmp cl_run1.txt cl_run3.txt || fail "K3: cl_run1/cl_run3 differ"
sha256sum cl_run1.txt

# K3 stderr must be empty
for f in cl_run1.err cl_run2.err cl_run3.err; do
  [ -s "$f" ] && fail "K3: non-empty stderr: $f"
done

# K3: exactly 88 CELL lines (4 cells x 22 arms)
[ "$(grep -c '^CELL ' cl_run1.txt)" = "88" ] || fail "K3: expected 88 CELL lines"

echo "--- kill bars ---"

field() { # $1=R $2=P-pattern $3=L $4=field -> value
  grep "^CELL R=$1 " cl_run1.txt | grep " P=$2 " | grep " L=$3 " \
    | grep -o " $4=[0-9-]*" | head -1 | cut -d= -f2
}
fixed_field() { field "$1" "$2" "-1" "$3"; }
j_val() { # $1=R $2=P $3=L -> J = rb + rf*L
  rb=$(field "$1" "$2" "$3" rebuilds); rf=$(field "$1" "$2" "$3" refusals)
  echo $(( rb + rf * $3 ))
}
jp_val() { # $1=R $2=P $3=L -> J' = rb + rf (L-free scoring)
  rb=$(field "$1" "$2" "$3" rebuilds); rf=$(field "$1" "$2" "$3" refusals)
  echo $(( rb + rf ))
}
ident_mod_p() { # $1=bar $2=R $3=P1 $4=P2 $5=L : line(P1) == line(P2) modulo P= field
  l1=$(grep "^CELL R=$2 " cl_run1.txt | grep " P=$3 " | grep " L=$5 " | sed "s/ P=$3 / P=POL /")
  l2=$(grep "^CELL R=$2 " cl_run1.txt | grep " P=$4 " | grep " L=$5 " | sed "s/ P=$4 / P=POL /")
  [ -n "$l1" ] || fail "$1: R=$2 P=$3 L=$5 line missing"
  [ -n "$l2" ] || fail "$1: R=$2 P=$4 L=$5 line missing"
  [ "$l1" = "$l2" ] || fail "$1: R=$2 P=$3 vs P=$4 L=$5 differ beyond P= field"
}
ident_mod_pl() { # $1=bar $2=R $3=P1 $4=L1 $5=P2 $6=L2 : lines equal modulo P= and L=
  l1=$(grep "^CELL R=$2 " cl_run1.txt | grep " P=$3 " | grep " L=$4 " | sed -e "s/ P=$3 / P=POL /" -e "s/ L=$4 / L=LVL /")
  l2=$(grep "^CELL R=$2 " cl_run1.txt | grep " P=$5 " | grep " L=$6 " | sed -e "s/ P=$5 / P=POL /" -e "s/ L=$6 / L=LVL /")
  [ -n "$l1" ] || fail "$1: R=$2 P=$3 L=$4 line missing"
  [ -n "$l2" ] || fail "$1: R=$2 P=$5 L=$6 line missing"
  [ "$l1" = "$l2" ] || fail "$1: R=$2 P=$3/L=$4 vs P=$5/L=$6 differ beyond P=/L= fields"
}
parent_line_mod_pl() { # $1=bar $2=R $3=PP $4=PL $5=P2 $6=L2 : parent frozen line == run line modulo P=/L=
  l1=$(grep "^CELL R=$2 " "$PARRUN" | grep " P=$3 " | grep " L=$4 " | sed -e "s/ P=$3 / P=POL /" -e "s/ L=$4 / L=LVL /")
  l2=$(grep "^CELL R=$2 " cl_run1.txt | grep " P=$5 " | grep " L=$6 " | sed -e "s/ P=$5 / P=POL /" -e "s/ L=$6 / L=LVL /")
  [ -n "$l1" ] || fail "$1: parent R=$2 P=$3 L=$4 line missing"
  [ -n "$l2" ] || fail "$1: R=$2 P=$5 L=$6 line missing"
  [ "$l1" = "$l2" ] || fail "$1: R=$2 parent P=$3/L=$4 vs P=$5/L=$6 differ beyond P=/L= fields"
}

# arm lists: P:L pairs (22 per cell; 20 adaptive)
ARMS="lazy:-1 eager:-1 fix2:1 fix2:3 fix2:7 fix2:10 noeg:1 noeg:3 noeg:7 noeg:10 coml1:1 coml1:3 coml1:7 coml1:10 comlg:1 comlg:3 comlg:7 comlg:10 comnoeg:1 comnoeg:3 comnoeg:7 comnoeg:10"
ADAPTIVE="fix2:1 fix2:3 fix2:7 fix2:10 noeg:1 noeg:3 noeg:7 noeg:10 coml1:1 coml1:3 coml1:7 coml1:10 comlg:1 comlg:3 comlg:7 comlg:10 comnoeg:1 comnoeg:3 comnoeg:7 comnoeg:10"

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
echo "PASS: K4a fixed arms anchor; cross-arm (D,Q) identical on all 4 cells (22 arms)"

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

# K4c: structural accounting on all 80 adaptive lines.
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
echo "PASS: K4c structural accounting on all 80 adaptive lines; lc=0 everywhere"

# K4d: exact replication of the parent's frozen lines (surgical-delta check).
for R in 21 60 82 120; do
  for pl in "fix2 1" "fix2 3" "fix2 7" "fix2 10" "noeg 1" "noeg 3" "noeg 7" "noeg 10"; do
    set -- $pl
    pline=$(grep "^CELL R=$R " "$PARRUN" | grep " P=$1 " | grep " L=$2 ")
    nline=$(grep "^CELL R=$R " cl_run1.txt | grep " P=$1 " | grep " L=$2 ")
    [ -n "$pline" ] || fail "K4d: parent line missing R=$R P=$1 L=$2"
    [ "$pline" = "$nline" ] || fail "K4d: R=$R P=$1 L=$2 line differs from parent frozen run"
  done
done
echo "PASS: K4d 32 fix2/noeg lines byte-identical to parent frozen run (delta is surgical)"

# K5a: quirk preserved under the L-free commit (coml1): the exact
# degenerate signature on the D32=0 cells at every L.
for R in 21 60 82; do
  for L in 1 3 7 10; do
    tc=$(field $R coml1 $L tc); cm=$(field $R coml1 $L cm); Dc=$(field $R coml1 $L Dc)
    dh=$(field $R coml1 $L dh); dlo=$(field $R coml1 $L dlo); dhi=$(field $R coml1 $L dhi)
    phin=$(field $R coml1 $L phin); phid=$(field $R coml1 $L phid)
    { [ "$tc" = "32" ] && [ "$cm" = "2" ] && [ "$Dc" = "0" ] && \
      [ "$dh" = "0" ] && [ "$dlo" = "0" ] && [ "$dhi" = "0" ] && \
      [ "$phin" = "0" ] && [ "$phid" = "1" ]; } \
      || fail "K5a: R=$R coml1 L=$L quirk signature broken (tc=$tc cm=$cm Dc=$Dc dh=$dh dlo=$dlo dhi=$dhi phin=$phin phid=$phid)"
  done
done
echo "PASS: K5a quirk preserved under L-free commit (tc=32, cm=2, Dc=0, degenerate snapshot) in coml1 on D32=0 cells"

# K5b: quirk killed: no comlg/comnoeg line on the D32=0 cells carries
# the quirk signature (cm=2 with Dc=0); comnoeg can never cm=2 at all
# (dec == 2 impossible by construction).
for R in 21 60 82; do
  for L in 1 3 7 10; do
    cm=$(field $R comlg $L cm); Dc=$(field $R comlg $L Dc)
    { [ "$cm" = "2" ] && [ "$Dc" = "0" ]; } \
      && fail "K5b: R=$R comlg L=$L quirk signature present (cm=2 Dc=0)"
    cm=$(field $R comnoeg $L cm); Dc=$(field $R comnoeg $L Dc)
    { [ "$cm" = "2" ] && [ "$Dc" = "0" ]; } \
      && fail "K5b: R=$R comnoeg L=$L quirk signature present (cm=2 Dc=0)"
  done
done
for R in 21 60 82 120; do
  for L in 1 3 7 10; do
    cm=$(field $R comnoeg $L cm)
    [ "$cm" != "2" ] || fail "K5b: R=$R comnoeg L=$L cm=2 (eager direction must be impossible)"
  done
done
echo "PASS: K5b quirk signature absent in comlg/comnoeg; comnoeg never cm=2"

# K5c: quirk-dominated identity: L-free commit changes nothing where
# the quirk dominates (coml1 == noeg modulo P= on the D32=0 cells).
for R in 21 60 82; do
  for L in 1 3 7 10; do
    ident_mod_p "K5c" $R coml1 noeg $L
  done
done
echo "PASS: K5c coml1 == noeg modulo P= on R=21/60/82 at every L (quirk-dominated cells)"

# K6a: the core question on R=120. coml1 at every L must equal the
# parent's frozen noeg L=1 R=120 line modulo P=/L= (cm=0, tc=128,
# flips=0, rb=11, rf=11). The parent's noeg L=7/10 lines sit at
# cm=2/tc=112, so passing here proves removing L from the commit rule
# changes behavior: the commit rule's L is observably load-bearing.
for L in 1 3 7 10; do
  parent_line_mod_pl "K6a" 120 noeg 1 coml1 $L
  cm=$(field 120 coml1 $L cm); tc=$(field 120 coml1 $L tc)
  fl=$(field 120 coml1 $L flips); rb=$(field 120 coml1 $L rebuilds)
  rf=$(field 120 coml1 $L refusals)
  { [ "$cm" = "0" ] && [ "$tc" = "128" ] && [ "$fl" = "0" ] && \
    [ "$rb" = "11" ] && [ "$rf" = "11" ]; } \
    || fail "K6a: R=120 coml1 L=$L fields cm=$cm tc=$tc flips=$fl rb=$rb rf=$rf (want 0/128/0/11/11)"
done
echo "PASS: K6a coml1 == parent noeg L=1 on R=120 (mod P=/L=) at every L: commit-rule L is load-bearing"

# K6b: the guard never binds on R=120 (dec == 2 never fires pre-shift
# under L := 1 there): comlg == coml1 modulo P=.
for L in 1 3 7 10; do
  ident_mod_p "K6b" 120 comlg coml1 $L
done
echo "PASS: K6b comlg == coml1 modulo P= on R=120 at every L (guard never binds)"

# K6c: no data-driven eager work under L-free commit on R=120:
# comnoeg == coml1 modulo P= (the lazy-only commit never fires either).
for L in 1 3 7 10; do
  ident_mod_p "K6c" 120 comnoeg coml1 $L
done
echo "PASS: K6c comnoeg == coml1 modulo P= on R=120 at every L (eager direction does no data-driven work there)"

# K7a: economics on R=120. J_coml1(120,L) = 11 + 11*L exactly
# (from K6a: rb=11, rf=11 at every L); the frozen J_noeg(120,7) = 78
# and J_noeg(120,10) = 93. The L-driven eager commit was J-beneficial
# at high L under the caller-stated cost ratio.
for L in 1 3 7 10; do
  want=$(( 11 + 11 * L ))
  got=$(j_val 120 coml1 $L)
  [ "$got" = "$want" ] || fail "K7a: J_coml1(120,$L)=$got != $want"
done
[ "$(j_val 120 noeg 7)" = "78" ] || fail "K7a: J_noeg(120,7) != 78"
[ "$(j_val 120 noeg 10)" = "93" ] || fail "K7a: J_noeg(120,10) != 93"
echo "PASS: K7a J_coml1(120,L)=11+11L (22/44/88/121) vs J_noeg(120,7)=78, J_noeg(120,10)=93: L-driven commit was J-beneficial"
# K7b: J' tension (reported, not barred).
echo "K7b R=120 J' = rb + rf (L-free scoring) vs J = rb + rf*L:"
for L in 1 3 7 10; do
  echo "  L=$L: J'_coml1=$(jp_val 120 coml1 $L) J_coml1=$(j_val 120 coml1 $L) | J'_noeg=$(jp_val 120 noeg $L) J_noeg=$(j_val 120 noeg $L)"
done
echo "K7b findings recorded (J-beneficial but J'-harmful: see REPORT.md)"
# K7c: quirk scoreboard on the D32=0 cells (reported, not barred):
# the quirk's cost/benefit under the L-free flip discipline.
echo "K7c quirk scoreboard (J, lower is better) on D32=0 cells:"
for R in 21 60 82; do
  for L in 1 3 7 10; do
    echo "  R=$R L=$L: J_coml1=$(j_val $R coml1 $L) J_comlg=$(j_val $R comlg $L) J_comnoeg=$(j_val $R comnoeg $L) J_noeg=$(j_val $R noeg $L)"
  done
done
echo "K7c findings recorded (see REPORT.md for the quirk scoreboard analysis)"

# K8a: control integrity: zero flips on R=21/82 for the new arms.
for R in 21 82; do
  for P in coml1 comlg comnoeg; do
    for L in 1 3 7 10; do
      fl=$(field $R $P $L flips)
      [ "$fl" = "0" ] || fail "K8a: R=$R P=$P L=$L flips=$fl != 0"
    done
  done
done
echo "PASS: K8a zero flips on R=21/82 for coml1/comlg/comnoeg at every L"
# K8b: findings (reported, not barred): comlg vs comnoeg identity on
# all cells/L: does `phid > phin` (L := 1) do data-driven eager work
# under L-free commit anywhere?
echo "K8b comlg vs comnoeg line identity (mod P=):"
for R in 21 60 82 120; do
  for L in 1 3 7 10; do
    l1=$(grep "^CELL R=$R " cl_run1.txt | grep " P=comlg " | grep " L=$L " | sed "s/ P=comlg / P=POL /")
    l2=$(grep "^CELL R=$R " cl_run1.txt | grep " P=comnoeg " | grep " L=$L " | sed "s/ P=comnoeg / P=POL /")
    if [ "$l1" = "$l2" ]; then st="IDENTICAL"; else st="DIFFER"; fi
    cm1=$(field $R comlg $L cm); tc1=$(field $R comlg $L tc)
    cm2=$(field $R comnoeg $L cm); tc2=$(field $R comnoeg $L tc)
    echo "  R=$R L=$L: $st (comlg cm=$cm1 tc=$tc1 | comnoeg cm=$cm2 tc=$tc2)"
  done
done
echo "K8b findings recorded (see REPORT.md)"
# K8c: findings (reported, not barred): R=60 new-arm behavior.
echo "K8c R=60 new arms (commit/flip/economics):"
for P in noeg coml1 comlg comnoeg; do
  for L in 1 3 7 10; do
    cm=$(field 60 $P $L cm); tc=$(field 60 $P $L tc); Dc=$(field 60 $P $L Dc)
    fl=$(field 60 $P $L flips); tf1=$(field 60 $P $L tf1); fd=$(field 60 $P $L fdir)
    se=$(field 60 $P $L sel)
    echo "  P=$P L=$L: cm=$cm tc=$tc Dc=$Dc flips=$fl tf1=$tf1 fdir=$fd sel=$se J=$(j_val 60 $P $L) J'=$(jp_val 60 $P $L)"
  done
done
echo "K8c findings recorded (see REPORT.md)"

# K9 hygiene: ASCII-only lane sources
if LC_ALL=C grep -l '[^[:print:][:space:]]' PREREG.md NAMECHECK.md cl_spec.zag cl_main.zag cl_build.sh 2>/dev/null; then
  fail "K9: non-ASCII byte found"
fi
echo "PASS: K9 ASCII-only, no world literals, one fn main per binary, reused sources unmodified, da_learn.zag untouched, parent lane unedited"

echo "ALL KILL BARS PASS"
