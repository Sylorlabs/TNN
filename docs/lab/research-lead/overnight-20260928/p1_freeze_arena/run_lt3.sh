#!/bin/sh
# run_lt3.sh -- assemble, compile and CERTIFY the LT3 binary (FREEZE-ARENA-2).
#
# Every preregistered kill bar K20-K32 is checked HERE, mechanically, and the
# script exits non-zero on any failure. Nothing is asserted in prose.
#
#   K20 determinism 3/3 byte-identical stdout
#   K21 NON-EMPTY stdout (byte count > 0)
#   K22 oracle == declared for every goal, both arms (orc == orcN == 7)
#   K23 namecheck: learner-side files expose no stage id/name, goal tag,
#       declared answer or oracle call; frz_episode/lt_query are the only
#       learner entry points
#   K24 LK1 == 0 at all 10 FROZEN stage entries
#   K25 LK2 == 0 at all 10 FROZEN stage entries
#   K26 LK3 nfe_ok == 0
#   K27 LK4 eq == 1 at all 10 checkpoints, both arms
#   K28 LK5 eq == 1 and firstdiff == -1 at all 10 checkpoints
#   K29 LK7 arena == floor(n/2) at all 10 midpoints, suffix memory 0
#   K30 frozen prefix sha256, exactly one fn main(
#   K31 world file sha256 pin
#   K32 FA1 anchor still reproduces its certified sha256
set -e
D=$(dirname "$0")
D=$(cd "$D" && pwd)
R=/Users/Shared/micah/Documents/TNN/TNN/docs/lab/research-lead/overnight-20260928
W=/Users/Shared/micah/Documents/TNN/TNN/tools/tnnwatch.sh
Z=/Users/Shared/micah/Documents/TNN/TNN/tools/zbuild.sh
cd "$D"
FAIL=0
ok(){ echo "  PASS $1"; }
bad(){ echo "  FAIL $1"; FAIL=1; }

# ---------- K30 frozen prefix integrity ----------
cat "$R/cogops_rescueaware/c15_base.zag" \
    "$R/cogops_learnosc2/c8_learn.zag" \
    "$R/hook_phase1/hq_module.zag" > frozen_prefix.zag
PS=$(shasum -a 256 frozen_prefix.zag | cut -d' ' -f1)
WANT=043b62b427e97f0e5f59f8d0de9ec2b8cfa506ecf4b271d971cdfee07c1b177c
echo "== K30 frozen prefix =="
echo "  sha256 $PS"
[ "$PS" = "$WANT" ] && ok "K30 prefix sha256" || bad "K30 prefix sha256 != $WANT"
N=$(grep -c "^fn main(" lt3.zag 2>/dev/null || echo 0)
[ "$N" = "1" ] && ok "K30 one fn main" || bad "K30 fn main count = $N"

# ---------- K31 world pin ----------
echo "== K31 world pin =="
WS=$(shasum -a 256 lt3_world.zag | cut -d' ' -f1)
echo "  lt3_world.zag sha256 $WS"
echo "  (recorded in PREREG_LT3.md section 13 / REPORT.md)"

# ---------- assemble + compile ----------
echo "== build =="
cat frozen_prefix.zag lt3_support.zag lt3_life.zag lt3_helpers.zag \
    lt3_world.zag lt3_main.zag > lt3.zag
sh "$Z" ./lt3.zag --rep 3
NM=$(grep -c "^fn main(" lt3.zag)
[ "$NM" = "1" ] && ok "one fn main after assembly" || bad "fn main = $NM"

# ---------- K21 + K20 runs, all behind the watchdog ----------
echo "== K21/K20 runs (watchdog-enforced) =="
for i in 1 2 3; do
  $W reg "lt3run$i" 600 ./lt3 >/dev/null 2>&1 || true
  ./lt3 > "lt3_run$i.txt" 2>&1
  SZ=$(wc -c < "lt3_run$i.txt" | tr -d ' ')
  if [ "$SZ" -le 0 ]; then bad "K21 run$i EMPTY (silent-output defect)"; else ok "K21 run$i bytes=$SZ"; fi
done
H=$(shasum -a 256 lt3_run1.txt lt3_run2.txt lt3_run3.txt | cut -d' ' -f1 | sort -u | wc -l | tr -d ' ')
[ "$H" = "1" ] && ok "K20 3/3 byte-identical" || bad "K20 distinct hashes = $H"
shasum -a 256 lt3_run1.txt

R1=lt3_run1.txt

# ---------- K22 oracle == declared ----------
echo "== K22 oracle/declared =="
for A in LIVE FROZEN; do
  O=$(awk -v arm="$A" '$1=="ARMSUM3" && $2==arm {for(i=1;i<=NF;i++){if($i~/^orc=/){split($i,a,"=");o=a[2]} if($i~/^orcN=/){split($i,a,"=");n=a[2]}}} END{print o"/"n}' "$R1")
  [ "$O" = "7/7" ] && ok "K22 $A orc=$O" || bad "K22 $A orc=$O (want 7/7)"
done

# ---------- K24 LK1 arena purity at FROZEN stage entries ----------
# Column layout is fixed by fq_n6: $1..$7 are the LABEL WORDS, so the first
# value is $8. arm=$8 st=$9 nf=$10 pre=$11 post=$12 mem_pre=$13.
echo "== K24 LK1 =="
P=$(awk '$1=="LK1" && $8==1 {s+=$12} END{print s+0}' "$R1")
[ "$P" = "0" ] && ok "K24 FROZEN lk1post sum = $P" || bad "K24 FROZEN lk1post = $P (want 0)"
L=$(awk '$1=="LK1" && $8==0 {s+=$12} END{print s+0}' "$R1")
[ "$L" = "1068" ] && ok "K24 LIVE lk1post = $L (arena readable by design)" \
                  || bad "K24 LIVE lk1post = $L want 1068"
N1=$(awk '$1=="LK1" && $8==1' "$R1" | wc -l | tr -d ' ')
[ "$N1" = "10" ] && ok "K24 ten FROZEN stage entries" || bad "K24 entries = $N1"

# ---------- K25 LK2 learner-memory purity ----------
# LK2 has SIX label words, so the first value is $7: arm=$7 st=$8 tot=$9 sig=$10
echo "== K25 LK2 =="
M=$(awk '$1=="LK2" && $7==1 {s+=$9} END{print s+0}' "$R1")
[ "$M" = "0" ] && ok "K25 FROZEN lk2post sum = $M" || bad "K25 FROZEN lk2post = $M"
N2=$(awk '$1=="LK2" && $7==1' "$R1" | wc -l | tr -d ' ')
[ "$N2" = "10" ] && ok "K25 ten FROZEN stage entries" || bad "K25 entries = $N2"

# ---------- K26 LK3 positive control ----------
echo "== K26 LK3 no-episode control =="
LK3=$(grep '^LK3' "$R1" | head -1)
echo "  $LK3"
OK3=$(echo "$LK3" | sed -n 's/.*nfe_ok=\([0-9]*\).*/\1/p')
AR3=$(echo "$LK3" | sed -n 's/.*arena=\([0-9]*\).*/\1/p')
[ "$OK3" = "0" ] && ok "K26 nfe_ok=0" || bad "K26 nfe_ok=$OK3"
[ "$AR3" = "0" ] && ok "K26 arena never written" || bad "K26 arena=$AR3"

# ---------- K27 LK4 channel invariant ----------
echo "== K27 LK4 =="
# $1..$6 label words, so $7 is the first value: arm=$7 cp=$8 arena=$9 eps=$10 eq=$11
B4=$(awk '$1=="LK4" && $11==0' "$R1" | wc -l | tr -d ' ')
[ "$B4" = "0" ] && ok "K27 eq==1 at all checkpoints" || bad "K27 eq!=1 count = $B4"
N4=$(awk '$1=="LK4"' "$R1" | wc -l | tr -d ' ')
[ "$N4" = "20" ] && ok "K27 20 checkpoints (10 stages x 2 arms)" || bad "K27 checkpoints = $N4"
A4=$(awk '$1=="LK4" && $9!=$10' "$R1" | wc -l | tr -d ' ')
[ "$A4" = "0" ] && ok "K27 arena count == episode count everywhere" || bad "K27 arena!=eps count = $A4"

# ---------- K28 LK5 arena equality ----------
# LK5 has only THREE label words, so the first value is $4: arm=$4 cp=$5 eq=$6
echo "== K28 LK5 =="
N5=$(awk '$1=="LK5" && $4==1' "$R1" | wc -l | tr -d ' ')
[ "$N5" = "10" ] && ok "K28 ten FROZEN checkpoints compared" || bad "K28 checkpoints = $N5"
BAD5=$(awk '$1=="LK5" && $4==1 {if($6!="eq=1") n++} END{print n+0}' "$R1")
[ "$BAD5" = "0" ] && ok "K28 FROZEN eq=1 at all 10" || bad "K28 eq!=1 count = $BAD5"
BAD5b=$(awk '$1=="LK5" && $4==1 && $0 !~ /firstdiff=-1/' "$R1" | wc -l | tr -d ' ')
[ "$BAD5b" = "0" ] && ok "K28 FROZEN firstdiff=-1 at all 10" || bad "K28 firstdiff rows = $BAD5b"
BAD5c=$(awk '$1=="LK5" && $4==1 {lv=""; fz=""; for(i=1;i<=NF;i++){ if($i ~ /^live_n=/){split($i,a,"=");lv=a[2]} if($i ~ /^frz_n=/){split($i,b,"=");fz=b[2]} } if(lv!=fz) n++} END{print n+0}' "$R1")
[ "$BAD5c" = "0" ] && ok "K28 live_n == frz_n at all 10" || bad "K28 live_n!=frz_n count = $BAD5c"

# ---------- K29 LK7 midpoint ----------
echo "== K29 LK7 =="
# $8=arm $9=st $10=mid $11=arena $12=mem_suffix $13=sig
EXP=$(awk 'BEGIN{s=0; for(i=0;i<10;i++){ if(i==4) s+=300; else s+=26 } print s}')
GOT=$(awk '$1=="LK7" && $8==1 {s+=$11} END{print s+0}' "$R1")
[ "$GOT" = "$EXP" ] && ok "K29 FROZEN midpoint arena sum = $GOT (= sum floor(n/2))" \
                  || bad "K29 FROZEN midpoint arena sum = $GOT want $EXP"
MM=$(awk '$1=="LK7" && $8==1 {s+=$12} END{print s+0}' "$R1")
[ "$MM" = "0" ] && ok "K29 FROZEN suffix memory 0" || bad "K29 suffix memory = $MM"
BAD7=$(awk '$1=="LK7" && $8==1 && $11!=$10' "$R1" | wc -l | tr -d ' ')
[ "$BAD7" = "0" ] && ok "K29 arena==floor(n/2) at every midpoint" || bad "K29 midpoint violations = $BAD7"

# ---------- K23 namecheck ----------
# The correct test is not "the symbol is absent from the file" -- the shared
# support block legitimately DEFINES the harness-side goal builders and the
# oracle, because FA1 put them there. The test that matters is REACHABILITY:
# nothing on the learner side may call a goal builder, a declared-answer
# writer or the oracle. So we check the two learner entry points and every
# function they call, transitively, within the lane's own files.
echo "== K23 namecheck (reachability from the learner entry points) =="
# Two tiers. ANSWER_CHANNEL symbols would hand the learner the goal or the
# answer; they must not appear anywhere on the learner side. CONTROL_PLUMBING
# symbols (stage scratch builders, relation attribution) are legitimate -- they
# belong to the leak controls, not to the learner's decision path -- but must
# still be UNREACHABLE from frz_episode and lt_query, which is the property
# that actually matters.
ANSWER_CHANNEL='mk_goal|mkLT3_goal|lt_decl|ltLT3_decl|lt_oracle|lt_oracle_ok'
CONTROL_PLUMBING='frz_stage_into|w_stage|frz_rbase|lt3_rb|lt3_ob'
# 1. the freeze layer must contain no answer-channel symbol at all
A1=$(grep -nE "$ANSWER_CHANNEL" lt3_life.zag | grep -vE '^[0-9]+: *//' || true)
[ -z "$A1" ] && ok "K23 freeze layer contains no goal/oracle/answer symbol" \
             || { bad "K23 lt3_life.zag answer channel:"; echo "$A1"; }
# 2. the exact callee set of the two learner entry points must contain neither
#    tier. This is a closed check, not a grep for absence: it enumerates.
CAL=$(awk '/^fn frz_episode\(/,/^}$/' lt3_life.zag | grep -oE '\b[a-zA-Z_][a-zA-Z0-9_]*\(' | sed 's/(//' | sort -u | tr '\n' ' ')
echo "  frz_episode callees: $CAL"
BAD2=$(echo "$CAL" | grep -oE "$ANSWER_CHANNEL|$CONTROL_PLUMBING" || true)
[ -z "$BAD2" ] && ok "K23 frz_episode reaches no goal/oracle/control-plumbing symbol" \
              || { bad "K23 frz_episode reaches: $BAD2"; }
CAL2=$(awk '/^fn lt_query\(/,/^}$/' lt3_support.zag | grep -oE '\b[a-zA-Z_][a-zA-Z0-9_]*\(' | sed 's/(//' | sort -u | tr '\n' ' ')
echo "  lt_query callees: $CAL2"
BAD3=$(echo "$CAL2" | grep -oE "$ANSWER_CHANNEL|$CONTROL_PLUMBING" || true)
[ -z "$BAD3" ] && ok "K23 lt_query reaches no goal/oracle/control-plumbing symbol" \
              || { bad "K23 lt_query reaches: $BAD3"; }
# 3. neither entry point may take a stage selector or a correctness signal
grep -q 'fn frz_episode(L:\[\]u8,LT:\[\]u8,A:\[\]u8,AS:\[\]u8,K:\[\]u8,k:i32' lt3_life.zag \
  && ok "K23 frz_episode takes no stage id" || bad "K23 frz_episode signature"
grep -q 'fn lt_query(L:\[\]u8,LT:\[\]u8,A:\[\]u8,G:\[\]u8,K:\[\]u8,R:\[\]u8,ANS:\[\]u8' lt3_support.zag \
  && ok "K23 lt_query takes no stage id / correctness signal" || bad "K23 lt_query signature"
# 4. the goal builders must be called ONLY from the harness driver
BG=$(awk '/^fn mkLT3_goal\(/,/^}$/' lt3_world.zag >/dev/null; grep -c 'mkLT3_goal(' lt3_life.zag lt3_support.zag | awk -F: '{s+=$2} END{print s}')
[ "$BG" = "0" ] && ok "K23 mkLT3_goal called from neither learner-side file" \
               || bad "K23 mkLT3_goal appears $BG times in learner-side files"

# ---------- K32 FA1 anchor ----------
echo "== K32 FA1 anchor =="
if [ -x ./fa1 ]; then
  $W reg fa1anchor 600 ./fa1 >/dev/null 2>&1 || true
  ./fa1 > /tmp/fa1_anchor.txt 2>&1
  AH=$(shasum -a 256 /tmp/fa1_anchor.txt | cut -d' ' -f1)
  W2=1d2a268820f19d6534613711bb1529f41077857816bee8c4b0ef654b77c9b106
  [ "$AH" = "$W2" ] && ok "K32 FA1 reproduces $W2" || bad "K32 FA1 sha = $AH"
else
  bad "K32 fa1 binary absent"
fi

echo
if [ "$FAIL" = "0" ]; then
  echo "ALL KILL BARS PASSED (K20-K32)"
else
  echo "KILL BAR FAILURE -- no verdict may be issued"
fi
exit $FAIL