#!/bin/bash
# cl_posthoc.sh -- SPEC-COMMIT-L post-hoc finding tables.
# Prints finding tables on the FROZEN cl_run1.txt data. This is
# post-hoc analysis, NOT a bar re-adjudication: it must not move any
# frozen bar.
export PATH="$HOME/safebin"
set -u
D="$(cd "$(dirname "$0")" && pwd)"
cd "$D" || exit 1
F=cl_run1.txt

field() {
  grep "^CELL R=$1 " $F | grep " P=$2 " | grep " L=$3 " \
    | grep -o " $4=[0-9-]*" | head -1 | cut -d= -f2
}
j_val() {
  rb=$(field "$1" "$2" "$3" rebuilds); rf=$(field "$1" "$2" "$3" refusals)
  echo $(( rb + rf * $3 ))
}
jp_val() {
  rb=$(field "$1" "$2" "$3" rebuilds); rf=$(field "$1" "$2" "$3" refusals)
  echo $(( rb + rf ))
}

echo "=== commit outcomes by cell/arm/L: the commit rule's L-dependence ==="
printf "%-4s %-8s %4s %5s %4s %4s %4s %6s %5s %5s %5s\n" R P L tc cm Dc flips tf1 J Jp
for R in 21 60 82 120; do
  for P in noeg coml1 comlg comnoeg; do
    for L in 1 3 7 10; do
      tc=$(field $R $P $L tc); cm=$(field $R $P $L cm); dc=$(field $R $P $L Dc)
      fl=$(field $R $P $L flips); tf1=$(field $R $P $L tf1)
      j=$(j_val $R $P $L); jp=$(jp_val $R $P $L)
      printf "%-4s %-8s %4s %5s %4s %4s %6s %5s %5s %5s\n" "$R" "$P" "$L" "$tc" "$cm" "$dc" "$fl" "$tf1" "$j" "$jp"
    done
  done
done
echo "(J = rb + rf*L; J' = rb + rf)"

echo ""
echo "=== quirk scoreboard: D32=0 cells, J by quirk handling ==="
printf "%-4s %4s %9s %9s %11s\n" R L coml1 comlg comnoeg
for R in 21 60 82; do
  for L in 1 3 7 10; do
    printf "%-4s %4s %9s %9s %11s\n" "$R" "$L" "$(j_val $R coml1 $L)" "$(j_val $R comlg $L)" "$(j_val $R comnoeg $L)"
  done
done
echo "(coml1 = quirk preserved; comlg = quirk guarded; comnoeg = eager dropped)"

echo ""
echo "=== R=120 economics: J and J' for L-bearing vs L-free commit ==="
printf "%-8s %4s %5s %5s %5s %5s %5s\n" P L J Jp rb rf rs
for P in noeg coml1 comlg comnoeg; do
  for L in 1 3 7 10; do
    rb=$(field 120 $P $L rebuilds); rf=$(field 120 $P $L refusals); rs=$(field 120 $P $L rs)
    printf "%-8s %4s %5s %5s %5s %5s %5s\n" "$P" "$L" "$(j_val 120 $P $L)" "$(jp_val 120 $P $L)" "$rb" "$rf" "$rs"
  done
done

echo ""
echo "=== comlg vs comnoeg: full line identity (mod P=) per cell/L ==="
for R in 21 60 82 120; do
  for L in 1 3 7 10; do
    l1=$(grep "^CELL R=$R " $F | grep " P=comlg " | grep " L=$L " | sed "s/ P=comlg / P=POL /")
    l2=$(grep "^CELL R=$R " $F | grep " P=comnoeg " | grep " L=$L " | sed "s/ P=comnoeg / P=POL /")
    if [ "$l1" = "$l2" ]; then echo "  R=$R L=$L: IDENTICAL"; else echo "  R=$R L=$L: DIFFER"; fi
  done
done

echo ""
echo "=== R=60 harm cell: full commit/flip trace for the new arms ==="
printf "%-8s %4s %5s %4s %4s %4s %6s %5s %5s %5s %5s\n" P L tc cm Dc flips tf1 fdir sel J
for P in noeg coml1 comlg comnoeg; do
  for L in 1 3 7 10; do
    tc=$(field 60 $P $L tc); cm=$(field 60 $P $L cm); dc=$(field 60 $P $L Dc)
    fl=$(field 60 $P $L flips); tf1=$(field 60 $P $L tf1); fd=$(field 60 $P $L fdir)
    se=$(field 60 $P $L sel)
    printf "%-8s %4s %5s %4s %4s %4s %6s %5s %5s %5s %5s\n" "$P" "$L" "$tc" "$cm" "$dc" "$fl" "$tf1" "$fd" "$se" "$(j_val 60 $P $L)"
  done
done
