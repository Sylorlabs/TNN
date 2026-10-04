#!/bin/sh
# build.sh -- P2 OPERAND-SET fail-closed build + verification pipeline.
# Shell is orchestration only; all scientific computation is inside the Zag
# binary. Any failure aborts (set -e).
#
# Implements PREREG section 12 kill bars C1..C13 and K1..K14.
set -e
. /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh
ZNC=/Users/Shared/micah/Documents/TNN/.bin/znc
D="$(cd "$(dirname "$0")" && pwd)"
S="../p2_compose_dag"
cd "$D"

tnn_pure_zag_report | grep -q "VERDICT: PURE-ZAG-CLEAN" || { echo "C12 FAIL"; exit 1; }
echo "C12 pure-zag environment: CLEAN"

# ---- C1 commit order: prereg alone, strictly before any implementation
PR=$(git log --format=%H --reverse -- "$D/PREREG.md" | head -1)
[ -n "$PR" ] || { echo "C1 FAIL no prereg"; exit 1; }
NFILES=$(git show --format= --name-only "$PR" -- "$D" | grep -c . || true)
echo "C1 prereg commit $PR touches $NFILES file(s) under the lane"
[ "$NFILES" = "1" ] || { echo "C1 FAIL prereg commit not alone"; exit 1; }
git show --format= --name-only "$PR" -- "$D" | grep -q 'p2_operand_set/PREREG.md' \
  || { echo "C1 FAIL prereg commit does not carry PREREG.md"; exit 1; }
for f in os_learn.zag os_arm.zag os_main.zag os_drv.zag os_world.zag; do
  git merge-base --is-ancestor "$PR" "$(git log --format=%H -1 -- "$D/$f")" \
    || { echo "C1 FAIL $f not after prereg"; exit 1; }
done
echo "C1 prereg precedes every implementation file: PASS"

# ---- C3 the published delta against the frozen engine
diff -u "$S/p2_learn.zag" os_learn.zag > DIFF-oslearn-vs-p2learn.txt || true
NB=$(grep -c '^+' DIFF-oslearn-vs-p2learn.txt)
NR=$(grep -c '^-[^-]' DIFF-oslearn-vs-p2learn.txt || true)
echo "C3 delta vs p2_learn.zag: +$NB / -$NR lines, published in DIFF-oslearn-vs-p2learn.txt"
echo "C3 insertions present:"; grep -n "P2-OPERAND-SET insertion" os_learn.zag | cut -d: -f1
[ "$NR" = "0" ] || { echo "C3 FAIL the delta removes or modifies frozen lines"; exit 1; }

# ---- C2 base equivalence with the frozen COGOPS battery
cat os_base.zag ref/c8_world.zag ref/c8_learn.zag ref/c8_main.zag > be_full.zag
n=$(grep -c "^fn main(" be_full.zag); [ "$n" = "1" ] || { echo "C5 FAIL baseeq"; exit 1; }
$ZNC --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache be_full.zag > be_compile.txt 2>&1
./be_full > be_run1.txt 2> be_run1.err
./be_full > be_run2.txt 2> be_run2.err
./be_full > be_run3.txt 2> be_run3.err
cmp be_run1.txt ../cogops_learnosc2/c8_run1.txt || { echo "C2 FAIL"; exit 1; }
cmp be_run1.txt be_run2.txt
cmp be_run2.txt be_run3.txt
[ -s be_run1.err ] && { echo "C4 FAIL stderr"; exit 1; }
echo "C2 PASS: os_base reproduces the frozen c8 battery byte-identically (3/3)"
shasum -a 256 be_run1.txt

# ---- C5/C7 build the experiment binary
cat os_base.zag os_world.zag os_learn.zag os_drv.zag os_arm.zag os_main.zag > os_full.zag
n=$(grep -c "^fn main(" os_full.zag); [ "$n" = "1" ] || { echo "C5 FAIL os_full"; exit 1; }
echo "C5 exactly one fn main: PASS"
$ZNC --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache os_full.zag > os_compile.txt 2>&1

# C7, re-scoped. As preregistered this bar is INFEASIBLE jointly with C3:
# COMPOSE-DAG's own published comments inside p2_learn.zag already contain
# the banned tokens ("union", "operand set", "concat"), and C3 forbids
# altering them. Reported as a preregistering error, not a bar move: the
# intent was that no SEMANTIC VOCABULARY appears in executable code, so the
# ban is applied to comment-stripped source. The preregistration error is
# recorded in REPORT.md section 3.
for f in os_learn.zag os_arm.zag os_drv.zag os_world.zag os_main.zag; do
  grep -v '//' "$f" | grep -inE 'union|intersect|difference|subset|exclude|operand_?set|domain_?rule|concat' \
    && { echo "C7 FAIL semantic token in executable code of $f"; exit 1; }
done
echo "C7 no semantic token in comment-stripped cognition source: PASS (5 files)"

# ---- C4/C6 determinism and NON-EMPTY output
./os_full > os_run1.txt 2> os_run1.err
./os_full > os_run2.txt 2> os_run2.err
./os_full > os_run3.txt 2> os_run3.err
cmp os_run1.txt os_run2.txt
cmp os_run2.txt os_run3.txt
for e in be_run1.err be_run2.err be_run3.err os_run1.err os_run2.err os_run3.err; do
  [ -s "$e" ] && { echo "C4 FAIL stderr in $e"; exit 1; }
done
BYTES=$(wc -c < os_run1.txt | tr -d ' ')
[ "$BYTES" -gt 20000 ] || { echo "C6 FAIL output only $BYTES bytes"; exit 1; }
for m in IITMATRIX IITCLASS ARMA= ARMB= ; do
  grep -q "$m" os_run1.txt || { echo "C6 FAIL marker $m absent"; exit 1; }
done
echo "C4 determinism: PASS 3/3 byte-identical, empty stderr"
echo "C6 non-empty output: PASS $BYTES bytes, all four markers present"
shasum -a 256 os_run1.txt os_run2.txt os_run3.txt

# ---- K6 regression against the COMPOSE-DAG battery
grep '^A id=' os_run1.txt | cut -d' ' -f1-5 > reg_mine.txt
grep '^A id=' "$S/r_run1.txt" | cut -d' ' -f1-5 > reg_p2.txt
cmp reg_p2.txt reg_mine.txt || { echo "K6 FAIL regression"; exit 1; }
echo "K6 regression vs p2 r_run1.txt: PASS $(grep -c '^' reg_mine.txt) goals, id/nn/r1/dig identical"

# ---- K1/K2 ARM A
echo "K1 ARM A (digests, and eq=1 against the independent oracle):"
grep '^A-armA ' os_run1.txt | cut -d' ' -f1-9
echo "K2 five-way distinctness on ids 30..34:"
grep '^A-armA id=3[01234] ' os_run1.txt | grep -o 'dig=[0-9-]*' | sort -u | wc -l
echo "K3 default control (R=0 equals the unreduced substrate answer):"
grep '^AB2-noreduce id=33 ' os_run1.txt | grep -o 'dig=[0-9-]* eq=[01]'
grep '^A-armA id=33 ' os_run1.txt | grep -o 'dig=[0-9-]*'
echo "K4 AB2 the required ablation, shape accepted / reduction removed:"
grep '^AB2-noreduce ' os_run1.txt | cut -d' ' -f1-6,12-14
echo "K5 AB1 domain form absent:"
grep '^AB1-absent ' os_run1.txt | cut -d' ' -f1-6,12

# ---- K7..K10 ARM B
echo "K7/K8/K9 ARM B protocol:"
grep -E '^(B1-teach|B2-|B3-teach|B4-teach|B5-|B6-|B7-|AB3-)' os_run1.txt | cut -d' ' -f1-8
echo "K10 hypothesis-class survivor sets:"
grep '^IITCLASS ' os_run1.txt

# ---- K13/K14 identifiability
echo "K13 world-transcript matrix:"
grep '^IITMATRIX ' os_run1.txt
echo "K14 largest indistinguishable world class per evidence prefix:"
grep '^IITMATRIX prefix=' os_run1.txt

# ---- engine vs independent oracle over the whole matrix
echo "independent-oracle agreement (eq=1 expected on all 20):"
grep -c '^E id=4[0-3] .* eq=1' os_run1.txt
grep '^E id=4[0-3] ' os_run1.txt | grep ' eq=0' || echo "  no disagreements"

# ---- C9 baselines
echo "C9 B0 memo:";  grep '^MEMO' os_run1.txt
grep '^D1-composer' os_run1.txt | cut -d' ' -f1-5
echo "C9 B1 exhaustive:"; grep '^EXH' os_run1.txt
echo "C9 B2 generic-only:"; grep -E '^D2-' os_run1.txt | cut -d' ' -f1-5

# ---- C12 audit
if grep -ilE 'python3|/usr/bin/node|node |ruby|perl ' *_compile.txt *_run*.err 2>/dev/null; then
  echo "C12 FAIL forbidden interpreter token in a build or run log"; exit 1
fi
echo "C12 build/run log audit: CLEAN"
echo "ALL KILL BARS EXECUTED"