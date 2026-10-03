#!/bin/bash
# at_build.sh -- SPEC-ABSTENTION-TRAP: build + run + verify.
# Usage: ./at_build.sh  (run from this directory)
# safebin PATH is mandatory; the pinned znc builds at_bin; at_bin runs
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
PARENT="$D/../spec_regime_change"
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
         at_spec.zag at_main.zag; do
  [ -f "$f" ] || fail "missing source: $f"
done
# K8 (part): reused sources byte-unmodified (no unstaged diff vs HEAD)
for f in "$DA/da_base.zag" "$DA/da_module.zag" "$DA/da_learn.zag" \
         "$RB/rb_world.zag" "$RB/rb_fix.zag" \
         "$ET/et_world.zag" "$ET/et_spec.zag" \
         "$RR/rr_spec.zag" "$LD/ld_spec.zag"; do
  /usr/bin/git diff --quiet -- "$f" || fail "K8: reused source modified: $f"
done
# K8 (part): da_learn.zag explicitly unmodified (separate lane only)
/usr/bin/git diff --quiet -- "$DA/da_learn.zag" || fail "K8: da_learn.zag modified"

# assemble experiment binary: all reused sources byte-unmodified +
# abstention-trap policy layer + harness main
cat "$DA/da_base.zag" "$RB/rb_world.zag" "$ET/et_world.zag" "$DA/da_module.zag" \
    "$DA/da_learn.zag" "$RB/rb_fix.zag" "$ET/et_spec.zag" "$RR/rr_spec.zag" \
    "$LD/ld_spec.zag" at_spec.zag at_main.zag > at_full.zag
[ "$(grep -c '^fn main(' at_full.zag)" = "1" ] || fail "expected exactly one fn main in at_full.zag"
# K8 (part): no world literals in new lane sources
for f in at_spec.zag at_main.zag; do
  grep -q "901\|902" "$f" && fail "K8: $f contains world literals"
done

"$ZNC" build at_full.zag -o at_bin > at_compile.txt 2>&1 || fail "znc build of at_full.zag failed"
grep -q ": error" at_compile.txt && fail "compiler reported an error (see at_compile.txt)"

# run experiment 3x
for i in 1 2 3; do
  ./at_bin > "at_run$i.txt" 2> "at_run$i.err"; echo "at_bin run$i exit=$?"
done

# K3 determinism: byte-identical across the 3 runs
cmp at_run1.txt at_run2.txt || fail "K3: at_run1/at_run2 differ"
cmp at_run1.txt at_run3.txt || fail "K3: at_run1/at_run3 differ"
sha256sum at_run1.txt

# K3 stderr must be empty
for f in at_run1.err at_run2.err at_run3.err; do
  [ -s "$f" ] && fail "K3: non-empty stderr: $f"
done

# K3: exactly 60 CELL lines (6 cells x 10 arms)
[ "$(grep -c '^CELL ' at_run1.txt)" = "60" ] || fail "K3: expected 60 CELL lines"

echo "--- kill bars ---"

field() { # $1=R $2=P-pattern $3=L $4=field -> value
  grep "^CELL R=$1 " at_run1.txt | grep " P=$2 " | grep " L=$3 " \
    | grep -o " $4=[0-9-]*" | head -1 | cut -d= -f2
}
fixed_field()  { field "$1" "$2" "-1" "$3"; }
adapt_field()  { field "$1" "adapt" "$2" "$3"; }
rechk_field()  { field "$1" "rechk" "$2" "$3"; }
j_val() { # $1=R $2=P $3=L -> J = rb + rf*L
  rb=$(field "$1" "$2" "$3" rebuilds); rf=$(field "$1" "$2" "$3" refusals)
  echo $(( rb + rf * $3 ))
}

# K4a: per-cell cross-arm (D,Q) identity + fixed-arm structural identities.
for R in 10 12 11 1 14 13; do
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
    dr=$(rechk_field $R $L D); qr=$(rechk_field $R $L Q)
    { [ "$da" = "$dd" ] && [ "$qa" = "$qd" ] && \
      [ "$dr" = "$dd" ] && [ "$qr" = "$qd" ]; } \
      || fail "K4a: R=$R L=$L adapt/rechk (D,Q) != lazy ($dd,$qd)"
  done
done
echo "PASS: K4a fixed arms anchor; cross-arm (D,Q) identical on all 6 cells"

# K4b: arrival splits show the shift (lazy arm).
dpre12=$(fixed_field 12 lazy Dpre); qpre12=$(fixed_field 12 lazy Qpre)
dpost12=$(fixed_field 12 lazy Dpost); qpost12=$(fixed_field 12 lazy Qpost)
{ [ "$qpost12" = "128" ] && [ "$dpost12" -lt 32 ] && \
  [ "$dpre12" -lt 32 ] && [ "$qpre12" -lt 32 ]; } \
  || fail "K4b: R=12 splits=($dpre12,$qpre12,$dpost12,$qpost12), want (<32,<32,<32,128)"
dpre11=$(fixed_field 11 lazy Dpre); qpre11=$(fixed_field 11 lazy Qpre)
dpost11=$(fixed_field 11 lazy Dpost); qpost11=$(fixed_field 11 lazy Qpost)
{ [ "$dpost11" = "128" ] && [ "$qpost11" -lt 32 ] && \
  [ "$dpre11" -lt 32 ] && [ "$qpre11" -lt 32 ]; } \
  || fail "K4b: R=11 splits=($dpre11,$qpre11,$dpost11,$qpost11), want (<32,<32,128,<32)"
dpre14=$(fixed_field 14 lazy Dpre); qpre14=$(fixed_field 14 lazy Qpre)
dpost14=$(fixed_field 14 lazy Dpost); qpost14=$(fixed_field 14 lazy Qpost)
{ [ "$qpost14" = "128" ] && [ "$dpost14" -lt 32 ] && \
  [ "$dpre14" -lt 64 ] && [ "$qpre14" -lt 64 ]; } \
  || fail "K4b: R=14 splits=($dpre14,$qpre14,$dpost14,$qpost14), want (<64,<64,<32,128)"
dpre13=$(fixed_field 13 lazy Dpre); qpre13=$(fixed_field 13 lazy Qpre)
dpost13=$(fixed_field 13 lazy Dpost); qpost13=$(fixed_field 13 lazy Qpost)
{ [ "$qpost13" = "128" ] && [ "$dpost13" -lt 32 ] && \
  [ "$dpre13" -lt 64 ] && [ "$qpre13" -lt 64 ]; } \
  || fail "K4b: R=13 splits=($dpre13,$qpre13,$dpost13,$qpost13), want (<64,<64,<32,128)"
dd10=$(fixed_field 10 lazy D); qd10=$(fixed_field 10 lazy Q)
{ [ "$dd10" -lt 48 ] && [ "$qd10" -lt 48 ]; } \
  || fail "K4b: R=10 sparse stationary (D,Q)=($dd10,$qd10), want <48 each"
echo "PASS: K4b regime splits: T1/T2/T4/T5 deterministic 128-pins, T0 sparse"

# K4c: T3 (R=1) cross-lane identity vs parent spec_regime_change R=1.
# My line minus the trailing " lc=0" must be byte-equal to the parent line.
[ -f "$PARENT/rc_run1.txt" ] || fail "K4c: parent rc_run1.txt missing"
for key in "P=lazy L=-1" "P=eager L=-1" "P=adapt L=0" "P=adapt L=1" \
           "P=adapt L=3" "P=adapt L=7"; do
  mine=$(grep "^CELL R=1 " at_run1.txt | grep " $key " | sed 's/ lc=[0-9-]*$//')
  par=$(grep "^CELL R=1 " "$PARENT/rc_run1.txt" | grep " $key ")
  [ "$mine" = "$par" ] || fail "K4c: R=1 $key line differs from parent R1 (rebuild changed inherited behavior)"
done
echo "PASS: K4c T3 pol-0/1/2 lines byte-equal parent R1 lines (modulo lc)"

# K4d: T3 recheck identical to adapt on all numeric fields.
awk '
/^CELL R=1 / {
  orig=$0; lkey=""
  for(i=1;i<=NF;i++) if($i ~ /^L=/){ lkey=substr($i,3) }
  sub(/ P=[a-z]+/, "", orig)
  if($0 ~ / P=adapt /) a[lkey]=orig
  if($0 ~ / P=rechk /) r[lkey]=orig
}
END{
  bad=0
  for(k in a){
    if(!(k in r)){ print "missing rechk L="k; bad=1 }
    else if(a[k] != r[k]){ print "MISMATCH L="k; bad=1 }
  }
  if(bad==0) print "IDENTICAL"
}' at_run1.txt | grep -q IDENTICAL || fail "K4d: R=1 rechk not field-equal to adapt"
echo "PASS: K4d T3 recheck field-equal adapt (recheck changes nothing when pre-shift decisive)"

# K5: trap occurrence + boundary.
n12=0; n13=0; n10=0; n11=0; n14=0; n1=0
for L in 0 1 3 7; do
  [ "$(adapt_field 12 $L cm)" = "0" ] && n12=$(( n12 + 1 ))
  [ "$(adapt_field 13 $L cm)" = "0" ] && n13=$(( n13 + 1 ))
  [ "$(adapt_field 10 $L cm)" = "0" ] && n10=$(( n10 + 1 ))
  [ "$(adapt_field 11 $L cm)" = "0" ] && n11=$(( n11 + 1 ))
  [ "$(adapt_field 14 $L cm)" = "0" ] && n14=$(( n14 + 1 ))
  [ "$(adapt_field 1 $L cm)" = "0" ] && n1=$(( n1 + 1 ))
done
echo "K5 FINDING abstention counts (adapt cm=0): T0(R=10)=$n10 T1(R=12)=$n12 T2(R=11)=$n11 T3(R=1)=$n1 T4(R=14)=$n14 T5(R=13)=$n13"
[ "$(adapt_field 12 0 cm)" = "0" ] || fail "K5a: R=12 adapt L=0 cm != 0 (trap did not trigger)"
[ "$(adapt_field 12 1 cm)" = "0" ] || fail "K5a: R=12 adapt L=1 cm != 0 (trap did not trigger)"
[ "$n12" -ge 3 ] || fail "K5b: n_abstain(R=12)=$n12 < 3 (trap weak at sparse end)"
[ "$n13" -le 3 ] || fail "K5b: n_abstain(R=13)=$n13 > 3 (trap not weaker at dense end)"
[ "$(adapt_field 13 7 cm)" = "2" ] || fail "K5c: R=13 adapt L=7 cm != 2 (dense end did not escape via eager commit)"
echo "PASS: K5a trap triggers on robust core; K5b boundary ordering; K5c dense end escapes"

# K6a: main recheck late-commit on T1 L=1.
lc61=$(rechk_field 12 1 lc); sel61=$(rechk_field 12 1 sel)
cm61=$(rechk_field 12 1 cm); tc61=$(rechk_field 12 1 tc)
echo "K6a R=12 rechk L=1: lc=$lc61 sel=$sel61 cm=$cm61 tc=$tc61"
{ [ "$lc61" = "1" ] && [ "$sel61" = "1" ] && [ "$cm61" = "2" ] && \
  [ "$tc61" -gt 128 ] && [ "$tc61" -le 176 ]; } \
  || fail "K6a: R=12 rechk L=1 not a prompt correct-direction late eager commit"
echo "PASS: K6a late eager commit, correct direction, prompt"

# K6b: L=0 safety on all recheck arms.
for R in 10 12 11 1 14 13; do
  s0=$(rechk_field $R 0 sel); c0=$(rechk_field $R 0 cm)
  { [ "$s0" = "0" ] && [ "$c0" != "2" ]; } \
    || fail "K6b: R=$R rechk L=0 sel=$s0 cm=$c0 (eager at L=0)"
done
{ [ "$(rechk_field 12 0 cm)" = "0" ] && [ "$(rechk_field 12 0 lc)" = "0" ]; } \
  || fail "K6b: R=12 rechk L=0 not clean budget-default"
echo "PASS: K6b never eager at L=0"

# K6c: no thrash.
read rtot rmax r10bad <<< "$(
awk '
function F(n,   i) {
  for (i=1;i<=NF;i++) if (index($i, n"=")==1) return substr($i, length(n)+2)+0
  return -999999
}
/^CELL / {
  for(i=1;i<=NF;i++) if(index($i,"P=")==1) p=substr($i,3)
  if(p != "rechk") next
  R=F("R")+0; L=F("L")+0; fl=F("flips")+0
  tot+=fl
  if(fl>mx) mx=fl
  if(R==10 && fl!=0) bad10++
}
END{ printf "%d %d %d", tot, mx, bad10 }' at_run1.txt)"
echo "K6c rechk: total_flips=$rtot max_per_ep=$rmax R10_nonzero=$r10bad"
[ "$rmax" -le 2 ] || fail "K6c: a rechk episode flipped $rmax times (> 2)"
[ "$rtot" -le 4 ] || fail "K6c: total rechk flips $rtot > 4 (thrash)"
[ "$r10bad" = "0" ] || fail "K6c: R=10 rechk flipped under stationary sparsity"
echo "PASS: K6c no thrash"

# K6d: T2 mirror -- recheck must not invent eager; J identical per L.
for L in 0 1 3 7; do
  s11=$(rechk_field 11 $L sel)
  [ "$s11" = "0" ] || fail "K6d: R=11 rechk L=$L sel=1 (spurious eager where lazy-optimal)"
  jr=$(j_val 11 rechk $L); ja=$(j_val 11 adapt $L)
  [ "$jr" = "$ja" ] || fail "K6d: R=11 L=$L J_rechk=$jr != J_adapt=$ja"
  fr=$(rechk_field 11 $L flips); fa=$(adapt_field 11 $L flips)
  [ "$fr" = "$fa" ] || fail "K6d: R=11 L=$L flips differ ($fr vs $fa)"
done
echo "PASS: K6d T2 recheck harmless (no eager, J identical)"

# K6e/f: late-commit consistency + structural accounting on all 40
# adapt + rechk lines.
for R in 10 12 11 1 14 13; do
  rod=$(fixed_field $R lazy rebuilds); rrf=$(fixed_field $R lazy refusals)
  for P in adapt rechk; do
    for L in 0 1 3 7; do
      if [ "$P" = "adapt" ]; then
        cm=$(adapt_field $R $L cm); tc=$(adapt_field $R $L tc)
        flips=$(adapt_field $R $L flips); pflips=$(adapt_field $R $L pflips)
        tf1=$(adapt_field $R $L tf1); fdir=$(adapt_field $R $L fdir)
        tf2=$(adapt_field $R $L tf2); rb=$(adapt_field $R $L rebuilds)
        an=$(adapt_field $R $L answered); rf=$(adapt_field $R $L refusals)
        kb=$(adapt_field $R $L kb); qq=$(adapt_field $R $L Q)
        od=$(adapt_field $R $L od); rs=$(adapt_field $R $L rs)
        dd=$(adapt_field $R $L D); Dc=$(adapt_field $R $L Dc)
        Qc=$(adapt_field $R $L Qc); lc=$(adapt_field $R $L lc)
        dpre=$(adapt_field $R $L Dpre); dpost=$(adapt_field $R $L Dpost)
        qpre=$(adapt_field $R $L Qpre); qpost=$(adapt_field $R $L Qpost)
      else
        cm=$(rechk_field $R $L cm); tc=$(rechk_field $R $L tc)
        flips=$(rechk_field $R $L flips); pflips=$(rechk_field $R $L pflips)
        tf1=$(rechk_field $R $L tf1); fdir=$(rechk_field $R $L fdir)
        tf2=$(rechk_field $R $L tf2); rb=$(rechk_field $R $L rebuilds)
        an=$(rechk_field $R $L answered); rf=$(rechk_field $R $L refusals)
        kb=$(rechk_field $R $L kb); qq=$(rechk_field $R $L Q)
        od=$(rechk_field $R $L od); rs=$(rechk_field $R $L rs)
        dd=$(rechk_field $R $L D); Dc=$(rechk_field $R $L Dc)
        Qc=$(rechk_field $R $L Qc); lc=$(rechk_field $R $L lc)
        dpre=$(rechk_field $R $L Dpre); dpost=$(rechk_field $R $L Dpost)
        qpre=$(rechk_field $R $L Qpre); qpost=$(rechk_field $R $L Qpost)
      fi
      tag="R=$R P=$P L=$L"
      { [ "$(( dpre + dpost ))" = "$dd" ] && [ "$(( qpre + qpost ))" = "$qq" ]; } \
        || fail "K6f: $tag arrival splits do not sum to (D,Q)"
      { [ "$an" = "$qq" ] && [ "$kb" = "$(( qq * 2 ))" ] && \
        [ "$rb" = "$(( od + rs ))" ] && [ "$rf" = "$od" ]; } \
        || fail "K6f: $tag an/kb/rb/rf identity broken"
      { { [ "$pflips" = "0" ] && [ "$tf1" = "0" ] && [ "$fdir" = "0" ]; } || \
        { [ "$pflips" != "0" ] && [ "$tf1" != "0" ] && [ "$fdir" != "0" ]; }; } \
        || fail "K6f: $tag pflips/tf1/fdir inconsistent ($pflips/$tf1/$fdir)"
      if [ "$pflips" != "0" ]; then
        { [ "$tf1" -gt 128 ] && [ "$tf1" -le 256 ]; } \
          || fail "K6f: $tag post-shift flip tick tf1=$tf1 not in (128,256]"
      fi
      if [ "$tf2" != "0" ]; then
        { [ "$tf2" -ge "$tf1" ] && [ "$tf2" -le 256 ]; } \
          || fail "K6f: $tag tf2=$tf2 inconsistent with tf1=$tf1"
      fi
      [ "$flips" -ge "$pflips" ] || fail "K6f: $tag flips=$flips < pflips=$pflips"
      # K6e: late-commit consistency.
      if [ "$P" = "rechk" ] && [ "$tc" -gt 128 ]; then
        [ "$lc" = "1" ] || fail "K6e: $tag tc=$tc > 128 but lc=0"
      else
        [ "$lc" = "0" ] || fail "K6e: $tag lc=1 without (rechk and tc>128)"
      fi
      if [ "$lc" = "1" ]; then
        { [ "$cm" = "1" ] || [ "$cm" = "2" ]; } \
          || fail "K6e: $tag lc=1 but cm=$cm not in {1,2}"
      fi
      if [ "$flips" = "0" ]; then
        if [ "$cm" = "0" ] || [ "$cm" = "1" ]; then
          { [ "$od" = "$rod" ] && [ "$rf" = "$rrf" ] && [ "$rs" = "0" ]; } \
            || fail "K6f: $tag cm=$cm lc=$lc not field-equal to lazy twin"
        fi
        if [ "$cm" = "2" ]; then
          exprs=$(( 1 + dd - Dc ))
          [ "$rs" = "$exprs" ] \
            || fail "K6f: $tag cm=2 rs=$rs != 1+(D-Dc)=$exprs"
          { [ "$od" -le "$Dc" ] && [ "$od" -le "$Qc" ]; } \
            || fail "K6f: $tag cm=2 od=$od > min(Dc,Qc)=($Dc,$Qc)"
        fi
      fi
    done
  done
done
echo "PASS: K6e late-commit consistency; K6f structural accounting on all 40 adapt+rechk lines"

# K7: economics. J = rb + rf*L.
echo "K7 economics (J_adapt vs J_rechk):"
for R in 12 14 13; do
  for L in 1 3 7; do
    acm=$(adapt_field $R $L cm); rlc=$(rechk_field $R $L lc)
    rsel=$(rechk_field $R $L sel)
    if [ "$acm" = "0" ] && [ "$rlc" = "1" ] && [ "$rsel" = "1" ]; then
      ja=$(j_val $R adapt $L); jr=$(j_val $R rechk $L)
      echo "  R=$R L=$L trapped+late-eager: J_adapt=$ja J_rechk=$jr"
      [ "$jr" -lt "$ja" ] || fail "K7a/d: R=$R L=$L J_rechk=$jr not < J_adapt=$ja"
    fi
  done
done
echo "PASS: K7a/d wherever the trap triggered and the recheck fired eager, recheck wins strictly"
for L in 0 1 3 7; do
  jr=$(j_val 11 rechk $L); ja=$(j_val 11 adapt $L)
  [ "$jr" = "$ja" ] || fail "K7b: R=11 L=$L J_rechk=$jr != J_adapt=$ja"
  jr=$(j_val 10 rechk $L); ja=$(j_val 10 adapt $L)
  [ "$jr" -le "$(( ja + 1 ))" ] || fail "K7c: R=10 L=$L J_rechk=$jr > J_adapt+1=$(( ja + 1 ))"
done
echo "PASS: K7b T2 J identical; K7c T0 J within +1"

# K8 hygiene: ASCII-only lane sources
if LC_ALL=C grep -l '[^[:print:][:space:]]' PREREG.md NAMECHECK.md at_spec.zag at_main.zag at_build.sh 2>/dev/null; then
  fail "K8: non-ASCII byte found"
fi
echo "PASS: K8 ASCII-only, no world literals, one fn main per binary, reused sources unmodified, da_learn.zag untouched"

echo "ALL KILL BARS PASS"
