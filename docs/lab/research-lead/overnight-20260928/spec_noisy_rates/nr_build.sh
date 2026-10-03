#!/bin/bash
# nr_build.sh -- SPEC-NOISY-RATES: build + run + verify.
# Usage: ./nr_build.sh  (run from this directory)
# safebin PATH is mandatory; the pinned znc builds nr_bin; nr_bin runs
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
         nr_spec.zag nr_main.zag; do
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
# noisy-rate policy layer + harness main
cat "$DA/da_base.zag" "$RB/rb_world.zag" "$ET/et_world.zag" "$DA/da_module.zag" \
    "$DA/da_learn.zag" "$RB/rb_fix.zag" "$ET/et_spec.zag" "$RR/rr_spec.zag" \
    "$LD/ld_spec.zag" nr_spec.zag nr_main.zag > nr_full.zag
[ "$(grep -c '^fn main(' nr_full.zag)" = "1" ] || fail "expected exactly one fn main in nr_full.zag"
# K8 (part): no world literals in new lane sources
for f in nr_spec.zag nr_main.zag; do
  grep -q "901\|902" "$f" && fail "K8: $f contains world literals"
done

"$ZNC" build nr_full.zag -o nr_bin > nr_compile.txt 2>&1 || fail "znc build of nr_full.zag failed"
grep -q ": error" nr_compile.txt && fail "compiler reported an error (see nr_compile.txt)"

# run experiment 3x
for i in 1 2 3; do
  ./nr_bin > "nr_run$i.txt" 2> "nr_run$i.err"; echo "nr_bin run$i exit=$?"
done

# K3 determinism: byte-identical across the 3 runs
cmp nr_run1.txt nr_run2.txt || fail "K3: nr_run1/nr_run2 differ"
cmp nr_run1.txt nr_run3.txt || fail "K3: nr_run1/nr_run3 differ"
sha256sum nr_run1.txt

# K3 stderr must be empty
for f in nr_run1.err nr_run2.err nr_run3.err; do
  [ -s "$f" ] && fail "K3: non-empty stderr: $f"
done

# K3: exactly 150 CELL lines (25 cells x 6 arms)
[ "$(grep -c '^CELL ' nr_run1.txt)" = "150" ] || fail "K3: expected 150 CELL lines"

echo "--- kill bars ---"

fixed_field() { # $1=M $2=N $3=P $4=field -> value
  # leading-space anchor: avoids substring collisions (e.g. od= inside plod=)
  grep "^CELL M=$1 N=$2 P=$3 " nr_run1.txt | grep -o " $4=[0-9-]*" | head -1 | cut -d= -f2
}
adapt_field() { # $1=M $2=N $3=L $4=field -> value
  grep "^CELL M=$1 N=$2 P=adapt L=$3 " nr_run1.txt | grep -o " $4=[0-9-]*" | head -1 | cut -d= -f2
}

# K4: noisy anchoring of the fixed arms + cross-arm arrival identity +
# noise actually present.
noisy=0
for M in 1 2 4 8 16; do
  for N in 1 2 4 8 16; do
    dd=$(fixed_field $M $N lazy D);       qd=$(fixed_field $M $N lazy Q)
    rd=$(fixed_field $M $N lazy rebuilds); ad=$(fixed_field $M $N lazy answered)
    fd=$(fixed_field $M $N lazy refusals); kd=$(fixed_field $M $N lazy kb)
    de=$(fixed_field $M $N eager D);       qe=$(fixed_field $M $N eager Q)
    re=$(fixed_field $M $N eager rebuilds); ae=$(fixed_field $M $N eager answered)
    fe=$(fixed_field $M $N eager refusals); ke=$(fixed_field $M $N eager kb)
    if [ "$rd" -gt "$dd" ] || [ "$rd" -gt "$qd" ]; then
      fail "K4: M=$M N=$N lazy rebuilds=$rd > min(D,Q)=($dd,$qd)"
    fi
    { [ "$ad" = "$qd" ] && [ "$fd" = "$rd" ] && [ "$kd" = "$(( qd * 2 ))" ]; } \
      || fail "K4: M=$M N=$N lazy: answered=$ad refusals=$fd kb=$kd (Q=$qd)"
    { [ "$re" = "$de" ] && [ "$ae" = "$qe" ] && [ "$fe" = "0" ] && [ "$ke" = "$(( qe * 2 ))" ]; } \
      || fail "K4: M=$M N=$N eager: rebuilds=$re answered=$ae refusals=$fe kb=$ke (D=$de Q=$qe)"
    # cross-arm arrival identity: adapt arms see the same (D,Q) as lazy
    for L in 0 1 3 7; do
      da=$(adapt_field $M $N $L D); qa=$(adapt_field $M $N $L Q)
      { [ "$da" = "$dd" ] && [ "$qa" = "$qd" ]; } \
        || fail "K4: M=$M N=$N L=$L adapt (D,Q)=($da,$qa) != lazy ($dd,$qd)"
    done
    if [ "$dd" != "$(( 256 / M ))" ] || [ "$qd" != "$(( 256 / N ))" ]; then
      noisy=$(( noisy + 1 ))
    fi
  done
done
[ "$noisy" -ge 20 ] || fail "K4: only $noisy/25 cells differ from the deterministic grid (noise absent?)"
echo "PASS: K4 fixed arms anchor on noisy world; cross-arm (D,Q) identical; $noisy/25 cells noisy"

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

# K5: estimation error (rate), price error (qh>=1, Amendment A1),
# price-interval coverage (decision-relevant, Amendment A1).
# Rate-interval future coverage is REPORTED AS A FINDING (A1).
read k5_n k5_ed k5_eq k5_pn k5_pe k5_cn k5_cov k5_fcovd k5_fcovq <<< "$(
awk "$AWKPARSE"'
/^CELL / {
  if (P() != "adapt") next;
  D=F("D"); Q=F("Q"); tc=F("tc"); Dc=F("Dc"); Qc=F("Qc");
  dh=F("dh"); qh=F("qh");
  dlo=F("dlo"); dhi=F("dhi"); qlo=F("qlo"); qhi=F("qhi");
  pnum=F("pnum"); pden=F("pden");
  plon=F("plon"); plod=F("plod"); phin=F("phin"); phid=F("phid");
  n++;
  td=4*D; tq=4*Q;
  dd = td>4 ? td : 4; dq = tq>4 ? tq : 4;
  ed = dh>td ? (dh-td)/dd : (td-dh)/dd;
  eq = qh>tq ? (qh-tq)/dq : (tq-qh)/dq;
  sumed+=ed; sumeq+=eq;
  if (qh>=1) {
    pn++;
    estp = pnum/pden;
    truep = (Q>0 && D>Q) ? (D-Q)/Q : 0;
    pe = estp>truep ? estp-truep : truep-estp;
    sumpe+=pe;
  }
  dQ=Q-Qc;
  if (dQ>0) {
    cn++;
    dD=D-Dc;
    tp = (dD>dQ) ? (dD-dQ)/dQ : 0;
    plo=plon/plod; phi=phin/phid;
    if (tp>=plo && tp<=phi) cov++;
  }
  post=256-tc;
  rd=1024*(D-Dc)/post; rq=1024*(Q-Qc)/post;
  if (rd>=dlo && rd<=dhi) fcovd++;
  if (rq>=qlo && rq<=qhi) fcovq++;
}
END{ printf "%d %.4f %.4f %d %.4f %d %.4f %.4f %.4f", n, sumed/n, sumeq/n, pn, sumpe/pn, cn, cov/cn, fcovd/n, fcovq/n }' nr_run1.txt)"
echo "K5: n=$k5_n mean_rel_err_d=$k5_ed mean_rel_err_q=$k5_eq"
echo "K5: price: n_qh1=$k5_pn mean_price_err=$k5_pe"
echo "K5: price-interval coverage: n=$k5_cn cov=$k5_cov"
echo "K5 FINDING (not barred, A1): rate-interval future coverage d=$k5_fcovd q=$k5_fcovq"
[ "$k5_n" = "100" ] || fail "K5: expected 100 adapt lines, got $k5_n"
awk "BEGIN{ exit !( $k5_ed <= 0.6 ) }" || fail "K5: mean drift-rate rel err $k5_ed > 0.6"
awk "BEGIN{ exit !( $k5_eq <= 0.6 ) }" || fail "K5: mean query-rate rel err $k5_eq > 0.6"
awk "BEGIN{ exit !( $k5_pe <= 2.0 ) }" || fail "K5: mean price err (qh>=1) $k5_pe > 2.0"
awk "BEGIN{ exit !( $k5_cov >= 0.70 ) }" || fail "K5: price-interval coverage $k5_cov < 0.70"
echo "PASS: K5 estimation error within bounds; price-interval calibrated (>=70%)"

# K6a/b/c: decisive commits, flips, L=0 structural.
read k6_n k6_dec k6_fl k6_l0bad <<< "$(
awk "$AWKPARSE"'
/^CELL / {
  if (P() != "adapt") next;
  L=F("L"); cm=F("cm"); sel=F("sel"); flips=F("flips");
  n++;
  if (cm==1 || cm==2) dec++;
  fl+=flips;
  if (L==0 && (cm==2 || sel==1)) bad++;
}
END{ printf "%d %d %d %d", n, dec, fl, bad }' nr_run1.txt)"
echo "K6: adapt=$k6_n decisive=$k6_dec total_flips=$k6_fl L0_eager_bad=$k6_l0bad"
[ "$k6_dec" -ge 30 ] || fail "K6a: only $k6_dec/100 decisive commits (< 30)"
[ "$k6_fl" -le 10 ] || fail "K6b: $k6_fl total flips (> 10): switch thrashes"
[ "$k6_l0bad" = "0" ] || fail "K6c: $k6_l0bad L=0 episodes committed eager"
echo "PASS: K6a/b/c decisive=$k6_dec flips=$k6_fl L0-clean"

# K6d: structural accounting on adapt lines.
for M in 1 2 4 8 16; do
  for N in 1 2 4 8 16; do
    rd=$(fixed_field $M $N lazy rebuilds); fd=$(fixed_field $M $N lazy refusals)
    for L in 0 1 3 7; do
      cm=$(adapt_field $M $N $L cm); flips=$(adapt_field $M $N $L flips)
      rb=$(adapt_field $M $N $L rebuilds); an=$(adapt_field $M $N $L answered)
      rf=$(adapt_field $M $N $L refusals); kb=$(adapt_field $M $N $L kb)
      qq=$(adapt_field $M $N $L Q); od=$(adapt_field $M $N $L od)
      rs=$(adapt_field $M $N $L rs); dd=$(adapt_field $M $N $L D)
      Dc=$(adapt_field $M $N $L Dc); Qc=$(adapt_field $M $N $L Qc)
      { [ "$an" = "$qq" ] && [ "$kb" = "$(( qq * 2 ))" ] && \
        [ "$rb" = "$(( od + rs ))" ] && [ "$rf" = "$od" ]; } \
        || fail "K6d: M=$M N=$N L=$L an/kb/rb/rf identity broken"
      if [ "$flips" = "0" ]; then
        if [ "$cm" = "0" ] || [ "$cm" = "1" ]; then
          { [ "$od" = "$rd" ] && [ "$rf" = "$fd" ] && [ "$rs" = "0" ]; } \
            || fail "K6d: M=$M N=$N L=$L cm=$cm not field-equal to lazy twin"
        fi
        if [ "$cm" = "2" ]; then
          exprs=$(( 1 + dd - Dc ))
          [ "$rs" = "$exprs" ] \
            || fail "K6d: M=$M N=$N L=$L cm=2 rs=$rs != 1+(D-Dc)=$exprs"
          { [ "$od" -le "$Dc" ] && [ "$od" -le "$Qc" ]; } \
            || fail "K6d: M=$M N=$N L=$L cm=2 od=$od > min(Dc,Qc)=($Dc,$Qc)"
        fi
      fi
    done
  done
done
echo "PASS: K6d structural accounting on all 100 adapt lines"

# K7: portfolio totals J = rb + rf*L per L over the 25 cells.
# NOTE: lazy/eager carry L=-1; accumulate their J per L explicitly.
read adapt0 adapt1 adapt3 adapt7 <<< "$(
awk "$AWKPARSE"'
/^CELL / {
  p=P(); l=F("L")+0; rb=F("rebuilds")+0; rf=F("refusals")+0;
  if (p=="adapt") ja[l]+=rb+rf*l;
}
END{ printf "%d %d %d %d", ja[0], ja[1], ja[3], ja[7] }' nr_run1.txt)"
read lazy0 lazy1 lazy3 lazy7 eagerT <<< "$(
awk "$AWKPARSE"'
/^CELL / {
  p=P(); l=F("L")+0; rb=F("rebuilds")+0; rf=F("refusals")+0;
  if (p=="lazy") { jl0+=rb; jl1+=rb+rf; jl3+=rb+3*rf; jl7+=rb+7*rf; }
  else if (p=="eager") je+=rb;
}
END{ printf "%d %d %d %d %d", jl0, jl1, jl3, jl7, je }' nr_run1.txt)"
echo "portfolio J: adapt=($adapt0,$adapt1,$adapt3,$adapt7) lazy=($lazy0,$lazy1,$lazy3,$lazy7) eager_rb=$eagerT"
[ "$adapt0" = "$lazy0" ] || fail "K7: L=0 adapt=$adapt0 != lazy=$lazy0 (switch fired at L=0?)"
[ "$adapt1" -lt "$lazy1" ] || fail "K7: L=1 adapt=$adapt1 not < lazy=$lazy1"
[ "$adapt3" -lt "$lazy3" ] || fail "K7: L=3 adapt=$adapt3 not < lazy=$lazy3"
[ "$adapt7" -lt "$lazy7" ] || fail "K7: L=7 adapt=$adapt7 not < lazy=$lazy7"
echo "PASS: K7 adapt ties lazy at L=0, beats lazy at L=1,3,7 (vs eager: finding, not barred)"

# K8 hygiene: ASCII-only lane sources
if LC_ALL=C grep -l '[^[:print:][:space:]]' PREREG.md NAMECHECK.md nr_spec.zag nr_main.zag nr_build.sh 2>/dev/null; then
  fail "K8: non-ASCII byte found"
fi
echo "PASS: K8 ASCII-only, no world literals, one fn main per binary, reused sources unmodified, da_learn.zag untouched"

echo "ALL KILL BARS PASS"
