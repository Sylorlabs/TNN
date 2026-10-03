#!/bin/bash
# build.sh -- CYCLES-CONVERGENT formal battery. Fail-closed: set -e.
# Audits: C7 (frozen digests), C9 (setup hygiene), C2 (3/3 determinism),
# C3/C4/C5 (report lines + INTER trace tails + total INTER counts +
# no WIDEN=2), C6 (census), C8 (opacity). Pure Zag via pinned safebin znc.
# One binary: the mechanism and base are fully frozen (no extension,
# no control).
set -e
export PATH="$HOME/safebin"
L=~/workspace/docs/lab/research-lead/overnight-20260928/cycles_convergent
cd "$L"
fail() { echo "AUDIT-FAIL: $1"; exit 1; }

# Toolchain guard (Step 0): no forbidden interpreter on PATH.
[ -z "$(which python3)" ] || fail "python3 on PATH"
[ -z "$(which python)" ] || fail "python on PATH"
which znc | grep -q safebin || fail "znc not from safebin"

# C7: frozen copies byte-identical to GEN-CYCLES/C420/C425 digests.
echo "$(
cat <<'EOF'
33cbd90db2ce77fb837a6542f70a8758f72e3210d6b9d6d5db4d325b035b03f6  gc_uni.zag
0a12cc9a4f9b10fc8c4ce2a2f65294d48d8d402f827ceeb9d3d6126e754cb125  gc_base.zag
e741ecde990d55345e2fe3aa794c75aa11a8fc5d5c54cf995aa38cb5dfcbb1b3  uni_nomain.zag
EOF
)" | sha256sum -c - || fail "frozen digest mismatch"
echo "C7 PASS (frozen sources intact)"

# C9: setup hygiene -- facts + MAPs + teaches only.
[ "$(grep -c "while" cc_setups.zag)" = "0" ] || fail "C9: iteration in setups"
[ "$(grep -c "exec_map" cc_setups.zag)" = "0" ] || fail "C9: direct exec_map in setups"
[ "$(grep -ci "prev" cc_setups.zag)" = "0" ] || fail "C9: repeat/fixpoint check in setups"
echo "C9 PASS (setup hygiene)"

# Assemble the binary: frozen base + frozen U + frozen mechanism + setups + main.
# cc_fbin : gc_solve over QC1/QC2/QC3.
cat gc_base.zag uni_nomain.zag gc_uni.zag cc_setups.zag cc_main.zag > cc_full.zag
grep -q "^fn gc_solve" cc_full.zag || fail "cc_full.zag missing gc_solve"
grep -q "^fn main" cc_full.zag || fail "cc_full.zag missing main"
grep -q "^fn setup_qc1" cc_full.zag || fail "cc_full.zag missing setup_qc1"
grep -q "^fn setup_qc2" cc_full.zag || fail "cc_full.zag missing setup_qc2"
grep -q "^fn setup_qc3" cc_full.zag || fail "cc_full.zag missing setup_qc3"

# Compile with pinned safebin znc.
znc cc_full.zag -o cc_fbin || fail "compile cc_fbin"

# Run 3x (C2 determinism).
./cc_fbin > cc_run1.txt; ./cc_fbin > cc_run2.txt; ./cc_fbin > cc_run3.txt
cmp cc_run1.txt cc_run2.txt || fail "C2 cc_fbin not deterministic"
cmp cc_run1.txt cc_run3.txt || fail "C2 cc_fbin not deterministic"
echo "C2 PASS (3/3 byte-identical)"
sha256sum cc_run1.txt

# Section line numbers for trace audits.
R1=$(grep -n "ARM=GC PROB=QC1" cc_run1.txt | cut -d: -f1)
R2=$(grep -n "ARM=GC PROB=QC2" cc_run1.txt | cut -d: -f1)
R3=$(grep -n "ARM=GC PROB=QC3" cc_run1.txt | cut -d: -f1)
[ -n "$R1" ] && [ -n "$R2" ] && [ -n "$R3" ] || fail "report lines missing"

# C3: QC1 convergent interior depth-3.
grep -q "ARM=GC PROB=QC1 ANS=7004 TRIES=14" cc_run1.txt || fail "C3 QC1 report line"
sed -n "1,${R1}p" cc_run1.txt | grep -q "WIDEN=2" && fail "C3 WIDEN=2 fired in QC1"
TAIL3=$(sed -n "1,${R1}p" cc_run1.txt | grep "^INTER=" | tail -3 | tr '\n' ',')
[ "$TAIL3" = "INTER=7002,INTER=7003,INTER=7004," ] \
  || fail "C3 winning trial trace wrong (tail3=$TAIL3)"
TOT=$(sed -n "1,${R1}p" cc_run1.txt | grep -c "^INTER=")
[ "$TOT" = "15" ] || fail "C3 total INTER count wrong (got $TOT, want 15)"
echo "C3 trace: winning [0,0,0] trial printed 7002,7003,7004; 15 INTER total, no early halt"

# C4: QC2 convergent interior depth-5.
grep -q "ARM=GC PROB=QC2 ANS=7106 TRIES=16" cc_run1.txt || fail "C4 QC2 report line"
sed -n "${R1},${R2}p" cc_run1.txt | grep -q "WIDEN=2" && fail "C4 WIDEN=2 fired in QC2"
TAIL5=$(sed -n "${R1},${R2}p" cc_run1.txt | grep "^INTER=" | tail -5 | tr '\n' ',')
[ "$TAIL5" = "INTER=7102,INTER=7103,INTER=7104,INTER=7105,INTER=7106," ] \
  || fail "C4 winning trial trace wrong (tail5=$TAIL5)"
TOT=$(sed -n "${R1},${R2}p" cc_run1.txt | grep -c "^INTER=")
[ "$TOT" = "24" ] || fail "C4 total INTER count wrong (got $TOT, want 24)"
echo "C4 trace: winning [0,0,0,0,0] trial printed 7102..7106; 24 INTER total, no early halt"

# C5: QC3 convergent to the chain end.
grep -q "ARM=GC PROB=QC3 ANS=7204 TRIES=14" cc_run1.txt || fail "C5 QC3 report line"
sed -n "${R2},${R3}p" cc_run1.txt | grep -q "WIDEN=2" && fail "C5 WIDEN=2 fired in QC3"
TAIL3=$(sed -n "${R2},${R3}p" cc_run1.txt | grep "^INTER=" | tail -3 | tr '\n' ',')
[ "$TAIL3" = "INTER=7202,INTER=7203,INTER=7204," ] \
  || fail "C5 winning trial trace wrong (tail3=$TAIL3)"
TOT=$(sed -n "${R2},${R3}p" cc_run1.txt | grep -c "^INTER=")
[ "$TOT" = "15" ] || fail "C5 total INTER count wrong (got $TOT, want 15)"
echo "C5 trace: winning [0,0,0] trial printed 7202,7203,7204; 15 INTER total, no early halt"

# C6: census lines.
[ "$(grep -c "CENSUS m=0 inmask=1 outmask=3 n=12" cc_run1.txt)" = "1" ] || fail "C6 m0 n=12 (QC1)"
[ "$(grep -c "CENSUS m=0 inmask=1 outmask=3 n=14" cc_run1.txt)" = "1" ] || fail "C6 m0 n=14 (QC2)"
[ "$(grep -c "CENSUS m=0 inmask=1 outmask=3 n=6" cc_run1.txt)" = "1" ] || fail "C6 m0 n=6 (QC3)"
[ "$(grep -c "CENSUS m=1 inmask=1 outmask=2 n=1" cc_run1.txt)" = "3" ] || fail "C6 m1 census"
[ "$(grep -c "CENSUS m=2 inmask=1 outmask=2 n=1" cc_run1.txt)" = "3" ] || fail "C6 m2 census"
[ "$(grep -c "CENSUS m=3 inmask=1 outmask=2 n=1" cc_run1.txt)" = "3" ] || fail "C6 m3 census"
echo "C6 PASS (census)"

# C8: opacity -- no domain-story tokens in any built source.
grep -rEi "hypothesis|refine|evaluat|domain|plan|causal|navigat|arithmet|grammar|language|audio|interven|belie|goal|agent" \
  --include="*.zag" . | grep -v "^./PREREG" && fail "C8 banned token found"
echo "C8 PASS (opacity)"

echo "ALL BUILD AUDITS PASS"
