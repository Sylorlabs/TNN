#!/bin/bash
# compare_refreeze.sh - compare clean re-freeze runs against d5984f313.
# Compares scores.jsonl and replies.jsonl (byte-identical per prereg K-rule).
# costs.txt excluded (wall_ms timing). driver.log excluded.
# Zero Python. Shell + sha256sum + git only.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
MINE="$HERE/runs"
REF="d5984f313:docs/lab/research-lead/overnight-20260928/c1_zagdriver/runs/runs"
cd ~/workspace/tnn-rsi || exit 1

pass=0; fail=0; failed_list=""
for w in w0 w1 w2 h0 h1; do
  for r in 1 2 3; do
    for n in c1 mem freq rand; do
      dir="${n}_${w}_r${r}"
      for f in scores.jsonl replies.jsonl; do
        a="$MINE/$dir/$f"
        if [ ! -f "$a" ]; then
          echo "MISSING $dir/$f"; fail=$((fail+1)); failed_list="$failed_list $dir/$f(missing)"; continue
        fi
        ha=$(sha256sum "$a" | cut -d' ' -f1)
        hb=$(git show "$REF/$dir/$f" 2>/dev/null | sha256sum | cut -d' ' -f1)
        if [ "$ha" = "$hb" ]; then
          pass=$((pass+1))
        else
          echo "DIFFER $dir/$f"; fail=$((fail+1)); failed_list="$failed_list $dir/$f"
        fi
      done
    done
  done
done
echo "COMPARE: pass=$pass fail=$fail (expect pass=240 fail=0)"
[ -n "$failed_list" ] && echo "FAILED:$failed_list"
[ "$fail" -eq 0 ] && [ "$pass" -eq 240 ] && echo "REFREEZE-BYTE-IDENTICAL"
