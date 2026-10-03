#!/bin/bash
# rc_build.sh -- SPEC-REGIME-CHANGE: build + run + verify.
# Usage: ./rc_build.sh  (run from this directory)
# safebin PATH is mandatory; the pinned znc builds rc_bin; rc_bin runs
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
         rc_spec.zag rc_main.zag; do
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
# regime-change policy layer + harness main
cat "$DA/da_base.zag" "$RB/rb_world.zag" "$ET/et_world.zag" "$DA/da_module.zag" \
    "$DA/da_learn.zag" "$RB/rb_fix.zag" "$ET/et_spec.zag" "$RR/rr_spec.zag" \
    "$LD/ld_spec.zag" rc_spec.zag rc_main.zag > rc_full.zag
[ "$(grep -c '^fn main(' rc_full.zag)" = "1" ] || fail "expected exactly one fn main in rc_full.zag"
# K8 (part): no world literals in new lane sources
for f in rc_spec.zag rc_main.zag; do
  grep -q "901\|902" "$f" && fail "K8: $f contains world literals"
done

"$ZNC" build rc_full.zag -o rc_bin > rc_compile.txt 2>&1 || fail "znc build of rc_full.zag failed"
grep -q ": error" rc_compile.txt && fail "compiler reported an error (see rc_compile.txt)"

# run experiment 3x
for i in 1 2 3; do
  ./rc_bin > "rc_run$i.txt" 2> "rc_run$i.err"; echo "rc_bin run$i exit=$?"
done

# K3 determinism: byte-identical across the 3 runs
cmp rc_run1.txt rc_run2.txt || fail "K3: rc_run1/rc_run2 differ"
cmp rc_run1.txt rc_run3.txt || fail "K3: rc_run1/rc_run3 differ"
sha256sum rc_run1.txt

# K3 stderr must be empty
for f in rc_run1.err rc_run2.err rc_run3.err; do
  [ -s "$f" ] && fail "K3: non-empty stderr: $f"
done

# K3: exactly 36 CELL lines (6 cells x 6 arms)
[ "$(grep -c '^CELL ' rc_run1.txt)" = "36" ] || fail "K3: expected 36 CELL lines"

echo "--- kill bars ---"

fixed_field() { # $1=R $2=P $3=field -> value
  # leading-space anchor: avoids substring collisions (e.g. D= inside Dpre=)
  grep "^CELL R=$1 " rc_run1.txt | grep " P=$2 " | grep -o " $3=[0-9-]*" | head -1 | cut -d= -f2
}
adapt_field() { # $1=R $2=L $3=field -> value
  grep "^CELL R=$1 " rc_run1.txt | grep " P=adapt L=$2 " | grep -o " $3=[0-9-]*" | head -1 | cut -d= -f2
}

# K4: regime anchoring. Fixed-arm structural identities (regime-
# independent), cross-arm arrival identity, and arrival splits that
# show the shift.
for R in 0 1 2 3 4 5; do
  dd=$(fixed_field $R lazy D);       qd=$(fixed_field $R lazy Q)
  rd=$(fixed_field $R lazy rebuilds); ad=$(fixed_field $R lazy answered)
  fd=$(fixed_field $R lazy refusals); kd=$(fixed_field $R lazy kb)
  de=$(fixed_field $R eager D);       qe=$(fixed_field $R eager Q)
  re=$(fixed_field $R eager rebuilds); ae=$(fixed_field $R eager answered)
  fe=$(fixed_field $R eager refusals); ke=$(fixed_field $R eager kb)
  if [ "$rd" -gt "$dd" ] || [ "$rd" -gt "$qd" ]; then
    fail "K4: R=$R lazy rebuilds=$rd > min(D,Q)=($dd,$qd)"
  fi
  { [ "$ad" = "$qd" ] && [ "$fd" = "$rd" ] && [ "$kd" = "$(( qd * 2 ))" ]; } \
    || fail "K4: R=$R lazy: answered=$ad refusals=$fd kb=$kd (Q=$qd)"
  { [ "$re" = "$de" ] && [ "$ae" = "$qe" ] && [ "$fe" = "0" ] && [ "$ke" = "$(( qe * 2 ))" ]; } \
    || fail "K4: R=$R eager: rebuilds=$re answered=$ae refusals=$fe kb=$ke (D=$de Q=$qe)"
  for L in 0 1 3 7; do
    da=$(adapt_field $R $L D); qa=$(adapt_field $R $L Q)
    { [ "$da" = "$dd" ] && [ "$qa" = "$qd" ]; } \
      || fail "K4: R=$R L=$L adapt (D,Q)=($da,$qa) != lazy ($dd,$qd)"
  done
done
echo "PASS: K4 fixed arms anchor; cross-arm (D,Q) identical on all 6 cells"
# K4 regime splits (lazy arm).
dpre1=$(fixed_field 1 lazy Dpre); qpre1=$(fixed_field 1 lazy Qpre)
dpost1=$(fixed_field 1 lazy Dpost); qpost1=$(fixed_field 1 lazy Qpost)
{ [ "$dpre1" = "128" ] && [ "$qpost1" = "128" ] && \
  [ "$dpost1" -lt 32 ] && [ "$qpre1" -lt 32 ]; } \
  || fail "K4: R1 splits (Dpre,Qpre,Dpost,Qpost)=($dpre1,$qpre1,$dpost1,$qpost1), want (128,<32,<32,128)"
dpre2=$(fixed_field 2 lazy Dpre); qpre2=$(fixed_field 2 lazy Qpre)
dpost2=$(fixed_field 2 lazy Dpost); qpost2=$(fixed_field 2 lazy Qpost)
{ [ "$qpre2" = "128" ] && [ "$dpost2" = "128" ] && \
  [ "$dpre2" -lt 32 ] && [ "$qpost2" -lt 32 ]; } \
  || fail "K4: R2 splits (Dpre,Qpre,Dpost,Qpost)=($dpre2,$qpre2,$dpost2,$qpost2), want (<32,128,128,<32)"
dpre3=$(fixed_field 3 lazy Dpre); qpre3=$(fixed_field 3 lazy Qpre)
dpost3=$(fixed_field 3 lazy Dpost); qpost3=$(fixed_field 3 lazy Qpost)
{ [ "$dpre3" -gt "$(( 2 * dpost3 ))" ] && [ "$qpre3" -gt "$(( 2 * qpost3 ))" ]; } \
  || fail "K4: R3 splits (Dpre,Qpre,Dpost,Qpost)=($dpre3,$qpre3,$dpost3,$qpost3), want pre > 2x post"
dpre0=$(fixed_field 0 lazy Dpre); qpre0=$(fixed_field 0 lazy Qpre)
dpost0=$(fixed_field 0 lazy Dpost); qpost0=$(fixed_field 0 lazy Qpost)
dd0=$(fixed_field 0 lazy D); qd0=$(fixed_field 0 lazy Q)
ddiff0=$(( dpre0 - dpost0 )); [ "$ddiff0" -lt 0 ] && ddiff0=$(( -ddiff0 ))
qdiff0=$(( qpre0 - qpost0 )); [ "$qdiff0" -lt 0 ] && qdiff0=$(( -qdiff0 ))
{ [ "$ddiff0" -le "$(( dd0 / 2 ))" ] && [ "$qdiff0" -le "$(( qd0 / 2 ))" ]; } \
  || fail "K4: R0 no-shift split uneven: |dpre-dpost|=$ddiff0 (D=$dd0) |qpre-qpost|=$qdiff0 (Q=$qd0)"
echo "PASS: K4 regime splits: R1/R2 exact-128 deterministic pins, R3 2x rate drop, R0 even split"

# Shared awk field parser: F("name") returns the numeric field value.
AWKPARSE='
function F(n,   i) {
  for (i=1;i<=NF;i++) if (index($i, n"=")==1) return substr($i, length(n)+2)+0;
  return -999999;
}
function P(   i) {
  for (i=1;i<=NF;i++) if (index($i, "P=")==1) return substr($i, 3);
  return "";
}
'

# K5a: no-shift cells (R0,R4,R5): commit-time EWMA error vs realized
# rates (stationary sanity, parent K5 form).
# K5b: shift cells (R1,R2,R3): e=192 EWMA error vs realized POST-shift
# rates (convergence after burn-in). e=144 error reported as finding.
read k5a_n k5a_ed k5a_eq k5b_n k5b_ed k5b_eq k5b144_ed k5b144_eq <<< "$(
awk "$AWKPARSE"'
/^CELL / {
  if (P() != "adapt") next;
  R=F("R")+0; D=F("D"); Q=F("Q");
  dh=F("dh"); qh=F("qh");
  dh144=F("dh144"); qh144=F("qh144");
  dh192=F("dh192"); qh192=F("qh192");
  Dpost=F("Dpost"); Qpost=F("Qpost");
  if (R==0 || R==4 || R==5) {
    n5a++;
    td=4*D; tq=4*Q;
    dd = td>4 ? td : 4; dq = tq>4 ? tq : 4;
    ed = dh>td ? (dh-td)/dd : (td-dh)/dd;
    eq = qh>tq ? (qh-tq)/dq : (tq-qh)/dq;
    s5a_ed+=ed; s5a_eq+=eq;
  } else {
    n5b++;
    pd=8*Dpost; pq=8*Qpost;
    dd = pd>64 ? pd : 64; dq = pq>64 ? pq : 64;
    e192d = dh192>pd ? (dh192-pd)/dd : (pd-dh192)/dd;
    e192q = qh192>pq ? (qh192-pq)/dq : (pq-qh192)/dq;
    s5b_ed+=e192d; s5b_eq+=e192q;
    e144d = dh144>pd ? (dh144-pd)/dd : (pd-dh144)/dd;
    e144q = qh144>pq ? (qh144-pq)/dq : (pq-qh144)/dq;
    s5b144_ed+=e144d; s5b144_eq+=e144q;
  }
}
END{ printf "%d %.4f %.4f %d %.4f %.4f %.4f %.4f", \
  n5a, s5a_ed/n5a, s5a_eq/n5a, n5b, s5b_ed/n5b, s5b_eq/n5b, \
  s5b144_ed/n5b, s5b144_eq/n5b }' rc_run1.txt)"
echo "K5a (no-shift, n=$k5a_n): mean_rel_err_d=$k5a_ed mean_rel_err_q=$k5a_eq"
echo "K5b (shift, n=$k5b_n): e192 err_d=$k5b_ed err_q=$k5b_eq"
echo "K5 FINDING (not barred): e144 burn-in err_d=$k5b144_ed err_q=$k5b144_eq"
[ "$k5a_n" = "12" ] || fail "K5a: expected 12 adapt lines on no-shift cells, got $k5a_n"
[ "$k5b_n" = "12" ] || fail "K5b: expected 12 adapt lines on shift cells, got $k5b_n"
awk "BEGIN{ exit !( $k5a_ed <= 0.6 ) }" || fail "K5a: mean drift-rate rel err $k5a_ed > 0.6"
awk "BEGIN{ exit !( $k5a_eq <= 0.6 ) }" || fail "K5a: mean query-rate rel err $k5a_eq > 0.6"
awk "BEGIN{ exit !( $k5b_ed <= 0.5 ) }" || fail "K5b: e192 drift-rate err vs post-shift $k5b_ed > 0.5"
awk "BEGIN{ exit !( $k5b_eq <= 0.5 ) }" || fail "K5b: e192 query-rate err vs post-shift $k5b_eq > 0.5"
echo "PASS: K5 estimator sound stationary; converges to new regime by e=192"

# K6a/b/c/e/f: flip aggregates.
read k6_n k6_totfl k6_maxfl k6_l0bad k6_r1pos k6_r2neg k6_r3pfl <<< "$(
awk "$AWKPARSE"'
/^CELL / {
  if (P() != "adapt") next;
  R=F("R")+0; L=F("L")+0; cm=F("cm")+0; sel=F("sel")+0;
  flips=F("flips")+0; pflips=F("pflips")+0; fdir=F("fdir")+0;
  n++;
  totfl+=flips;
  if (flips>maxfl) maxfl=flips;
  if (L==0 && (cm==2 || sel==1)) bad++;
  if (R==1 && fdir==1) r1pos++;
  if (R==2 && fdir==-1) r2neg++;
  if (R==3) r3pfl+=pflips;
}
END{ printf "%d %d %d %d %d %d %d", n, totfl, maxfl, bad, r1pos, r2neg, r3pfl }' rc_run1.txt)"
echo "K6: adapt=$k6_n total_flips=$k6_totfl max_per_ep=$k6_maxfl L0_bad=$k6_l0bad R1_fdirpos=$k6_r1pos R2_fdirneg=$k6_r2neg R3_pflips=$k6_r3pfl"
[ "$k6_n" = "24" ] || fail "K6: expected 24 adapt lines, got $k6_n"
[ "$k6_totfl" -le 12 ] || fail "K6a: $k6_totfl total flips (> 12): switch thrashes"
[ "$k6_maxfl" -le 2 ] || fail "K6b: an episode flipped $k6_maxfl times (> 2): oscillation"
[ "$k6_l0bad" = "0" ] || fail "K6c: $k6_l0bad L=0 episodes committed eager"
[ "$k6_r1pos" -ge 1 ] || fail "K6e: zero lazy->eager post-shift flips on R1"
[ "$k6_r2neg" -ge 1 ] || fail "K6e: zero eager->lazy post-shift flips on R2"
[ "$k6_r3pfl" = "0" ] || fail "K6f: $k6_r3pfl post-shift flips on R3 (rate-only change)"
echo "PASS: K6a/b/c no thrash/oscillation/L0-clean; K6e flips both directions; K6f R3 silent"

# K6d: structural accounting on all 24 adapt lines.
for R in 0 1 2 3 4 5; do
  rd=$(fixed_field $R lazy rebuilds); fd=$(fixed_field $R lazy refusals)
  for L in 0 1 3 7; do
    cm=$(adapt_field $R $L cm); flips=$(adapt_field $R $L flips)
    pflips=$(adapt_field $R $L pflips); tf1=$(adapt_field $R $L tf1)
    fdir=$(adapt_field $R $L fdir); tf2=$(adapt_field $R $L tf2)
    rb=$(adapt_field $R $L rebuilds); an=$(adapt_field $R $L answered)
    rf=$(adapt_field $R $L refusals); kb=$(adapt_field $R $L kb)
    qq=$(adapt_field $R $L Q); od=$(adapt_field $R $L od)
    rs=$(adapt_field $R $L rs); dd=$(adapt_field $R $L D)
    Dc=$(adapt_field $R $L Dc); Qc=$(adapt_field $R $L Qc)
    dpre=$(adapt_field $R $L Dpre); dpost=$(adapt_field $R $L Dpost)
    qpre=$(adapt_field $R $L Qpre); qpost=$(adapt_field $R $L Qpost)
    { [ "$(( dpre + dpost ))" = "$dd" ] && [ "$(( qpre + qpost ))" = "$qq" ]; } \
      || fail "K6d: R=$R L=$L arrival splits do not sum to (D,Q)"
    { [ "$an" = "$qq" ] && [ "$kb" = "$(( qq * 2 ))" ] && \
      [ "$rb" = "$(( od + rs ))" ] && [ "$rf" = "$od" ]; } \
      || fail "K6d: R=$R L=$L an/kb/rb/rf identity broken"
    { { [ "$pflips" = "0" ] && [ "$tf1" = "0" ] && [ "$fdir" = "0" ]; } || \
      { [ "$pflips" != "0" ] && [ "$tf1" != "0" ] && [ "$fdir" != "0" ]; }; } \
      || fail "K6d: R=$R L=$L pflips/tf1/fdir inconsistent ($pflips/$tf1/$fdir)"
    if [ "$pflips" != "0" ]; then
      { [ "$tf1" -gt 128 ] && [ "$tf1" -le 256 ]; } \
        || fail "K6d: R=$R L=$L post-shift flip tick tf1=$tf1 not in (128,256]"
    fi
    if [ "$tf2" != "0" ]; then
      { [ "$tf2" -ge "$tf1" ] && [ "$tf2" -le 256 ]; } \
        || fail "K6d: R=$R L=$L tf2=$tf2 inconsistent with tf1=$tf1"
    fi
    [ "$flips" -ge "$pflips" ] || fail "K6d: R=$R L=$L flips=$flips < pflips=$pflips"
    if [ "$flips" = "0" ]; then
      if [ "$cm" = "0" ] || [ "$cm" = "1" ]; then
        { [ "$od" = "$rd" ] && [ "$rf" = "$fd" ] && [ "$rs" = "0" ]; } \
          || fail "K6d: R=$R L=$L cm=$cm not field-equal to lazy twin"
      fi
      if [ "$cm" = "2" ]; then
        exprs=$(( 1 + dd - Dc ))
        [ "$rs" = "$exprs" ] \
          || fail "K6d: R=$R L=$L cm=2 rs=$rs != 1+(D-Dc)=$exprs"
        { [ "$od" -le "$Dc" ] && [ "$od" -le "$Qc" ]; } \
          || fail "K6d: R=$R L=$L cm=2 od=$od > min(Dc,Qc)=($Dc,$Qc)"
      fi
    fi
  done
done
echo "PASS: K6d structural accounting on all 24 adapt lines"

# K7: regime economics. J = rb + rf*L.
# K7a: R1 adapt <= lazy+1 for all L. K7b: R2 L in {0,7} adapt <= eager+1.
# K7c: R2 flipped (fdir=-1) episodes: strictly better than eager.
read k7_ja10 k7_ja11 k7_ja13 k7_ja17 k7_jl10 k7_jl11 k7_jl13 k7_jl17 \
     k7_ja20 k7_ja27 k7_je2 k7c_n k7c_bad <<< "$(
awk "$AWKPARSE"'
/^CELL / {
  R=F("R")+0; p=P(); l=F("L")+0; rb=F("rebuilds")+0; rf=F("refusals")+0;
  fdir=F("fdir")+0;
  if (p=="lazy") { jl0=rb; jl1=rb+rf; jl3=rb+3*rf; jl7=rb+7*rf; }
  else if (p=="eager") { je=rb; }
  else if (p=="adapt") { ja=rb+rf*l; }
  if (R==1 && p=="lazy") { lz10=jl0; lz11=jl1; lz13=jl3; lz17=jl7; }
  if (R==1 && p=="adapt" && l==0) a10=ja;
  if (R==1 && p=="adapt" && l==1) a11=ja;
  if (R==1 && p=="adapt" && l==3) a13=ja;
  if (R==1 && p=="adapt" && l==7) a17=ja;
  if (R==2 && p=="eager") je2=je;
  if (R==2 && p=="adapt" && l==0) a20=ja;
  if (R==2 && p=="adapt" && l==7) a27=ja;
  if (R==2 && p=="adapt" && fdir==-1) { k7cn++; if (ja>=je2) k7cbad++; }
}
END{ printf "%d %d %d %d %d %d %d %d %d %d %d %d %d", \
  a10, a11, a13, a17, lz10, lz11, lz13, lz17, a20, a27, je2, k7cn, k7cbad }' rc_run1.txt)"
echo "K7a R1: adapt=($k7_ja10,$k7_ja11,$k7_ja13,$k7_ja17) lazy=($k7_jl10,$k7_jl11,$k7_jl13,$k7_jl17)"
echo "K7b R2: adapt L0=$k7_ja20 L7=$k7_ja27 eager=$k7_je2"
echo "K7c R2 flipped: n=$k7c_n not-strictly-better=$k7c_bad"
[ "$k7_ja10" -le "$(( k7_jl10 + 1 ))" ] || fail "K7a: R1 L=0 adapt=$k7_ja10 > lazy+1=$(( k7_jl10 + 1 ))"
[ "$k7_ja11" -le "$(( k7_jl11 + 1 ))" ] || fail "K7a: R1 L=1 adapt=$k7_ja11 > lazy+1=$(( k7_jl11 + 1 ))"
[ "$k7_ja13" -le "$(( k7_jl13 + 1 ))" ] || fail "K7a: R1 L=3 adapt=$k7_ja13 > lazy+1=$(( k7_jl13 + 1 ))"
[ "$k7_ja17" -le "$(( k7_jl17 + 1 ))" ] || fail "K7a: R1 L=7 adapt=$k7_ja17 > lazy+1=$(( k7_jl17 + 1 ))"
[ "$k7_ja20" -le "$(( k7_je2 + 1 ))" ] || fail "K7b: R2 L=0 adapt=$k7_ja20 > eager+1=$(( k7_je2 + 1 ))"
[ "$k7_ja27" -le "$(( k7_je2 + 1 ))" ] || fail "K7b: R2 L=7 adapt=$k7_ja27 > eager+1=$(( k7_je2 + 1 ))"
[ "$k7c_n" -ge 1 ] || fail "K7c: no fdir=-1 episodes on R2 to evaluate"
[ "$k7c_bad" = "0" ] || fail "K7c: $k7c_bad/$k7c_n R2 flipped episodes not strictly better than eager"
echo "PASS: K7a R1 adapt<=lazy+1; K7b R2 non-flipping adapt<=eager+1; K7c flips pay off strictly"

# K8 hygiene: ASCII-only lane sources
if LC_ALL=C grep -l '[^[:print:][:space:]]' PREREG.md NAMECHECK.md rc_spec.zag rc_main.zag rc_build.sh 2>/dev/null; then
  fail "K8: non-ASCII byte found"
fi
echo "PASS: K8 ASCII-only, no world literals, one fn main per binary, reused sources unmodified, da_learn.zag untouched"

echo "ALL KILL BARS PASS"
