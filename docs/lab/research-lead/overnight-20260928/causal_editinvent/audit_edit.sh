#!/bin/sh
# audit_edit.sh -- source audit for CAUSAL-EDITINVENT (prereg 811fc06c9).
# Verifies the invented edit type (EXTEND-DELAY) is absent from source.
# Shell only. Exit 0 if all checks pass, 1 otherwise.
# Usage: sh audit_edit.sh <editinvent.zag>
f="$1"
if [ ! -r "$f" ]; then
  printf 'UNREADABLE: %s\n' "$f"
  exit 1
fi
fail=0

# A1: dmax init to 2; only store after init is in invent as dmax+1 (cur+1).
# Find all set32 to dmax_cell.
printf 'A1: dmax stores...\n'
stores=$(LC_ALL=C grep -n 'set32(dmax_cell,0' -- "$f")
printf '%s\n' "$stores"
n_stores=$(printf '%s\n' "$stores" | grep -c .)
if [ "$n_stores" -ne 2 ]; then
  printf 'A1-FAIL: expected 2 stores to dmax_cell (init + invent), found %s\n' "$n_stores"
  fail=1
fi
# The invent store must use cur+1, not a literal.
if ! LC_ALL=C grep -q 'set32(dmax_cell,0,nxt)' -- "$f"; then
  printf 'A1-FAIL: invent store not via computed nxt\n'
  fail=1
fi
if LC_ALL=C grep -q 'set32(dmax_cell,0,3)' -- "$f"; then
  printf 'A1-FAIL: literal 3 assigned to dmax\n'
  fail=1
fi
# Verify the invent store is inside fn invent (check surrounding lines).
if ! LC_ALL=C grep -B20 'set32(dmax_cell,0,nxt)' -- "$f" | LC_ALL=C grep -q 'fn invent'; then
  printf 'A1-FAIL: dmax store not inside fn invent\n'
  fail=1
fi

# A2: neighbors_dmax takes dmax param; no delay literal 3 in its body.
# Extract neighbors_dmax function body by line numbers (robust).
printf 'A2: neighbors_dmax body check...\n'
start_n=$(LC_ALL=C grep -n '^fn neighbors_dmax' -- "$f" | cut -d: -f1 | head -1)
end_n=$(LC_ALL=C grep -n '^fn in_table' -- "$f" | cut -d: -f1 | head -1)
body=$(sed -n "${start_n},$((end_n-1))p" -- "$f")
# Check for literal 3 in delay-value contexts. We forbid ', 3)' or ',3)'
# (a literal 3 as a set32 value or function arg) within the body.
# This excludes 'i32', 'n*32', 'b+20' etc. which contain '3' but are not literals.
code3=$(printf '%s\n' "$body" | LC_ALL=C grep -cE ', ?3\)')
if [ "$code3" -ne 0 ]; then
  printf 'A2-FAIL: literal 3 as value found in neighbors_dmax body (%s occurrences)\n' "$code3"
  fail=1
fi
# Verify dmax is a parameter.
if ! printf '%s\n' "$body" | head -1 | LC_ALL=C grep -q 'dmax:i32'; then
  printf 'A2-FAIL: neighbors_dmax missing dmax parameter\n'
  fail=1
fi

# A3: no pre-built [(X->Y,3)]; no delay3 function names (excluding diag_ whitelisted).
printf 'A3: pre-built delay-3 check...\n'
if LC_ALL=C grep -qi 'add_delay3\|extend_delay' -- "$f"; then
  printf 'A3-FAIL: forbidden function/name pattern found\n'
  fail=1
fi
# 'delay3' as a standalone name (not part of diag_count_delay3).
if LC_ALL=C grep -q '[^_]delay3' -- "$f"; then
  printf 'A3-FAIL: standalone delay3 name found\n'
  fail=1
fi
# g_set constructing a (0,1,3) rule: g_set(..., 1, 0,1,3, ...)
if LC_ALL=C grep -q 'g_set(.*0,1,3' -- "$f"; then
  printf 'A3-FAIL: pre-built (X->Y,3) via g_set\n'
  fail=1
fi

# A4: diagnose tests both max_rules and delay_max; binding by counts.
printf 'A4: diagnose coverage...\n'
if ! LC_ALL=C grep -q 'fn diagnose' -- "$f"; then
  printf 'A4-FAIL: fn diagnose missing\n'
  fail=1
fi
if ! LC_ALL=C grep -q 'diag_count_maxrules3' -- "$f"; then
  printf 'A4-FAIL: max_rules enumeration missing\n'
  fail=1
fi
if ! LC_ALL=C grep -q 'diag_count_delay3' -- "$f"; then
  printf 'A4-FAIL: delay enumeration missing\n'
  fail=1
fi
# No branch on family ID selecting delay (check diagnose does not reference R3/case_id/phase).
d_start=$(LC_ALL=C grep -n '^fn diagnose' -- "$f" | cut -d: -f1 | head -1)
d_end=$(LC_ALL=C grep -n '^fn invent' -- "$f" | cut -d: -f1 | head -1)
diagbody=$(sed -n "${d_start},$((d_end-1))p" -- "$f")
if printf '%s\n' "$diagbody" | LC_ALL=C grep -qi 'R3\|case_id\|phase'; then
  printf 'A4-FAIL: diagnose references family/case/phase\n'
  fail=1
fi

# A5: prove_insufficient called before diagnose in main.
printf 'A5: call order...\n'
mainbody=$(awk '/^fn main/,0 {print}' "$f")
line_prove=$(printf '%s\n' "$mainbody" | LC_ALL=C grep -n 'prove_insufficient(E3)' | head -1 | cut -d: -f1)
line_diag=$(printf '%s\n' "$mainbody" | LC_ALL=C grep -n 'diagnose(E3)' | head -1 | cut -d: -f1)
if [ -z "$line_prove" ] || [ -z "$line_diag" ]; then
  printf 'A5-FAIL: missing prove_insufficient or diagnose call in main\n'
  fail=1
elif [ "$line_prove" -ge "$line_diag" ]; then
  printf 'A5-FAIL: prove_insufficient not before diagnose\n'
  fail=1
fi

if [ "$fail" -eq 0 ]; then
  printf 'AUDIT-PASS: invented edit type absent from source (A1-A5).\n'
else
  printf 'AUDIT-FAIL.\n'
fi
exit $fail
