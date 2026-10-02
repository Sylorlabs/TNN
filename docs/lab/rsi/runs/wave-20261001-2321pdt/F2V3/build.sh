#!/bin/bash
# F2 v4 build script (wave-20261001-2321pdt, lane F2V3). Pure Zag.
# Concatenates learner + world, compiles with the pinned znc via safebin PATH.
# Binaries and concatenation intermediates live in /tmp (ephemeral);
# sources and logs live in the lane dir.
# Usage: bash build.sh [sealed|regression|all]   (run from ~/workspace/tnn-rsi)
set -e
export PATH="$HOME/safebin"
LANE="docs/lab/rsi/runs/wave-20261001-2321pdt/F2V3"
OLD="docs/lab/rsi/runs/wave-20261001-2021pdt/F2v3"
MODE="${1:-all}"
if [ "$MODE" = "sealed" ] || [ "$MODE" = "all" ]; then
  cat "$LANE/f2v4_learner.zag" "$LANE/f2v4_world_aprime.zag" > /tmp/f2v4_a.zag
  cat "$LANE/f2v4_learner.zag" "$LANE/sealed/f2v4_world_c2prime.zag" > /tmp/f2v4_c2.zag
  znc /tmp/f2v4_a.zag -o /tmp/f2v4_a
  znc /tmp/f2v4_c2.zag -o /tmp/f2v4_c2
  echo "SEALED BUILD OK: /tmp/f2v4_a /tmp/f2v4_c2"
fi
if [ "$MODE" = "regression" ] || [ "$MODE" = "all" ]; then
  # 2021pdt worlds are REGRESSION ONLY (retired as test worlds).
  cat "$LANE/f2v4_learner.zag" "$OLD/f2v3_world_a.zag" > /tmp/f2v4_reg_a.zag
  cat "$LANE/f2v4_learner.zag" "$OLD/sealed/f2v3_world_cprime.zag" > /tmp/f2v4_reg_c.zag
  znc /tmp/f2v4_reg_a.zag -o /tmp/f2v4_reg_a
  znc /tmp/f2v4_reg_c.zag -o /tmp/f2v4_reg_c
  echo "REGRESSION BUILD OK: /tmp/f2v4_reg_a /tmp/f2v4_reg_c"
fi
