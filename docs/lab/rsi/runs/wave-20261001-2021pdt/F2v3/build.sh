#!/bin/bash
# F2 v3 build script (wave-20261001-2021pdt, lane F2v3). Pure Zag.
# Concatenates learner + world, compiles with the pinned znc via safebin PATH.
# Binaries and concatenation intermediates live in /tmp (ephemeral);
# sources and logs live in the lane dir.
# Usage: bash build.sh   (run from ~/workspace/tnn-rsi)
set -e
export PATH="$HOME/safebin"
LANE="docs/lab/rsi/runs/wave-20261001-2021pdt/F2v3"
cat "$LANE/f2v3_learner.zag" "$LANE/f2v3_world_a.zag" > /tmp/f2v3_a.zag
cat "$LANE/f2v3_learner.zag" "$LANE/f2v3_world_cdev1.zag" > /tmp/f2v3_cdev1.zag
cat "$LANE/f2v3_learner.zag" "$LANE/f2v3_world_cdev2.zag" > /tmp/f2v3_cdev2.zag
# NC3 ablation: frozen v2 learner (no DPDS) against the dev worlds
V2="docs/lab/rsi/runs/wave-20261001-1721pdt/F2v2"
cat "$V2/f2v2_learner.zag" "$LANE/f2v3_world_cdev1.zag" > /tmp/f2v3_nc3.zag
cat "$V2/f2v2_learner.zag" "$LANE/f2v3_world_cdev2.zag" > /tmp/f2v3_nc3b.zag
znc /tmp/f2v3_a.zag -o /tmp/f2v3_a
znc /tmp/f2v3_cdev1.zag -o /tmp/f2v3_cdev1
znc /tmp/f2v3_cdev2.zag -o /tmp/f2v3_cdev2
znc /tmp/f2v3_nc3.zag -o /tmp/f2v3_nc3
znc /tmp/f2v3_nc3b.zag -o /tmp/f2v3_nc3b
echo "BUILD OK: /tmp/f2v3_a /tmp/f2v3_cdev1 /tmp/f2v3_cdev2 /tmp/f2v3_nc3 /tmp/f2v3_nc3b"
