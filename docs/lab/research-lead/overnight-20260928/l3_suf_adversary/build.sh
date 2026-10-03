#!/bin/sh
# build.sh -- L3-SUF-1 adversary evaluator build. Pure Zag; pinned znc only.
# Links the FROZEN learner sources (read-only, sha256-verified) with the
# sealed world builders (adv_world*.zag) and the sealed battery driver
# (adv_main.zag). The builder's src/ is NOT modified.
set -e
export PATH="$HOME/safebin"
HERE=$(dirname "$0")
cd "$HERE"
FROZ=../l3_suf_intermediate/src
mkdir -p build
echo "--- frozen source sha256 (build-time record) ---"
sha256sum $FROZ/prelude.zag $FROZ/learner1.zag $FROZ/learner2.zag $FROZ/learner3.zag $FROZ/controls.zag $FROZ/driver.zag | tee build/frozen_src.sha256
cat $FROZ/prelude.zag adv_world.zag adv_world2.zag adv_world3.zag $FROZ/learner1.zag $FROZ/learner2.zag $FROZ/learner3.zag $FROZ/controls.zag $FROZ/driver.zag adv_main.zag > build/adv_unit.zag
wc -l build/adv_unit.zag
znc build/adv_unit.zag -o build/adv_eval 2>build/adv_build.log || { echo "ADV BUILD FAILED"; grep -E "error" build/adv_build.log | head -20; exit 1; }
echo "build ok"
sha256sum build/adv_eval | tee build/bin.sha256
cp build/adv_eval build/adv_eval1 && znc build/adv_unit.zag -o build/adv_eval2 2>/dev/null
cmp build/adv_eval1 build/adv_eval2 && echo "REBUILD IDENTICAL"
rm -f build/adv_eval1 build/adv_eval2
