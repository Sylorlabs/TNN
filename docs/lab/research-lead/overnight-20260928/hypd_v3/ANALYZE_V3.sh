#!/bin/bash
# ANALYZE_V3.sh -- Hypothesis D v3: extract verdicts from a raw log.
# Pure shell. No Python anywhere.
# Usage: ANALYZE_V3.sh <raw_log>
set -u
F="$1"
echo "=== FILE $F ==="
head -4 "$F"
echo "--- tasks ---"
grep -E "^(TASK|VERDICT|EVALS|BEST_SCORE|BEST_PROG|HIDDEN|SEED_IN|CARRY_OUT|CARRY_DROPPED_INVALID|OCC_NICHES|CARRY_BLOCK_CHECK|SOLVE) " "$F" | head -60
echo "--- T3 solution program (if SOLVE) ---"
grep -A2 "^TASK 3 " "$F" | grep "^SOLVE " | head -3
echo "--- 17570 I-lines (native generation evidence) ---"
grep "^I " "$F" | grep " niche=17570" | head -5
echo "--- prefix lines ---"
grep -E "^(PREFIX_EVAL|PREFIX_INSERT) " "$F" | head -5
echo "--- T3 CARRY_BLOCK_CHECK ---"
grep "^CARRY_BLOCK_CHECK" "$F"
echo "--- parent_src of T3 SOLVE (0=archive 1=seed) ---"
grep "^SOLVE " "$F" | tail -2
