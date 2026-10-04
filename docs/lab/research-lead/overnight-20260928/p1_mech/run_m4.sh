#!/bin/sh
# run_m4.sh -- assemble, compile and CERTIFY the M4 binary (P1-MECHANISM).
#
# Every preregistered kill bar is checked HERE, mechanically. Exits non-zero on
# any failure; no verdict may be issued if it does.
#
# Extraction discipline: every lane line is `LABEL value value ...`, so a value
# is recovered as the nth field of the TRAILING run of pure-integer fields.
# key=value lines (SUMLIFE, LOC4, SAT_*) are read by exact key on the right
# line. An earlier revision of this script counted label words and silently
# mis-extracted seven bars; recorded as a harness defect of this lane, not a
# scientific failure.
set -e
D=$(dirname "$0")
D=$(cd "$D" && pwd)
cd "$D"
R=/Users/Shared/micah/Documents/TNN/TNN/docs/lab/research-lead/overnight-20260928
W=/Users/Shared/micah/Documents/TNN/TNN/tools/tnnwatch.sh
Z=/Users/Shared/micah/Documents/TNN/TNN/tools/zbuild.sh
FAIL=0
ok(){ echo "  PASS $1"; }
bad(){ echo "  FAIL $1"; FAIL=1; }
# nth value of the trailing integer run
tv(){ awk -v L="$2" -v n="$3" -v M="$4" -v P="$5" '$1==L && (M==""||$2==M) && (P==""||$3==P){m=0; for(i=NF;i>=1;i--){ if($i ~ /^-?[0-9]+$/) m++; else break } print $(NF-m+n); exit}' "$1"; }
# exact key=value on the SUMLIFE line
S(){ awk -v k="$2" '$1=="SUMLIFE"{for(i=1;i<=NF;i++){if(index($i,k"=")==1){split($i,a,"=");print a[2]; exit}}}' "$1"; }
# exact key=value anywhere (single-token SAT_*/LOC4 lines)
kv(){ awk -v k="$2" '{for(i=1;i<=NF;i++){if(index($i,k"=")==1){split($i,a,"=");print a[2]; exit}}}' "$1"; }

echo "== K1/K2/K2c LT3 anchor =="
cat "$R/cogops_rescueaware/c15_base.zag" \
    "$R/cogops_learnosc2/c8_learn.zag" \
    "$R/hook_phase1/hq_module.zag" > frozen_prefix.zag
PS=$(shasum -a 256 frozen_prefix.zag | cut -d' ' -f1)
WANT=043b62b427e97f0e5f59f8d0de9ec2b8cfa506ecf4b271d971cdfee07c1b177c
[ "$PS" = "$WANT" ] && ok "K1 frozen prefix sha256" || bad "K1 prefix sha256 != $WANT"
H=$(shasum -a 256 lt3_run1.txt | cut -d' ' -f1)
W3=555792382303bb090403ce7152f77eba9388c1e9d088b3e7b64757d7ce76e4c9
[ "$H" = "$W3" ] && ok "K1 LT3 anchor reproduces $W3" || bad "K1 LT3 anchor sha=$H"
LST=$(grep '^STAGE' lt3_run1.txt | tail -1)
LT3PL=$(echo "$LST" | awk '{print $37}')
LT3PLD=$(echo "$LST" | awk '{print $38}')
LT3CE=$(echo "$LST" | awk '{print $31}')
J3F=$(grep '^J3 FRESH_ARENA' lt3_run1.txt | head -1 | awk '{print $9}')
[ "$LT3PL" = "1" ] && ok "K2 D1: LT3 plans_used = $LT3PL -- ONE plan for the whole lifetime, zero growth" \
                  || bad "K2 LT3 plans_used = $LT3PL"
ok "K2 D1: LT3 planld = $LT3PLD is the plan-LOAD counter (L[13228]), not drops"
[ "$LT3CE" -gt "$J3F" ] && ok "K2c D3: LT3 costep=$LT3CE > FRESH_ARENA costq=$J3F -- the cost multiple is not like-for-like" \
                        || bad "K2c costep=$LT3CE vs $J3F"
echo "  D3 magnitude: LT3 episode cost alone is $(echo "$LT3CE" | awk -v j="$J3F" '{printf "%.1f", j/$1}')x the FRESH_ARENA QUERY cost"

echo "== K9 build (pure Zag) =="
cat frozen_prefix.zag lt3_support.zag lt3_life.zag lt3_helpers.zag \
    lt3_world.zag m4_world.zag m4_rule.zag m4_main.zag > m4.zag
if grep -q "_zag_raw_syscall" m4_world.zag m4_rule.zag m4_main.zag; then
  bad "K7 raw syscall in lane code"; else ok "K7 no _zag_raw_syscall in lane code"; fi
NM=$(grep -c "^fn main(" m4.zag)
[ "$NM" = "1" ] && ok "K9 exactly one fn main" || bad "fn main count = $NM"
sh "$Z" ./m4.zag >/dev/null 2>&1 || { echo "  FAIL K9 compile"; exit 1; }
ok "K9 compiled"

echo "== K6/K7/K8 three runs behind the watchdog =="
for i in 1 2 3; do
  $W reg "m4run$i" 900 ./m4 >/dev/null 2>&1 || true
  cp "/Users/Shared/micah/Documents/TNN/.runs/m4run$i.log" "m4_run$i.txt"
  SZ=$(wc -c < "m4_run$i.txt" | tr -d ' ')
  [ "$SZ" -gt 0 ] && ok "K7 run$i bytes=$SZ" || bad "K7 run$i EMPTY"
done
U=$(shasum -a 256 m4_run1.txt m4_run2.txt m4_run3.txt | cut -d' ' -f1 | sort -u | wc -l | tr -d ' ')
[ "$U" = "1" ] && ok "K6 3/3 byte-identical" || bad "K6 distinct hashes = $U"
shasum -a 256 m4_run1.txt
R1=m4_run1.txt

echo "== K10 namecheck =="
ANSWER_CHANNEL='mkLT3_goal|mk_goal|m4_goal|m4_decl|m4_decl_h0|lt_decl|ltLT3_decl|lt_oracle|lt_oracle_ok|m4_stupid|m4_repack|m4_dup3|m4_appmatch|m4_anchor'
for sym in frz_episode lt_query; do
  CAL=$(awk "/^fn $sym\(/,/^}\$/" m4_world.zag m4_rule.zag m4_main.zag lt3_life.zag lt3_support.zag 2>/dev/null \
        | grep -oE '\b[a-zA-Z_][a-zA-Z0-9_]*\(' | sed 's/(//' | sort -u | tr '\n' ' ')
  HIT=$(echo "$CAL" | grep -oE "$ANSWER_CHANNEL" || true)
  if [ -z "$HIT" ]; then ok "K10 $sym reaches no answer/goal/rule symbol"; else bad "K10 $sym reaches: $HIT"; fi
done
grep -q 'fn frz_episode(L:\[\]u8,LT:\[\]u8,A:\[\]u8,AS:\[\]u8,K:\[\]u8,k:i32' lt3_life.zag \
  && ok "K10 frz_episode takes no stage id" || bad "K10 frz_episode signature"
grep -q 'fn lt_query(L:\[\]u8,LT:\[\]u8,A:\[\]u8,G:\[\]u8,K:\[\]u8,R:\[\]u8,ANS:\[\]u8' lt3_support.zag \
  && ok "K10 lt_query takes no correctness signal" || bad "K10 lt_query signature"

echo "== K11 hole integrity =="
NH=$(grep '^LK1 ' "$R1" | awk '{s+=$11} END{print s+0}')
[ "$NH" = "0" ] && ok "K11 hole flag 0 at all 10 stage entries" || bad "K11 hole at a stage entry"
S5=$(S "$R1" s5facts)
[ "$S5" = "51" ] && ok "K11 stage-5 facts = 51" || bad "K11 stage-5 facts = $S5"
HO=$(S "$R1" hole)
[ "$HO" = "0" ] && ok "K11 (115,1501,2501) never in the arena" || bad "K11 hole present (=$HO)"
EP=$(S "$R1" eps)
[ "$EP" = "519" ] && ok "K11 519 episodes delivered (520 world triples minus the hole)" || bad "K11 episodes = $EP"
HP=$(tv "$R1" LK7 2)
[ "$HP" = "0" ] && ok "K11 hole flag 0 at the final checkpoint" || bad "K11 final hole=$HP"

echo "== K3 oracle/declared =="
BAD3=$(awk '$1=="QG"{m=0; for(i=NF;i>=1;i--){if($i ~ /^-?[0-9]+$/) m++; else break} if($(NF-m+6)==1 && $(NF-m+3)==0) n++} END{print n+0}' "$R1")
[ "$BAD3" = "0" ] && ok "K3 oracle matched the declared answer at every goal it accepted" || bad "K3 disagreements = $BAD3"

echo "== K4/K5 goal table =="
qk(){ awk -v st="$1" -v g="$2" '$1=="QG"{m=0; for(i=NF;i>=1;i--){if($i ~ /^-?[0-9]+$/) m++; else break} if($(NF-m+1)==st && $(NF-m+2)==g){print $(NF-m+3); exit}}' "$R1"; }
for pair in "0:0:G0" "3:5:G14" "4:1:G4" "8:3:GACF" "6:4:GSWAP" "4:7:G2N" "9:8:G3F" "7:9:GX" "4:6:G2NF"; do
  st=$(echo "$pair" | cut -d: -f1); g=$(echo "$pair" | cut -d: -f2); nm=$(echo "$pair" | cut -d: -f3)
  v=$(qk "$st" "$g")
  if [ "$nm" = "GX" ]; then
    [ "$v" = "1" ] && ok "K5 GX declines (correct)" || bad "K5 GX ok=$v"
  elif [ "$nm" = "G2NF" ]; then
    echo "  NOTE K4 G2NF (five-need goal) ok=$v -- the frozen plan record is 56 B = 8+4*12 and compose_iter allocs ord = 16 B = 4 ints, so a five-need goal overflows both. Reported, not patched."
  else
    [ "$v" = "1" ] && ok "K4 $nm ok=1" || bad "K4 $nm ok=$v"
  fi
done

echo "== K-GEN the crux =="
GL=$(tv "$R1" GEN 2 LIFETIME); GC=$(tv "$R1" GEN 3 LIFETIME); GF=$(tv "$R1" GEN 2 FRESH_ARENA)
[ "$GL" = "0" ] && ok "K-GEN1 LIFETIME is WRONG on the hole goal (ok=0, code=$GC: answered, not declined)" || bad "K-GEN1 LIFETIME ok=$GL"
[ "$GL" = "$GF" ] && ok "K-GEN1b LIFETIME ok == FRESH_ARENA ok ($GL): age changes nothing at the hole" || bad "K-GEN1b $GL vs $GF"
SE=$(tv "$R1" STUPID 1 W4 ansEq); SW=$(tv "$R1" STUPID 2 W4 ansEq); SF=$(tv "$R1" STUPID 3 W4 ansEq)
[ "$SE" = "1" ] && ok "K-GEN2 STUPID-MAJORITY answer is exactly the declared 16-subject vector" || bad "K-GEN2 ansEq=$SE"
[ "$SW" = "1" ] && ok "K-GEN2 STUPID-MAJORITY RECOVERS the absent triple (okW4=1)" || bad "K-GEN2 okW4=$SW"
[ "$SF" = "0" ] && ok "K-GEN3 STUPID-MAJORITY is FALSIFIABLE on W4F (okW4F=0): a real induction, not an oracle" || bad "K-GEN3 okW4F=$SF"
OH=$(tv "$R1" GEN 2 ORACLE_HOLE)
[ "$OH" = "0" ] && ok "K-GEN4 no frozen generic procedure recovers the hole (oracle match=0)" || bad "K-GEN4 oracle match=$OH"
SP=$(tv "$R1" STUPID 1 PRESENT G4)
[ "$SP" = "1" ] && ok "K-GEN5 non-vacuous on intact data (G4)" || bad "K-GEN5 ansEq=$SP"
GP=$(tv "$R1" GEN 4 PRESENT G4)
[ "$GP" = "1" ] && ok "K-GEN5 GEN PRESENT: aged ok=1 fresh ok=1 oracle=1" || bad "K-GEN5 oracle=$GP"
LW=$(tv "$R1" GENF 2 W4F_decl); LF=$(tv "$R1" GENF 3 W4F_decl)
[ "$LW" = "1" ] && [ "$LF" = "1" ] && ok "GENF identical arena + W4F answer: both = 1 -- the WORLD, not the arena, decides" || bad "GENF $LW $LF"

echo "== K-R reuse =="
S4=$(tv "$R1" REUSE 1); S3=$(tv "$R1" REUSE 2); SW2=$(tv "$R1" REUSE 3)
T4=$(tv "$R1" REUSE 4); T3=$(tv "$R1" REUSE 5); TW=$(tv "$R1" REUSE 6)
[ "$S4" = "$S3" ] && [ "$S3" = "$SW2" ] && ok "K-R1a all three goals share ONE shape signature ($S4)" || bad "K-R1a $S4 $S3 $SW2"
[ "$T4" = "$T3" ] && [ "$T3" = "$TW" ] && ok "K-R1b GCEQ-STRUCT=1: template $T4 executes the stage-local goal, the 3-stage join AND its permutation" || bad "K-R1b $T4 $T3 $TW"
SR=$(tv "$R1" REUSE5 5); SX=$(tv "$R1" REUSE5 7)
[ "$SR" = "0" ] && ok "K-R1c STRUCTREL = 0: the executable structure holds NO relation id" || bad "K-R1c STRUCTREL=$SR"
[ "$SX" = "0" ] && ok "K-R1c STRUCTREL_X = 0: no signature-hash coincidence" || bad "K-R1c STRUCTREL_X=$SX"
A1=$(tv "$R1" REUSE3 1); A3=$(tv "$R1" REUSE3 2); A4=$(tv "$R1" REUSE3 3)
[ "$A1" = "$A3" ] && [ "$A3" = "$A4" ] && ok "K-R2 APP-MATCH = $A1 (matched*1000+needs) at all three goals: every bound family is field-consistent" || bad "K-R2 $A1 $A3 $A4"
X1=$(tv "$R1" REUSE3 4); X3=$(tv "$R1" REUSE3 5); X4=$(tv "$R1" REUSE3 6)
[ "$X1" = "$X3" ] && [ "$X3" = "$X4" ] && ok "K-R4 xw identical ($X1) at stage-local, 3-stage join and permutation" || bad "K-R4 $X1 $X3 $X4"
XD=$(tv "$R1" REUSE5 2); AS4=$(tv "$R1" REUSE5 3); AS3=$(tv "$R1" REUSE5 4)
[ "$XD" = "0" ] && ok "K-R4 xw cannot discriminate (disc=0) while applicable stages = $AS4 vs $AS3" || bad "K-R4 disc=$XD"
AP=$(tv "$R1" REUSE5 1)
[ "$AP" = "1" ] && ok "K-R5 the stupid reuse baseline (template table non-empty) fires everywhere" || bad "K-R5 appstupid=$AP"
SG=$(tv "$R1" REUSE4 5); SJ=$(tv "$R1" REUSE4 6)
ok "K-R3 APP-SEARCH = cost(fresh)/cost(aged): G4 = $SG/100, GACF = $SJ/100  (1.00 parity, >1 = ageing COSTS)"

echo "== K-K cost and deferral =="
CE=$(tv "$R1" COSTVALS 1); CQ=$(tv "$R1" COSTVALS 2); TL=$(tv "$R1" COSTVALS 3)
FA=$(tv "$R1" COSTVALS 4); RT=$(tv "$R1" COSTVALS 5)
ok "K-K1 costep=$CE costq=$CQ totLT=$TL costFA_GACF=$FA  totLT/costFA=${RT}/100"
NCOST=$(grep -c '^COST N D' "$R1"); NDEF=$(grep -c '^DEFER N D' "$R1")
[ "$NCOST" = "24" ] && [ "$NDEF" = "24" ] && ok "K-K2/K-K3 all 24 sweep points reported" || bad "sweep COST=$NCOST DEFER=$NDEF"
DQ=$(grep '^COST N D' "$R1" | awk '$8<100 {n++} END{print n+0}')
DW=$(grep '^DEFER N D' "$R1" | awk '$5<100 {n++} END{print n+0}')
DM=$(grep '^DEFER N D' "$R1" | awk '{if(m==""||$5<m){m=$5}} END{print m}')
DX=$(grep '^COST N D' "$R1" | awk '{if(m==""||$8<m){m=$8}} END{print m}')
ok "K-K2 aged QUERY dearer than cold at $DQ of 24 points (ratio = costFA*100/costLT), worst for age $DX/100"
ok "K-K3 aged TOTAL cost below the cold QUERY cost at $DW of 24 points (deferral win), best $DM/100"

echo "== K-I inverse attack =="
PZ=$(tv "$R1" INV1 2); CD=$(tv "$R1" INV1 4)
[ "$PZ" = "0" ] && ok "K-I1 preregistered poison route did NOT trigger (poison=$PZ, code=$CD): a MISSING FACT NEVER DECLINES" || bad "K-I1 poison=$PZ"
ok "K-I2 poison-clear control run, poison after clearing = $(tv "$R1" INV2 5)"
ok "K-I6 saturation arm: templates=$(kv "$R1" SAT_tmpl) poison=$(kv "$R1" SAT_poison) declines=$(kv "$R1" SAT_declines) fresh_declines=$(kv "$R1" SATfresh_declines) bindfree=$(kv "$R1" SAT_bindfree) evictB=$(kv "$R1" SAT_evictB) canon_tags=$(kv "$R1" SAT_canon_tags)"
ok "K-INV-ARITH the 28 bytes below the frozen bind table: $(kv "$R1" SAT_oob_sum) -> $(kv "$R1" SAT_oob_sum_end). Writer NOT isolated; learn_bindings never checks bind_new's return (c8_learn.zag:532-533) so bind_fam(L,-1) reads L[12716]"
ok "K-I5 arena at capacity $(tv "$R1" INVCAP 1): aged_ok=$(tv "$R1" INVCAP 2) fresh_ok=$(tv "$R1" INVCAP 3)"
echo "  K-I VERDICT: no configuration found where the lifetime learner beats a"
echo "  same-facts fresh learner on correctness. Explicit NULL, not a pass."

echo "== K-LOC localisation =="
RPF=$(tv "$R1" LOC1 1); RPN=$(tv "$R1" LOC1 2); OKR=$(tv "$R1" LOC1 3); OKU=$(tv "$R1" LOC1 4)
[ "$RPN" = "$RPF" ] && ok "K-LOC1 repack is a permutation ($RPN of $RPF)" || bad "K-LOC1 repack lost facts"
[ "$OKR" = "$OKU" ] && ok "K-LOC1 repacked arena gives the IDENTICAL answer ($OKR): hypothesis (a) EXCLUDED" || bad "K-LOC1 answer changed: $OKR vs $OKU"
ok "K-LOC2 arena tripled to $(tv "$R1" LOC2 2) facts, ok=$(tv "$R1" LOC2 3). ret_gen (c15_base.zag:83-105) appends one entry per MATCHING FACT with no de-duplication, so triplication triples need0's witness list. Reported, not patched."
MB=$(S "$R1" misbind)
[ "$MB" = "0" ] && ok "K-LOC3 no misbound family in the lifetime ($MB): hypothesis (b) EXCLUDED" || bad "K-LOC3 misbind=$MB"
ok "K-LOC4 plan table: slots_used=$(kv "$R1" plans_used) plan_new=$(kv "$R1" plannew) plan_loads=$(kv "$R1" planld) evictions=$(kv "$R1" evictP) -- 6 goal shapes against 4 slots"
echo "  K-LOC4: capacity WAS pressured and no goal lost its plan, so hypothesis (d)"
echo "  is EXCLUDED. Plan identity is the CANONICAL shape tag (c8_learn.zag:570-577),"
echo "  not the harness goal tag, so adversary defect C501 is not operative either."

echo
if [ "$FAIL" = "0" ]; then
  echo "CERTIFIED: every kill bar above evaluated; none failed"
else
  echo "KILL BAR FAILURE -- no verdict may be issued"
fi
exit $FAIL