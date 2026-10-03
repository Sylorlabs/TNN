#!/bin/bash
# ft_posthoc.sh -- SPEC-FLIP-THRESHOLD post-hoc finding tables.
# Prints finding tables on the FROZEN ft_run1.txt data. This is
# post-hoc analysis, NOT a bar re-adjudication: it must not move any
# frozen bar.
export PATH="$HOME/safebin"
set -u
D="$(cd "$(dirname "$0")" && pwd)"
cd "$D" || exit 1
F=ft_run1.txt

field() {
  grep "^CELL R=$1 " $F | grep " P=$2 " | grep " L=$3 " \
    | grep -o " $4=[0-9-]*" | head -1 | cut -d= -f2
}
j_val() {
  rb=$(field "$1" "$2" "$3" rebuilds); rf=$(field "$1" "$2" "$3" refusals)
  echo $(( rb + rf * $3 ))
}

echo "=== R=60 harm cell: rescue timing and cost by threshold arm ==="
printf "%-8s %4s %5s %6s %5s %5s %4s %4s %5s\n" P L tf1 flips fdir rs od J V
for P in adapt fix2 qmean adaptd; do
  for L in 1 3 7 10; do
    tf1=$(field 60 $P $L tf1); fl=$(field 60 $P $L flips); fd=$(field 60 $P $L fdir)
    rs=$(field 60 $P $L rs); od=$(field 60 $P $L od); j=$(j_val 60 $P $L)
    je=$(j_val 60 eager -1); v=$(( je - j ))
    printf "%-8s %4s %5s %6s %5s %5s %4s %5s %4s\n" "$P" "$L" "$tf1" "$fl" "$fd" "$rs" "$od" "$j" "$v"
  done
done
je=$(j_val 60 eager -1); jl=$(j_val 60 lazy -1)
echo "fixed lazy J=$jl fixed eager J=$je (V = J_eager - J_arm)"

echo ""
echo "=== control cells: flips by arm (spurious-flip check) ==="
printf "%-4s %-8s %4s %6s %5s %4s\n" R P L flips tf1 J
for R in 21 82 120; do
  for P in adapt fix2 qmean adaptd; do
    for L in 1 3 7 10; do
      fl=$(field $R $P $L flips); tf1=$(field $R $P $L tf1); j=$(j_val $R $P $L)
      ja=$(j_val $R adapt $L)
      if [ "$fl" != "0" ]; then
        printf "%-4s %-8s %4s %6s %5s %4s (adapt J=%s)\n" "$R" "$P" "$L" "$fl" "$tf1" "$j" "$ja"
      fi
    done
  done
done
echo "(arms with flips=0 on a control cell are not listed)"

echo ""
echo "=== R=120 (same regime as R=60, D32=1): rescue timing ==="
printf "%-8s %4s %5s %6s %5s\n" P L tf1 flips J
for P in adapt fix2 qmean adaptd; do
  for L in 1 3 7 10; do
    tf1=$(field 120 $P $L tf1); fl=$(field 120 $P $L flips); j=$(j_val 120 $P $L)
    printf "%-8s %4s %5s %6s %5s\n" "$P" "$L" "$tf1" "$fl" "$j"
  done
done
