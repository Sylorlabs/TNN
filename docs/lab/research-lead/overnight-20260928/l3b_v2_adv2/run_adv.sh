#!/bin/sh
# run_adv.sh -- frozen run harness for the L3B v2 independent adversary.
# POSIX shell only. No Python at any stage.
#
# Does: compile l3b_v2_adv.zag with the pinned znc, run 3x under timeout
# (Family E probes a heap boundary and may terminate abnormally; the
# termination signature itself is the frozen E prediction), byte-compare,
# run the mechanism-identity and anti-widening audits, check every frozen
# primary bar, and derive the L3B-V2-ADV verdict.
#
# Bar mapping to the frozen prereg (PREREG_L3B_V2_ADV.md):
#   A-NOSEARCH/A-HIDDEN0/A-CREATE0/A-HIDDEN3, B-*, C-CREATE3/C-DISP3/C-RECALL3,
#   D-CREATE8/D-DISP1/D-RECALL1/D-REVISIT3, E-BOUNDARY (termination signature).
#
# Usage: sh run_adv.sh
# Exit 0 iff verdict is L3B-V2-ADV-BOUNDED or L3B-V2-ADV-BREAK
# (both are completed adversarial verdicts); exit 1 on L3B-V2-ADV-FAIL.

ZNC=/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1
D=docs/lab/research-lead/overnight-20260928/l3b_v2_adv2
SNIP=docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh
BIN=/tmp/l3badv_bin
R1=/tmp/l3badv_r1.txt
R2=/tmp/l3badv_r2.txt
R3=/tmp/l3badv_r3.txt
RAW=$D/ADV_RESULT_RAW.txt
V2REF=/tmp/l3badv_v2ref.zag

if [ ! -x "$ZNC" ]; then
  echo "ZNC-MISSING $ZNC" >&2
  exit 1
fi

"$ZNC" "$D/l3b_v2_adv.zag" -o "$BIN" >/tmp/l3badv_build.log 2>&1
if [ ! -x "$BIN" ]; then
  echo "BUILD-FAIL (see /tmp/l3badv_build.log)" >&2
  exit 1
fi

timeout -s KILL 120 "$BIN" >"$R1" 2>&1; E1=$?
timeout -s KILL 120 "$BIN" >"$R2" 2>&1; E2=$?
timeout -s KILL 120 "$BIN" >"$R3" 2>&1; E3=$?
echo "EXIT-CODES $E1 $E2 $E3"

cp "$R1" "$RAW"

{
echo "==== HARNESS AUDIT ===="
echo "EXIT-CODES $E1 $E2 $E3"

# ---- DET: 3/3 byte-identical (whatever E does, it must be deterministic)
if cmp -s "$R1" "$R2" && cmp -s "$R2" "$R3"; then
  echo "ADV-AUDIT DET PASS"
  DET=1
else
  echo "ADV-AUDIT DET FAIL"
  DET=0
fi

# ---- MECH-IDENTICAL: the reference mechanism (everything before main in
# 7a1d3265d) must be a verbatim PREFIX of the attack file. (The attack adds
# only aep/adv_bar helpers and a new main after the mechanism, so a full
# pre-main comparison would wrongly fail.)
git show 7a1d3265d:docs/lab/research-lead/overnight-20260928/l3b_v2/l3b_v2.zag > "$V2REF" 2>/dev/null
awk '/^fn main\(\)i32 \{/{exit} {print}' "$V2REF" > /tmp/l3badv_v2head.txt
VL=$(wc -l < /tmp/l3badv_v2head.txt)
head -n "$VL" "$D/l3b_v2_adv.zag" > /tmp/l3badv_atkprefix.txt
if cmp -s /tmp/l3badv_v2head.txt /tmp/l3badv_atkprefix.txt; then
  echo "ADV-AUDIT MECH-IDENTICAL PASS (reference mechanism is a verbatim $VL-line prefix)"
  MECH=1
else
  echo "ADV-AUDIT MECH-IDENTICAL FAIL"
  MECH=0
fi

# ---- INTERP-IDENTICAL ----
HA=$(sed -n '/INTERP-BEGIN/,/INTERP-END/p' "$D/l3b_v2_adv.zag" | sha256sum | cut -d' ' -f1)
HB=$(sed -n '/INTERP-BEGIN/,/INTERP-END/p' "$V2REF" | sha256sum | cut -d' ' -f1)
if [ "$HA" = "$HB" ]; then
  echo "ADV-AUDIT INTERP-IDENTICAL PASS sha256=$HA"
  INTERP=1
else
  echo "ADV-AUDIT INTERP-IDENTICAL FAIL"
  INTERP=0
fi

# ---- NO-REL-OF ----
if grep -q 'rel_of' "$D/l3b_v2_adv.zag"; then
  echo "ADV-AUDIT NO-REL-OF FAIL"
  NRO=0
else
  echo "ADV-AUDIT NO-REL-OF PASS"
  NRO=1
fi

# ---- E-AUDIT: do_fire has no bounds check on the archive index ----
DOFIRE=$(sed -n '/^fn do_fire/,/^}/p' "$D/l3b_v2_adv.zag")
if echo "$DOFIRE" | grep -q 'vn.*<.*8\|< *8\|av_cap\|BOUNDS'; then
  echo "ADV-AUDIT E-BOUNDS-CHECK PRESENT (unexpected)"
  EBOUND=0
else
  echo "ADV-AUDIT E-BOUNDS-CHECK PASS (absent: 9th CREATE writes past 8-entry archive)"
  EBOUND=1
fi

# ---- Primary bars (binary-emitted) ----
PRIM_OK=1
for b in A-NOSEARCH A-HIDDEN0 A-CREATE0 B-NOSEARCH B-HIDDEN0 B-CREATE0 \
         C-CREATE3 C-DISP3 C-RECALL3 D-CREATE8 D-DISP1 D-RECALL1 D-REVISIT3; do
  if grep -q "ADV-BAR $b PASS" "$R1"; then
    echo "ADV-AUDIT BAR $b PASS"
  else
    echo "ADV-AUDIT BAR $b FAIL"
    PRIM_OK=0
  fi
done

# ---- BREAK-evidence bars (PASS here means break evidence FOUND) ----
BREAK_EV=0
for b in A-HIDDEN3 B-HIDDEN3; do
  if grep -q "ADV-BAR $b PASS" "$R1"; then
    echo "ADV-AUDIT BREAK-EV $b PRESENT"
    BREAK_EV=1
  else
    echo "ADV-AUDIT BREAK-EV $b absent"
  fi
done

# ---- Dispatch signatures (frozen wrong-pick-then-correct pattern) ----
SIG_OK=1
for s in "TRACE-DISPATCH from=3 to=2 on=21" "TRACE-DISPATCH from=2 to=1 on=6" \
         "TRACE-DISPATCH from=1 to=3 on=7" "TRACE-DISPATCH from=8 to=1 on=21"; do
  if grep -q "$s" "$R1"; then
    echo "ADV-AUDIT SIG '$s' PASS"
  else
    echo "ADV-AUDIT SIG '$s' FAIL"
    SIG_OK=0
  fi
done

# ---- D-KEYS: the eight predicted TRACE-CREATE key lines ----
KEYS_OK=1
for kv in "v=1 p1=V p2=(A,V,V)" "v=2 p1=V p2=(A,V,C4)" "v=3 p1=V p2=(A,V,C6)" \
          "v=4 p1=V p2=(S,V,C2)" "v=5 p1=V p2=(M,V,C3)" "v=6 p1=V p2=(M,V,V)" \
          "v=7 p1=V p2=(A,V,(A,V,C1))" "v=8 p1=V p2=(A,V,C1)"; do
  if grep -q "TRACE-CREATE $kv" "$R1"; then
    echo "ADV-AUDIT KEY '$kv' PASS"
  else
    echo "ADV-AUDIT KEY '$kv' FAIL"
    KEYS_OK=0
  fi
done

# ---- E-BOUNDARY: termination signature identical 3/3 ----
# Frozen: 9th CREATE attempt executes with vn=8 (past the 8-entry archive).
# Abnormal termination or corrupted tail expected; signature must be stable.
E_SIG_OK=1
if [ "$E1" = "$E2" ] && [ "$E2" = "$E3" ]; then
  echo "ADV-AUDIT E-EXIT-STABLE PASS code=$E1"
else
  echo "ADV-AUDIT E-EXIT-STABLE FAIL ($E1 $E2 $E3)"
  E_SIG_OK=0
fi
if [ "$E1" -ne 0 ]; then
  echo "ADV-AUDIT E-ABNORMAL-EXIT PASS (code=$E1: boundary confirmed)"
elif grep -q "ADV-FAME probe end" "$R1"; then
  echo "ADV-AUDIT E-ABNORMAL-EXIT MISSING (exit 0, probe completed: E-UNEXPECTED, investigate)"
  E_SIG_OK=0
else
  echo "ADV-AUDIT E-ABNORMAL-EXIT PARTIAL (exit 0 but probe end missing: truncated output)"
fi
tail -3 "$R1" | sed 's/^/ADV-AUDIT E-TAIL: /'

# ---- PURE: shell-only dash check on lane files ----
if sh "$SNIP" "$D/PREREG_L3B_V2_ADV.md" "$D/PREREG_L3B_V2_ADV_ADDENDUM.md" "$D/NAMECHECK.md" "$D/l3b_v2_adv.zag" "$D/run_adv.sh" >/tmp/l3badv_dash.log 2>&1; then
  echo "ADV-AUDIT PURE PASS"
  PURE=1
else
  echo "ADV-AUDIT PURE FAIL"
  cat /tmp/l3badv_dash.log
  PURE=0
fi

# ---- verdict ----
if [ "$BREAK_EV" = 1 ]; then
  echo "L3B-V2-ADV-BREAK"
elif [ "$PRIM_OK" = 1 ] && [ "$SIG_OK" = 1 ] && [ "$KEYS_OK" = 1 ] && \
     [ "$DET" = 1 ] && [ "$MECH" = 1 ] && [ "$INTERP" = 1 ] && \
     [ "$NRO" = 1 ] && [ "$PURE" = 1 ] && [ "$EBOUND" = 1 ] && [ "$E_SIG_OK" = 1 ]; then
  echo "L3B-V2-ADV-BOUNDED"
else
  echo "L3B-V2-ADV-FAIL"
fi
echo "ADV-GROUPS PRIM=$PRIM_OK SIG=$SIG_OK KEYS=$KEYS_OK DET=$DET MECH=$MECH INTERP=$INTERP NRO=$NRO PURE=$PURE EBOUND=$EBOUND ESIG=$E_SIG_OK BREAKEV=$BREAK_EV"
} >>"$RAW"

tail -40 "$RAW"
if grep -q '^L3B-V2-ADV-BOUNDED$' "$RAW" || grep -q '^L3B-V2-ADV-BREAK$' "$RAW"; then
  exit 0
else
  exit 1
fi
