#!/bin/bash
# build.sh -- CYCLES-GENERALIZE formal battery. Fail-closed: set -e.
# Audits: G8 (frozen digests + additive diffs), G2 (3/3 determinism),
# G3/G4/G5/G6 (report lines + trace evidence), G7 (reduction cmp),
# G9 (opacity). Pure Zag via pinned safebin znc.
set -e
export PATH="$HOME/safebin"
L=~/workspace/docs/lab/research-lead/overnight-20260928/cycles_generalize
cd "$L"
fail() { echo "AUDIT-FAIL: $1"; exit 1; }

# Toolchain guard (Step 0): no forbidden interpreter on PATH.
[ -z "$(which python3)" ] || fail "python3 on PATH"
[ -z "$(which python)" ] || fail "python on PATH"
which znc | grep -q safebin || fail "znc not from safebin"

# G8a: frozen copies byte-identical to GEN-CYCLES digests.
echo "$(
cat <<'EOF'
33cbd90db2ce77fb837a6542f70a8758f72e3210d6b9d6d5db4d325b035b03f6  gc_uni.zag
0a12cc9a4f9b10fc8c4ce2a2f65294d48d8d402f827ceeb9d3d6126e754cb125  gc_base.zag
e741ecde990d55345e2fe3aa794c75aa11a8fc5d5c54cf995aa38cb5dfcbb1b3  uni_nomain.zag
aa28dac4506bfa8dc2a7f821bbb15fff2bdf89dc157c16def1472d97965baea6  cyc_nomain.zag
EOF
)" | sha256sum -c - || fail "frozen digest mismatch"

# G8b: cg_uni.zag differs from frozen ONLY by the preregistered HALT check.
[ "$(diff gc_uni.zag cg_uni.zag | grep -E '^[0-9]' | tr '\n' ';')" = "38a39,41;48a52;" ] \
  || fail "cg_uni.zag hunk list != preregistered"
[ "$(diff gc_uni.zag cg_uni.zag | grep -c '^<')" = "0" ] || fail "cg_uni.zag deletes frozen lines"
diff gc_uni.zag cg_uni.zag | grep '^>' | grep -v "v==-3" | grep -v "T3 addition" \
  | grep -v "cur at its pre-step value" | grep -v "so the signal is not mistaken" \
  | grep -q . && fail "cg_uni.zag has unregistered additions"

# G8c: cg_base.zag differs from frozen ONLY by the preregistered pkind/class-5.
[ "$(diff gc_base.zag cg_base.zag | grep -E '^[0-9]' | tr '\n' ';')" = "18c18,19;88a90;140a143,155;147a163;" ] \
  || fail "cg_base.zag hunk list != preregistered"
[ "$(diff gc_base.zag cg_base.zag | grep '^<' | grep -v 'Classes: 0=WALK' | wc -l)" = "0" ] \
  || fail "cg_base.zag deletes non-comment frozen lines"

# Assemble the four binaries.
# cg_fbin : frozen base + frozen U + frozen mechanism (QC,QG,QH)
# cg_fbin0: frozen base + frozen U + frozen mechanism (QK0 control)
# cg_xbin : frozen base + frozen U + EXTENDED mechanism (QC,QG,QH; G7)
# cg_xsbin: extended base + frozen U + EXTENDED mechanism (QK signal)
cat gc_base.zag uni_nomain.zag gc_uni.zag cyc_nomain.zag cg_setups.zag cg_main_red.zag > cg_full.zag
cat gc_base.zag uni_nomain.zag gc_uni.zag cg_setups.zag cg_main_k0.zag > cg_k0full.zag
cat gc_base.zag uni_nomain.zag cg_uni.zag cyc_nomain.zag cg_setups.zag cg_main_red.zag > cg_xfull.zag
cat cg_base.zag uni_nomain.zag cg_uni.zag cg_setups.zag cg_main_ksig.zag > cg_xsigfull.zag
for f in cg_full cg_k0full cg_xfull cg_xsigfull; do
  grep -q "^fn gc_solve" "$f.zag" || fail "$f.zag missing gc_solve"
  grep -q "^fn main" "$f.zag" || fail "$f.zag missing main"
done

# Compile with pinned safebin znc.
znc cg_full.zag -o cg_fbin || fail "compile cg_fbin"
znc cg_k0full.zag -o cg_fbin0 || fail "compile cg_fbin0"
znc cg_xfull.zag -o cg_xbin || fail "compile cg_xbin"
znc cg_xsigfull.zag -o cg_xsbin || fail "compile cg_xsbin"

# Run 3x each (G2 determinism).
./cg_fbin > cg_run1.txt; ./cg_fbin > cg_run2.txt; ./cg_fbin > cg_run3.txt
./cg_fbin0 > cg_k01.txt; ./cg_fbin0 > cg_k02.txt; ./cg_fbin0 > cg_k03.txt
./cg_xbin > cg_x1.txt; ./cg_xbin > cg_x2.txt; ./cg_xbin > cg_x3.txt
./cg_xsbin > cg_ks1.txt; ./cg_xsbin > cg_ks2.txt; ./cg_xsbin > cg_ks3.txt
cmp cg_run1.txt cg_run2.txt || fail "G2 cg_fbin not deterministic"
cmp cg_run1.txt cg_run3.txt || fail "G2 cg_fbin not deterministic"
cmp cg_k01.txt cg_k02.txt || fail "G2 cg_fbin0 not deterministic"
cmp cg_k01.txt cg_k03.txt || fail "G2 cg_fbin0 not deterministic"
cmp cg_x1.txt cg_x2.txt || fail "G2 cg_xbin not deterministic"
cmp cg_x1.txt cg_x3.txt || fail "G2 cg_xbin not deterministic"
cmp cg_ks1.txt cg_ks2.txt || fail "G2 cg_xsbin not deterministic"
cmp cg_ks1.txt cg_ks3.txt || fail "G2 cg_xsbin not deterministic"
echo "G2 PASS (3/3 each)"
sha256sum cg_run1.txt cg_k01.txt cg_x1.txt cg_ks1.txt

# QC regression sanity (C403 on frozen, must reproduce GEN-CYCLES).
grep -q "ARM=GC PROB=QC ANS=1005 TRIES=23" cg_run1.txt || fail "QC regression moved"

# G3: T1 alternating family.
grep -q "ARM=GC PROB=QG ANS=3006 TRIES=236" cg_run1.txt || fail "G3 QG report line"
grep -q "CENSUS m=0 inmask=3 outmask=3 n=7" cg_run1.txt || fail "G3 QG m0 census"
grep -q "CENSUS m=1 inmask=3 outmask=3 n=5" cg_run1.txt || fail "G3 QG m1 census"

# G4: T2 data-dependent halting.
grep -q "ARM=GC PROB=QH ANS=4002 TRIES=15" cg_run1.txt || fail "G4 QH report line"
grep -q "CENSUS m=0 inmask=3 outmask=2 n=4" cg_run1.txt || fail "G4 QH m0 census"
QHREP=$(grep -n "ARM=GC PROB=QH" cg_run1.txt | cut -d: -f1)
TAIL3=$(sed -n "1,${QHREP}p" cg_run1.txt | grep "^INTER=" | tail -3 | tr '\n' ',')
[ "$TAIL3" = "INTER=-2,INTER=4002,INTER=4002," ] \
  || fail "G4 winning trial did not halt data-dependently (tail3=$TAIL3)"
echo "G4 trace evidence: winning k=3 trial printed 2 INTER lines (4002,4002)"

# No WIDEN=2 anywhere in the frozen QC/QG/QH output.
QCREP=$(grep -n "ARM=GC PROB=QC " cg_run1.txt | cut -d: -f1)
sed -n "${QCREP},${QHREP}p" cg_run1.txt | grep -q "WIDEN=2" && fail "WIDEN=2 fired in QC/QG/QH"

# G5: T3 control (frozen mechanism must FAIL the HALT-kind workload).
grep -q "ARM=GC PROB=QK0 ANS=-2 TRIES=78" cg_k01.txt || fail "G5 QK0 report line"
grep -q "WIDEN=2" cg_k01.txt || fail "G5 WIDEN=2 did not fire in control"

# G6: T3 signal (extended executor halts on the HALT-kind signal).
grep -q "ARM=XH PROB=QK ANS=5002 TRIES=15" cg_ks1.txt || fail "G6 QK report line"
grep -q "^INTER=-3$" cg_ks1.txt || fail "G6 no INTER=-3 (signal never fired)"
grep -q "CENSUS m=0 inmask=3 outmask=6 n=3" cg_ks1.txt || fail "G6 QK m0 census (HALT kind bit)"
grep -q "WIDEN=2" cg_ks1.txt && fail "G6 WIDEN=2 fired in signal run"

# G7: reduction -- extended+frozen-base byte-identical to frozen on QC/QG/QH.
cmp cg_x1.txt cg_run1.txt || fail "G7 reduction moved"
echo "G7 PASS (extended executor byte-identical on QC/QG/QH)"

# G9: opacity -- no domain-story tokens in any built source.
grep -rEi "hypothesis|refine|evaluat|domain|plan|causal|navigat|arithmet|grammar|language|audio|interven|belie|goal|agent" \
  --include="*.zag" . | grep -v "^./PREREG" && fail "G9 banned token found"
echo "G9 PASS (opacity)"

echo "ALL BUILD AUDITS PASS"
