#!/bin/sh
# build.sh -- L3-INR implementation build. Pure Zag; pinned znc only.
# Concatenates sources (single-file compilation units), compiles learner and
# world binaries, then verifies deterministic rebuild (byte-identical sha256).
set -e
export PATH="$HOME/safebin"
HERE=$(dirname "$0")
cd "$HERE"
mkdir -p ../build
cat prelude.zag graph.zag state.zag learner.zag > ../build/build_learner.zag
cat prelude.zag world.zag > ../build/build_world.zag
cat prelude.zag ../tools/spearman.zag > ../build/build_sp.zag
znc ../build/build_learner.zag -o ../build/learner_bin 2>../build/learner_build.log || { echo "LEARNER BUILD FAILED"; tail -5 ../build/learner_build.log; exit 1; }
znc ../build/build_world.zag -o ../build/world_bin 2>../build/world_build.log || { echo "WORLD BUILD FAILED"; tail -5 ../build/world_build.log; exit 1; }
znc ../build/build_sp.zag -o ../build/spearman 2>../build/sp_build.log || { echo "SPEARMAN BUILD FAILED"; tail -5 ../build/sp_build.log; exit 1; }
echo "build ok"
sha256sum ../build/learner_bin ../build/world_bin | tee ../build/bin.sha256
# deterministic rebuild check (in build dir; /tmp may be full on shared workers)
cp ../build/learner_bin ../build/lr1 && cp ../build/world_bin ../build/wr1
znc ../build/build_learner.zag -o ../build/lr2 2>/dev/null
znc ../build/build_world.zag -o ../build/wr2 2>/dev/null
cmp ../build/lr1 ../build/lr2 && cmp ../build/wr1 ../build/wr2 && echo "REBUILD IDENTICAL"
rm -f ../build/lr1 ../build/lr2 ../build/wr1 ../build/wr2
