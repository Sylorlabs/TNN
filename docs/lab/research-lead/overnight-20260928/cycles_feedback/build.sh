#!/bin/bash
# build.sh -- CYCLES-FEEDBACK formal battery. Fail-closed: set -e.
# Audits: F7 (frozen digests), F9 (setup hygiene), F10 (feedback-genuine
# edge inventory), F2 (3/3 determinism), F3/F4/F5 (report lines + INTER
# trace tails + no WIDEN=2), F6 (census), F8 (opacity). Pure Zag via
# pinned safebin znc. One binary: the mechanism and base are fully frozen
# (no extension, no control).
set -e
export PATH="$HOME/safebin"
L=~/workspace/docs/lab/research-lead/overnight-20260928/cycles_feedback
cd "$L"
fail() { echo "AUDIT-FAIL: $1"; exit 1; }

# Toolchain guard (Step 0): no forbidden interpreter on PATH.
[ -z "$(which python3)" ] || fail "python3 on PATH"
[ -z "$(which python)" ] || fail "python on PATH"
which znc | grep -q safebin || fail "znc not from safebin"

# F7: frozen copies byte-identical to GEN-CYCLES/C420/C425/C428 digests.
echo "$(
cat <<'EOF'
33cbd90db2ce77fb837a6542f70a8758f72e3210d6b9d6d5db4d325b035b03f6  gc_uni.zag
0a12cc9a4f9b10fc8c4ce2a2f65294d48d8d402f827ceeb9d3d6126e754cb125  gc_base.zag
e741ecde990d55345e2fe3aa794c75aa11a8fc5d5c54cf995aa38cb5dfcbb1b3  uni_nomain.zag
EOF
)" | sha256sum -c - || fail "frozen digest mismatch"
echo "F7 PASS (frozen sources intact)"

# F9: setup hygiene -- facts + MAPs + teaches only.
[ "$(grep -c "while" qf_setups.zag)" = "0" ] || fail "F9: iteration in setups"
[ "$(grep -c "exec_map" qf_setups.zag)" = "0" ] || fail "F9: direct exec_map in setups"
[ "$(grep -ci "prev" qf_setups.zag)" = "0" ] || fail "F9: repeat/fixpoint check in setups"
echo "F9 PASS (setup hygiene)"

# F10: feedback-genuine -- the 801/802 edge lists match the preregistered
# inventory exactly (PREREG Section 3). Neither relation may contain a
# directed cycle on its own; the extracted lists are inspected against
# the preregistered DAG edge sets here.
E801=$(grep -o "fact_add(A,[0-9]*,801,[0-9]*)" qf_setups.zag | sort)
E802=$(grep -o "fact_add(A,[0-9]*,802,[0-9]*)" qf_setups.zag | sort)
WANT801="fact_add(A,7999,801,8000)
fact_add(A,8000,801,8001)
fact_add(A,8001,801,8101)
fact_add(A,8002,801,8102)"
WANT802="fact_add(A,8001,802,8999)
fact_add(A,8101,802,8002)
fact_add(A,8102,802,8001)"
[ "$E801" = "$WANT801" ] || fail "F10: 801 edge list diverged (got: $E801)"
[ "$E802" = "$WANT802" ] || fail "F10: 802 edge list diverged (got: $E802)"
# Directed-cycle check on each relation alone (preregistered DAGs):
# 801 pairs: (7999,8000),(8000,8001),(8001,8101),(8002,8102) -- acyclic.
# 802 pairs: (8101,8002),(8102,8001),(8001,8999) -- acyclic.
# Any return path 8001->8101->8002->8102->8001 uses both relations.
echo "F10 PASS (feedback-genuine: 801/802 edge lists match; neither cycles alone)"

# Assemble the binary: frozen base + frozen U + frozen mechanism + setups + main.
# qf_fbin : gc_solve over QF1/QF2/QF3.
cat gc_base.zag uni_nomain.zag gc_uni.zag qf_setups.zag qf_main.zag > qf_full.zag
grep -q "^fn gc_solve" qf_full.zag || fail "qf_full.zag missing gc_solve"
grep -q "^fn main" qf_full.zag || fail "qf_full.zag missing main"
grep -q "^fn setup_qf1" qf_full.zag || fail "qf_full.zag missing setup_qf1"
grep -q "^fn setup_qf2" qf_full.zag || fail "qf_full.zag missing setup_qf2"
grep -q "^fn setup_qf3" qf_full.zag || fail "qf_full.zag missing setup_qf3"

# Compile with pinned safebin znc.
znc qf_full.zag -o qf_fbin || fail "compile qf_fbin"

# Run 3x (F2 determinism).
./qf_fbin > qf_run1.txt; ./qf_fbin > qf_run2.txt; ./qf_fbin > qf_run3.txt
cmp qf_run1.txt qf_run2.txt || fail "F2 qf_fbin not deterministic"
cmp qf_run1.txt qf_run3.txt || fail "F2 qf_fbin not deterministic"
echo "F2 PASS (3/3 byte-identical)"
sha256sum qf_run1.txt

# Section line numbers for trace audits.
R1=$(grep -n "ARM=GC PROB=QF1" qf_run1.txt | cut -d: -f1)
R2=$(grep -n "ARM=GC PROB=QF2" qf_run1.txt | cut -d: -f1)
R3=$(grep -n "ARM=GC PROB=QF3" qf_run1.txt | cut -d: -f1)
[ -n "$R1" ] && [ -n "$R2" ] && [ -n "$R3" ] || fail "report lines missing"

# F3: QF1 feedback loop, full-loop return.
grep -q "ARM=GC PROB=QF1 ANS=8001 TRIES=44" qf_run1.txt || fail "F3 QF1 report line"
sed -n "1,${R1}p" qf_run1.txt | grep -q "WIDEN=2" && fail "F3 WIDEN=2 fired in QF1"
TAIL4=$(sed -n "1,${R1}p" qf_run1.txt | grep "^INTER=" | tail -4 | tr '\n' ',')
[ "$TAIL4" = "INTER=8101,INTER=8002,INTER=8102,INTER=8001," ] \
  || fail "F3 winning trial trace wrong (tail4=$TAIL4)"
echo "F3 trace: winning [0,1,0,1] trial printed 8101,8002,8102,8001; no early halt on winner"

# F4: QF2 feedback lasso, tail entry.
grep -q "ARM=GC PROB=QF2 ANS=8001 TRIES=76" qf_run1.txt || fail "F4 QF2 report line"
sed -n "${R1},${R2}p" qf_run1.txt | grep -q "WIDEN=2" && fail "F4 WIDEN=2 fired in QF2"
TAIL6=$(sed -n "${R1},${R2}p" qf_run1.txt | grep "^INTER=" | tail -6 | tr '\n' ',')
[ "$TAIL6" = "INTER=8000,INTER=8001,INTER=8101,INTER=8002,INTER=8102,INTER=8001," ] \
  || fail "F4 winning trial trace wrong (tail6=$TAIL6)"
echo "F4 trace: winning [0,0,0,1,0,1] trial printed 8000,8001,8101,8002,8102,8001"

# F5: QF3 feedback loop, mid-loop stop.
grep -q "ARM=GC PROB=QF3 ANS=8102 TRIES=17" qf_run1.txt || fail "F5 QF3 report line"
sed -n "${R2},${R3}p" qf_run1.txt | grep -q "WIDEN=2" && fail "F5 WIDEN=2 fired in QF3"
TAIL3=$(sed -n "${R2},${R3}p" qf_run1.txt | grep "^INTER=" | tail -3 | tr '\n' ',')
[ "$TAIL3" = "INTER=8101,INTER=8002,INTER=8102," ] \
  || fail "F5 winning trial trace wrong (tail3=$TAIL3)"
echo "F5 trace: winning [0,1,0] trial printed 8101,8002,8102; no early halt on winner"

# F6: census lines.
[ "$(grep -c "CENSUS m=0 inmask=1 outmask=1 n=4" qf_run1.txt)" = "2" ] || fail "F6 m0 n=4 (QF1+QF3)"
[ "$(grep -c "CENSUS m=0 inmask=1 outmask=1 n=8" qf_run1.txt)" = "1" ] || fail "F6 m0 n=8 (QF2)"
[ "$(grep -c "CENSUS m=1 inmask=1 outmask=3 n=5" qf_run1.txt)" = "2" ] || fail "F6 m1 n=5 (QF1+QF2)"
[ "$(grep -c "CENSUS m=1 inmask=1 outmask=3 n=4" qf_run1.txt)" = "1" ] || fail "F6 m1 n=4 (QF3)"
[ "$(grep -c "CENSUS m=2 inmask=1 outmask=2 n=1" qf_run1.txt)" = "3" ] || fail "F6 m2 census"
[ "$(grep -c "CENSUS m=3 inmask=1 outmask=2 n=1" qf_run1.txt)" = "3" ] || fail "F6 m3 census"
echo "F6 PASS (census)"

# F8: opacity -- no domain-story tokens in any built source.
grep -rEi "hypothesis|refine|evaluat|domain|plan|causal|navigat|arithmet|grammar|language|audio|interven|belie|goal|agent" \
  --include="*.zag" . | grep -v "^./PREREG" && fail "F8 banned token found"
echo "F8 PASS (opacity)"

echo "ALL BUILD AUDITS PASS"
