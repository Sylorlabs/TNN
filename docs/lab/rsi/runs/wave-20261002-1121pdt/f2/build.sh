#!/bin/bash
# F2 v6 sealed-eval rebuild (lane F2, wave-20261002-1121pdt).
# Rebuilds binaries from the FROZEN committed sources of wave-20261002-0521pdt
# (f2v6_learner.zag @50693d022; sealed worlds hash-verified against the
# prereg freeze record). No source is modified. Pure Zag, safebin PATH.
# Binaries and concatenation intermediates live in /tmp (ephemeral);
# sources and logs live in the lane dir.
# Usage: bash build.sh [sealed|nc|regression|all]
set -e
export PATH="$HOME/safebin"
D=~/workspace/tnn-rsi-work/wave-20261002-1121pdt/f2
SRC="$D/docs/lab/rsi/runs/wave-20261002-0521pdt/F2"
V4LEARNER_SRC="$D/docs/lab/rsi/runs/wave-20261002-0521pdt/F2"
# v4 sealed worlds live in the 2321pdt lane dir (read-only, inherited)
V4="docs/lab/rsi/runs/wave-20261001-2321pdt/F2V3"
V5BASE="$D/docs/lab/rsi/runs/wave-20261002-0221pdt/F2/f2v5_learner.zag"
MODE="${1:-all}"
cd "$D"
if [ "$MODE" = "sealed" ] || [ "$MODE" = "all" ]; then
  cat "$SRC/f2v6_learner.zag" "$SRC/sealed/f2v6_world_shift2.zag" > /tmp/f2v6_shift2.zag
  znc /tmp/f2v6_shift2.zag -o /tmp/f2v6_shift2
  echo "SEALED BUILD OK: /tmp/f2v6_shift2"
fi
if [ "$MODE" = "nc" ] || [ "$MODE" = "all" ]; then
  cat "$SRC/f2v6_learner.zag" "$SRC/sealed/f2v6_world_shift1.zag" > /tmp/f2v6_shift1.zag
  znc /tmp/f2v6_shift1.zag -o /tmp/f2v6_shift1
  cat "$SRC/f2v6_learner.zag" "$SRC/sealed/f2v6_world_osc.zag" > /tmp/f2v6_osc.zag
  znc /tmp/f2v6_osc.zag -o /tmp/f2v6_osc
  znc "$SRC/f2v6_nc2.zag" -o /tmp/f2v6_nc2
  echo "NC BUILD OK: /tmp/f2v6_shift1 /tmp/f2v6_osc /tmp/f2v6_nc2"
fi
if [ "$MODE" = "nc3" ] || [ "$MODE" = "all" ]; then
  cat "$V5BASE" "$SRC/sealed/f2v6_world_shift2.zag" > /tmp/f2v6_nc3.zag
  znc /tmp/f2v6_nc3.zag -o /tmp/f2v6_nc3
  echo "NC3 BUILD OK: /tmp/f2v6_nc3"
fi
if [ "$MODE" = "regression" ] || [ "$MODE" = "all" ]; then
  cat "$SRC/f2v6_learner.zag" "$V4/f2v4_world_aprime.zag" > /tmp/f2v6_reg_a.zag
  cat "$SRC/f2v6_learner.zag" "$V4/sealed/f2v4_world_c2prime.zag" > /tmp/f2v6_reg_c2.zag
  znc /tmp/f2v6_reg_a.zag -o /tmp/f2v6_reg_a
  znc /tmp/f2v6_reg_c2.zag -o /tmp/f2v6_reg_c2
  echo "REGRESSION BUILD OK: /tmp/f2v6_reg_a /tmp/f2v6_reg_c2"
fi
