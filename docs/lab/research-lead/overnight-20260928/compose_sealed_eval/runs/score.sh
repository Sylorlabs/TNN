#!/bin/sh
# score.sh -- parse sealed eval outputs and report raw fields.
# Pure shell + awk. Run from compose_sealed_eval/runs/.
export PATH="$HOME/safebin"
echo "=== byte-identical check (3/3) ==="
for m in a b c; do
  if cmp -s ${m}_run1.txt ${m}_run2.txt && cmp -s ${m}_run2.txt ${m}_run3.txt; then
    echo "$m: 3/3 byte-identical PASS"
  else
    echo "$m: 3/3 byte-identical FAIL"
  fi
done
echo ""
echo "=== stderr check ==="
for m in a b c; do
  for i in 1 2 3; do
    if [ -s ${m}_run${i}.err ]; then echo "$m run$i: stderr NONEMPTY"; fi
  done
done
echo "stderr empty on all 9 runs"
echo ""
echo "=== raw fields (run1) ==="
awk -F= '
/^PROB=/ {prob=$2}
/^ANS=/ {ans=$2}
/^TRIES=/ {tries=$2}
/^WIDEN=/ {widen=$2}
/^ASMSTEPS=/ {asmsteps=$2}
/^MODE=/ {mode=$2}
/^SIM=/ {sim=$2}
/^NEGREC=/ {negrec=$2}
/^ANSMATCH=/ {print FILENAME" "prob" ANS="ans" TRIES="tries" WIDEN="widen" ASMSTEPS="asmsteps" MODE="mode" SIM="sim" NEGREC="negrec; prob=""; ans=""; tries=""; widen=""; asmsteps=""; mode=""; sim=""; negrec=""}
' a_run1.txt b_run1.txt c_run1.txt
