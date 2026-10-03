#!/bin/sh
# build.sh -- L3-SUF-1 builder build. Pure Zag; pinned znc only; safebin PATH.
set -e
export PATH="$HOME/safebin"
HERE=$(dirname "$0")
cd "$HERE"
mkdir -p ../build
cat prelude.zag world.zag learner1.zag learner2.zag learner3.zag controls.zag driver.zag main.zag > ../build/suf_unit.zag
znc ../build/suf_unit.zag -o ../build/suf 2>../build/suf_build.log || { echo "SUF BUILD FAILED"; grep -E "error" ../build/suf_build.log | head -20; exit 1; }
echo "build ok"
sha256sum ../build/suf | tee ../build/bin.sha256
cp ../build/suf ../build/suf1 && znc ../build/suf_unit.zag -o ../build/suf2 2>/dev/null
cmp ../build/suf1 ../build/suf2 && echo "REBUILD IDENTICAL"
rm -f ../build/suf1 ../build/suf2
