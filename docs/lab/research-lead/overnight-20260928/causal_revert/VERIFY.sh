#!/bin/sh
# VERIFY.sh -- check every frozen prediction line from PREREG_CAUSAL_REVERT.md
# (as corrected by PREREG_AMENDMENT_1.md) against RUN1.txt.
# Usage: ./VERIFY.sh   (run from the causal_revert/ directory; RUN.sh first)
set -e
F=RUN1.txt
if [ ! -f "$F" ]; then
  echo "VERIFY-FAIL: $F not found; run ./RUN.sh first" >&2
  exit 1
fi
PASS=0
FAIL=0
chk() {
  # chk <description> <grep-pattern>
  if grep -q "$2" "$F"; then
    PASS=$((PASS+1))
  else
    echo "MISSING: $1  (pattern: $2)"
    FAIL=$((FAIL+1))
  fi
}

# ---- R1 REVISE ----
chk "R1 REVISE P0 construct" "^R1 REVISE P0 CONSTRUCT graphs=9 classes=2$"
chk "R1 REVISE P0 round target" "^R1 REVISE P0 ROUND 1 TARGET V\*=2 t\*=3 PLAN \[S,W,W,W,O(2)\] EXEC real=0 ELIM \[(0,1,1),(1,2,2)\] sig=(1,3)$"
chk "R1 REVISE P0 resolved" "^R1 REVISE P0 RESOLVED winner=\[(0,1,1)\] rounds=1$"
chk "R1 REVISE P1 revise k=2" "^R1 REVISE P1 REVISE k=2 classes=2$"
chk "R1 REVISE P1 round target" "^R1 REVISE P1 ROUND 1 TARGET V\*=2 t\*=1 PLAN \[S,W,O(2)\] EXEC real=1 ELIM \[(0,1,2),(0,2,2)\] sig=(2,2)$"
chk "R1 REVISE P1 resolved" "^R1 REVISE P1 RESOLVED winner=\[(0,1,2),(0,2,1)\] rounds=1$"
chk "R1 REVISE P2 revise k=2" "^R1 REVISE P2 REVISE k=2 classes=1$"
chk "R1 REVISE P2 resolved" "^R1 REVISE P2 RESOLVED winner=\[(0,1,1)\] rounds=0$"
chk "R1 REVISE summary" "^SUMMARY R1 REVISE ok=3/3 correct=3/3 rounds_total=2 W2eqW0=1$"

# ---- R1 REBUILD ----
chk "R1 REBUILD P0 construct" "^R1 REBUILD P0 CONSTRUCT graphs=9 classes=2$"
chk "R1 REBUILD P0 resolved" "^R1 REBUILD P0 RESOLVED winner=\[(0,1,1)\] rounds=1$"
chk "R1 REBUILD P1 construct" "^R1 REBUILD P1 CONSTRUCT graphs=3 classes=2$"
chk "R1 REBUILD P1 resolved" "^R1 REBUILD P1 RESOLVED winner=\[(0,1,2),(0,2,1)\] rounds=1$"
chk "R1 REBUILD P2 construct" "^R1 REBUILD P2 CONSTRUCT graphs=9 classes=2$"
chk "R1 REBUILD P2 resolved" "^R1 REBUILD P2 RESOLVED winner=\[(0,1,1)\] rounds=1$"
chk "R1 REBUILD summary" "^SUMMARY R1 REBUILD ok=3/3 correct=3/3 rounds_total=3 W2eqW0=1$"

# ---- R1 FROZEN ----
chk "R1 FROZEN P0 resolved" "^R1 FROZEN P0 RESOLVED winner=\[(0,1,1)\] rounds=1$"
chk "R1 FROZEN P1 keep" "^R1 FROZEN P1 FROZEN-KEEP$"
chk "R1 FROZEN P1 inconsistent" "^R1 FROZEN P1 WINNER-INCONSISTENT$"
chk "R1 FROZEN P2 keep" "^R1 FROZEN P2 FROZEN-KEEP$"
chk "R1 FROZEN P2 resolved" "^R1 FROZEN P2 RESOLVED winner=\[(0,1,1)\] rounds=0$"
chk "R1 FROZEN summary" "^SUMMARY R1 FROZEN ok=3/3 correct=2/3 rounds_total=1 W2eqW0=1$"

# ---- R2 REVISE ----
chk "R2 REVISE P0 resolved" "^R2 REVISE P0 RESOLVED winner=\[(0,1,1)\] rounds=1$"
chk "R2 REVISE P1 revise k=1" "^R2 REVISE P1 REVISE k=1 classes=1$"
chk "R2 REVISE P1 resolved" "^R2 REVISE P1 RESOLVED winner=\[(0,1,2)\] rounds=0$"
chk "R2 REVISE P2 keep" "^R2 REVISE P2 KEEP$"
chk "R2 REVISE P2 resolved" "^R2 REVISE P2 RESOLVED winner=\[(0,1,2)\] rounds=0$"
chk "R2 REVISE summary" "^SUMMARY R2 REVISE ok=3/3 correct=3/3 rounds_total=1 W2eqW0=0 W2eqW1=1 W2neqW0=1$"

# ---- R2 REBUILD (amended predictions) ----
chk "R2 REBUILD P0 resolved" "^R2 REBUILD P0 RESOLVED winner=\[(0,1,1)\] rounds=1$"
chk "R2 REBUILD P1 construct" "^R2 REBUILD P1 CONSTRUCT graphs=9 classes=3$"
chk "R2 REBUILD P1 round1 elim" "ELIM \[(0,1,2),(1,2,1)\] sig=(2,3)"
chk "R2 REBUILD P1 round2 elim" "ELIM \[(0,1,2),(1,2,2)\] sig=(2,4)"
chk "R2 REBUILD P1 resolved" "^R2 REBUILD P1 RESOLVED winner=\[(0,1,2)\] rounds=2$"
chk "R2 REBUILD P2 construct" "^R2 REBUILD P2 CONSTRUCT graphs=9 classes=3$"
chk "R2 REBUILD P2 resolved" "^R2 REBUILD P2 RESOLVED winner=\[(0,1,2)\] rounds=2$"
chk "R2 REBUILD summary" "^SUMMARY R2 REBUILD ok=3/3 correct=3/3 rounds_total=5 W2eqW0=0 W2eqW1=1 W2neqW0=1$"

# ---- R2 FROZEN ----
chk "R2 FROZEN P0 resolved" "^R2 FROZEN P0 RESOLVED winner=\[(0,1,1)\] rounds=1$"
chk "R2 FROZEN P1 inconsistent" "^R2 FROZEN P1 WINNER-INCONSISTENT$"
chk "R2 FROZEN P2 inconsistent" "^R2 FROZEN P2 WINNER-INCONSISTENT$"
chk "R2 FROZEN summary" "^SUMMARY R2 FROZEN ok=3/3 correct=1/3 rounds_total=1 W2eqW0=1 W2eqW1=1 W2neqW0=0$"

# ---- termination ----
chk "done marker" "^CAUSAL-REVERT-DONE$"

echo "VERIFY: PASS=$PASS FAIL=$FAIL"
if [ "$FAIL" -ne 0 ]; then
  echo "VERIFY-FAIL" >&2
  exit 1
fi
echo "VERIFY-OK all frozen predictions match"
