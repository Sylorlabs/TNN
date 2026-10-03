#!/bin/bash
# F2 v6 build script (wave-20261002-0521pdt, lane F2). Pure Zag.
# Concatenates learner + world, compiles with the pinned znc via safebin PATH.
# Binaries and concatenation intermediates live in /tmp (ephemeral);
# sources and logs live in the lane dir.
# Usage: bash build.sh [sealed|regression|nc|all]   (run from ~/workspace/tnn-rsi)
set -e
export PATH="$HOME/safebin"
LANE="docs/lab/rsi/runs/wave-20261002-0521pdt/F2"
V4="docs/lab/rsi/runs/wave-20261001-2321pdt/F2V3"
V5BASE="docs/lab/rsi/runs/wave-20261002-0221pdt/F2/f2v5_learner.zag"
MODE="${1:-all}"
if [ "$MODE" = "sealed" ] || [ "$MODE" = "all" ]; then
  cat "$LANE/f2v6_learner.zag" "$LANE/sealed/f2v6_world_shift2.zag" > /tmp/f2v6_shift2.zag
  znc /tmp/f2v6_shift2.zag -o /tmp/f2v6_shift2
  echo "SEALED BUILD OK: /tmp/f2v6_shift2"
fi
if [ "$MODE" = "regression" ] || [ "$MODE" = "all" ]; then
  cat "$LANE/f2v6_learner.zag" "$V4/f2v4_world_aprime.zag" > /tmp/f2v6_reg_a.zag
  cat "$LANE/f2v6_learner.zag" "$V4/sealed/f2v4_world_c2prime.zag" > /tmp/f2v6_reg_c2.zag
  znc /tmp/f2v6_reg_a.zag -o /tmp/f2v6_reg_a
  znc /tmp/f2v6_reg_c2.zag -o /tmp/f2v6_reg_c2
  echo "REGRESSION BUILD OK: /tmp/f2v6_reg_a /tmp/f2v6_reg_c2"
fi
if [ "$MODE" = "nc" ] || [ "$MODE" = "all" ]; then
  # NC3: pristine v5-base (one-revision cap) on SHIFT2
  cat "$V5BASE" "$LANE/sealed/f2v6_world_shift2.zag" > /tmp/f2v6_nc3.zag
  znc /tmp/f2v6_nc3.zag -o /tmp/f2v6_nc3
  # NC4: v6 binary on SHIFT1 (single shift)
  cat "$LANE/f2v6_learner.zag" "$LANE/sealed/f2v6_world_shift1.zag" > /tmp/f2v6_shift1.zag
  znc /tmp/f2v6_shift1.zag -o /tmp/f2v6_shift1
  # NC5: v6 binary on OSC (alternating regimes)
  cat "$LANE/f2v6_learner.zag" "$LANE/sealed/f2v6_world_osc.zag" > /tmp/f2v6_osc.zag
  znc /tmp/f2v6_osc.zag -o /tmp/f2v6_osc
  # NC2: passive-replay baseline on SHIFT2 physics
  znc "$LANE/f2v6_nc2.zag" -o /tmp/f2v6_nc2
  echo "NC BUILD OK: /tmp/f2v6_nc3 /tmp/f2v6_shift1 /tmp/f2v6_osc /tmp/f2v6_nc2"
fi
