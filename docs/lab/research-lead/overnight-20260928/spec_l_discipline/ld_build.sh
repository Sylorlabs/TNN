#!/bin/bash
# ld_build.sh -- SPEC-L-DISCIPLINE: build + run + verify.
# Usage: ./ld_build.sh  (run from this directory)
# safebin PATH is mandatory; the pinned znc builds ld_bin; ld_bin runs
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
PFL="$D/../spec_flip_threshold"
PFLRUN="$PFL/ft_run1.txt"
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
         ld_spec.zag ld_main.zag; do
  [ -f "$f" ] || fail "missing source: $f"
done
# K9 (part): reused sources byte-unmodified (no unstaged diff vs HEAD).
# The 9 grandparent sources; the flip-threshold lane's ft_spec.zag is
# superseded here by copy-plus-delta (ld_spec.zag), never edited.
for f in "$DA/da_base.zag" "$DA/da_module.zag" "$DA/da_learn.zag" \
         "$RB/rb_world.zag" "$RB/rb_fix.zag" \
         "$ET/et_world.zag" "$ET/et_spec.zag" \
         "$RR/rr_spec.zag" "$LD/ld_spec.zag"; do
  /usr/bin/git diff --quiet -- "$f" || fail "K9: reused source modified: $f"
done
# K9 (part): da_learn.zag explicitly unmodified (separate lane only)
/usr/bin/git diff --quiet -- "$DA/da_learn.zag" || fail "K9: da_learn.zag modified"
# K9 (part): the parent lane's ft_spec.zag / ft_main.zag superseded, never edited
/usr/bin/git diff --quiet -- "$PFL/ft_spec.zag" || fail "K9: parent ft_spec.zag modified"
/usr/bin/git diff --quiet -- "$PFL/ft_main.zag" || fail "K9: parent ft_main.zag modified"
# K5a needs the parent's frozen run intact
[ "$(sha256sum "$PFLRUN" | cut -d' ' -f1)" = "99d52d2b3aac843ad8ddc2225c742c95bf6cc977d9ee6570af8970defaf957a8" ] \
  || fail "K5a: parent frozen run sha256 mismatch"

# assemble experiment binary: all reused sources byte-unmodified +
# L-discipline policy layer + harness main. ft_spec.zag is NOT
# assembled (superseded by ld_spec.zag); assembling both would
# duplicate fn definitions.
cat "$DA/da_base.zag" "$RB/rb_world.zag" "$ET/et_world.zag" "$DA/da_module.zag" \
    "$DA/da_learn.zag" "$RB/rb_fix.zag" "$ET/et_spec.zag" "$RR/rr_spec.zag" \
    "$LD/ld_spec.zag" ld_spec.zag ld_main.zag > ld_full.zag
[ "$(grep -c '^fn main(' ld_full.zag)" = "1" ] || fail "expected exactly one fn main in ld_full.zag"
# K9 (part): no world literals in new lane sources
for f in ld_spec.zag ld_main.zag; do
  grep -q "901\|902" "$f" && fail "K9: $f contains world literals"
done

"$ZNC" build ld_full.zag -o ld_bin > ld_compile.txt 2>&1 || fail "znc build of ld_full.zag failed"
grep -q ": error" ld_compile.txt && fail "compiler reported an error (see ld_compile.txt)"

# run experiment 3x
for i in 1 2 3; do
  ./ld_bin > "ld_run$i.txt" 2> "ld_run$i.err"; echo "ld_bin run$i exit=$?"
done

# K3 determinism: byte-identical across the 3 runs
cmp ld_run1.txt ld_run2.txt || fail "K3: ld_run1/ld_run2 differ"
cmp ld_run1.txt ld_run3.txt || fail "K3: ld_run1/ld_run3 differ"
sha256sum ld_run1.txt

# K3 stderr must be empty
for f in ld_run1.err ld_run2.err ld_run3.err; do
  [ -s "$f" ] && fail "K3: non-empty stderr: $f"
done

# K3: exactly 88 CELL lines (4 cells x 22 arms)
[ "$(grep -c '^CELL ' ld_run1.txt)" = "88" ] || fail "K3: expected 88 CELL lines"

echo "--- kill bars ---"

field() { # $1=R $2=P-pattern $3=L $4=field -> value
  grep "^CELL R=$1 " ld_run1.txt | grep " P=$2 " | grep " L=$3 " \
    | grep -o " $4=[0-9-]*" | head -1 | cut -d= -f2
}
fixed_field() { field "$1" "$2" "-1" "$3"; }
adapt_field() { field "$1" "adapt" "$2" "$3"; }
fix2_field() { field "$1" "fix2" "$2" "$3"; }
noeg_field() { field "$1" "noeg" "$2" "$3"; }
j_val() { # $1=R $2=P $3=L -> J = rb + rf*L
  rb=$(field "$1" "$2" "$3" rebuilds); rf=$(field "$1" "$2" "$3" refusals)
  echo $(( rb + rf * $3 ))
}
jp_val() { # $1=R $2=P $3=L -> J' = rb + rf (L-free scoring)
  rb=$(field "$1" "$2" "$3" rebuilds); rf=$(field "$1" "$2" "$3" refusals)
  echo $(( rb + rf ))
}
ident_mod_p() { # $1=bar $2=R $3=P1 $4=P2 $5=L : line(P1) == line(P2) modulo P= field
  l1=$(grep "^CELL R=$2 " ld_run1.txt | grep " P=$3 " | grep " L=$5 " | sed "s/ P=$3 / P=POL /")
  l2=$(grep "^CELL R=$2 " ld_run1.txt | grep " P=$4 " | grep " L=$5 " | sed "s/ P=$4 / P=POL /")
  [ -n "$l1" ] || fail "$1: R=$2 P=$3 L=$5 line missing"
  [ -n "$l2" ] || fail "$1: R=$2 P=$4 L=$5 line missing"
  [ "$l1" = "$l2" ] || fail "$1: R=$2 P=$3 vs P=$4 L=$5 differ beyond P= field"
}

# arm lists: P:L pairs (22 per cell; 20 adaptive)
ARMS="lazy:-1 eager:-1 adapt:1 adapt:3 adapt:7 adapt:10 fix2:1 fix2:3 fix2:7 fix2:10 noeg:1 noeg:3 noeg:7 noeg:10 noj:1 noj:3 noj:7 noj:10 nol:1 nol:3 nol:7 nol:10"
ADAPTIVE="adapt:1 adapt:3 adapt:7 adapt:10 fix2:1 fix2:3 fix2:7 fix2:10 noeg:1 noeg:3 noeg:7 noeg:10 noj:1 noj:3 noj:7 noj:10 nol:1 nol:3 nol:7 nol:10"

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

# K5a: exact replication of the parent's frozen lines (surgical-delta check).
for R in 21 60 82 120; do
  for pl in "adapt 1" "adapt 3" "adapt 7" "adapt 10" "fix2 1" "fix2 3" "fix2 7" "fix2 10"; do
    set -- $pl
    pline=$(grep "^CELL R=$R " "$PFLRUN" | grep " P=$1 " | grep " L=$2 ")
    nline=$(grep "^CELL R=$R " ld_run1.txt | grep " P=$1 " | grep " L=$2 ")
    [ -n "$pline" ] || fail "K5a: parent line missing R=$R P=$1 L=$2"
    [ "$pline" = "$nline" ] || fail "K5a: R=$R P=$1 L=$2 line differs from parent frozen run"
  done
done
echo "PASS: K5a 32 adapt/fix2 lines byte-identical to parent frozen run (delta is surgical)"

# K5b: quirk fires identically in the new arms (commit path unchanged).
for R in 21 60 82; do
  for P in noeg noj nol; do
    for L in 1 3 7 10; do
      tc=$(field $R $P $L tc); cm=$(field $R $P $L cm); Dc=$(field $R $P $L Dc)
      { [ "$tc" = "32" ] && [ "$cm" = "2" ] && [ "$Dc" = "0" ]; } \
        || fail "K5b: R=$R P=$P L=$L quirk not identical (tc=$tc cm=$cm Dc=$Dc)"
    done
  done
done
echo "PASS: K5b quirk fires identically (tc=32, cm=2, Dc=0) in noeg/noj/nol on D32=0 cells"

# K5c: monotone latency within each adaptive arm on R=60 (theorem).
check_mono() { # $1=P $2=La $3=Lb
  fla=$(field 60 $1 $2 flips); tfa=$(field 60 $1 $2 tf1)
  flb=$(field 60 $1 $3 flips); tfb=$(field 60 $1 $3 tf1)
  if [ "$flb" -ge 1 ]; then
    { [ "$fla" -ge 1 ] && [ "$tfa" -le "$tfb" ]; } \
      || fail "K5c: P=$1 La=$2 (flips=$fla tf1=$tfa) vs Lb=$3 (flips=$flb tf1=$tfb): latency not monotone"
  fi
}
for pair in "1 3" "3 7" "7 10"; do
  set -- $pair
  check_mono adapt $1 $2; check_mono fix2 $1 $2
  check_mono noeg $1 $2; check_mono noj $1 $2; check_mono nol $1 $2
done
echo "PASS: K5c latency monotone non-decreasing in L within every adaptive arm (R=60)"

# K5d: L=1 identity -- noeg L=1 == fix2 L=1 and nol L=1 == noj L=1 modulo P=.
for R in 21 60 82 120; do
  ident_mod_p "K5d" $R noeg fix2 1
  ident_mod_p "K5d" $R nol noj 1
done
echo "PASS: K5d L=1 identities hold (noeg==fix2, nol==noj modulo P=) on all 4 cells"

# K6: the eager-direction question on the harm cell -- noeg == fix2 modulo P=.
for L in 1 3 7 10; do
  ident_mod_p "K6" 60 noeg fix2 $L
done
echo "PASS: K6 removing L from the flip-path eager direction changes nothing on R=60 (L not load-bearing there)"

# K7a: alias correctness -- scoring must not touch dynamics.
for R in 21 60 82 120; do
  for L in 1 3 7 10; do
    ident_mod_p "K7a" $R noj fix2 $L
    ident_mod_p "K7a" $R nol noeg $L
  done
done
echo "PASS: K7a alias correctness: noj==fix2 and nol==noeg modulo P= on all cells/L (J-free scoring touches no dynamics)"
# K7b: J' findings on R=60 (reported, not barred).
echo "K7b R=60 J' = rb + rf (L-free scoring):"
for L in 1 3 7 10; do
  jpf=$(jp_val 60 fix2 $L); jpa=$(jp_val 60 adapt $L)
  echo "  L=$L: J'_fix2=$jpf J'_adapt=$jpa J_fix2=$(j_val 60 fix2 $L) J_adapt=$(j_val 60 adapt $L)"
done
jpe=$(jp_val 60 eager -1)
echo "  J'_eager=$jpe J_eager=$(j_val 60 eager -1)"
echo "K7b findings recorded (see REPORT.md for the J' ranking analysis)"

# K8: both L-free / control integrity -- noeg == fix2 modulo P= on control cells.
for R in 21 82 120; do
  for L in 1 3 7 10; do
    ident_mod_p "K8" $R noeg fix2 $L
  done
done
echo "PASS: K8 no spurious divergence on control cells: noeg==fix2 modulo P= on R=21/82/120"
# K8 findings: new-arm flips/J on control cells + commit-side L-dependence bound.
echo "K8 control-cell findings:"
for R in 21 82 120; do
  for P in fix2 noeg; do
    for L in 1 3 7 10; do
      fl=$(field $R $P $L flips); tf1=$(field $R $P $L tf1); fd=$(field $R $P $L fdir)
      cm=$(field $R $P $L cm); tc=$(field $R $P $L tc)
      echo "  R=$R P=$P L=$L: flips=$fl tf1=$tf1 fdir=$fd cm=$cm tc=$tc J=$(j_val $R $P $L) J'=$(jp_val $R $P $L)"
    done
  done
done

# K9 hygiene: ASCII-only lane sources
if LC_ALL=C grep -l '[^[:print:][:space:]]' PREREG.md NAMECHECK.md ld_spec.zag ld_main.zag ld_build.sh 2>/dev/null; then
  fail "K9: non-ASCII byte found"
fi
echo "PASS: K9 ASCII-only, no world literals, one fn main per binary, reused sources unmodified, da_learn.zag untouched, parent lane unedited"

echo "ALL KILL BARS PASS"
