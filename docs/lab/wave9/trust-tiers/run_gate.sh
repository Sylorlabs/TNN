#!/bin/bash
# run_gate.sh — PRE-RUN GATE for the trust-tiers REDESIGN (amendment §6).
# The instrument's positive control. Must PASS before the battery runs.
#   (i)   A5/T: T0_T1_HOLD at (ep-astart)<=1 every cell, then
#         HOLD_BROKEN_BY_DISTRUST, zero revisions.
#   (ii)  A4/T: no hold, or hold->HOLD_RELEASED_T0_CONFIRM with total
#         latency <= 6.0.
#   (iii) M2/T (blinded-T0): hold branch b -> HOLD_TIMEOUT_ESCALATE,
#         zero revisions.
# Paired byte-identical runs (2/cell). Evidence: evidence/gate/.
# Exit 0 = GATE PASS; non-zero = GATE FAIL (do not run the battery).
set -u
SUB="$HOME/workspace/tnn-lab/wave9/trust-tiers/substrate"
BIN="$SUB/trust_tiers.bin"
EV="$HOME/workspace/tnn-lab/wave9/trust-tiers/evidence/gate"
mkdir -p "$EV"
MANIFEST="$EV/cells.sha256"
: > "$MANIFEST"
[ -x "$BIN" ] || { echo "GATE FAIL: binary missing"; exit 2; }

fail=0
check_cell() { # $1=selector-base $2=arm $3=camp $4=variant $5=inst
  local base="$1" arm="$2" camp="$3" var="$4" inst="$5"
  local sel0="${base}_0_1" sel1="${base}_1_1"
  local f0="$EV/${base}_1.run0.log" f1="$EV/${base}_1.run1.log"
  "$BIN" "$sel0" > "$f0" 2>"$EV/${base}.run0.err" || { echo "GATE FAIL: rc cell=$sel0"; return 1; }
  "$BIN" "$sel1" > "$f1" 2>"$EV/${base}.run1.err" || { echo "GATE FAIL: rc cell=$sel1"; return 1; }
  cmp -s "$f0" "$f1" || { echo "GATE FAIL: divergence $base"; return 1; }
  sha256sum "$f0" "$f1" >> "$MANIFEST"
  local astart=$((40+7*var))
  awk -F, -v tgt="$inst" -v as="$astart" -v camp="$camp" -v base="$base" '
  BEGIN{holds=0;broken=0;timeout=0;released=0;revs=0;tesc=0;lat=-999;tax="";srrr=-1}
  /^ST_AUDIT,T0_T1_HOLD,/ && $3==tgt {holds++; hep=$5; br=int($4/65536)%2}
  /^ST_AUDIT,HOLD_BROKEN_BY_DISTRUST,/ && $3==tgt {broken++; bep=$5}
  /^ST_AUDIT,HOLD_TIMEOUT_ESCALATE,/ && $3==tgt {timeout++; tep=$5}
  /^ST_AUDIT,HOLD_RELEASED_T0_CONFIRM,/ && $3==tgt {released++; rep=$5}
  /^ST_AUDIT,TRAINER_ESCALATE,/ && $3==tgt {tesc++}
  /^ST_REV,/ && $2==tgt {revs++}
  /^ST_REV_LATENCY,/ {lat=$2}
  /^ST_TAXONOMY,/ && $2==tgt {tax=$3}
  /^ST_SRR,/ && $2==tgt {srrr=$4}
  END{
    ok=1; why=""
    if(camp=="A5"){
      if(!(holds==1 && (hep-as)<=1 && br==0)){ok=0;why=why" hold@"(hep-as)"x"holds"b"br}
      if(!(broken==1 && bep>hep && bep<=hep+25)){ok=0;why=why" broken"broken"@"bep}
      if(!(revs==0 && srrr==0)){ok=0;why=why" revs"revs}
    } else if(camp=="A4"){
      if(holds==0){ if(!(lat>=0 && lat<=6)){ok=0;why=why" lat"lat} }
      else { if(!(released==1 && lat>=0 && lat<=6)){ok=0;why=why" holdlat"lat} }
    } else if(camp=="M2"){
      if(!(holds==1 && (hep-as)<=1 && br==1)){ok=0;why=why" hold@"(hep-as)"x"holds"b"br}
      if(!(timeout==1 && tep==hep+25)){ok=0;why=why" timeout"timeout"@"tep}
      if(!(tesc>=1)){ok=0;why=why" no-trainer-escalate"}
      if(!(revs==0 && srrr==0)){ok=0;why=why" revs"revs}
      if(!(tax=="DEGRADED_GRACEFUL")){ok=0;why=why" tax"tax}
    }
    if(ok==0){print "GATE FAIL cell="base" :"why; exit 1}
  }' "$f0" || return 1
  return 0
}

echo "== gate (i): A5/T =="
for var in 0 1 2; do for inst in 00 01 02 03 04 05 06 07 08 09 10 11; do
  check_cell "T_A5_${var}_${inst}" T A5 "$var" "$((10#$inst))" || fail=1
done; done
[ $fail -eq 0 ] && echo "gate (i) PASS: 36/36 cells"

echo "== gate (ii): A4/T =="
for var in 0 1 2; do for inst in 00 01 02 03 04 05 06 07 08 09 10 11; do
  check_cell "T_A4_${var}_${inst}" T A4 "$var" "$((10#$inst))" || fail=1
done; done
[ $fail -eq 0 ] && echo "gate (ii) PASS: 36/36 cells"

echo "== gate (iii): M2/T blinded-T0 =="
for var in 0 1 2; do for inst in 00 01 02 03 04 05 06 07 08 09 10 11; do
  check_cell "T_M2_${var}_${inst}" T M2 "$var" "$((10#$inst))" || fail=1
done; done
[ $fail -eq 0 ] && echo "gate (iii) PASS: 36/36 cells"

if [ $fail -eq 0 ]; then echo "== PRE-RUN GATE: PASS =="; exit 0; fi
echo "== PRE-RUN GATE: FAIL =="; exit 3
