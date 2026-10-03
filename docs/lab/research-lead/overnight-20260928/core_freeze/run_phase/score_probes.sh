#!/bin/sh
# Score QUERY probes: compare ANSWER lines in binary output to QUERY expected values.
# Usage: score_probes.sh <world.txt> <binary_stdout.txt>
# Output: lines "OK s r expected got" / "MISS s r expected got", then "SCORE n_correct n_total".

set -u
WORLD="$1"; OUT="$2"

# Build expected table: for each QUERY line, "s r expected".
grep '^QUERY' "$WORLD" | awk '{print $2, $3, $4}' > /tmp/score_exp.$$
# Build actual table: for each ANSWER line, "s r got".
grep '^ANSWER' "$OUT" | awk '{print $2, $3, $4}' > /tmp/score_got.$$

CORRECT=0; TOTAL=0
# Join on (s,r): for each expected, find the matching actual (first match in order).
# We walk both files in lockstep since output order matches event order.
paste -d'|' /tmp/score_exp.$$ /tmp/score_got.$$ | while IFS='|' read -r exp got; do
  es=$(echo "$exp" | awk '{print $1}'); er=$(echo "$exp" | awk '{print $2}'); ee=$(echo "$exp" | awk '{print $3}')
  gs=$(echo "$got" | awk '{print $1}'); gr=$(echo "$got" | awk '{print $2}'); gv=$(echo "$got" | awk '{print $3}')
  if [ "$es" = "$gs" ] && [ "$er" = "$gr" ]; then
    if [ "$ee" = "$gv" ]; then
      echo "OK $es $er expected=$ee got=$gv"
    else
      echo "MISS $es $er expected=$ee got=$gv"
    fi
  else
    echo "ORDER-MISMATCH exp=($es $er) got=($gs $gr)"
  fi
done > /tmp/score_lines.$$

CORRECT=$(grep -c '^OK' /tmp/score_lines.$$)
TOTAL=$(wc -l < /tmp/score_lines.$$)
cat /tmp/score_lines.$$
echo "SCORE $CORRECT $TOTAL"
rm -f /tmp/score_exp.$$ /tmp/score_got.$$ /tmp/score_lines.$$
