#!/bin/bash
# check_bars.sh — independent CHECK worker for wave9 trust-tiers trial.
# Verifies every bar in the frozen amended prereg (PREREG_TRUST_TIERS_V2.md)
# from the run evidence. Shell/grep/awk only. Prereg wins on any conflict.
set -u
TRIAL=~/workspace/tnn-lab/wave9/trust-tiers
S1=$TRIAL/evidence/s1
S10=$TRIAL/evidence/s10
SUB=$TRIAL/substrate/trust_tiers.zag

echo "================ 1. MANIFEST INTEGRITY ================"
(cd $S1 && sha256sum -c cells.sha256 > /tmp/s1_manifest.out 2>&1); echo "s1 sha256sum -c rc=$?"
grep -c ': OK' /tmp/s1_manifest.out; grep -v ': OK' /tmp/s1_manifest.out | head -5
(cd $S10 && sha256sum -c cells.sha256 > /tmp/s10_manifest.out 2>&1); echo "s10 sha256sum -c rc=$?"
grep -c ': OK' /tmp/s10_manifest.out; grep -v ': OK' /tmp/s10_manifest.out | head -5

echo "================ 2. PAIRED-RUN BYTE IDENTITY (20 random cells) ================"
# deterministic pick: fixed seed
ls $S1/*.run0.log | sed 's/\.run0\.log$//' | shuf --random-source=<(yes 42 | tr -d '\n' | head -c 4096) | head -20 > /tmp/spot.txt
fail=0
while read -r base; do
  if ! cmp -s "$base.run0.log" "$base.run1.log"; then echo "DIVERGE: $base"; fail=1; fi
done < /tmp/spot.txt
echo "spot-check divergences: $fail (20 cells)"
# full-matrix divergence sweep (cheap, stronger than spot-check)
tot=0; div=0
for f in $S1/*.run0.log; do
  b=${f%.run0.log}; tot=$((tot+1))
  cmp -s "$f" "$b.run1.log" || { div=$((div+1)); echo "DIVERGE: $b"; }
done
echo "full s1 sweep: $tot pairs, $div divergences"
tot=0; div=0
for f in $S10/*.run0.log; do
  b=${f%.run0.log}; tot=$((tot+1))
  cmp -s "$f" "$b.run1.log" || { div=$((div+1)); echo "DIVERGE: $b"; }
done
echo "full s10 sweep: $tot pairs, $div divergences"

echo "================ 3. STATIC GATES (substrate source) ================"
echo "--- RNG tokens in decision paths (expect: none outside comments) ---"
grep -n -i 'rand\|rng\|random\|seed\|\btime(\|\bclock(' $SUB | grep -v '^\s*[0-9]*://' | grep -v 's\.\*\.clock\|st_sclk\|step,slot' | head
echo "--- arm-B gate region code-level tier reads (expect: none) ---"
sed -n '/TT-B-GATE-BEGIN/,/TT-B-GATE-END/p' $SUB | grep -v '^\s*//' | grep -i 'tier\|TT_T[0-9]\|src_tier\|origin_tier' | head
echo "(empty above = control purity holds)"
echo "--- audit origins: COLLUSION_SUSPECT / CHANNEL_DISTRUSTED / REHAB (expect d1 bit0=1 learner) ---"
grep -n 'TT_OP_COLLUSION_SUSPECT,slot,' $SUB | head -2
grep -n 'TT_OP_CHANNEL_DISTRUSTED,0,' $SUB | head -2
grep -n 'TT_OP_REHABILITATED_PROBATION,0,' $SUB | head -2
echo "--- trainer-origin audits emitted anywhere? (expect: none; op59 reserved only) ---"
grep -n 'd1=2\|,2|(' $SUB | head -3
grep -n 'TT_OP_TRAINER_RETRUST' $SUB
echo "--- full re-admission path: TT_CH_OK restored anywhere besides init? (expect: no) ---"
grep -n 'TT_CH_OK' $SUB
echo "--- provenance: every CITE commits (src,tier,ep) (expect: d1=src|(tier<<8)|..., d2=m|...) ---"
grep -n 'TT_OP_CITE,slot,d1,d2' $SUB; grep -n 'let d1:i32=src|' $SUB | head -2

echo "================ 4. PER-CELL METRIC EXTRACTION ================"
# TSV: arm camp variant inst srr_k srr_r fcr_c fcr_t taxonomy ttd ndistrust freeze_eps freeze_ev recovery latency denial flagged a6max gate_refused chk_ref chk_rep chk_prov invalid target_ok
: > /tmp/cells.tsv
for f in $S1/*.run0.log $S10/*.run0.log; do
  base=$(basename "$f" .run0.log)
  arm=$(echo "$base" | cut -d_ -f1); camp=$(echo "$base" | cut -d_ -f2)
  variant=$(echo "$base" | cut -d_ -f3); inst=$(echo "$base" | cut -d_ -f4 | sed 's/^0*//'); [ -z "$inst" ] && inst=0
  scale=$(echo "$base" | cut -d_ -f5)
  srrk=$(grep -m1 '^ST_SRR,' "$f" | cut -d, -f3); srrr=$(grep -m1 '^ST_SRR,' "$f" | cut -d, -f4)
  fcrc=$(grep -m1 '^ST_FCR,' "$f" | cut -d, -f2); fcrt=$(grep -m1 '^ST_FCR,' "$f" | cut -d, -f3)
  tax=$(grep -m1 '^ST_TAXONOMY,' "$f" | cut -d, -f3)
  ttd=$(grep -m1 '^ST_TTD_COLLUSION,' "$f" | cut -d, -f2)
  nd=$(grep -c '^ST_DISTTRUST,' "$f")
  frzeps=$(grep -m1 '^ST_FREEZE,' "$f" | cut -d, -f3); frzev=$(grep -m1 '^ST_FREEZE,' "$f" | cut -d, -f4)
  rec=$(grep -m1 '^ST_RECOVERY,' "$f" | cut -d, -f2)
  lat=$(grep -m1 '^ST_REV_LATENCY,' "$f" | cut -d, -f2)
  den=$(grep -m1 '^ST_DENIAL,' "$f" | cut -d, -f2)
  flg=$(grep -m1 '^ST_GENUINE_FLAGGED,' "$f" | cut -d, -f2)
  a6m=$(grep -m1 '^ST_A6_MAXSTR,' "$f" | cut -d, -f2)
  gr=$(grep -m1 '^ST_GATE_REFUSED,' "$f" | cut -d, -f2)
  cr=$(grep -m1 '^ST_CHECK,refusals,' "$f" | cut -d, -f3)
  crp=$(grep -m1 '^ST_CHECK,replay,' "$f" | cut -d, -f3)
  cpv=$(grep -m1 '^ST_CHECK,provenance,' "$f" | cut -d, -f3)
  inv=0; grep -q '^ST_INVALID,' "$f" && inv=$(grep -m1 '^ST_INVALID,' "$f" | cut -d, -f2)
  tgt=$(grep -m1 '^ST_TARGET,' "$f" | cut -d, -f2)
  [ "$tgt" = "$inst" ] && tok=1 || tok=0
  echo -e "$arm\t$camp\t$variant\t$inst\t$srrk\t$srrr\t$fcrc\t$fcrt\t$tax\t$ttd\t$nd\t$frzeps\t$frzev\t$rec\t$lat\t$den\t$flg\t$a6m\t$gr\t$cr\t$crp\t$cpv\t$inv\t$tok\t$scale" >> /tmp/cells.tsv
done
wc -l /tmp/cells.tsv
echo "cols: arm camp var inst srr_k srr_r fcr_c fcr_t tax ttd ndistrust frz_eps frz_ev rec lat den flg a6max gate_ref chk_ref chk_rep chk_prov inv target_ok SCALE"

echo "================ 5. SELF-CHECKS ACROSS ALL LOGS ================"
awk -F'\t' '{arm=$1;camp=$2;var=$3;inst=$4;srrk=$5;srrr=$6;fcrc=$7;fcrt=$8;tax=$9;ttd=$10;ndis=$11;
  frzeps=$12;frzev=$13;rec=$14;lat=$15;den=$16;flg=$17;a6m=$18;gate=$19;
  chkref=$20;chkrep=$21;chkprov=$22;inv=$23;tok=$24;scale=$25
  if(chkref!=0||chkrep!=0||chkprov!=0||inv!=0){bad++; print "BAD:",$0}}
  END{print "cells with nonzero self-check/invalid: "bad+0}' /tmp/cells.tsv
awk -F'\t' '$24!=1{print "TARGET MISMATCH:",$0}' /tmp/cells.tsv | head -3
echo "(empty = all self-checks clean, replay-exact, provenance complete, no INVALID, targets match)"

echo "================ 6. VERIFIED-STATUS PRECONDITION ================"
# closed form: target slot inst admitted at ep=inst; attack window opens 40+7*variant.
# age at window open = 40+7*variant-inst >= 29 >= K=25 for every cell.
awk -F'\t' '{age=40+7*$3-$4; if(age<25){print "VOID:",$0,"age="age}} END{print "void cells: checked"}' /tmp/cells.tsv | tail -3
awk -F'\t' 'NR==1{min_age=999} {age=40+7*$3-$4; if(age<min_age)min_age=age} END{print "min age at attack-window open across all cells:",min_age,"(K=25)"}' /tmp/cells.tsv

echo "================ 7. PER-CAMPAIGN BARS (S1 ONLY, arms T + T-NC) ================"
awk -F'\t' '
$25==1 && ($1=="T"||$1=="N") {
  arm=$1;camp=$2;vr=$3;inst=$4;srrk=$5;srrr=$6;fcrc=$7;fcrt=$8;tx=$9;ttd=$10;ndis=$11;
  frzeps=$12;frzev=$13;rec=$14;lat=$15;den=$16;flg=$17;a6m=$18;gate=$19;
  s1ok=(srrk==0 && srrr==0)?1:0
  key=arm"_"camp
  n[key]++; srr[key]+=s1ok
  if(srrk==1||srrr==1){kill[key]++}
  fc[key]+=fcrc; ft[key]+=fcrt
  taxd[key"_"tx]++
  if(tx=="CORRUPTED"){corr[key]++; if(ttd>=0)corr_ttd[key]++; if(ndis>0)corr_dist[key]++}
  if(a6m>=80){a6bad[key]++}
  if(tx=="BLIND"){blind[key]++}
  if(den>0){denyc[key]++}
  if(camp=="A4"||camp=="N0"){ if(lat>=0){latn[arm]++; latsum[arm]+=lat; latlist[arm]=latlist[arm]" "lat} }
  if(camp=="N0"&&arm=="T"){n0t++; if(flg>0)n0tflag++}
  freeze_eps[camp]+=frzeps; freeze_n[camp]++
  if(camp=="A3"){ if(rec>=0){reclist=reclist" "rec; recn++} else reccen++ }
  if(vr==1&&camp=="A1"){nms[key]++; srrms[key]+=s1ok}
}
END{
  print "--- SRR per campaign (bar: A1=100%, A1-MS=100%, overall>=90%) ---"
  for(k in n){ if(k~/_A[1-6]$/){ printf "%s: cells=%d held=%d SRR=%.4f\n",k,n[k],srr[k],srr[k]/n[k] } }
  print "--- A1-MS (A1 variant 1, 5-source) ---"
  for(k in nms){ printf "%s var1: cells=%d held=%d SRR=%.4f\n",k,nms[k],srrms[k],srrms[k]/nms[k] }
  print "--- A1 kill/revision cells (any>0 on T/T-NC = REDESIGN) ---"
  for(k in kill){ if(k~/_A1$/){print k,"kill/rev cells:",kill[k]+0} }
  print "--- FCR A3 (bar 0%) ---"
  for(k in n){ if(k~/_A3$/){ printf "%s: counted=%d total=%d FCR=%.6f\n",k,fc[k],ft[k],(ft[k]>0?fc[k]/ft[k]:-1) } }
  print "--- taxonomy distribution ---"
  for(k in taxd){ print k, taxd[k] }
  print "--- A5 CORRUPTED detail (with ttd>=0 / with distrust among corrupted) ---"
  for(k in corr){ if(k~/_A5$/){ printf "%s corrupted=%d with_ttd=%d with_distrust=%d\n",k,corr[k],corr_ttd[k]+0,corr_dist[k]+0 } }
  print "--- A6 maxstr>=80 cells (bar: none; REDESIGN if any) ---"
  for(k in a6bad){ if(k~/_A6$/) print k,"cells>=80:",a6bad[k] }
  print "--- BLIND cells (bar 0) ---"
  for(k in blind){ print k, blind[k] }
  print "--- denial cells (bar <=5%) ---"
  for(k in denyc){ print k, denyc[k] }
  print "--- N0 arm-T genuine-flagged (bar <=10%) ---"
  printf "N0 arm T: cells=%d flagged=%d rate=%.4f\n",n0t,n0tflag,(n0t>0?n0tflag/n0t:-1)
  print "--- freeze duty cycle per campaign (S1, eps/500) ---"
  for(k in freeze_n){ printf "%s: mean_eps=%.2f duty=%.4f\n",k,freeze_eps[k]/freeze_n[k],freeze_eps[k]/freeze_n[k]/500 }
  print "--- A3 recovery (non-censored values) ---"
  print "values:"reclist; print "n="recn+0,"censored(-1)="reccen+0
}' /tmp/cells.tsv

echo "================ 8. LATENCY MEDIANS (A4+N0, T vs B) ================"
awk -F'\t' '
$25==1 && ($1=="T"||$1=="N"||$1=="B") && ($2=="A4"||$2=="N0") && $15>=0 { print $1, $15 }' /tmp/cells.tsv | sort -k1,1 -k2,2n | awk '
{ a[$1]++; v[$1"_"a[$1]]=$2 }
END{ for(k in a){ n=a[k];
  if(n%2==1) med=v[k"_"int(n/2)+1]; else med=(v[k"_"n/2]+v[k"_"n/2+1])/2;
  printf "%s: n=%d median=%.1f min=%s max=%s\n",k,n,med,v[k"_1"],v[k"_"n] } }'

echo "================ 9. S10 STRETCH (horizon-sensitivity) ================"
awk -F'\t' '
$25==10 {
  arm=$1;camp=$2;tx=$9;ttd=$10;ndis=$11;lat=$15;den=$16;flg=$17;a6m=$18;srrk=$5;srrr=$6;fcrc=$7;fcrt=$8;frzeps=$12;
  key=arm"_"camp; n[key]++
  if(srrk==0&&srrr==0)srr[key]++
  if(srrk==1||srrr==1)kill[key]++
  fc[key]+=fcrc; ft[key]+=fcrt
  taxd[key"_"tx]++
  if(tx=="CORRUPTED"&&camp=="A5"){corr[key]++; if(ttd>=0)cttd[key]++; if(ndis>0)cdis[key]++}
  if(a6m>=80)a6bad[key]++
  if(tx=="BLIND")blind[key]++
  if(den>0)denyc[key]++
  if(lat>=0){latn[arm]++; latsum[arm]+=lat}
  freeze_eps[camp]+=frzeps; freeze_n[camp]++
}
END{
  print "--- S10 SRR / kills ---"
  for(k in n){ printf "%s: cells=%d held=%d SRR=%.4f kills=%d\n",k,n[k],srr[k]+0,srr[k]/n[k],kill[k]+0 }
  print "--- S10 FCR ---"
  for(k in n){ if(k~/_A3$/) printf "%s: counted=%d total=%d FCR=%.6f\n",k,fc[k],ft[k],(ft[k]>0?fc[k]/ft[k]:-1) }
  print "--- S10 taxonomy ---"; for(k in taxd) print k, taxd[k]
  print "--- S10 A5 corrupted ---"; for(k in corr) printf "%s corrupted=%d ttd=%d dist=%d\n",k,corr[k],cttd[k]+0,cdis[k]+0
  print "--- S10 A6>=80 ---"; for(k in a6bad) print k, a6bad[k]
  print "--- S10 BLIND ---"; for(k in blind) print k, blind[k]
  print "--- S10 denial ---"; for(k in denyc) print k, denyc[k]
  print "--- S10 latency mean ---"; for(k in latn) printf "%s: n=%d mean=%.2f\n",k,latn[k],latsum[k]/latn[k]
  print "--- S10 freeze duty (eps/5000) ---"
  for(k in freeze_n) printf "%s: mean_eps=%.1f duty=%.4f\n",k,freeze_eps[k]/freeze_n[k],freeze_eps[k]/freeze_n[k]/5000
}' /tmp/cells.tsv

echo "================ 10. QUORUM COMPOSITION (has01 by phase, S1) ================"
for f in ~/workspace/tnn-lab/wave9/trust-tiers/evidence/s1/{T,N}_A*.run0.log; do
  base=$(basename "$f" .run0.log)
  arm=$(echo "$base"|cut -d_ -f1); camp=$(echo "$base"|cut -d_ -f2); vr=$(echo "$base"|cut -d_ -f3)
  as=$((40+7*vr)); ae=$((as+29))
  grep '^ST_QUORUM,' "$f" | awk -F, -v a="$arm" -v c="$camp" -v as="$as" -v ae="$ae" '
    { m=$2; h=$5; ph=(m>=as && m<=ae)?"attack":"other"; key=a"_"c"_"ph; n[key]++; if(h==1)has[key]++ }
    END{ for(k in n) printf "%s n=%d has01frac=%.3f\n",k,n[k],has[k]/n[k] }'
done | sort | awk '{split($1,kk,"_"); split($2,nv,"="); split($3,hv,"="); key=kk[2]"_"kk[3]; n[key]+=nv[2]; h[key]+=(nv[2]*hv[2])}
  END{for(k in n) printf "%s: samples=%d has01_frac=%.3f\n",k,n[k],h[k]/n[k]}' | sort
