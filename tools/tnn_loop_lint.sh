#!/usr/bin/env bash
# tnn_loop_lint.sh -- guard against the defect that cost C1571 the most.
#
# DEFECT (C1571): two `while(cond){ ... }` logging loops had no increment on
# the loop variable. The loop never terminated, the output cursor grew past
# the output buffer, and _zag_print(ob[0..c]) then read out of bounds ->
# SEGFAULT with zero output. The segfault MOVED whenever unrelated code
# changed layout, so it was indistinguishable from memory corruption.
#
# A missing increment must be caught statically, not by segfault.
#
# Method: for each while-loop, extract the loop variable from the condition,
# then require that the body either returns, breaks, or mutates THAT variable.
# Other variables changing does not count.
#
# Usage: tools/tnn_loop_lint.sh <dir-or-file> [...]
# Exit 0 clean, 1 suspected non-advancing loop.

set -uo pipefail

violations=0

scan() {
  local f="$1"
  [ -f "$f" ] || return 0
  case "$f" in *.zag) ;; *) return 0 ;; esac

  local out
  out=$(awk -v FILE="$f" '
    { line[NR] = $0 }
    END {
      n = NR
      i = 1
      while (i <= n) {
        if (line[i] ~ /while[ \t]*\(/) {
          start = i
          # --- loop variable from the condition ---
          cond = line[i]
          p = index(cond, "while")
          if (p > 0) {
            rest = substr(cond, p)
            q = index(rest, "(")
            if (q > 0) {
              rest2 = substr(rest, q + 1)
              r = index(rest2, ")")
              if (r > 0) condtxt = substr(rest2, 1, r - 1)
            }
          }
          # first identifier in the condition that is followed by a comparison
          var = ""
          if (match(condtxt, /[A-Za-z_][A-Za-z0-9_]*/)) {
            cand = substr(condtxt, RSTART, RLENGTH)
            after = substr(condtxt, RSTART + RLENGTH)
            if (after ~ /^[ \t]*(<|>|==|!=|<=|>=)/) var = cand
          }
          # --- brace-matched body, INCLUDING the while line ---
          depth = 0
          j = i
          body = ""
          while (j <= n) {
            l = line[j]
            o = gsub(/\{/, "{", l)
            cl = gsub(/\}/, "}", l)
            depth += o - cl
            body = body " " l
            if (o > 0 && depth <= 0) break
            j++
          }
          advances = 0
          why = ""
          if (body ~ /(^|[^A-Za-z0-9_])return([^A-Za-z0-9_]|$)/) { advances = 1; why = "return" }
          if (body ~ /(^|[^A-Za-z0-9_])break([^A-Za-z0-9_]|$)/)  { advances = 1; why = "break" }
          if (var != "") {
            # var = ...   (but not var == / var != / var <= / var >=)
            if (body ~ ("(^|[^A-Za-z0-9_])" var "[ \t]*=[^=]")) { advances = 1; why = "assign " var }
            # var + 1 / var++ / var += 1
            if (body ~ ("(^|[^A-Za-z0-9_])" var "[ \t]*\\+[ \t]*1")) { advances = 1; why = "inc " var }
            if (body ~ ("\\+\\+" var)) { advances = 1; why = "inc++ " var }
            if (body ~ ("(^|[^A-Za-z0-9_])" var "[ \t]*-[ \t]*1")) { advances = 1; why = "dec " var }
            if (body ~ (var "\\+\\+")) { advances = 1; why = "inc++ " var }
            if (body ~ ("(^|[^A-Za-z0-9_])" var "[ \t]*-[ \t]*-[ \t]*")) { advances = 1; why = "dec-- " var }
          }
          if (!advances) {
            printf("LOOP-STALL %s:%d var=[%s]\n", FILE, start, var)
            printf("    %s\n", line[start])
            printf("    body has no return/break and no mutation of [%s]\n", var)
          }
          i = j + 1
        } else {
          i++
        }
      }
    }
  ' "$f")

  if [ -n "$out" ]; then
    echo "$out"
    local cnt
    cnt=$(echo "$out" | grep -c '^LOOP-STALL' || true)
    violations=$((violations + cnt))
  fi
}

targets=("$@")
if [ ${#targets[@]} -eq 0 ]; then targets=("."); fi

for t in "${targets[@]}"; do
  if [ -d "$t" ]; then
    while IFS= read -r f; do scan "$f"; done < <(find "$t" -name '*.zag' -type f)
  else
    scan "$t"
  fi
done

if [ "$violations" -gt 0 ]; then
  echo "tnn_loop_lint: RESULT=FAIL suspected_non_advancing_loops=${violations}"
  exit 1
fi
echo "tnn_loop_lint: RESULT=CLEAN"
exit 0