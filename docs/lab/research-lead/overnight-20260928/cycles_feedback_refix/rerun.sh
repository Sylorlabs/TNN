#!/bin/bash
# rerun.sh -- CYCLES-FEEDBACK-REFIX re-run of the frozen C430 binary.
# Fail-closed: set -e. NOTHING is rebuilt here: qf_fbin is copied from
# the C430 lane and its sha256 is verified before any execution.
# Audits: F7 (binary intact), F2 (3/3 determinism + C430 digest match),
# F3/F4/F5 (report lines + INTER trace tails + no WIDEN=2), F6 (census).
# Pure binary re-run; shell only for runs and byte-verification.
set -e
export PATH="$HOME/safebin"
L=~/workspace/docs/lab/research-lead/overnight-20260928/cycles_feedback_refix
SRC=~/workspace/docs/lab/research-lead/overnight-20260928/cycles_feedback
cd "$L"
fail() { echo "AUDIT-FAIL: $1"; exit 1; }

# Toolchain guard (Step 0): no forbidden interpreter on PATH.
[ -z "$(which python3)" ] || fail "python3 on PATH"
[ -z "$(which python)" ] || fail "python on PATH"

# Copy the frozen binary (do NOT rebuild) and verify its digest first.
cp "$SRC/qf_fbin" qf_fbin
chmod +x qf_fbin
BIN_DIGEST="c7c459e556f94f53b42be53d57f26d5fb6e024004a6511c6179599b1a48dddf3"
echo "$BIN_DIGEST  qf_fbin" | sha256sum -c - || fail "F7 binary digest mismatch"
echo "F7 PASS (frozen binary intact, not rebuilt)"

# Run 3x (F2 determinism).
./qf_fbin > qf_rerun1.txt; ./qf_fbin > qf_rerun2.txt; ./qf_fbin > qf_rerun3.txt
cmp qf_rerun1.txt qf_rerun2.txt || fail "F2 qf_fbin not deterministic"
cmp qf_rerun1.txt qf_rerun3.txt || fail "F2 qf_fbin not deterministic"
echo "F2 PASS (3/3 byte-identical)"
RUN_DIGEST=$(sha256sum qf_rerun1.txt | cut -d' ' -f1)
echo "run digest: $RUN_DIGEST"
[ "$RUN_DIGEST" = "538fd190e096063abf1ae6856eacc6465219a7fbc69cd1b2fe1bce2624f51b37" ] \
  || fail "F2 re-run digest differs from C430 run digest"
echo "F2 consistency PASS (re-run digest equals C430 run digest)"

# Section line numbers for trace audits.
R1=$(grep -n "ARM=GC PROB=QF1" qf_rerun1.txt | cut -d: -f1)
R2=$(grep -n "ARM=GC PROB=QF2" qf_rerun1.txt | cut -d: -f1)
R3=$(grep -n "ARM=GC PROB=QF3" qf_rerun1.txt | cut -d: -f1)
[ -n "$R1" ] && [ -n "$R2" ] && [ -n "$R3" ] || fail "report lines missing"

# F3: QF1 feedback loop, full-loop return (CORRECTED bar: TRIES=28).
grep -q "ARM=GC PROB=QF1 ANS=8001 TRIES=28" qf_rerun1.txt || fail "F3 QF1 report line"
sed -n "1,${R1}p" qf_rerun1.txt | grep -q "WIDEN=2" && fail "F3 WIDEN=2 fired in QF1"
TAIL4=$(sed -n "1,${R1}p" qf_rerun1.txt | grep "^INTER=" | tail -4 | tr '\n' ',')
[ "$TAIL4" = "INTER=8101,INTER=8002,INTER=8102,INTER=8001," ] \
  || fail "F3 winning trial trace wrong (tail4=$TAIL4)"
echo "F3 PASS: QF1 reports TRIES=28; winning [0,1,0,1] tail 8101,8002,8102,8001; no WIDEN=2"

# F4: QF2 feedback lasso, tail entry.
grep -q "ARM=GC PROB=QF2 ANS=8001 TRIES=76" qf_rerun1.txt || fail "F4 QF2 report line"
sed -n "${R1},${R2}p" qf_rerun1.txt | grep -q "WIDEN=2" && fail "F4 WIDEN=2 fired in QF2"
TAIL6=$(sed -n "${R1},${R2}p" qf_rerun1.txt | grep "^INTER=" | tail -6 | tr '\n' ',')
[ "$TAIL6" = "INTER=8000,INTER=8001,INTER=8101,INTER=8002,INTER=8102,INTER=8001," ] \
  || fail "F4 winning trial trace wrong (tail6=$TAIL6)"
echo "F4 PASS: QF2 reports TRIES=76; winning [0,0,0,1,0,1] tail 8000,8001,8101,8002,8102,8001"

# F5: QF3 feedback loop, mid-loop stop.
grep -q "ARM=GC PROB=QF3 ANS=8102 TRIES=17" qf_rerun1.txt || fail "F5 QF3 report line"
sed -n "${R2},${R3}p" qf_rerun1.txt | grep -q "WIDEN=2" && fail "F5 WIDEN=2 fired in QF3"
TAIL3=$(sed -n "${R2},${R3}p" qf_rerun1.txt | grep "^INTER=" | tail -3 | tr '\n' ',')
[ "$TAIL3" = "INTER=8101,INTER=8002,INTER=8102," ] \
  || fail "F5 winning trial trace wrong (tail3=$TAIL3)"
echo "F5 PASS: QF3 reports TRIES=17; winning [0,1,0] tail 8101,8002,8102"

# F6: census lines.
[ "$(grep -c "CENSUS m=0 inmask=1 outmask=1 n=4" qf_rerun1.txt)" = "2" ] || fail "F6 m0 n=4 (QF1+QF3)"
[ "$(grep -c "CENSUS m=0 inmask=1 outmask=1 n=8" qf_rerun1.txt)" = "1" ] || fail "F6 m0 n=8 (QF2)"
[ "$(grep -c "CENSUS m=1 inmask=1 outmask=3 n=5" qf_rerun1.txt)" = "2" ] || fail "F6 m1 n=5 (QF1+QF2)"
[ "$(grep -c "CENSUS m=1 inmask=1 outmask=3 n=4" qf_rerun1.txt)" = "1" ] || fail "F6 m1 n=4 (QF3)"
[ "$(grep -c "CENSUS m=2 inmask=1 outmask=2 n=1" qf_rerun1.txt)" = "3" ] || fail "F6 m2 census"
[ "$(grep -c "CENSUS m=3 inmask=1 outmask=2 n=1" qf_rerun1.txt)" = "3" ] || fail "F6 m3 census"
echo "F6 PASS (census)"

echo "ALL RERUN AUDITS PASS"
