#!/bin/sh
# run_adv.sh -- frozen run harness for the L3B C0-C adversary attack.
# POSIX shell only. No Python at any stage.
#
# Does: verify protocol-region byte-identity vs committed l3b.zag,
# compile l3b_attack.zag with the pinned in-repo znc, run 3x,
# byte-compare, evaluate the frozen per-family bars from program
# summary lines plus grep counts, run the shell-only dash check,
# assemble ADV_RAW.txt, and print the verdict.
#
# Usage: sh run_adv.sh
# Exit 0 iff verdict is L3B-C0C-BOUNDARY-EXPOSED.

ZNC=/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1
D=docs/lab/research-lead/overnight-20260928/l3b_c0c_adv
SNIP=docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh
REF=2fb110ce7
BIN=/tmp/l3b_c0c_bin
R1=/tmp/l3b_c0c_r1.txt
R2=/tmp/l3b_c0c_r2.txt
R3=/tmp/l3b_c0c_r3.txt
RAW=$D/ADV_RAW.txt
DIFFP=$D/DIFF_PROOF.txt

if [ ! -x "$ZNC" ]; then
  echo "ZNC-MISSING $ZNC" >&2
  exit 1
fi

# ---- K3 protocol-region byte-identity proof ----
git show $REF:docs/lab/research-lead/overnight-20260928/l3b_residual_growth/l3b.zag \
  | sed -n '1,438p' > /tmp/c0c_proto_ref.txt
sed -n '1,438p' "$D/l3b_attack.zag" > /tmp/c0c_proto_new.txt
{
  echo "protocol-region diff proof (l3b_attack.zag lines 1-438 vs committed l3b.zag at $REF lines 1-438)"
  if cmp -s /tmp/c0c_proto_ref.txt /tmp/c0c_proto_new.txt; then
    echo "PROTO-IDENTICAL"
  else
    echo "PROTO-DIFFERS"
    cmp /tmp/c0c_proto_ref.txt /tmp/c0c_proto_new.txt | head -20
  fi
  sha256sum /tmp/c0c_proto_ref.txt /tmp/c0c_proto_new.txt
} > "$DIFFP" 2>&1
cat "$DIFFP"

# ---- build ----
"$ZNC" "$D/l3b_attack.zag" -o "$BIN" >/tmp/l3b_c0c_build.log 2>&1
if [ ! -x "$BIN" ]; then
  echo "BUILD-FAIL (see /tmp/l3b_c0c_build.log)" >&2
  cat /tmp/l3b_c0c_build.log >&2
  exit 1
fi

"$BIN" >"$R1" 2>&1
"$BIN" >"$R2" 2>&1
"$BIN" >"$R3" 2>&1

cp "$R1" "$RAW"

{
echo "==== HARNESS AUDIT ===="

# ---- determinism: 3/3 byte-identical ----
if cmp -s "$R1" "$R2" && cmp -s "$R2" "$R3"; then
  echo "C0C-BAR DETERMINISM PASS"
  DET=1
else
  echo "C0C-BAR DETERMINISM FAIL"
  DET=0
fi

# ---- section-scoped grep counts ----
A2SEC=$(sed -n '/C0C-FAM-A2-BEGIN/,/C0C-FAM-A2-END/p' "$R1")
B2SEC=$(sed -n '/C0C-FAM-B2-BEGIN/,/C0C-FAM-B2-END/p' "$R1")
A2_CREATE=$(printf '%s' "$A2SEC" | grep -c '^TRACE-CREATE')
A2_RETIRE=$(printf '%s' "$A2SEC" | grep -c '^TRACE-RETIRE')
A2_NOGROW=$(printf '%s' "$A2SEC" | grep -c '^NO-GROWTH')
B2_CREATE=$(printf '%s' "$B2SEC" | grep -c '^TRACE-CREATE')
B2_RETIRE=$(printf '%s' "$B2SEC" | grep -c '^TRACE-RETIRE')
echo "A2 counts: create=$A2_CREATE retire=$A2_RETIRE nogrowth=$A2_NOGROW"
echo "B2 counts: create=$B2_CREATE retire=$B2_RETIRE"

# ---- v3 CALLS: SPLIT present, MERGE absent ----
V3CALLS=$(awk '/^TRACE-CREATE inst=1 .* v=3 /{getline; print}' "$R1")
echo "V3CALLS: $V3CALLS"
V3SPLIT=0; V3MERGE=1
case "$V3CALLS" in
  *SPLIT\(* ) V3SPLIT=1;;
esac
case "$V3CALLS" in
  *MERGE\(* ) V3MERGE=1;;
  * ) V3MERGE=0;;
esac
if [ "$V3SPLIT" = 1 ] && [ "$V3MERGE" = 0 ]; then
  echo "C0C-BAR V3-CALLS PASS"
  VCALL=1
else
  echo "C0C-BAR V3-CALLS FAIL (split=$V3SPLIT merge=$V3MERGE)"
  VCALL=0
fi

# ---- program-side bars (tracked per family) ----
A2_PBARS=1
for b in KX-A2 A2-NOCREATE A2-HIDDEN A2-N2; do
  if grep -q "RG-BAR $b PASS" "$R1"; then
    echo "C0C-BAR $b PASS (program)"
  else
    echo "C0C-BAR $b FAIL (program)"
    A2_PBARS=0
  fi
done
B2_PBARS=1
for b in B2-VERSION B2-VRELS B2-SCORES; do
  if grep -q "RG-BAR $b PASS" "$R1"; then
    echo "C0C-BAR $b PASS (program)"
  else
    echo "C0C-BAR $b FAIL (program)"
    B2_PBARS=0
  fi
done

# ---- dash check ----
if sh "$SNIP" "$D/PREREG_C0C.md" "$D/FAMILIES.md" "$D/l3b_attack.zag" "$D/run_adv.sh" >/tmp/c0c_dash.log 2>&1; then
  echo "C0C-BAR DASH PASS"
  DASH=1
else
  echo "C0C-BAR DASH FAIL"
  cat /tmp/c0c_dash.log
  DASH=0
fi

# ---- verdict assembly per frozen prereg rules ----
A2_BOUND=0; B2_BOUND=0
if [ "$A2_PBARS" = 1 ] && [ "$A2_CREATE" = 0 ] && [ "$A2_RETIRE" = 0 ] && [ "$A2_NOGROW" = 2 ]; then
  A2_BOUND=1
fi
if [ "$B2_PBARS" = 1 ] && [ "$B2_CREATE" = 3 ] && [ "$B2_RETIRE" = 2 ] && [ "$VCALL" = 1 ]; then
  B2_BOUND=1
fi
A2_OPEN=0; B2_OPEN=0
A2_HIDDEN_GOT=$(printf '%s' "$A2SEC" | grep -o 'hidden=[0-9]*' | tail -1 | cut -d= -f2)
if [ "$A2_CREATE" -gt 0 ] && [ "${A2_HIDDEN_GOT:-0}" -ge 2 ]; then
  A2_OPEN=1
fi
B2_SUM=$(grep 'C0C-B2 version=' "$R1" | tail -1)
B2_SWITCH=$(printf '%s' "$B2_SUM" | grep -o 'switchok=[0-9]*' | cut -d= -f2)
B2_FINAL=$(printf '%s' "$B2_SUM" | grep -o 'final=[0-9]*' | cut -d= -f2)
B2_HID=$(printf '%s' "$B2_SUM" | grep -o 'hidden=[0-9]*' | cut -d= -f2)
if [ "${B2_SWITCH:-0}" = 6 ] && [ "${B2_FINAL:-0}" = 2 ] && [ "${B2_HID:-0}" = 3 ]; then
  B2_OPEN=1
fi

if [ "$A2_BOUND" = 1 ] && [ "$B2_BOUND" = 1 ] && [ "$DET" = 1 ] && [ "$DASH" = 1 ]; then
  echo "L3B-C0C-BOUNDARY-EXPOSED"
elif [ "$A2_OPEN" = 1 ] || [ "$B2_OPEN" = 1 ]; then
  echo "L3B-C0C-OPEN-FORM"
else
  echo "L3B-C0C-UNPREDICTED"
fi
} >>"$RAW"

tail -30 "$RAW"
if grep -q '^L3B-C0C-BOUNDARY-EXPOSED$' "$RAW"; then
  exit 0
else
  exit 1
fi
