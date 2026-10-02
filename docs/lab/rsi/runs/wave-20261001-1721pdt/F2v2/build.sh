#!/bin/bash
# F2 v2 build script (wave-20261001-1721pdt, lane F2v2). Pure Zag.
# Concatenates learner + world, compiles with the pinned znc via safebin PATH.
# Usage: bash build.sh   (run from ~/workspace/tnn-rsi)
set -e
export PATH="$HOME/safebin"
LANE="docs/lab/rsi/runs/wave-20261001-1721pdt/F2v2"
cat "$LANE/f2v2_learner.zag" "$LANE/f2v2_world_a.zag" > /tmp/f2v2_a.zag
cat "$LANE/f2v2_learner.zag" "$LANE/f2v2_world_c.zag" > /tmp/f2v2_c.zag
znc /tmp/f2v2_a.zag -o /tmp/f2v2_a
znc /tmp/f2v2_c.zag -o /tmp/f2v2_c
echo "BUILD OK: /tmp/f2v2_a /tmp/f2v2_c"
