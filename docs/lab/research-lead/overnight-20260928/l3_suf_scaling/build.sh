#!/bin/sh
# build.sh -- L3-SUF-1-SCALING evaluator builds. Pure Zag; pinned znc only.
# Links the FROZEN learner sources (read-only, sha256-verified) with this
# worker's own scaling world builder (scale_world.zag) and driver
# (scale_main.zag, one (family,scale) per binary). The builder's src/ and
# the adversary's sealed worlds are NOT touched.
set -e
export PATH="$HOME/safebin"
echo "--- toolchain guard ---"
which znc
if which python3 2>/dev/null; then echo "FORBIDDEN: python3 in PATH"; exit 1; fi
if which python 2>/dev/null; then echo "FORBIDDEN: python in PATH"; exit 1; fi
echo "no forbidden interpreter in safebin PATH"
HERE=$(dirname "$0")
cd "$HERE"
FROZ=../l3_suf_intermediate/src
mkdir -p build
echo "--- frozen source sha256 (build-time record) ---"
sha256sum $FROZ/prelude.zag $FROZ/learner1.zag $FROZ/learner2.zag $FROZ/learner3.zag $FROZ/controls.zag $FROZ/driver.zag | tee build/frozen_src.sha256
for fam in 0 1; do
  for sc in 0 1 2 3 4 5; do
    sed -e "s/@@FAM@@/$fam/g" -e "s/@@SC@@/$sc/g" scale_main.zag > build/main_${fam}_${sc}.zag
    cat $FROZ/prelude.zag scale_world.zag $FROZ/learner1.zag $FROZ/learner2.zag $FROZ/learner3.zag $FROZ/controls.zag $FROZ/driver.zag build/main_${fam}_${sc}.zag > build/unit_${fam}_${sc}.zag
    znc build/unit_${fam}_${sc}.zag -o build/scale_${fam}_${sc} 2>build/build_${fam}_${sc}.log || { echo "BUILD FAILED fam=$fam sc=$sc"; grep -E "error" build/build_${fam}_${sc}.log | head -20; exit 1; }
    echo "build ok fam=$fam sc=$sc"
  done
done
sha256sum build/scale_*_* | tee build/bin.sha256
# determinism of the build itself: rebuild one unit, compare
cp build/scale_0_0 build/scale_0_0.a
cat $FROZ/prelude.zag scale_world.zag $FROZ/learner1.zag $FROZ/learner2.zag $FROZ/learner3.zag $FROZ/controls.zag $FROZ/driver.zag build/main_0_0.zag > build/unit_0_0b.zag
znc build/unit_0_0b.zag -o build/scale_0_0b 2>/dev/null
cmp build/scale_0_0.a build/scale_0_0b && echo "REBUILD IDENTICAL"
rm -f build/scale_0_0.a build/scale_0_0b build/unit_0_0b.zag
