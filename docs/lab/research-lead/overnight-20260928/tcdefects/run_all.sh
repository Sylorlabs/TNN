#!/bin/bash
# run_all.sh -- build, run and determinism-check every tcdefects reproducer.
#
# Shell is ORCHESTRATION ONLY (brief 10.x). Every computation lives in the .zag
# files. Every run goes through tnnwatch.sh with a hard wall-clock limit
# (brief 10.1), and nothing is left unattended.
#
# Expected shape of the result is documented in
# docs/ops/ZAG_TOOLCHAIN_DEFECTS.md. C5b_for_loop is EXPECTED TO FAIL TO
# COMPILE; that is the finding, not a harness error.
set -u
. /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh
W=/Users/Shared/micah/Documents/TNN/TNN/tools/tnnwatch.sh
D="$(cd "$(dirname "$0")" && pwd)"
cd "$D" || exit 2

EXPECT_COMPILE_FAIL="C5b_for_loop"

TOTAL=0; BAD=0
for src in *.zag; do
  n="${src%.zag}"
  TOTAL=$((TOTAL+1))
  printf '\n===== %s =====\n' "$n"
  if ! znc "$src" >"$D/.znc_out" 2>&1; then
    if [ "$n" = "$EXPECT_COMPILE_FAIL" ]; then
      echo "  COMPILE-FAIL (EXPECTED for $n): $(head -1 "$D/.znc_out")"
      continue
    fi
    echo "  *** UNEXPECTED COMPILE-FAIL: $(head -3 "$D/.znc_out" | tr '\n' ' ')"
    BAD=$((BAD+1))
    continue
  fi
  case "$(file -b "$D/$n" 2>/dev/null)" in
    *ELF*) echo "  *** INFRA-FAIL: ELF on darwin"; BAD=$((BAD+1)); continue;;
  esac
  H=""
  for i in 1 2 3; do
    $W reg "tc_${n}_r$i" 120 "$D/$n" >/dev/null 2>&1
    st=$(sed -n 's/^status=//p' "/Users/Shared/micah/Documents/TNN/.runs/tc_${n}_r$i.meta" 2>/dev/null)
    s=$(shasum -a 256 < "/Users/Shared/micah/Documents/TNN/.runs/tc_${n}_r$i.log" 2>/dev/null | cut -c1-12)
    H="$H $s"
    [ "$st" = "DONE" ] || { echo "  *** watchdog status=$st"; BAD=$((BAD+1)); }
  done
  u=$(printf '%s\n' $H | tr ' ' '\n' | sort -u | wc -l | tr -d ' ')
  if [ "$u" = "1" ]; then echo "  DETERMINISM PASS 3/3 ($H)"; else echo "  *** DETERMINISM FAIL ($u distinct) -- THIS IS A FINDING"; fi
  if grep -q ' FAIL' "/Users/Shared/micah/Documents/TNN/.runs/tc_${n}_r1.log" 2>/dev/null; then
    echo "  *** ASSERTION FAILURES:"; grep ' FAIL' "/Users/Shared/micah/Documents/TNN/.runs/tc_${n}_r1.log" | sed 's/^/      /'
  fi
done
rm -f "$D/.znc_out"
printf '\n===== SUMMARY: %d reproducers, %d unexpected problems =====\n' "$TOTAL" "$BAD"
exit 0
