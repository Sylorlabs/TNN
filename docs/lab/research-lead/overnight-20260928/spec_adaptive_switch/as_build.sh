#!/bin/bash
# as_build.sh -- SPEC-ADAPTIVE-SWITCH: build + run + verify.
# Usage: ./as_build.sh  (run from this directory)
# safebin PATH is mandatory; the pinned znc builds as_bin and
# as_calib_bin; as_bin runs 3x; sha256/cmp equality across the three
# runs is checked; the frozen kill bars from PREREG.md are adjudicated.
export PATH="$HOME/safebin"
set -u
D="$(cd "$(dirname "$0")" && pwd)"
DA="$D/../disagreement_attribution"
RB="$D/../spec_relationblind"
ET="$D/../spec_epochtag"
RR="$D/../spec_refusal_recovery"
LD="$D/../spec_lazy_default"
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
         as_spec.zag as_main.zag as_calib.zag; do
  [ -f "$f" ] || fail "missing source: $f"
done
# K9 (part): reused sources byte-unmodified (no unstaged diff vs HEAD)
for f in "$DA/da_base.zag" "$DA/da_module.zag" "$DA/da_learn.zag" \
         "$RB/rb_world.zag" "$RB/rb_fix.zag" \
         "$ET/et_world.zag" "$ET/et_spec.zag" \
         "$RR/rr_spec.zag" "$LD/ld_spec.zag"; do
  /usr/bin/git diff --quiet -- "$f" || fail "K9: reused source modified: $f"
done
# K9 (part): da_learn.zag explicitly unmodified (separate lane only)
/usr/bin/git diff --quiet -- "$DA/da_learn.zag" || fail "K9: da_learn.zag modified"

# assemble experiment binary: all reused sources byte-unmodified +
# adaptive policy layer + harness main
cat "$DA/da_base.zag" "$RB/rb_world.zag" "$ET/et_world.zag" "$DA/da_module.zag" \
    "$DA/da_learn.zag" "$RB/rb_fix.zag" "$ET/et_spec.zag" "$RR/rr_spec.zag" \
    "$LD/ld_spec.zag" as_spec.zag as_main.zag > as_full.zag
[ "$(grep -c '^fn main(' as_full.zag)" = "1" ] || fail "expected exactly one fn main in as_full.zag"
# assemble calibration binary: same reused set + calibration main
cat "$DA/da_base.zag" "$RB/rb_world.zag" "$ET/et_world.zag" "$DA/da_module.zag" \
    "$DA/da_learn.zag" "$RB/rb_fix.zag" "$ET/et_spec.zag" "$RR/rr_spec.zag" \
    as_calib.zag > as_calib_full.zag
[ "$(grep -c '^fn main(' as_calib_full.zag)" = "1" ] || fail "expected exactly one fn main in as_calib_full.zag"
# K9 (part): no world literals in new lane sources
for f in as_spec.zag as_main.zag as_calib.zag; do
  grep -q "901\|902" "$f" && fail "K9: $f contains world literals"
done

"$ZNC" build as_full.zag -o as_bin > as_compile.txt 2>&1 || fail "znc build of as_full.zag failed"
grep -q ": error" as_compile.txt && fail "compiler reported an error (see as_compile.txt)"
"$ZNC" build as_calib_full.zag -o as_calib_bin > as_calib_compile.txt 2>&1 || fail "znc build of as_calib_full.zag failed"
grep -q ": error" as_calib_compile.txt && fail "compiler reported an error (see as_calib_compile.txt)"

# run experiment 3x
for i in 1 2 3; do
  ./as_bin > "as_run$i.txt" 2> "as_run$i.err"; echo "as_bin run$i exit=$?"
done

# K3 determinism: byte-identical across the 3 runs
cmp as_run1.txt as_run2.txt || fail "K3: as_run1/as_run2 differ"
cmp as_run1.txt as_run3.txt || fail "K3: as_run1/as_run3 differ"
sha256sum as_run1.txt

# K3 stderr must be empty
for f in as_run1.err as_run2.err as_run3.err; do
  [ -s "$f" ] && fail "K3: non-empty stderr: $f"
done

# K3: exactly 150 CELL lines (25 cells x 6 arms)
[ "$(grep -c '^CELL ' as_run1.txt)" = "150" ] || fail "K3: expected 150 CELL lines"

# K8 calibration (nondeterministic timing; recorded, not identity-barred)
{ echo "# as_calib wall-clock run at $(date -u +%Y-%m-%dT%H:%M:%SZ)"; ./as_calib_bin; } > as_calib.txt 2> as_calib.err
cat as_calib.txt
grep -q "^CALIB rebuild_ns_min=[1-9][0-9]* iters=200$" as_calib.txt || fail "K8: no valid CALIB line in as_calib.txt"
echo "PASS: K8 genuine positive wall-clock rebuild measurement recorded"

echo "--- kill bars ---"

fixed_field() { # $1=M $2=N $3=P $4=field -> value
  grep "^CELL M=$1 N=$2 P=$3 " as_run1.txt | grep -o "$4=[0-9-]*" | head -1 | cut -d= -f2
}
adapt_field() { # $1=M $2=N $3=L $4=field -> value
  grep "^CELL M=$1 N=$2 P=adapt L=$3 " as_run1.txt | grep -o "$4=[0-9-]*" | head -1 | cut -d= -f2
}

for M in 1 2 4 8 16; do
  for N in 1 2 4 8 16; do
    dd=$(fixed_field $M $N lazy D);       qd=$(fixed_field $M $N lazy Q)
    rd=$(fixed_field $M $N lazy rebuilds); ad=$(fixed_field $M $N lazy answered)
    fd=$(fixed_field $M $N lazy refusals); kd=$(fixed_field $M $N lazy kb)
    de=$(fixed_field $M $N eager D);       qe=$(fixed_field $M $N eager Q)
    re=$(fixed_field $M $N eager rebuilds); ae=$(fixed_field $M $N eager answered)
    fe=$(fixed_field $M $N eager refusals); ke=$(fixed_field $M $N eager kb)
    if [ "$dd" -lt "$qd" ]; then m=$dd; else m=$qd; fi
    # K4: fixed lazy reproduces parent default economics
    { [ "$rd" = "$m" ] && [ "$ad" = "$qd" ] && [ "$fd" = "$rd" ] && [ "$kd" = "$(( qd * 2 ))" ]; } \
      || fail "K4: M=$M N=$N lazy: rebuilds=$rd answered=$ad refusals=$fd kb=$kd"
    # K4: fixed eager reproduces parent eager economics
    { [ "$re" = "$de" ] && [ "$ae" = "$qe" ] && [ "$fe" = "0" ] && [ "$ke" = "$(( qe * 2 ))" ]; } \
      || fail "K4: M=$M N=$N eager: rebuilds=$re answered=$ae refusals=$fe kb=$ke"
  done
done
echo "PASS: K4 fixed arms reproduce SPEC-LAZY-DEFAULT economics on all 25 cells"

# K5: frozen selection table. Rows M=1,2,4,8,16 outer; N=1,2,4,8,16 inner.
# Built from 5-char row chunks (each chunk independently checkable);
# the length guard fails loudly on any transcription slip.
S0="LLLLL""LLLLL""LLLLL""LLLLL""LLLLL"
S1="ELLLL""EELLL""EEELL""EEEEL""EEEEE"
S3="EELLL""EEELL""EEEEL""EEEEE""EEEEE"
S7="EEELL""EEEEL""EEEEE""EEEEE""EEEEE"
for S in "$S0" "$S1" "$S3" "$S7"; do
  [ "${#S}" = "25" ] || fail "K5: selection string not 25 chars: $S"
done
li=0
for L in 0 1 3 7; do
  case $li in
    0) S="$S0";; 1) S="$S1";; 2) S="$S3";; 3) S="$S7";;
  esac
  mi=0
  for M in 1 2 4 8 16; do
    ni=0
    for N in 1 2 4 8 16; do
      idx=$(( mi * 5 + ni ))
      expch=${S:idx:1}
      [ "$expch" = "E" ] && exp=1 || exp=0
      sel=$(adapt_field $M $N $L sel)
      [ "$sel" = "$exp" ] || fail "K5: M=$M N=$N L=$L sel=$sel != frozen $exp ($expch)"
      # K5 (part): sel consistent with the rule on the line's own Dw,Qw,L
      Dw=$(adapt_field $M $N $L Dw); Qw=$(adapt_field $M $N $L Qw)
      [ "$Dw" = "$(( 16 / M ))" ] || fail "K5: M=$M N=$N L=$L Dw=$Dw != 16/M=$(( 16 / M ))"
      [ "$Qw" = "$(( 16 / N ))" ] || fail "K5: M=$M N=$N L=$L Qw=$Qw != 16/N=$(( 16 / N ))"
      rulesel=0
      if [ "$Dw" -le "$Qw" ]; then
        [ "$L" -gt 0 ] && rulesel=1 || rulesel=0
      else
        [ "$(( L * Qw ))" -gt "$(( Dw - Qw ))" ] && rulesel=1 || rulesel=0
      fi
      [ "$sel" = "$rulesel" ] || fail "K5: M=$M N=$N L=$L sel=$sel != rule-on-own-fields $rulesel"
      # K6 (part): price fields are the exact measured rational
      pnum=$(adapt_field $M $N $L pnum); pden=$(adapt_field $M $N $L pden)
      if [ "$Dw" -gt "$Qw" ]; then expnum=$(( Dw - Qw )); else expnum=0; fi
      { [ "$pnum" = "$expnum" ] && [ "$pden" = "$Qw" ]; } \
        || fail "K6: M=$M N=$N L=$L pnum/pden=$pnum/$pden != $expnum/$Qw"
      ni=$(( ni + 1 ))
    done
    mi=$(( mi + 1 ))
  done
  li=$(( li + 1 ))
done
echo "PASS: K5 all 100 adapt selections match the frozen table and the rule on own observed fields"

# K5 boundary strictness: the 9 equality cells (L == price) must be lazy
for spec in "1 2 1" "2 4 1" "4 8 1" "8 16 1" "1 4 3" "2 8 3" "4 16 3" "1 8 7" "2 16 7"; do
  set -- $spec
  [ "$(adapt_field $1 $2 $3 sel)" = "0" ] || fail "K5-boundary: M=$1 N=$2 L=$3 not lazy at equality"
done
echo "PASS: K5-boundary all 9 strict-equality cells stay lazy (strict >)"

for M in 1 2 4 8 16; do
  for N in 1 2 4 8 16; do
    rd=$(fixed_field $M $N lazy rebuilds); ad=$(fixed_field $M $N lazy answered); fd=$(fixed_field $M $N lazy refusals)
    for L in 0 1 3 7; do
      sel=$(adapt_field $M $N $L sel)
      rb=$(adapt_field $M $N $L rebuilds); an=$(adapt_field $M $N $L answered); rf=$(adapt_field $M $N $L refusals)
      kb=$(adapt_field $M $N $L kb); qq=$(adapt_field $M $N $L Q)
      Dw=$(adapt_field $M $N $L Dw); Qw=$(adapt_field $M $N $L Qw); dd=$(adapt_field $M $N $L D)
      # K6: answered=Q, kb=2Q on every adapt line
      { [ "$an" = "$qq" ] && [ "$kb" = "$(( qq * 2 ))" ]; } \
        || fail "K6: M=$M N=$N L=$L answered=$an kb=$kb Q=$qq"
      if [ "$sel" = "0" ]; then
        # K6: lazy-selected adapt line is field-equal to its fixed-lazy twin
        { [ "$rb" = "$rd" ] && [ "$an" = "$ad" ] && [ "$rf" = "$fd" ]; } \
          || fail "K6: M=$M N=$N L=$L sel=0 differs from lazy twin: rb=$rb/$rd an=$an/$ad rf=$rf/$fd"
      else
        # K6: eager-selected: warmup ran lazy, post-switch eager (1 restamp/drift, 0 refusals)
        if [ "$Dw" -lt "$Qw" ]; then mw=$Dw; else mw=$Qw; fi
        exprb=$(( mw + dd - Dw )); exprf=$mw
        { [ "$rb" = "$exprb" ] && [ "$rf" = "$exprf" ]; } \
          || fail "K6: M=$M N=$N L=$L sel=1: rb=$rb != $exprb rf=$rf != $exprf"
      fi
    done
  done
done
echo "PASS: K6 structural accounting on all 100 adapt lines"

# K7: portfolio totals J = rb + rf*L per L over the 25 cells
read adapt0 adapt1 adapt3 adapt7 lazy_rb lazy_rf eager_rb <<< "$(
awk '
/^CELL / {
  p=""; l=0; rb=0; rf=0
  for(i=1;i<=NF;i++){
    if($i ~ /^P=/){ p=substr($i,3) }
    else if($i ~ /^L=/){ l=substr($i,3)+0 }
    else if($i ~ /^rebuilds=/){ rb=substr($i,10)+0 }
    else if($i ~ /^refusals=/){ rf=substr($i,10)+0 }
  }
  if(p=="adapt"){ ja[l]+=rb+rf*l }
  else if(p=="lazy"){ lrb+=rb; lrf+=rf }
  else if(p=="eager"){ erb+=rb }
}
END{ printf "%d %d %d %d %d %d %d", ja[0], ja[1], ja[3], ja[7], lrb, lrf, erb }' as_run1.txt)"
echo "portfolio: adapt(L=0,1,3,7)=$adapt0,$adapt1,$adapt3,$adapt7 lazy_rb=$lazy_rb lazy_rf=$lazy_rf eager_rb=$eager_rb"
[ "$lazy_rb" = "1328" ] || fail "K7: lazy total rebuilds=$lazy_rb != 1328"
[ "$lazy_rf" = "1328" ] || fail "K7: lazy total refusals=$lazy_rf != 1328"
[ "$eager_rb" = "2480" ] || fail "K7: eager total rebuilds=$eager_rb != 2480"
# L=0: switch never fires; adapt ties lazy exactly
{ [ "$adapt0" = "1328" ] && [ "$(( lazy_rb + 0 * lazy_rf ))" = "1328" ]; } \
  || fail "K7: L=0 adapt=$adapt0 != 1328"
# L=1: adapt 1801 beats lazy 2656 and eager 2480
{ [ "$adapt1" = "1801" ] && [ "$(( lazy_rb + 1 * lazy_rf ))" = "2656" ]; } \
  || fail "K7: L=1 adapt=$adapt1 != 1801 or lazy=$(( lazy_rb + lazy_rf )) != 2656"
[ "$adapt1" -lt "$eager_rb" ] || fail "K7: L=1 adapt=$adapt1 not < eager=$eager_rb"
# L=3: adapt 2297 beats lazy 5312 and eager 2480
{ [ "$adapt3" = "2297" ] && [ "$(( lazy_rb + 3 * lazy_rf ))" = "5312" ]; } \
  || fail "K7: L=3 adapt=$adapt3 != 2297 or lazy=$(( lazy_rb + 3 * lazy_rf )) != 5312"
[ "$adapt3" -lt "$eager_rb" ] || fail "K7: L=3 adapt=$adapt3 not < eager=$eager_rb"
# L=7: adapt 2869 beats lazy 10624 (vs eager 2480: measured finding, not barred)
{ [ "$adapt7" = "2869" ] && [ "$(( lazy_rb + 7 * lazy_rf ))" = "10624" ]; } \
  || fail "K7: L=7 adapt=$adapt7 != 2869 or lazy=$(( lazy_rb + 7 * lazy_rf )) != 10624"
echo "PASS: K7 portfolio totals match frozen values; adapt beats lazy at all L>0, beats eager at L=1,3"

# K9 hygiene: ASCII-only lane sources
if LC_ALL=C grep -l '[^[:print:][:space:]]' PREREG.md NAMECHECK.md as_spec.zag as_main.zag as_calib.zag as_build.sh 2>/dev/null; then
  fail "K9: non-ASCII byte found"
fi
echo "PASS: K9 ASCII-only, no world literals, one fn main per binary, reused sources unmodified, da_learn.zag untouched"

echo "ALL KILL BARS PASS"
