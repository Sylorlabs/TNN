#!/bin/sh
# run_l3b_v2.sh -- frozen run harness for the L3B constructor-v2 experiment.
# POSIX shell only. No Python at any stage.
#
# Does: compile l3b_v2.zag with the pinned znc, run 3x, byte-compare
# (V2-DET), run the anti-widening source audits (V2-AUD-A/B/C, combined
# into V2-A2e), run the shell-only dash check (V2-PURE), assemble
# L3B_V2_RAW.txt, derive the L3B-V2 verdict.
#
# Bar mapping to the frozen prereg (PREREG_L3B_V2.md + PREREG_ADDENDUM_1.md):
#   V2-F1a=P-A2a V2-F1b=P-A2b V2-F1c=P-A2c V2-F1d=P-A2d V2-A2e=P-A2e
#   V2-F2a=P-B2a V2-F2b=P-B2b V2-F2c=P-B2c V2-F2d=P-B2d
#   V2-R1=P-R1 V2-R2=P-R2 V2-R3=P-R3
#
# Usage: sh run_l3b_v2.sh
# Exit 0 iff verdict is L3B-V2-PASS.

ZNC=/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1
D=docs/lab/research-lead/overnight-20260928/l3b_v2
SNIP=docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh
V1ZAG=l3b_v1_for_audit.zag
BIN=/tmp/l3bv2_bin
R1=/tmp/l3bv2_r1.txt
R2=/tmp/l3bv2_r2.txt
R3=/tmp/l3bv2_r3.txt
RAW=$D/L3B_V2_RAW.txt

if [ ! -x "$ZNC" ]; then
  echo "ZNC-MISSING $ZNC" >&2
  exit 1
fi

"$ZNC" "$D/l3b_v2.zag" -o "$BIN" >/tmp/l3bv2_build.log 2>&1
if [ ! -x "$BIN" ]; then
  echo "BUILD-FAIL (see /tmp/l3bv2_build.log)" >&2
  exit 1
fi

"$BIN" >"$R1" 2>&1
"$BIN" >"$R2" 2>&1
"$BIN" >"$R3" 2>&1

cp "$R1" "$RAW"

{
echo "==== HARNESS AUDIT ===="

# ---- V2-DET: 3/3 byte-identical ----
if cmp -s "$R1" "$R2" && cmp -s "$R2" "$R3"; then
  echo "V2-BAR V2-DET PASS"
  DET=1
else
  echo "V2-BAR V2-DET FAIL"
  DET=0
fi

# ---- V2-AUD-A: interpreter region byte-identical to v1 ----
git show 2fb110ce7:docs/lab/research-lead/overnight-20260928/l3b_residual_growth/l3b.zag > /tmp/$V1ZAG 2>/dev/null
HA=$(sed -n '/INTERP-BEGIN/,/INTERP-END/p' "$D/l3b_v2.zag" | sha256sum | cut -d' ' -f1)
HB=$(sed -n '/INTERP-BEGIN/,/INTERP-END/p' /tmp/$V1ZAG | sha256sum | cut -d' ' -f1)
AUDA=1
if [ "$HA" != "$HB" ]; then
  echo "V2-AUDIT-A FAIL interp-region-differs"
  AUDA=0
else
  echo "V2-AUDIT-A PASS interp-identical sha256=$HA"
fi

# ---- V2-AUD-B: the fixed-vocabulary analyzer is gone, not extended ----
AUDB=1
if grep -q 'rel_of' "$D/l3b_v2.zag"; then
  echo "V2-AUDIT-B FAIL rel_of-present"
  AUDB=0
else
  echo "V2-AUDIT-B PASS no-vocabulary-analyzer"
fi

# ---- V2-AUD-C: no family-specific token in the mechanism source ----
AUDC=1
if grep -w -E 'A2|B2|QUAD|ALT' "$D/l3b_v2.zag" >/dev/null; then
  echo "V2-AUDIT-C FAIL family-token-found"
  grep -w -E 'A2|B2|QUAD|ALT' "$D/l3b_v2.zag" | head -5
  AUDC=0
else
  echo "V2-AUDIT-C PASS no-family-token"
fi

if [ "$AUDA" = 1 ] && [ "$AUDB" = 1 ] && [ "$AUDC" = 1 ]; then
  echo "V2-BAR V2-A2e PASS"
  A2E=1
else
  echo "V2-BAR V2-A2e FAIL"
  A2E=0
fi

# ---- V2-PURE: shell-only dash check on lane files ----
if sh "$SNIP" "$D/PREREG_L3B_V2.md" "$D/PREREG_ADDENDUM_1.md" "$D/NAMECHECK.md" "$D/l3b_v2.zag" "$D/run_l3b_v2.sh" >/tmp/l3bv2_dash.log 2>&1; then
  echo "V2-BAR V2-PURE PASS"
  PURE=1
else
  echo "V2-BAR V2-PURE FAIL"
  cat /tmp/l3bv2_dash.log
  PURE=0
fi

# ---- verdict ----
F1=1; F2=1; REG=1
for b in V2-F1a V2-F1b V2-F1c V2-F1d; do
  if ! grep -q "V2-BAR $b PASS" "$R1"; then F1=0; fi
done
if [ "$A2E" != 1 ]; then F1=0; fi
for b in V2-F2a V2-F2b V2-F2c V2-F2d; do
  if ! grep -q "V2-BAR $b PASS" "$R1"; then F2=0; fi
done
for b in V2-R1 V2-R2 V2-R3; do
  if ! grep -q "V2-BAR $b PASS" "$R1"; then REG=0; fi
done

if [ "$F1" = 1 ] && [ "$F2" = 1 ] && [ "$REG" = 1 ] && [ "$DET" = 1 ] && [ "$PURE" = 1 ]; then
  echo "L3B-V2-PASS"
elif [ "$REG" = 1 ] && [ "$DET" = 1 ] && [ "$PURE" = 1 ] && { { [ "$F1" = 1 ] && [ "$F2" = 0 ]; } || { [ "$F1" = 0 ] && [ "$F2" = 1 ]; }; }; then
  echo "L3B-V2-PARTIAL"
else
  echo "L3B-V2-FAIL"
fi
echo "V2-GROUPS F1=$F1 F2=$F2 REG=$REG DET=$DET PURE=$PURE"
} >>"$RAW"

tail -25 "$RAW"
if grep -q '^L3B-V2-PASS$' "$RAW"; then
  exit 0
else
  exit 1
fi
