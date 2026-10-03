#!/bin/sh
# GEN-POOLFLOOD build + verification pipeline. Fail-closed: any failure aborts.
# Encodes PREREG.md Section 6 construction sequence and the F2-F6 audits.
# NOTE: opacity grep uses -E (ERE). A BRE alternation (a|b) is literal and
# would make the audit vacuous; the ERE form is the genuine audit.
set -e
export PATH="$HOME/safebin"
cd "$(dirname "$0")"

echo "=== GEN-POOLFLOOD build pipeline ==="

# ---- Step 0: remove stale generated artifacts (idempotent re-runs) ----
echo "--- Step 0: clean stale artifacts ---"
rm -f pf_full.zag pf_bin pf_compile.txt \
  pf_bin_run1.txt pf_bin_run2.txt pf_bin_run3.txt \
  pf_bin_run1.err pf_bin_run2.err pf_bin_run3.err \
  pf_sec_PF1.txt pf_sec_PF2.txt exp_PF1.txt exp_PF2.txt \
  setup_pf1_frozen_extract.txt setup_pf1_mine.txt
echo "stale artifacts removed"

# ---- Step 1: canonical digests (PREREG Sec 2; NAMECHECK Step 1; F5) ----
echo "--- Step 1: canonical digests ---"
echo "17dd1cbdeb6a36e654f0b2d8fc57a730a7e58da8c5097081d466de1cc4eb8afc  ../gen_redim/rbase.zag" | sha256sum -c -
echo "3c7ebbe140b341cd90d7629117fcc4d7604cb86bc2cb4505ff0ebb31b3572476  ../gen_redim/rgen.zag" | sha256sum -c -
echo "da8760b68ca8d710a3d2545a484f65bf3d14d97bbcd3005422a17c989fb9dfcc  ../gen_redim/rgen_nomain.zag" | sha256sum -c -
echo "a43078d45410faefcc46689ea2951a1857e4f23af07aace7da202239658386d1  ../gen_redim/rd_sec_S5.txt" | sha256sum -c -
# setup_pf1 must be a byte-exact copy of the frozen setup_s5
sed -n '/^fn setup_s5(A:\[\]u8)void {$/,/^}$/p' ../gen_redim/rd_smain.zag | sed 's/setup_s5/setup_pf1/' > setup_pf1_frozen_extract.txt
sed -n '/^fn setup_pf1(A:\[\]u8)void {$/,/^}$/p' pf_main.zag > setup_pf1_mine.txt
cmp setup_pf1_frozen_extract.txt setup_pf1_mine.txt
echo "setup_pf1 byte-exact vs frozen setup_s5"
# This lane holds no other .zag files besides the driver (F5 second half)
[ -f pf_main.zag ] || { echo "F5 FAIL: missing pf_main.zag"; exit 1; }
n=$(ls *.zag | wc -l)
[ "$n" = "1" ] || { echo "F5 FAIL: expected 1 driver .zag file before assembly, found $n"; ls *.zag; exit 1; }
echo "F5: canonical sources byte-identical; lane holds only the driver"

# ---- Step 2: F6 opacity audit (PREREG Sec 3; genuine ERE audit) ----
echo "--- Step 2: F6 opacity audit ---"
TOKENS="hypothesis|refine|evaluat|domain|plan|causal|navigat|arithmet|grammar|language|audio|interven|belie|goal|agent"
HITS=$(grep -Ein "$TOKENS" pf_main.zag PREREG.md 2>/dev/null | grep -v "^[^:]*:[0-9]*:[a-z|.]*$" || true)
if [ -n "$HITS" ]; then
  echo "F6 FAIL: banned-token hits outside the definitional list:"; echo "$HITS"; exit 1
fi
echo "F6 audit: no banned tokens outside the definitional list"

# ---- Step 3: assemble (PREREG Sec 6.3; canonical sources untouched) ----
echo "--- Step 3: assemble ---"
cat ../gen_redim/rbase.zag ../gen_redim/rgen_nomain.zag pf_main.zag > pf_full.zag
n=$(grep -c "^fn main()i32 {" pf_full.zag); [ "$n" = "1" ] || { echo "assembly has $n mains"; exit 1; }
n=$(ls *.zag | wc -l)
[ "$n" = "2" ] || { echo "F5 FAIL: expected 2 .zag files after assembly, found $n"; ls *.zag; exit 1; }
echo "assembly built, one main"

# ---- Step 4: compile with pinned znc ----
echo "--- Step 4: compile ---"
znc pf_full.zag -o pf_bin > pf_compile.txt 2>&1
echo "pf_bin sha256: $(sha256sum pf_bin | cut -d' ' -f1)"

# ---- Step 5: run 3x, pairwise byte-identical, stderr empty (F2) ----
echo "--- Step 5: 3x runs ---"
./pf_bin > pf_bin_run1.txt 2> pf_bin_run1.err
./pf_bin > pf_bin_run2.txt 2> pf_bin_run2.err
./pf_bin > pf_bin_run3.txt 2> pf_bin_run3.err
cmp pf_bin_run1.txt pf_bin_run2.txt
cmp pf_bin_run2.txt pf_bin_run3.txt
for e in pf_bin_run1.err pf_bin_run2.err pf_bin_run3.err; do
  if [ -s "$e" ]; then echo "F2 FAIL: $e non-empty"; exit 1; fi
done
echo "pf_bin: 3/3 byte-identical, stderr empty, output sha256 $(sha256sum pf_bin_run1.txt | cut -d' ' -f1)"
echo "F2 DETERMINISM: PASS"

# ---- Step 6: split PF1 / PF2 sections on ARM lines ----
echo "--- Step 6: section split ---"
sed -n '1,/^ARM=GEN PROB=PF1/p' pf_bin_run1.txt > pf_sec_PF1.txt
sed -n '/^ARM=GEN PROB=PF1/,/^ARM=GEN PROB=PF2/p' pf_bin_run1.txt | tail -n +2 > pf_sec_PF2.txt
wc -l pf_sec_PF1.txt pf_sec_PF2.txt

# ---- Step 7: F3 PF1-BASELINE ----
echo "--- Step 7: F3 PF1-BASELINE ---"
# Pre-verify the canonical section before transforming it (fail-closed)
[ "$(tail -1 ../gen_redim/rd_sec_S5.txt)" = "ARM=GEN PROB=S5 ANS=-2 TRIES=2734" ] || { echo "F3 FAIL: canonical S5 ARM line moved"; exit 1; }
[ "$(head -3 ../gen_redim/rd_sec_S5.txt | sha256sum | cut -d' ' -f1)" = "$(printf 'INTER=2\nINTER=3\nINTER=201\n' | sha256sum | cut -d' ' -f1)" ] || { echo "F3 FAIL: canonical S5 head moved"; exit 1; }
sed 's/PROB=S5/PROB=PF1/' ../gen_redim/rd_sec_S5.txt > exp_PF1.txt
[ "$(grep -c 'PROB=PF1' exp_PF1.txt)" = "1" ] || { echo "F3 FAIL: label substitution count wrong"; exit 1; }
[ "$(grep -c 'PROB=S5' exp_PF1.txt)" = "0" ] || { echo "F3 FAIL: stale S5 label remains"; exit 1; }
cmp pf_sec_PF1.txt exp_PF1.txt && echo "F3 PF1-BASELINE: PASS (byte-identical to canonical S5 modulo label)"
[ "$(grep -c '^INTER=' pf_sec_PF1.txt)" = "3" ] || { echo "F3 FAIL: INTER count"; exit 1; }
[ "$(grep -c '^INTER2=' pf_sec_PF1.txt)" = "2731" ] || { echo "F3 FAIL: INTER2 count"; exit 1; }
[ "$(grep -c '^WIDEN=1' pf_sec_PF1.txt)" = "0" ] || { echo "F3 FAIL: WIDEN present"; exit 1; }
tail -1 pf_sec_PF1.txt | grep -qx "ARM=GEN PROB=PF1 ANS=-2 TRIES=2734" || { echo "F3 FAIL: ARM line"; exit 1; }
echo "PF1 counts exact: 3 INTER, 2731 INTER2, 0 WIDEN, ARM exact"

# ---- Step 8: F4 PF2-FLOOD ----
echo "--- Step 8: F4 PF2-FLOOD ---"
# Mechanical construction per PREREG Section 5 (canonical section pre-verified above)
head -3 ../gen_redim/rd_sec_S5.txt > exp_PF2.txt
i=0; while [ "$i" -lt 7 ]; do echo "INTER=201" >> exp_PF2.txt; i=$((i+1)); done
tail -n +4 ../gen_redim/rd_sec_S5.txt | sed 's/PROB=S5/PROB=PF2/; s/TRIES=2734/TRIES=2741/' >> exp_PF2.txt
[ "$(wc -l < exp_PF2.txt)" = "2742" ] || { echo "F4 FAIL: exp_PF2 line count"; exit 1; }
[ "$(sed -n '4,10p' exp_PF2.txt | grep -c '^INTER=201$')" = "7" ] || { echo "F4 FAIL: inserted lines"; exit 1; }
cmp pf_sec_PF2.txt exp_PF2.txt && echo "F4 PF2-FLOOD: PASS (byte-identical to constructed expected)"
[ "$(grep -c '^INTER=' pf_sec_PF2.txt)" = "10" ] || { echo "F4 FAIL: INTER count"; exit 1; }
[ "$(grep -c '^INTER2=' pf_sec_PF2.txt)" = "2731" ] || { echo "F4 FAIL: INTER2 count"; exit 1; }
[ "$(grep -c '^WIDEN=1' pf_sec_PF2.txt)" = "0" ] || { echo "F4 FAIL: WIDEN present"; exit 1; }
tail -1 pf_sec_PF2.txt | grep -qx "ARM=GEN PROB=PF2 ANS=-2 TRIES=2741" || { echo "F4 FAIL: ARM line"; exit 1; }
echo "PF2 counts exact: 10 INTER, 2731 INTER2, 0 WIDEN, ARM exact"

echo "=== GEN-POOLFLOOD pipeline complete: all kill bars decided ==="
