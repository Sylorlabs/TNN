#!/bin/sh
# run_l3b.sh -- frozen run harness for the L3B residual-growth experiment.
# POSIX shell only. No Python at any stage.
#
# Does: compile l3b.zag with the pinned znc, run 3x, byte-compare
# (K-RG-7), run the C0-A source audit greps A1/A2, run the shell-only
# dash check (K-RG-8), assemble L3B_RAW.txt, derive K-RG-9 and the final
# L3B-GROWTH verdict.
#
# Usage: sh run_l3b.sh
# Exit 0 iff verdict is L3B-GROWTH-PASS.

ZNC=/home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc
D=docs/lab/research-lead/overnight-20260928/l3b_residual_growth
SNIP=docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh
BIN=/tmp/l3b_bin
R1=/tmp/l3b_r1.txt
R2=/tmp/l3b_r2.txt
R3=/tmp/l3b_r3.txt
RAW=$D/L3B_RAW.txt

if [ ! -x "$ZNC" ]; then
  echo "ZNC-MISSING $ZNC" >&2
  exit 1
fi

"$ZNC" "$D/l3b.zag" -o "$BIN" >/tmp/l3b_build.log 2>&1
if [ ! -x "$BIN" ]; then
  echo "BUILD-FAIL (see /tmp/l3b_build.log)" >&2
  exit 1
fi

"$BIN" >"$R1" 2>&1
"$BIN" >"$R2" 2>&1
"$BIN" >"$R3" 2>&1

# ---- assemble raw output from run 1 ----
cp "$R1" "$RAW"

{
echo "==== HARNESS AUDIT ===="

# ---- K-RG-7 determinism ----
if cmp -s "$R1" "$R2" && cmp -s "$R2" "$R3"; then
  echo "RG-BAR K-RG-7 PASS"
  K7=1
else
  echo "RG-BAR K-RG-7 FAIL"
  K7=0
fi

# ---- A1: interpreter region audit ----
REGION=$(sed -n '/INTERP-BEGIN/,/INTERP-END/p' "$D/l3b.zag")
A1=1
for pat in '== 0' '== 6' '== 7' '== 8' '== 9'; do
  if printf '%s' "$REGION" | grep -q "$pat"; then
    echo "RG-AUDIT-A1 FAIL pattern-found: $pat"
    A1=0
  fi
done
for w in CONST VAR ADD MUL SUB; do
  if ! printf '%s' "$REGION" | grep -q "$w"; then
    echo "RG-AUDIT-A1 FAIL op-missing: $w"
    A1=0
  fi
done
if [ "$A1" = 1 ]; then
  echo "RG-AUDIT-A1 PASS"
fi

# ---- A2: no dedicated-production vocabulary ----
if grep -q 'apply_rel\|COUPLED\|tag 7\|== 7' "$D/l3b.zag"; then
  echo "RG-AUDIT-A2 FAIL"
  A2=0
else
  echo "RG-AUDIT-A2 PASS"
  A2=1
fi

# ---- K-RG-8 purity: shell-only dash check on lane files ----
if sh "$SNIP" "$D/PREREG_L3B.md" "$D/l3b.zag" "$D/run_l3b.sh" >/tmp/l3b_dash.log 2>&1; then
  echo "RG-BAR K-RG-8 PASS"
  K8=1
else
  echo "RG-BAR K-RG-8 FAIL"
  cat /tmp/l3b_dash.log
  K8=0
fi

# ---- K-RG-9: combined C0-A audit ----
A3=$(grep -c 'RG-AUDIT-A3 PASS' "$R1")
A4=$(grep -c 'RG-AUDIT-A4 PASS' "$R1")
if [ "$A1" = 1 ] && [ "$A2" = 1 ] && [ "$A3" = 1 ] && [ "$A4" = 1 ]; then
  echo "RG-BAR K-RG-9 PASS"
  K9=1
else
  echo "RG-BAR K-RG-9 FAIL (A1=$A1 A2=$A2 A3=$A3 A4=$A4)"
  K9=0
fi

# ---- overall verdict ----
V=1
for b in K-RG-1 K-RG-2 K-RG-3 K-RG-4 K-RG-5 K-RG-6; do
  if ! grep -q "RG-BAR $b PASS" "$R1"; then
    V=0
  fi
done
if [ "$K7" != 1 ] || [ "$K8" != 1 ] || [ "$K9" != 1 ]; then
  V=0
fi
if [ "$V" = 1 ]; then
  echo "L3B-GROWTH-PASS"
else
  echo "L3B-GROWTH-FAIL"
fi
} >>"$RAW"

tail -20 "$RAW"
if grep -q '^L3B-GROWTH-PASS$' "$RAW"; then
  exit 0
else
  exit 1
fi
