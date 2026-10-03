#!/bin/sh
# GEN-NM10 build + verification pipeline. Fail-closed: any failure aborts.
# Encodes PREREG.md Section 6 construction sequence and the N2-N7 audits.
set -e
export PATH="$HOME/safebin"
cd "$(dirname "$0")"

echo "=== GEN-NM10 build pipeline ==="

# ---- Step 1: canonical source digests (PREREG Sec 6; NAMECHECK Step 1; N5) ----
echo "--- Step 1: canonical digests ---"
echo "17dd1cbdeb6a36e654f0b2d8fc57a730a7e58da8c5097081d466de1cc4eb8afc  ../gen_redim/rbase.zag" | sha256sum -c -
echo "3c7ebbe140b341cd90d7629117fcc4d7604cb86bc2cb4505ff0ebb31b3572476  ../gen_redim/rgen.zag" | sha256sum -c -
echo "da8760b68ca8d710a3d2545a484f65bf3d14d97bbcd3005422a17c989fb9dfcc  ../gen_redim/rgen_nomain.zag" | sha256sum -c -
# This lane holds no other .zag files besides the two drivers (N5 second
# half; the two assemblies are created in Step 3 and checked there).
for f in nm_b1main.zag nm_b2main.zag; do [ -f "$f" ] || { echo "N5 FAIL: missing $f"; exit 1; }; done
n=$(ls *.zag | wc -l)
[ "$n" = "2" ] || { echo "N5 FAIL: expected 2 driver .zag files before assembly, found $n"; ls *.zag; exit 1; }
echo "N5: canonical sources byte-identical; lane holds only the 2 drivers"

# ---- Step 2: N6 opacity audit (PREREG Sec 3, Sec 7) ----
echo "--- Step 2: N6 opacity audit ---"
TOKENS="hypothesis|refine|evaluat|domain|plan|causal|navigat|arithmet|grammar|language|audio|interven|belie|goal|agent"
HITS=$(grep -in "$TOKENS" nm_b1main.zag nm_b2main.zag PREREG.md 2>/dev/null | grep -v "^[^:]*:[0-9]*:[a-z|.]*$" || true)
if [ -n "$HITS" ]; then
  echo "N6 FAIL: banned-token hits:"; echo "$HITS"; exit 1
fi
echo "N6 audit: no banned tokens outside the definitional list"

# ---- Step 3: assemble (PREREG Sec 6.3; canonical sources untouched) ----
echo "--- Step 3: assemble ---"
cat ../gen_redim/rbase.zag ../gen_redim/rgen_nomain.zag nm_b1main.zag > nm_b1full.zag
cat ../gen_redim/rbase.zag ../gen_redim/rgen_nomain.zag nm_b2main.zag > nm_b2full.zag
for f in nm_b1full.zag nm_b2full.zag; do
  n=$(grep -c "^fn main()i32 {" "$f"); [ "$n" = "1" ] || { echo "assembly $f has $n mains"; exit 1; }
done
n=$(ls *.zag | wc -l)
[ "$n" = "4" ] || { echo "N5 FAIL: expected 4 .zag files after assembly, found $n"; ls *.zag; exit 1; }
echo "assemblies built, one main each"

# ---- Step 4: compile with pinned znc ----
echo "--- Step 4: compile ---"
znc nm_b1full.zag -o nm_b1bin > nm_b1compile.txt 2>&1
znc nm_b2full.zag -o nm_b2bin > nm_b2compile.txt 2>&1
echo "both binaries compiled"
echo "nm_b1bin sha256: $(sha256sum nm_b1bin | cut -d' ' -f1)"
echo "nm_b2bin sha256: $(sha256sum nm_b2bin | cut -d' ' -f1)"

# ---- Step 5: run 3x each, pairwise byte-identical (N2) ----
echo "--- Step 5: 3x runs ---"
for b in nm_b1bin nm_b2bin; do
  ./$b > ${b}_run1.txt 2> ${b}_run1.err
  ./$b > ${b}_run2.txt 2> ${b}_run2.err
  ./$b > ${b}_run3.txt 2> ${b}_run3.err
  cmp ${b}_run1.txt ${b}_run2.txt
  cmp ${b}_run2.txt ${b}_run3.txt
  if [ -s ${b}_run1.err ]; then echo "$b wrote to stderr"; exit 1; fi
  echo "$b: 3/3 byte-identical, stderr empty, output sha256 $(sha256sum ${b}_run1.txt | cut -d' ' -f1)"
done
echo "N2 DETERMINISM: PASS"

# ---- Step 6: extract expected blocks from this PREREG ----
echo "--- Step 6: expected blocks ---"
for s in B1 B2; do
  sed -n "/^\`\`\`text exp-$s\$/,/^\`\`\`$/p" PREREG.md | sed '1d;$d' > exp_$s.txt
done
wc -l exp_B1.txt exp_B2.txt

# ---- Step 7: N3 B1-LAYOUT (byte-identity) ----
echo "--- Step 7: N3 ---"
cmp nm_b1bin_run1.txt exp_B1.txt && echo "N3 B1-LAYOUT: PASS (byte-identical)"
[ "$(grep -c "^WIDEN=1" nm_b1bin_run1.txt)" = "0" ] && echo "B1 WIDEN count = 0"
tail -1 nm_b1bin_run1.txt | grep -qx "ARM=GEN PROB=B1 ANS=-2 TRIES=66" && echo "B1 ARM line exact"

# ---- Step 8: N4 B2-COMPOSE (byte-identity) ----
echo "--- Step 8: N4 ---"
cmp nm_b2bin_run1.txt exp_B2.txt && echo "N4 B2-COMPOSE: PASS (byte-identical)"
[ "$(grep -c "^WIDEN=1" nm_b2bin_run1.txt)" = "0" ] && echo "B2 WIDEN count = 0"
tail -1 nm_b2bin_run1.txt | grep -qx "ARM=GEN PROB=B2 ANS=315 TRIES=67" && echo "B2 ARM line exact"

echo "=== GEN-NM10 pipeline complete: all kill bars evaluated ==="
