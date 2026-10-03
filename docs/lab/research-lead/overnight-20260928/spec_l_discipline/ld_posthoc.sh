#!/bin/bash
# ld_posthoc.sh -- SPEC-L-DISCIPLINE post-hoc finding tables.
# Prints finding tables on the FROZEN ld_run1.txt data. This is
# post-hoc analysis, NOT a bar re-adjudication: it must not move any
# frozen bar.
export PATH="$HOME/safebin"
set -u
D="$(cd "$(dirname "$0")" && pwd)"
cd "$D" || exit 1
F=ld_run1.txt

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

echo "=== identity summary: noeg vs fix2, noj vs fix2, nol vs noeg (mod P=) ==="
for pair in "noeg fix2" "noj fix2" "nol noeg"; do
  set -- $pair
  ndiff=0; ntot=0
  for R in 21 60 82 120; do
    for L in 1 3 7 10; do
      ntot=$(( ntot + 1 ))
      l1=$(grep "^CELL R=$R " $F | grep " P=$1 " | grep " L=$L " | sed "s/ P=$1 / P=POL /")
      l2=$(grep "^CELL R=$R " $F | grep " P=$2 " | grep " L=$L " | sed "s/ P=$2 / P=POL /")
      [ "$l1" = "$l2" ] || { ndiff=$(( ndiff + 1 )); echo "  DIFF: R=$R L=$L $1 vs $2"; }
    done
  done
  echo "$1 vs $2: $(( ntot - ndiff ))/$ntot identical modulo P="
done

echo ""
echo "=== R=60 harm cell: J vs J' by arm (does L-free scoring change conclusions?) ==="
printf "%-8s %4s %5s %5s %5s %5s %5s\n" P L J Jp rs od
for P in adapt fix2 noeg eager lazy; do
  for L in 1 3 7 10 -1; do
    case "$P" in
      eager|lazy) [ "$L" != "-1" ] && continue ;;
      *) [ "$L" = "-1" ] && continue ;;
    esac
    rs=$(field 60 $P $L rs); od=$(field 60 $P $L od)
    j=$(j_val 60 $P $L); jp=$(jp_val 60 $P $L)
    printf "%-8s %4s %5s %5s %5s %5s\n" "$P" "$L" "$j" "$jp" "$rs" "$od"
  done
done
echo "(J = rb + rf*L; J' = rb + rf)"

echo ""
echo "=== all cells: rescue timing for the L-discipline arms ==="
printf "%-4s %-6s %4s %5s %6s %5s %5s %5s\n" R P L tf1 flips fdir J Jp
for R in 21 60 82 120; do
  for P in fix2 noeg noj nol; do
    for L in 1 3 7 10; do
      tf1=$(field $R $P $L tf1); fl=$(field $R $P $L flips); fd=$(field $R $P $L fdir)
      j=$(j_val $R $P $L); jp=$(jp_val $R $P $L)
      printf "%-4s %-6s %4s %5s %6s %5s %5s %5s\n" "$R" "$P" "$L" "$tf1" "$fl" "$fd" "$j" "$jp"
    done
  done
done

echo ""
echo "=== commit-side L-dependence (out-of-scope bound): R=120 commit fields by L ==="
printf "%-8s %4s %4s %4s %4s %4s\n" P L tc cm Dc Qc
for P in adapt fix2 noeg; do
  for L in 1 3 7 10; do
    tc=$(field 120 $P $L tc); cm=$(field 120 $P $L cm)
    dc=$(field 120 $P $L Dc); qc=$(field 120 $P $L Qc)
    printf "%-8s %4s %4s %4s %4s %4s\n" "$P" "$L" "$tc" "$cm" "$dc" "$qc"
  done
done
echo "(the commit rule keeps L in every arm; its L-dependence bounds the L-free claim)"
