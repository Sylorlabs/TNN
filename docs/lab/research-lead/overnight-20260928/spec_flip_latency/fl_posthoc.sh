#!/bin/bash
# fl_posthoc.sh -- SPEC-FLIP-LATENCY post-hoc finding tables.
# Labeled post-hoc analysis, NOT a bar re-adjudication: it prints
# finding tables on the frozen fl_run1.txt data and must not move
# any frozen bar. Pure shell/grep/awk.
export PATH="$HOME/safebin"
set -u
D="$(cd "$(dirname "$0")" && pwd)"
cd "$D" || exit 1
F=fl_run1.txt

field() {
  grep "^CELL R=$1 " "$F" | grep " P=$2 " | grep " L=$3 " \
    | grep -o " $4=[0-9-]*" | head -1 | cut -d= -f2
}
j_val() {
  rb=$(field "$1" "$2" "$3" rebuilds); rf=$(field "$1" "$2" "$3" refusals)
  echo $(( rb + rf * $3 ))
}

echo "=== 1. Latency curve on the harm cell (R=60): tf1 / flips / fdir / tf2 ==="
printf "%-9s %-28s %-28s %-28s %-28s\n" "L" "adapt(tf1,flips)" "guard(tf1,flips)" "fastchk(tf1,flips)" "fastewma(tf1,flips)"
for L in 1 3 7 10 15 20 30; do
  pa=""; pg=""; pf=""; pw=""
  for P in adapt guard fastchk fastewma; do
    case "$P" in
      adapt) LL="$L" ;;
      guard) case "$L" in 3|7|10) LL="$L";; *) LL="-";; esac ;;
      *) case "$L" in 1|7|10) LL="$L";; *) LL="-";; esac ;;
    esac
    if [ "$LL" = "-" ]; then v="--";
    else
      t=$(field 60 "$P" "$LL" tf1); fl=$(field 60 "$P" "$LL" flips)
      fd=$(field 60 "$P" "$LL" fdir); t2=$(field 60 "$P" "$LL" tf2)
      v="$t,$fl,$fd,$t2"
    fi
    case "$P" in adapt) pa="$v";; guard) pg="$v";; fastchk) pf="$v";; fastewma) pw="$v";; esac
  done
  printf "%-9s %-28s %-28s %-28s %-28s\n" "$L" "$pa" "$pg" "$pf" "$pw"
done

echo ""
echo "=== 2. Cost J = rb + rf*L on R=60 (lower is better) ==="
printf "%-9s %-8s %-8s %-8s %-8s %-8s %-8s\n" "L" "lazy" "eager" "adapt" "guard" "fastchk" "fastewma"
jl0=$(j_val 60 lazy -1); je0=$(j_val 60 eager -1)
for L in 1 3 7 10 15 20 30; do
  ja=$(j_val 60 adapt "$L")
  case "$L" in 3|7|10) jg=$(j_val 60 guard "$L");; *) jg="--";; esac
  case "$L" in 1|7|10) jf=$(j_val 60 fastchk "$L"); jw=$(j_val 60 fastewma "$L");; *) jf="--"; jw="--";; esac
  printf "%-9s %-8s %-8s %-8s %-8s %-8s %-8s\n" "$L" "$jl0" "$je0" "$ja" "$jg" "$jf" "$jw"
done
echo "(lazy/eager J shown at L=-1 row convention: lazy J is L-dependent; values above use the arm's own L)"
echo "lazy J by L:"
for L in 1 3 7 10 15 20 30; do printf "  L=%-3s J_lazy=%s\n" "$L" "$(j_val 60 lazy "$L")"; done

echo ""
echo "=== 3. Eager-stint restamps rs and on-demand od on R=60 ==="
printf "%-9s %-16s %-16s %-16s %-16s\n" "L" "adapt(rs,od)" "guard(rs,od)" "fastchk(rs,od)" "fastewma(rs,od)"
for L in 1 3 7 10 15 20 30; do
  pa=""; pg=""; pf=""; pw=""
  for P in adapt guard fastchk fastewma; do
    case "$P" in
      adapt) LL="$L" ;;
      guard) case "$L" in 3|7|10) LL="$L";; *) LL="-";; esac ;;
      *) case "$L" in 1|7|10) LL="$L";; *) LL="-";; esac ;;
    esac
    if [ "$LL" = "-" ]; then v="--";
    else
      rs=$(field 60 "$P" "$LL" rs); od=$(field 60 "$P" "$LL" od)
      tc=$(field 60 "$P" "$LL" tc); cm=$(field 60 "$P" "$LL" cm)
      v="rs=$rs od=$od tc=$tc cm=$cm"
    fi
    case "$P" in adapt) pa="$v";; guard) pg="$v";; fastchk) pf="$v";; fastewma) pw="$v";; esac
  done
  printf "%-9s %-16s %-16s %-16s %-16s\n" "$L" "$pa" "$pg" "$pf" "$pw"
done

echo ""
echo "=== 4. EWMA snapshots at e=144/192 on R=60 (dh144,qh144,dh192,qh192) ==="
for P in adapt fastchk fastewma; do
  case "$P" in adapt) LL=7;; *) LL=7;; esac
  d1=$(field 60 "$P" "$LL" dh144); q1=$(field 60 "$P" "$LL" qh144)
  d2=$(field 60 "$P" "$LL" dh192); q2=$(field 60 "$P" "$LL" qh192)
  echo "  $P L=$LL: dh144=$d1 qh144=$q1 dh192=$d2 qh192=$q2"
done

echo ""
echo "=== 5. Other cells: adapt tf1/flips (sanity: rescue only where shift hurts) ==="
for R in 21 82 120; do
  row="R=$R:"
  for L in 1 3 7 10 15 20 30; do
    t=$(field "$R" adapt "$L" tf1); fl=$(field "$R" adapt "$L" flips)
    row="$row L$L:$t/$fl"
  done
  echo "  $row"
done
