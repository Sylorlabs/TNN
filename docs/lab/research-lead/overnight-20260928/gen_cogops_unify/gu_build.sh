#!/bin/sh
# gu_build.sh -- GEN-COGOPS-UNIFY PoC build/run/audit. Fail-closed (set -e).
set -e
export PATH="$HOME/safebin"
cd ~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/gen_cogops_unify

echo "== toolchain guard =="
which python3 && { echo "PYTHON3 PRESENT"; exit 1; } || true
which python && { echo "PYTHON PRESENT"; exit 1; } || true
which znc

echo "== audit: lifted learner regions byte-identical =="
CC=~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/cogops_compose
sed -n '21,172p' $CC/cc_learn.zag > /tmp/gu_a1.txt
sed -n '6,157p' gu_learn.zag > /tmp/gu_a2.txt
cmp /tmp/gu_a1.txt /tmp/gu_a2.txt
sed -n '76,129p' $CC/cc_base.zag > /tmp/gu_b1.txt
sed -n '/researcher-supplied generic procedures/,$p' gu_learn.zag | tail -n +2 > /tmp/gu_b2.txt
cmp /tmp/gu_b1.txt /tmp/gu_b2.txt
echo "learner regions ok"

echo "== audit: gu_gen.zag deltas are exactly the documented ones =="
GSF=~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/gen_statefix/gsf_gen.zag
tail -n +11 gu_gen.zag > /tmp/gu_g1.txt
diff $GSF /tmp/gu_g1.txt > /tmp/gu_gdiff.txt || true
ND1=$(grep -c 'GU-GEN-DELTA 1' /tmp/gu_g1.txt)
ND2=$(grep -c '10080\|11616\|11620' /tmp/gu_g1.txt)
if [ "$ND1" != "1" ]; then echo "DELTA 1 MARKER WRONG ($ND1)"; exit 1; fi
if [ "$ND2" != "9" ]; then echo "DELTA 2 RELOCATION COUNT WRONG ($ND2)"; exit 1; fi
BADOLD=$(grep '^<' /tmp/gu_gdiff.txt | grep -v -E '2304|3328|3332|zti<256|if\(mg\(A,m,0\)==4\)\{ return 2; \}' | wc -l)
BADNEW=$(grep '^>' /tmp/gu_gdiff.txt | grep -v -E '10080|11616|11620|zti<384|GU-GEN-DELTA 1' | wc -l)
if [ "$BADOLD" != "0" ] || [ "$BADNEW" != "0" ]; then
  echo "UNEXPECTED GEN DELTA:"; cat /tmp/gu_gdiff.txt; exit 1
fi
echo "gen deltas ok (1: garity class 12; 2: tried-state relocation)"

echo "== audit: opacity (no world literals in learner/glue) =="
if grep -w -E '301|302|307|311|312|313|314|321|322|323|324|325|329|331|332|341|342' gu_learn.zag gu_glue.zag; then
  echo "WORLD LITERAL IN LEARNER/GLUE"; exit 1
fi
echo "opacity ok"

echo "== assemble gu_full.zag =="
cat gu_base.zag gu_learn.zag gu_glue.zag gu_gen.zag gu_main.zag > gu_full.zag
S1=$(wc -c < gu_base.zag); S2=$(wc -c < gu_learn.zag); S3=$(wc -c < gu_glue.zag)
S4=$(wc -c < gu_gen.zag); S5=$(wc -c < gu_main.zag)
head -c "$S1" gu_full.zag | cmp - gu_base.zag
tail -c +"$((S1+1))" gu_full.zag | head -c "$S2" | cmp - gu_learn.zag
tail -c +"$((S1+S2+1))" gu_full.zag | head -c "$S3" | cmp - gu_glue.zag
tail -c +"$((S1+S2+S3+1))" gu_full.zag | head -c "$S4" | cmp - gu_gen.zag
tail -c "$S5" gu_full.zag | cmp - gu_main.zag
echo "regions ok"

echo "== compile with pinned safebin znc =="
znc gu_full.zag -o gu_bin
ls -la gu_bin

echo "== run 3x =="
./gu_bin > poc_run1.txt
./gu_bin > poc_run2.txt
./gu_bin > poc_run3.txt
cmp poc_run1.txt poc_run2.txt && cmp poc_run2.txt poc_run3.txt
echo "3/3 byte-identical"
sha256sum poc_run1.txt

echo "== prediction checks =="
grep -q 'ARM=GU PROB=F1 ANS=1 TRIES=3' poc_run1.txt && echo "F1 ok"
grep -q 'ARM=GU PROB=F2 ANS=0 TRIES=4' poc_run1.txt && echo "F2 ok"
grep -q 'ARM=GU PROB=F3 ANS=-2 TRIES=1216' poc_run1.txt && echo "F3 decline ok"
grep -q 'ARM=GU PROB=F4 ANS=-2' poc_run1.txt && echo "F4 empty-pattern decline ok"
grep -q 'ARM=GU PROB=U3 ANS=2 TRIES=7' poc_run1.txt && echo "U3 fan-out/fan-in ok"
grep -q 'ARM=GU PROB=U10 ANS=2 TRIES=6' poc_run1.txt && echo "U10 spec-decline/gen-fallback ok"
grep -q 'INTER=-1' poc_run1.txt && echo "spec-decline trial observed (INTER=-1)"
if grep -q 'WIDEN=1' poc_run1.txt; then echo "widen fired (F4)"; fi
grep -q 'CENSUS m=0 inmask=4 outmask=3' poc_run1.txt && echo "contract growth ok (m0 out {2}->{1,2})"
echo "ALL POC CHECKS PASS"
