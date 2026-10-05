#!/usr/bin/env bash
# tnn_bars_lint.sh -- enforce STANDING RULE R3.
#
# R3: never trust a precomputed verdict emitted by the experiment.
# A bar must be derived from a comparison against a measured quantity,
# never baked in as a constant.
#
# TWO ANTI-PATTERNS, both real, both observed in this program:
#
#  A. Hardcoded verdict in the label string.
#         c=o_app(ob,c,"BAR K7_random_ok=1");     <-- FAKE
#     The number lives inside the string literal. Nothing was compared.
#     This is the exact C1471 defect that concealed a real evaluator bug.
#
#  B. Verdict-named variable assigned only bare literals.
#         let random_ok:i32=1; ... print random_ok   <-- FAKE
#
# CORRECT shape: append a label ending in '=' and interpolate a value that
# was itself computed by a comparison:
#         c=o_app(ob,c,"BAR K7_random_ok="); c=o_i64(ob,c,k7 as i64);
#
# Usage: tools/tnn_bars_lint.sh <dir-or-file> [...]
# Exit 0 = clean, 1 = violations.

set -uo pipefail

VERDICT_RE='(ok|valid|pass|clean|uniform|sound|verified|good)'

violations=0
checked=0

scan() {
  local f="$1"
  [ -f "$f" ] || return 0
  case "$f" in *.zag) ;; *) return 0 ;; esac

  # ---- Pattern A: digit baked into a BAR/verdict label string ----
  local hits
  hits=$(grep -nE "o_app\([^,]+,[^,]+,\"[^\"]*(BAR|_bar)[^\"]*${VERDICT_RE}[^\"]*=[0-9]" "$f" 2>/dev/null)
  if [ -n "$hits" ]; then
    while IFS= read -r line; do
      [ -z "$line" ] && continue
      echo "R3-A VIOLATION ${f}:${line%%:*}: verdict digit hardcoded in label string"
      echo "    ${line#* }"
      echo "    -> print the label with '=' and interpolate a compared value."
      violations=$((violations+1))
    done <<< "$hits"
  fi

  # Any BAR label with a baked digit at all (including non-verdict bars):
  # constant claims such as "L3=0" still bypass the measurement path.
  local anyhit
  anyhit=$(grep -nE "o_app\([^,]+,[^,]+,\"(BAR|_bar)[^\"]*=[0-9]" "$f" 2>/dev/null)
  if [ -n "$anyhit" ]; then
    while IFS= read -r line; do
      [ -z "$line" ] && continue
      # skip if already reported by pattern A
      if ! grep -qE "${VERDICT_RE}" <<< "${line#* }"; then
        echo "R3-note ${f}:${line%%:*}: BAR constant in label string (verify this is intended)"
        echo "    ${line#* }"
      fi
    done <<< "$anyhit"
  fi

  # ---- Pattern B: verdict-named variable assigned only bare literals ----
  local names
  names=$(grep -oE "[A-Za-z_][A-Za-z0-9_]*${VERDICT_RE}[A-Za-z0-9_]*" "$f" 2>/dev/null | sort -u)
  [ -z "$names" ] && return 0

  while IFS= read -r name; do
    [ -z "$name" ] && continue
    checked=$((checked+1))
    local derived
    derived=$(grep -E "(let[[:space:]]+${name}[[:space:]]*:|set32\([^)]*,[[:space:]]*${name}[[:space:]]*,)" "$f" 2>/dev/null \
             | grep -E '(<=|>=|==|!=|<|>)' | head -1)
    if [ -z "$derived" ]; then
      local literal
      literal=$(grep -E "(let[[:space:]]+${name}[[:space:]]*:i32=(0|1);|set32\([^)]*,[[:space:]]*${name}[[:space:]]*,[[:space:]]*(0|1)\);)" "$f" 2>/dev/null | head -1)
      if [ -n "$literal" ]; then
        echo "R3-B VIOLATION ${f}: verdict-named bar '${name}' assigned only a bare literal."
        echo "    ${literal}"
        violations=$((violations+1))
      fi
    fi
  done <<< "$names"
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

echo "tnn_bars_lint: pattern-B identifiers checked=${checked}"
if [ "$violations" -gt 0 ]; then
  echo "tnn_bars_lint: RESULT=FAIL violations=${violations}"
  exit 1
fi
echo "tnn_bars_lint: RESULT=CLEAN"
exit 0