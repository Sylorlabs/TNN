#!/bin/bash
# ft_build.sh -- SPEC-FLIP-THRESHOLD: build + run + verify.
# Usage: ./ft_build.sh  (run from this directory)
# safebin PATH is mandatory; the pinned znc builds ft_bin; ft_bin runs
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
PFL="$D/../spec_flip_latency"
PFLRUN="$PFL/fl_run1.txt"
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
         ft_spec.zag ft_main.zag; do
  [ -f "$f" ] || fail "missing source: $f"
done
# K10 (part): reused sources byte-unmodified (no unstaged diff vs HEAD).
# The 9 grandparent sources; the flip-latency lane's fl_spec.zag is
# superseded here by copy-plus-delta (ft_spec.zag), never edited.
for f in "$DA/da_base.zag" "$DA/da_module.zag" "$DA/da_learn.zag" \
         "$RB/rb_world.zag" "$RB/rb_fix.zag" \
         "$ET/et_world.zag" "$ET/et_spec.zag" \
         "$RR/rr_spec.zag" "$LD/ld_spec.zag"; do
  /usr/bin/git diff --quiet -- "$f" || fail "K10: reused source modified: $f"
done
# K10 (part): da_learn.zag explicitly unmodified (separate lane only)
/usr/bin/git diff --quiet -- "$DA/da_learn.zag" || fail "K10: da_learn.zag modified"
# K10 (part): the parent lane's fl_spec.zag superseded, never edited
/usr/bin/git diff --quiet -- "$PFL/fl_spec.zag" || fail "K10: parent fl_spec.zag modified"
/usr/bin/git diff --quiet -- "$PFL/fl_main.zag" || fail "K10: parent fl_main.zag modified"
# K5a needs the parent's frozen run intact
[ "$(sha256sum "$PFLRUN" | cut -d' ' -f1)" = "b81f6080d57a4bc7b29eb71a820fc3897a0b5bb68680f60c28bf509af629d9ac" ] \
  || fail "K5a: parent frozen run sha256 mismatch"

# assemble experiment binary: all reused sources byte-unmodified +
# threshold policy layer + harness main. fl_spec.zag is NOT
# assembled (superseded by ft_spec.zag); assembling both would
# duplicate fn definitions.
cat "$DA/da_base.zag" "$RB/rb_world.zag" "$ET/et_world.zag" "$DA/da_module.zag" \
    "$DA/da_learn.zag" "$RB/rb_fix.zag" "$ET/et_spec.zag" "$RR/rr_spec.zag" \
    "$LD/ld_spec.zag" ft_spec.zag ft_main.zag > ft_full.zag
[ "$(grep -c '^fn main(' ft_full.zag)" = "1" ] || fail "expected exactly one fn main in ft_full.zag"
# K10 (part): no world literals in new lane sources
for f in ft_spec.zag ft_main.zag; do
  grep -q "901\|902" "$f" && fail "K10: $f contains world literals"
done

"$ZNC" build ft_full.zag -o ft_bin > ft_compile.txt 2>&1 || fail "znc build of ft_full.zag failed"
grep -q ": error" ft_compile.txt && fail "compiler reported an error (see ft_compile.txt)"

# run experiment 3x
for i in 1 2 3; do
  ./ft_bin > "ft_run$i.txt" 2> "ft_run$i.err"; echo "ft_bin run$i exit=$?"
done

# K3 determinism: byte-identical across the 3 runs
cmp ft_run1.txt ft_run2.txt || fail "K3: ft_run1/ft_run2 differ"
cmp ft_run1.txt ft_run3.txt || fail "K3: ft_run1/ft_run3 differ"
sha256sum ft_run1.txt

# K3 stderr must be empty
for f in ft_run1.err ft_run2.err ft_run3.err; do
  [ -s "$f" ] && fail "K3: non-empty stderr: $f"
done

# K3: exactly 84 CELL lines (4 cells x 21 arms)
[ "$(grep -c '^CELL ' ft_run1.txt)" = "84" ] || fail "K3: expected 84 CELL lines"

echo "--- kill bars ---"

field() { # $1=R $2=P-pattern $3=L $4=field -> value
  grep "^CELL R=$1 " ft_run1.txt | grep " P=$2 " | grep " L=$3 " \
    | grep -o " $4=[0-9-]*" | head -1 | cut -d= -f2
}
fixed_field() { field "$1" "$2" "-1" "$3"; }
adapt_field() { field "$1" "adapt" "$2" "$3"; }
guard_field() { field "$1" "guard" "$2" "$3"; }
fix2_field() { field "$1" "fix2" "$2" "$3"; }
qmean_field() { field "$1" "qmean" "$2" "$3"; }
adaptd_field() { field "$1" "adaptd" "$2" "$3"; }
j_val() { # $1=R $2=P $3=L -> J = rb + rf*L
  rb=$(field "$1" "$2" "$3" rebuilds); rf=$(field "$1" "$2" "$3" refusals)
  echo $(( rb + rf * $3 ))
}

# arm lists: P:L pairs (21 per cell; 19 adaptive)
ARMS="lazy:-1 eager:-1 adapt:1 adapt:3 adapt:7 adapt:10 guard:3 guard:7 guard:10 fix2:1 fix2:3 fix2:7 fix2:10 qmean:1 qmean:3 qmean:7 qmean:10 adaptd:1 adaptd:3 adaptd:7 adaptd:10"
ADAPTIVE="adapt:1 adapt:3 adapt:7 adapt:10 guard:3 guard:7 guard:10 fix2:1 fix2:3 fix2:7 fix2:10 qmean:1 qmean:3 qmean:7 qmean:10 adaptd:1 adaptd:3 adaptd:7 adaptd:10"

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
echo "PASS: K4a fixed arms anchor; cross-arm (D,Q) identical on all 4 cells (21 arms)"

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

# K4c: structural accounting on all 76 adaptive lines.
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
echo "PASS: K4c structural accounting on all 76 adaptive lines; lc=0 everywhere"

# K5a: exact replication of the parent's frozen lines (rename-only delta check).
for R in 21 60 82 120; do
  for pl in "adapt 1" "adapt 3" "adapt 7" "guard 3" "guard 7"; do
    set -- $pl
    pline=$(grep "^CELL R=$R " "$PFLRUN" | grep " P=$1 " | grep " L=$2 ")
    nline=$(grep "^CELL R=$R " ft_run1.txt | grep " P=$1 " | grep " L=$2 ")
    [ -n "$pline" ] || fail "K5a: parent line missing R=$R P=$1 L=$2"
    [ "$pline" = "$nline" ] || fail "K5a: R=$R P=$1 L=$2 line differs from parent frozen run"
  done
done
echo "PASS: K5a 20 adapt/guard lines byte-identical to parent frozen run (delta is surgical)"

# K5b: quirk fires identically in the new arms (pre-shift path unchanged).
for R in 21 60 82; do
  for P in fix2 qmean adaptd; do
    for L in 1 3 7 10; do
      tc=$(field $R $P $L tc); cm=$(field $R $P $L cm); Dc=$(field $R $P $L Dc)
      { [ "$tc" = "32" ] && [ "$cm" = "2" ] && [ "$Dc" = "0" ]; } \
        || fail "K5b: R=$R P=$P L=$L quirk not identical (tc=$tc cm=$cm Dc=$Dc)"
    done
  done
done
echo "PASS: K5b quirk fires identically (tc=32, cm=2, Dc=0) in fix2/qmean/adaptd on D32=0 cells"

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
  check_mono qmean $1 $2; check_mono adaptd $1 $2
done
for pair in "3 7" "7 10"; do
  set -- $pair; check_mono guard $1 $2
done
echo "PASS: K5c latency monotone non-decreasing in L within every adaptive arm (R=60)"

# K5d: L=1 identity -- fix2 L=1 line equals adapt L=1 line modulo P= field.
for R in 21 60 82 120; do
  aline=$(grep "^CELL R=$R " ft_run1.txt | grep " P=adapt " | grep " L=1 " | sed 's/ P=adapt / P=POL /')
  fline=$(grep "^CELL R=$R " ft_run1.txt | grep " P=fix2 "  | grep " L=1 " | sed 's/ P=fix2 / P=POL /')
  [ -n "$aline" ] || fail "K5d: R=$R adapt L=1 line missing"
  [ "$aline" = "$fline" ] || fail "K5d: R=$R fix2 L=1 differs from adapt L=1 beyond P= field"
done
echo "PASS: K5d fix2 L=1 identical to adapt L=1 modulo P= on all 4 cells (fixed bar = inherited bar at L=1)"

# K6: threshold redesign moves tf1 (theorems; R=60).
check_ease() { # $1=easier-P $2=harder-P $3=L : tf1_e <= tf1_h; flips_h>=1 -> flips_e>=1
  # First-flip ticks are read in extended reals: tf1=0 with flips=0
  # encodes +infinity (never flips), so the tick comparison applies
  # only when the harder arm flipped; the flips implication is the
  # operative clause otherwise (the easier arm rescuing where the
  # harder arm never flips is the redesign working, not a violation;
  # K7b requires exactly this at L=10).
  fle=$(field 60 $1 $3 flips); tfe=$(field 60 $1 $3 tf1)
  flh=$(field 60 $2 $3 flips); tfh=$(field 60 $2 $3 tf1)
  if [ "$flh" -ge 1 ]; then
    [ "$tfe" -le "$tfh" ] || fail "K6: P=$1 tf1=$tfe > P=$2 tf1=$tfh at L=$3 (bar-ease violated)"
    [ "$fle" -ge 1 ] || fail "K6: P=$2 flipped at L=$3 but easier P=$1 did not"
  fi
}
for L in 1 3 7 10; do
  check_ease fix2 adapt $L     # K6a
  check_ease qmean adapt $L    # K6b
  check_ease adaptd adapt $L   # K6c
  check_ease fix2 adaptd $L    # K6d
done
echo "PASS: K6a-d bar-ease orderings hold: tf1_fix2 <= tf1_adaptd <= tf1_adapt and tf1_qmean <= tf1_adapt (R=60)"
# K6e: the fixed bar's rescue timing is L-independent.
tfa1=$(adapt_field 60 1 tf1); fla1=$(adapt_field 60 1 flips); fda1=$(adapt_field 60 1 fdir)
for L in 1 3 7 10; do
  tff=$(fix2_field 60 $L tf1); flf=$(fix2_field 60 $L flips); fdf=$(fix2_field 60 $L fdir)
  echo "  L=$L: fix2(tf1=$tff flips=$flf fdir=$fdf) adapt(1)(tf1=$tfa1 flips=$fla1 fdir=$fda1)"
  { [ "$tff" = "$tfa1" ] && [ "$flf" = "$fla1" ] && [ "$fdf" = "$fda1" ]; } \
    || fail "K6e: L=$L fix2 rescue (tf1/flips/fdir) != adapt(1): fixed bar sees L after all"
done
echo "PASS: K6e fixed-bar rescue timing is L-independent (tf1/flips/fdir equal adapt L=1)"

# K7: J comparisons on R=60.
jf7=$(j_val 60 fix2 7); ja7=$(j_val 60 adapt 7)
je=$(j_val 60 eager -1); jf10=$(j_val 60 fix2 10)
echo "K7 R=60: J_fix2(7)=$jf7 J_adapt(7)=$ja7 J_fix2(10)=$jf10 J_eager=$je"
{ [ "$ja7" = "142" ]; } || fail "K7: R=60 J_adapt(7)=$ja7 (want 142; replication broken)"
[ "$jf7" -lt "$ja7" ] || fail "K7a: R=60 J_fix2(7)=$jf7 not < J_adapt(7)=$ja7"
echo "PASS: K7a fixed threshold improves J at L=7 ($jf7 < $ja7)"
[ "$jf10" -lt "$je" ] || fail "K7b: R=60 J_fix2(10)=$jf10 not < J_eager=$je"
echo "PASS: K7b fixed threshold restores positive rescue value at L=10 ($jf10 < $je)"

# K8a: quirk exonerated -- guard flip ticks identical to adapt (R=60).
for L in 3 7 10; do
  tfa=$(adapt_field 60 $L tf1); fla=$(adapt_field 60 $L flips); fda=$(adapt_field 60 $L fdir)
  tfg=$(guard_field 60 $L tf1); flg=$(guard_field 60 $L flips); fdg=$(guard_field 60 $L fdir)
  { [ "$tfa" = "$tfg" ] && [ "$fla" = "$flg" ] && [ "$fda" = "$fdg" ]; } \
    || fail "K8a: L=$L guard/adapt flip ticks differ (exoneration broken)"
done
echo "PASS: K8a guard/adapt tick-identity replicated: latency is a flip-rule property"
# K8b: the redesign moves tf1 with identical quirk fields.
tf_adapt7=$(adapt_field 60 7 tf1); tf_fix27=$(fix2_field 60 7 tf1)
tf_qmean7=$(qmean_field 60 7 tf1); tf_adaptd7=$(adaptd_field 60 7 tf1)
distinct=$(for t in $tf_adapt7 $tf_fix27 $tf_qmean7 $tf_adaptd7; do echo "$t"; done | sort -u | wc -l)
echo "K8b R=60 L=7 tf1: adapt=$tf_adapt7 fix2=$tf_fix27 qmean=$tf_qmean7 adaptd=$tf_adaptd7 ($distinct distinct)"
[ "$distinct" -ge 2 ] || fail "K8b: tf1 identical across all four threshold arms (redesign is a no-op)"
for P in adapt fix2 qmean adaptd; do
  tc=$(field 60 $P 7 tc); cm=$(field 60 $P 7 cm); Dc=$(field 60 $P 7 Dc)
  { [ "$tc" = "32" ] && [ "$cm" = "2" ] && [ "$Dc" = "0" ]; } \
    || fail "K8b: R=60 P=$P L=7 quirk fields differ (tc=$tc cm=$cm Dc=$Dc)"
done
echo "PASS: K8b tf1 spread across threshold arms with identical quirk fields: flip-rule property"

# K9a: bar-ease flips implication holds on every cell (mechanism integrity).
for R in 21 60 82 120; do
  for L in 1 3 7 10; do
    fla=$(field $R adapt $L flips)
    if [ "$fla" -ge 1 ]; then
      for P in fix2 qmean adaptd; do
        fle=$(field $R $P $L flips)
        [ "$fle" -ge 1 ] || fail "K9a: R=$R L=$L adapt flipped but $P did not"
      done
    fi
  done
done
echo "PASS: K9a bar-ease flips implication holds on all 4 cells"

# K10 hygiene: ASCII-only lane sources
if LC_ALL=C grep -l '[^[:print:][:space:]]' PREREG.md NAMECHECK.md ft_spec.zag ft_main.zag ft_build.sh 2>/dev/null; then
  fail "K10: non-ASCII byte found"
fi
echo "PASS: K10 ASCII-only, no world literals, one fn main per binary, reused sources unmodified, da_learn.zag untouched, parent lane unedited"

echo "ALL KILL BARS PASS"
