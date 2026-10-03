#!/bin/bash
# build.sh -- CYCLES-OSCILLATORY formal battery. Fail-closed: set -e.
# Audits: O7 (frozen digests), O9 (setup hygiene), O2 (3/3 determinism),
# O3/O4/O5 (report lines + INTER trace tails + no WIDEN=2), O6 (census),
# O8 (opacity). Pure Zag via pinned safebin znc. One binary: the
# mechanism and base are fully frozen (no extension, no control).
set -e
export PATH="$HOME/safebin"
L=~/workspace/docs/lab/research-lead/overnight-20260928/cycles_oscillatory
cd "$L"
fail() { echo "AUDIT-FAIL: $1"; exit 1; }

# Toolchain guard (Step 0): no forbidden interpreter on PATH.
[ -z "$(which python3)" ] || fail "python3 on PATH"
[ -z "$(which python)" ] || fail "python on PATH"
which znc | grep -q safebin || fail "znc not from safebin"

# O7: frozen copies byte-identical to GEN-CYCLES/C420 digests.
echo "$(
cat <<'EOF'
33cbd90db2ce77fb837a6542f70a8758f72e3210d6b9d6d5db4d325b035b03f6  gc_uni.zag
0a12cc9a4f9b10fc8c4ce2a2f65294d48d8d402f827ceeb9d3d6126e754cb125  gc_base.zag
e741ecde990d55345e2fe3aa794c75aa11a8fc5d5c54cf995aa38cb5dfcbb1b3  uni_nomain.zag
EOF
)" | sha256sum -c - || fail "frozen digest mismatch"
echo "O7 PASS (frozen sources intact)"

# O9: setup hygiene -- facts + MAPs + teaches only.
[ "$(grep -c "while" qo_setups.zag)" = "0" ] || fail "O9: iteration in setups"
[ "$(grep -c "exec_map" qo_setups.zag)" = "0" ] || fail "O9: direct exec_map in setups"
[ "$(grep -ci "prev" qo_setups.zag)" = "0" ] || fail "O9: repeat/fixpoint check in setups"
echo "O9 PASS (setup hygiene)"

# Assemble the binary: frozen base + frozen U + frozen mechanism + setups + main.
# qo_fbin : gc_solve over QO1/QO2/QO3.
cat gc_base.zag uni_nomain.zag gc_uni.zag qo_setups.zag qo_main.zag > qo_full.zag
grep -q "^fn gc_solve" qo_full.zag || fail "qo_full.zag missing gc_solve"
grep -q "^fn main" qo_full.zag || fail "qo_full.zag missing main"
grep -q "^fn setup_qo1" qo_full.zag || fail "qo_full.zag missing setup_qo1"
grep -q "^fn setup_qo2" qo_full.zag || fail "qo_full.zag missing setup_qo2"
grep -q "^fn setup_qo3" qo_full.zag || fail "qo_full.zag missing setup_qo3"

# Compile with pinned safebin znc.
znc qo_full.zag -o qo_fbin || fail "compile qo_fbin"

# Run 3x (O2 determinism).
./qo_fbin > qo_run1.txt; ./qo_fbin > qo_run2.txt; ./qo_fbin > qo_run3.txt
cmp qo_run1.txt qo_run2.txt || fail "O2 qo_fbin not deterministic"
cmp qo_run1.txt qo_run3.txt || fail "O2 qo_fbin not deterministic"
echo "O2 PASS (3/3 byte-identical)"
sha256sum qo_run1.txt

# Section line numbers for trace audits.
R1=$(grep -n "ARM=GC PROB=QO1" qo_run1.txt | cut -d: -f1)
R2=$(grep -n "ARM=GC PROB=QO2" qo_run1.txt | cut -d: -f1)
R3=$(grep -n "ARM=GC PROB=QO3" qo_run1.txt | cut -d: -f1)
[ -n "$R1" ] && [ -n "$R2" ] && [ -n "$R3" ] || fail "report lines missing"

# O3: QO1 period-2 on-cycle.
grep -q "ARM=GC PROB=QO1 ANS=6001 TRIES=15" qo_run1.txt || fail "O3 QO1 report line"
sed -n "1,${R1}p" qo_run1.txt | grep -q "WIDEN=2" && fail "O3 WIDEN=2 fired in QO1"
TAIL4=$(sed -n "1,${R1}p" qo_run1.txt | grep "^INTER=" | tail -4 | tr '\n' ',')
[ "$TAIL4" = "INTER=6002,INTER=6001,INTER=6002,INTER=6001," ] \
  || fail "O3 winning trial trace wrong (tail4=$TAIL4)"
echo "O3 trace: winning [0,0,0,0] trial printed 6002,6001,6002,6001, no early halt"

# O4: QO2 tail-entry lasso.
grep -q "ARM=GC PROB=QO2 ANS=6003 TRIES=15" qo_run1.txt || fail "O4 QO2 report line"
sed -n "${R1},${R2}p" qo_run1.txt | grep -q "WIDEN=2" && fail "O4 WIDEN=2 fired in QO2"
TAIL4=$(sed -n "${R1},${R2}p" qo_run1.txt | grep "^INTER=" | tail -4 | tr '\n' ',')
[ "$TAIL4" = "INTER=6002,INTER=6003,INTER=6004,INTER=6003," ] \
  || fail "O4 winning trial trace wrong (tail4=$TAIL4)"
echo "O4 trace: winning [0,0,0,0] trial printed 6002,6003,6004,6003, no early halt"

# O5: QO3 period-3.
grep -q "ARM=GC PROB=QO3 ANS=6001 TRIES=14" qo_run1.txt || fail "O5 QO3 report line"
sed -n "${R2},${R3}p" qo_run1.txt | grep -q "WIDEN=2" && fail "O5 WIDEN=2 fired in QO3"
TAIL3=$(sed -n "${R2},${R3}p" qo_run1.txt | grep "^INTER=" | tail -3 | tr '\n' ',')
[ "$TAIL3" = "INTER=6002,INTER=6003,INTER=6001," ] \
  || fail "O5 winning trial trace wrong (tail3=$TAIL3)"
echo "O5 trace: winning [0,0,0] trial printed 6002,6003,6001, no early halt"

# O6: census lines.
[ "$(grep -c "CENSUS m=0 inmask=1 outmask=1 n=6" qo_run1.txt)" = "2" ] || fail "O6 m0 n=6 count (QO1+QO3)"
[ "$(grep -c "CENSUS m=0 inmask=1 outmask=1 n=8" qo_run1.txt)" = "1" ] || fail "O6 m0 n=8 count (QO2)"
[ "$(grep -c "CENSUS m=1 inmask=1 outmask=2 n=1" qo_run1.txt)" = "3" ] || fail "O6 m1 census"
[ "$(grep -c "CENSUS m=2 inmask=1 outmask=2 n=1" qo_run1.txt)" = "3" ] || fail "O6 m2 census"
[ "$(grep -c "CENSUS m=3 inmask=1 outmask=2 n=1" qo_run1.txt)" = "3" ] || fail "O6 m3 census"
echo "O6 PASS (census)"

# O8: opacity -- no domain-story tokens in any built source.
grep -rEi "hypothesis|refine|evaluat|domain|plan|causal|navigat|arithmet|grammar|language|audio|interven|belie|goal|agent" \
  --include="*.zag" . | grep -v "^./PREREG" && fail "O8 banned token found"
echo "O8 PASS (opacity)"

echo "ALL BUILD AUDITS PASS"
