#!/bin/bash
# Independent check for EXP-3: re-derive key metrics from the transcript
# with awk, WITHOUT trusting the driver's own cl_check/AGG lines.
# Compares independent recomputation vs driver-reported values.
# Usage: ./check_nr.sh <transcript> <variant: A|B> <scale: small|scale>
set -u
F=${1:?transcript}; V=${2:?variant}; S=${3:?scale}
if [ "$S" = small ]; then NS=1; else NS=10; fi
NT=$((NS*6))
pass=0; fail=0
chk(){ if eval "$2"; then echo "PASS(indep): $1"; pass=$((pass+1)); else echo "FAIL(indep): $1"; fail=$((fail+1)); fi; }

# --- independent recomputation from transcript verbs ---
C2_ABSTAIN=$(awk -F, '/^TR_CHOICE2/{if($4==-1)c++} END{print c+0}' "$F")
C2_TRUE=$(awk -F, '/^TR_CHOICE2/{if($4==0)c++} END{print c+0}' "$F")
C2_FALSE=$(awk -F, '/^TR_CHOICE2/{if($4==1)c++} END{print c+0}' "$F")
M2=$(awk -F, '/^TR_CHOICE2/{m+=($5-$6)} END{print m+0}' "$F")
C3_TRUE=$(awk -F, '/^TR_CHOICE3/{if($4==0)c++} END{print c+0}' "$F")
C3_FALSE=$(awk -F, '/^TR_CHOICE3/{if($4==1)c++} END{print c+0}' "$F")
C3_ABSTAIN=$(awk -F, '/^TR_CHOICE3/{if($4==-1)c++} END{print c+0}' "$F")
M3=$(awk -F, '/^TR_CHOICE3/{m+=($5-$6)} END{print m+0}' "$F")
NREVISE=$(grep -c '^TR_REVISE' "$F")
NREVISE_TRUE=$(grep -c '^TR_REVISE,[0-9]*,0,' "$F")
NCONCEDE_F=$(grep -c '^TR_CONCEDE,[0-9]*,1,' "$F")
NVERIFY=$(grep -c '^TR_VERIFY' "$F")
NVERIFY_BAD=$(grep '^TR_VERIFY' "$F" | grep -vc ',1,1$')
NRC_BAD=$(grep '^TR_REVISE' "$F" | grep -vc ',0,0,0,0,0,')
NREPLAY_BAD=$(grep -c 'CL_CHECK,sess_replay_[a-z]*,[^0]' "$F")
NQX_NONE=$(awk -F, '/^TR_QX/{if($5==0)c++} END{print c+0}' "$F")
NTBDIAG_TRUE=$(awk -F, '/^TR_TBDIAG/{if($4==0)c++} END{print c+0}' "$F")

# --- driver-reported values ---
D_M2=$(grep -oE 'CL_CHECK,[ab]_margin2,-?[0-9]+' "$F" | head -1 | awk -F, '{print $3}')
D_M3=$(grep -oE 'CL_CHECK,[ab]_margin3,-?[0-9]+' "$F" | head -1 | awk -F, '{print $3}')
D_REVISED=$(grep -oE '^[0-9]+,false_revised$' "$F" | awk -F, '{print $1}')

echo "== independent recomputation vs driver =="
chk "margin2-match"      "[ \"$M2\" = \"$D_M2\" ]"
chk "margin3-match"      "[ \"$M3\" = \"$D_M3\" ]"
chk "revise-count-match" "[ \"$NREVISE\" = \"$D_REVISED\" ]"

echo "== transcript-level expectations =="
if [ "$V" = A ]; then
  chk "A: R2 abstains=$NT"      "[ \"$C2_ABSTAIN\" = \"$NT\" ]"
  chk "A: R2 true-picks=0"      "[ \"$C2_TRUE\" = 0 ]"
  chk "A: R3 true-picks=$((NT*4/6))" "[ \"$C3_TRUE\" = \"$((NT*4/6))\" ]"
  chk "A: R3 abstains=$((NT*2/6))"   "[ \"$C3_ABSTAIN\" = \"$((NT*2/6))\" ]"
  chk "A: tbdiag all TRUE"      "[ \"$NTBDIAG_TRUE\" = \"$NT\" ]"
  chk "A: margin2=0"            "[ \"$M2\" = 0 ]"
else
  chk "B: R2 false-picks=$NT"   "[ \"$C2_FALSE\" = \"$NT\" ]"
  chk "B: R2 true-picks=0"      "[ \"$C2_TRUE\" = 0 ]"
  chk "B: R3 false-picks=$NT"   "[ \"$C3_FALSE\" = \"$NT\" ]"
  chk "B: overclaim-exposed=$NT" "[ \"$NQX_NONE\" = \"$NT\" ]"
  chk "B: margin2=$((-4*NT))"   "[ \"$M2\" = \"$((-4*NT))\" ]"
  chk "B: margin3=$((-28*NT/6))" "[ \"$M3\" = \"$((-28*NT/6))\" ]"
fi
chk "revise=$((NT*3))"          "[ \"$NREVISE\" = \"$((NT*3))\" ]"
chk "no-true-revisions"         "[ \"$NREVISE_TRUE\" = 0 ]"
chk "concede-false=$((NT*3))"   "[ \"$NCONCEDE_F\" = \"$((NT*3))\" ]"
chk "verify-lines=$((NT*16))"   "[ \"$NVERIFY\" = \"$((NT*16))\" ]"
if [ "$V" = A ]; then
  chk "verify-all-good"           "[ \"$NVERIFY_BAD\" = 0 ]"
else
  NNONV_SIDE_NOT0=$(grep '^TR_VERIFY' "$F" | grep -v ',1,1$' | awk -F, '$4!=0' | wc -l)
  NV_SIDE_NOT1=$(grep '^TR_VERIFY' "$F" | grep ',1,1$' | awk -F, '$4!=1' | wc -l)
  chk "B: non-verifying lines are all side-0(TRUE)" "[ \"$NNONV_SIDE_NOT0\" = 0 ]"
  chk "B: verifying lines are all side-1(FALSE)"   "[ \"$NV_SIDE_NOT1\" = 0 ]"
  chk "B: half/half split" "[ \"$NVERIFY_BAD\" = \"$((NVERIFY/2))\" ]"
fi
chk "revise-rc-all-zero"        "[ \"$NRC_BAD\" = 0 ]"
chk "replays-exact"             "[ \"$NREPLAY_BAD\" = 0 ]"
chk "no-falsified"              "! grep -q 'FALSIFIED_F' $F"

echo "== RESULT(indep): pass=$pass fail=$fail =="
[ "$fail" -eq 0 ]
