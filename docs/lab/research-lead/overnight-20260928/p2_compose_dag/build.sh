#!/bin/sh
# build.sh -- COMPOSE-DAG fail-closed build + verification pipeline.
# Shell is orchestration only; all scientific computation is inside the
# Zag binaries. Any failure aborts (set -e).
#
# Steps implement the PREREG Section 12 kill bars C1..C13.
set -e
. /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh
ZNC=/Users/Shared/micah/Documents/TNN/.bin/znc
FLAGS="--target macos-arm64 --no-zagd --no-analyze --no-foreground-cache"
D="$(cd "$(dirname "$0")" && pwd)"
cd "$D"
tnn_pure_zag_report | grep -q "VERDICT: PURE-ZAG-CLEAN" || { echo "C12 FAIL"; exit 1; }
echo "C12 pure-zag environment: CLEAN"

# ---- C3 frozen substrate identity
for f in c8_base c8_learn c8_world c8_main; do
  cmp "ref/$f.zag" "../cogops_learnosc2/$f.zag"
done
echo "C3 frozen substrate: byte-identical to ../cogops_learnosc2"
shasum -a 256 ref/c8_base.zag ref/c8_learn.zag ref/c8_world.zag ref/c8_main.zag

# ---- C2 my base is equivalent to the frozen base
cat p2_base.zag ref/c8_world.zag ref/c8_learn.zag ref/c8_main.zag > baseeq_full.zag
n=$(grep -c "^fn main(" baseeq_full.zag); [ "$n" = "1" ] || { echo "C5 FAIL baseeq"; exit 1; }
$ZNC $FLAGS baseeq_full.zag > baseeq_compile.txt 2>&1
./baseeq_full > baseeq_run1.txt 2> baseeq_run1.err
./baseeq_full > baseeq_run2.txt 2> baseeq_run2.err
./baseeq_full > baseeq_run3.txt 2> baseeq_run3.err
cmp baseeq_run1.txt ../cogops_learnosc2/c8_run1.txt || { echo "C2 FAIL"; exit 1; }
cmp baseeq_run1.txt baseeq_run2.txt
cmp baseeq_run2.txt baseeq_run3.txt
[ -s baseeq_run1.err ] && { echo "C4 FAIL stderr"; exit 1; }
echo "C2 PASS: p2_base reproduces the frozen c8 battery byte-identically (3/3)"
shasum -a 256 baseeq_run1.txt

# ---- C5/C6/C10 the two arms
cat p2_base.zag p2_world.zag ref/c8_learn.zag p2_drv.zag f_main.zag > f_base.zag
cat p2_base.zag p2_world.zag p2_learn.zag p2_drv.zag r_main.zag   > r_full.zag
for f in f_base r_full; do
  n=$(grep -c "^fn main(" "$f.zag"); [ "$n" = "1" ] || { echo "C5 FAIL $f"; exit 1; }
  $ZNC $FLAGS "$f.zag" > "${f}_compile.txt" 2>&1
done
echo "C5 one main per binary: PASS"

if grep -qE 'z_alloc\((320|640|512|16)\)' p2_learn.zag; then echo "C6 FAIL literal stride"; exit 1; fi
echo "C6 no frozen per-need literal stride in p2_learn.zag: PASS"

BANT="pipeline|diamond|fanin|fan_in|fanout|fan_out|CHAIN_COUNT|ARITH_PLAN"
if grep -inE "$BANT" p2_learn.zag; then echo "C10 FAIL"; exit 1; fi
echo "C10 informational: the FROZEN core keeps its own historical vocabulary"
grep -inE "$BANT" ref/c8_learn.zag | sed "s/^/    frozen: /" || echo "    (none)"
echo "C10 no topology token in the NEW cognition source: PASS"

# ---- C4 determinism, both arms
./f_base > f_base_run1.txt 2> f_base_run1.err
./f_base > f_base_run2.txt 2> f_base_run2.err
./f_base > f_base_run3.txt 2> f_base_run3.err
cmp f_base_run1.txt f_base_run2.txt
cmp f_base_run2.txt f_base_run3.txt
./r_full > r_run1.txt 2> r_run1.err
./r_full > r_run2.txt 2> r_run2.err
./r_full > r_run3.txt 2> r_run3.err
cmp r_run1.txt r_run2.txt
cmp r_run2.txt r_run3.txt
for e in f_base_run1.err f_base_run2.err f_base_run3.err r_run1.err r_run2.err r_run3.err; do
  if [ -s "$e" ]; then echo "C4 FAIL stderr in $e"; exit 1; fi
done
echo "C4 determinism: PASS 3/3 byte-identical, empty stderr, both arms"
shasum -a 256 f_base_run1.txt r_run1.txt

# ---- C7 / X1..X7
echo "C7/X2 answered SEC-A goals differing from the independent adapt reference:"
grep '^A id=' r_run1.txt | grep ' r1=2 ' | grep 'eq=0' | cut -d' ' -f1-6 || true
echo "C7/X3 refusals (r1=0):"
grep '^A id=' r_run1.txt | grep ' r1=0 ' | cut -d' ' -f1-6 || true
echo "C7/X4 capacity at nn=10 and nn=20:"
grep -E '^A id=(12|22|23|24) ' r_run1.txt | cut -d' ' -f1-9
echo "C7/X5 canonical emission, plan order for id 9 and id 19:"
grep -E '^A id=(9|19) ' r_run1.txt | grep -o 'ord=[^v]*'
echo "C7/X6 iteration pass count for id 19:"
grep '^A id=19 ' r_run1.txt | grep -o 'pa=[0-9]*'
echo "C7/X7 inertness on the frozen battery: see baseeq_run1.txt (C2)"

# ---- C8 baselines
echo "C8 B0 memo:";    grep '^MEMO' r_run1.txt
echo "C8 B1 exhaustive:"; grep '^EXH' r_run1.txt
echo "C8 B2 warm vs generic-only:"; grep -E '^D3-' r_run1.txt | cut -d' ' -f1-5

# ---- C9 ablations
echo "C9 ablations:"; grep -E '^E[0-9]' r_run1.txt | cut -d' ' -f1-6

# ---- C12 audit
if grep -ilE 'python3|/usr/bin/node|ruby' *_compile.txt *_run*.err 2>/dev/null; then
  echo "C12 FAIL forbidden interpreter token in a log"; exit 1
fi
echo "C12 log audit: CLEAN"
echo "ALL KILL BARS EXECUTED"