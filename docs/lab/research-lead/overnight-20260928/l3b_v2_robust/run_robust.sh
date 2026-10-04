#!/bin/sh
# run_robust.sh -- frozen run harness for the L3B v2 robustness layer.
# POSIX shell only. No Python at any stage.
#
# Does: compile l3b_v2_robust.zag with the pinned znc, run 3x,
# byte-compare (RB-DET), verify the 205-program grammar and interpreter
# regions are byte-identical to v2 (RB-GRAM, RB-INTERP), audit for new
# semantic cases/modes/family tokens (RB-NOSEM), verify the ambiguity
# and archive-full traces (RB-TRACE), run the shell-only dash check
# (RB-PURE), assemble L3B_V2_ROBUST_RAW.txt, derive the verdict.
#
# Bar mapping to the frozen prereg (PREREG_L3B_V2_ROBUST.md):
#   RB-F1a..d = square reproduction; RB-F2a..d = alternating reproduction;
#   RB-AMB1..5 = ambiguity policy; RB-ARCH1/2/3a/3b = archive discipline.
#
# Usage: sh run_robust.sh
# Exit 0 iff verdict is L3B-V2-ROBUST-PASS.

ZNC=/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1
D=docs/lab/research-lead/overnight-20260928/l3b_v2_robust
SNIP=docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh
V2=docs/lab/research-lead/overnight-20260928/l3b_v2/l3b_v2.zag
BIN=/tmp/rb_robust_bin
R1=/tmp/rb_robust_r1.txt
R2=/tmp/rb_robust_r2.txt
R3=/tmp/rb_robust_r3.txt
RAW=$D/L3B_V2_ROBUST_RAW.txt

if [ ! -x "$ZNC" ]; then
  echo "ZNC-MISSING $ZNC" >&2
  exit 1
fi

"$ZNC" "$D/l3b_v2_robust.zag" -o "$BIN" >/tmp/rb_robust_build.log 2>&1
if [ ! -x "$BIN" ]; then
  echo "BUILD-FAIL (see /tmp/rb_robust_build.log)" >&2
  exit 1
fi

"$BIN" >"$R1" 2>&1; E1=$?
"$BIN" >"$R2" 2>&1; E2=$?
"$BIN" >"$R3" 2>&1; E3=$?

cp "$R1" "$RAW"

{
echo "==== HARNESS AUDIT ===="

# ---- RB-DET: 3/3 byte-identical, exit 0 ----
if cmp -s "$R1" "$R2" && cmp -s "$R2" "$R3" && [ "$E1" = 0 ] && [ "$E2" = 0 ] && [ "$E3" = 0 ]; then
  echo "RB-BAR RB-DET PASS"
  DET=1
else
  echo "RB-BAR RB-DET FAIL e=$E1/$E2/$E3"
  DET=0
fi

# ---- RB-GRAM: 205-program grammar region byte-identical to v2 ----
GA=$(sed -n '/---- Program table/,/---- Generic enumerative search/p' "$D/l3b_v2_robust.zag" | sha256sum | cut -d' ' -f1)
GB=$(sed -n '/---- Program table/,/---- Generic enumerative search/p' "$V2" | sha256sum | cut -d' ' -f1)
if [ "$GA" = "$GB" ]; then
  echo "RB-BAR RB-GRAM PASS sha256=$GA"
  GRAM=1
else
  echo "RB-BAR RB-GRAM FAIL"
  GRAM=0
fi

# ---- RB-INTERP: interpreter region byte-identical to v2 ----
IA=$(sed -n '/INTERP-BEGIN/,/INTERP-END/p' "$D/l3b_v2_robust.zag" | sha256sum | cut -d' ' -f1)
IB=$(sed -n '/INTERP-BEGIN/,/INTERP-END/p' "$V2" | sha256sum | cut -d' ' -f1)
if [ "$IA" = "$IB" ]; then
  echo "RB-BAR RB-INTERP PASS sha256=$IA"
  INTERP=1
else
  echo "RB-BAR RB-INTERP FAIL"
  INTERP=0
fi

# ---- RB-NOSEM: no new semantic cases, modes, bridges, family tokens ----
NOSEM=1
if grep -q 'rel_of' "$D/l3b_v2_robust.zag"; then
  echo "RB-AUDIT-NOSEM FAIL rel_of-present"; NOSEM=0
fi
if grep -w -E 'A2|B2|QUAD|ALT' "$D/l3b_v2_robust.zag" >/dev/null; then
  echo "RB-AUDIT-NOSEM FAIL family-token-found"; NOSEM=0
fi
if grep -E '_MODE|BRIDGE|CREATE_CAUSAL|CREATE_NEGATION|CREATE_ABS|CREATE_LANGUAGE' "$D/l3b_v2_robust.zag" >/dev/null; then
  echo "RB-AUDIT-NOSEM FAIL mode-or-handler-token-found"; NOSEM=0
fi
if [ "$NOSEM" = 1 ]; then
  echo "RB-BAR RB-NOSEM PASS"
fi

# ---- RB-TRACE: ambiguity record + archive-full signal, no first-match ----
TRACE=1
if ! grep -q 'TRACE-AMBIGUOUS on=6 matches=2 chosen=3 policy=most-recent' "$R1"; then
  echo "RB-AUDIT-TRACE FAIL no-ambiguity-record"; TRACE=0
fi
if grep -q 'TRACE-DISPATCH from=2 to=1 on=6' "$R1"; then
  echo "RB-AUDIT-TRACE FAIL silent-first-match-present"; TRACE=0
fi
if ! grep -q 'TRACE-ARCHIVE-FULL inst=5 ep=3' "$R1"; then
  echo "RB-AUDIT-TRACE FAIL no-archive-full-signal"; TRACE=0
fi
if [ "$TRACE" = 1 ]; then
  echo "RB-BAR RB-TRACE PASS"
fi

# ---- RB-PURE: shell-only dash check on lane files ----
if sh "$SNIP" "$D/PREREG_L3B_V2_ROBUST.md" "$D/l3b_v2_robust.zag" "$D/run_robust.sh" >/tmp/rb_robust_dash.log 2>&1; then
  echo "RB-BAR RB-PURE PASS"
  PURE=1
else
  echo "RB-BAR RB-PURE FAIL"
  cat /tmp/rb_robust_dash.log
  PURE=0
fi

# ---- verdict ----
FAM=1
for b in RB-F1a RB-F1b RB-F1c RB-F1d RB-F2a RB-F2b RB-F2c RB-F2d \
         RB-AMB1 RB-AMB2 RB-AMB3 RB-AMB4 RB-AMB5 \
         RB-ARCH1 RB-ARCH2 RB-ARCH3a RB-ARCH3b; do
  if ! grep -q "V2-BAR $b PASS" "$R1"; then FAM=0; fi
done

if [ "$FAM" = 1 ] && [ "$DET" = 1 ] && [ "$GRAM" = 1 ] && [ "$INTERP" = 1 ] && \
   [ "$NOSEM" = 1 ] && [ "$TRACE" = 1 ] && [ "$PURE" = 1 ]; then
  echo "L3B-V2-ROBUST-PASS"
else
  echo "L3B-V2-ROBUST-FAIL"
fi
echo "RB-GROUPS FAM=$FAM DET=$DET GRAM=$GRAM INTERP=$INTERP NOSEM=$NOSEM TRACE=$TRACE PURE=$PURE"
} >>"$RAW"

tail -30 "$RAW"
if grep -q '^L3B-V2-ROBUST-PASS$' "$RAW"; then
  exit 0
else
  exit 1
fi
