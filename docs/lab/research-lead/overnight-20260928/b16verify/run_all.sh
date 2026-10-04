#!/bin/bash
# b16verify: reproduce every result in TOOLCHAIN_VERDICT.md.
# Shell is orchestration only. All computation is inside the Zag binaries.
set -u
. /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh
cd "$(dirname "$0")"
ZB=/Users/Shared/micah/Documents/TNN/TNN/tools/zbuild.sh
D=/Users/Shared/micah/Documents/TNN/TNN/docs/lab/research-lead/overnight-20260928

for p in p1_min p2_withbase p3_sweep p6_tworeader; do
  echo "##### $p"
  $ZB ./$p.zag --rep 3 2>&1 | grep -E "^\[znc\]|\[run 1\]|DETERMINISM|VERDICT|MISMATCH|CELL|BYTES|REF|CELLS|COMPAR|SKIPP|FIRST|SIZE|CHAIN|FACT|ORACLE|H1_|A_vs"
done

echo "##### P4 large-TU sweep (B17)"
$ZB ./p4_gen.zag 2>&1 | tail -2
for n in 100 400 1000 2000 4000; do
  cat tl_prelude.zag gen${n}_blocks.zag > p4_${n}.zag
  printf "TU p4_%s lines=%s " "$n" "$(wc -l < p4_${n}.zag)"
  $ZB ./p4_${n}.zag --rep 3 2>&1 | grep -E "MATCH|error|COMPILE-FAIL" | head -1
done

echo "##### section-5 constraints, one binary each"
for f in sec5_c1_and sec5_c2_or sec5_c3_demorgan sec5_c4_bang_and \
         sec5_c5_bare_bang sec5_c6_d3 sec5_c6_d4 sec5_c6_d5 sec5_c6_d8 \
         sec5_c7_for sec5_c8_slice_as_ptr sec5_c9_malloc_direct; do
  printf "%-26s " "$f"
  o=$($ZB ./$f.zag 2>&1)
  if [ $? -eq 0 ]; then
    echo "OK   $(echo "$o" | grep -vE '^\[znc\]|^\[zbuild\]|^$' | tr '\n' ' ')"
  else
    echo "FAIL $(echo "$o" | grep -m1 'error\|znc:' | head -1)"
  fi
done

echo "##### reporter's own 3840-line TU"
$ZB ./reporter_lt1_full.zag --rep 3 2>&1 | grep -E "^\[znc\]|DETERMINISM" | head -3
./reporter_lt1_full > my_lt1.txt 2>&1
diff my_lt1.txt "$D/p1_lifetime_ab/lt1_run1.txt" >/dev/null \
  && echo "lt1_full reproduces p1_lifetime_ab/lt1_run1.txt BYTE-IDENTICALLY" \
  || echo "lt1_full DIFFERS from recorded run1"