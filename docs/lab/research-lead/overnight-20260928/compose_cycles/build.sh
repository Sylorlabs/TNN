#!/bin/sh
# build.sh -- frozen PREREG Section 6 assembly/build/run + audits C2-C6.
# Fail-closed: any audit failure aborts (set -e).
set -e
export PATH="$HOME/safebin"
cd ~/workspace/docs/lab/research-lead/overnight-20260928/compose_cycles

echo "== audit C4: base diff shows exactly the Section 7 edits =="
diff ref_uc_base.zag cyc_base.zag > /tmp/cyc_diff.txt || true
HUNKS=$(grep -E '^[0-9]+[acd][0-9,]+$' /tmp/cyc_diff.txt)
EXPECTED="18c18
127a128,140
133a147"
test "$HUNKS" = "$EXPECTED" || { echo "C4 HUNK MISMATCH"; echo "$HUNKS"; exit 1; }
echo "C4 ok: exactly the 3 frozen hunks (class comment, stepf, exec_map branch)"

echo "== audit C5: driver has no exec_map calls and no while loops =="
test "$(grep -c 'exec_map' cyc_new.zag)" = "0"
test "$(grep -c 'while' cyc_new.zag)" = "0"
echo "C5 ok"

echo "== audit C6: no domain-story tokens in built sources =="
if grep -i -E 'hypothesis|refine|evaluat|domain|causal|navigat|arithmet|grammar|language|audio|interven|belie|goal|agent' cyc_base.zag cyc_new.zag ref_uc_uni.zag; then
  echo "C6 BANNED TOKEN FOUND"; exit 1
fi
echo "C6 ok"

echo "== assemble =="
sed '/^fn main/,$d' ref_uc_uni.zag > uni_nomain.zag
cat cyc_base.zag uni_nomain.zag cyc_new.zag > cyc_full.zag
S1=$(wc -c < cyc_base.zag); S2=$(wc -c < uni_nomain.zag); S3=$(wc -c < cyc_new.zag)
head -c "$S1" cyc_full.zag | cmp - cyc_base.zag
head -c "$S2" cyc_full.zag | tail -c +1 > /tmp/r2; tail -c +"$((S1+1))" cyc_full.zag | head -c "$S2" | cmp - uni_nomain.zag
tail -c "$S3" cyc_full.zag | cmp - cyc_new.zag
echo "region cmps ok (S1=$S1 S2=$S2 S3=$S3)"

echo "== compile with pinned safebin znc =="
znc cyc_full.zag -o cyc_bin
ls -la cyc_bin

echo "== run 3x =="
./cyc_bin > cyc_run1.txt
./cyc_bin > cyc_run2.txt
./cyc_bin > cyc_run3.txt
cmp cyc_run1.txt cyc_run2.txt && cmp cyc_run2.txt cyc_run3.txt
echo "3/3 byte-identical (C2)"
sha256sum cyc_run1.txt cyc_run2.txt cyc_run3.txt

echo "== report line =="
grep 'ARM=UNI' cyc_run1.txt
echo "BUILD DONE"
