#!/bin/sh
# build2.sh -- L3-RX-K10 build. Pure Zag; pinned znc only; safebin PATH.
# Rebuilds the FROZEN learner (digest must match CODEFREEZE) and this
# lane's own harness programs. Shell only for plumbing + sha256.
set -e
export PATH="$HOME/safebin"
HERE=$(dirname "$0")
cd "$HERE"
mkdir -p ../build
# frozen learner (system under test; never modified)
cat ../build/frozen_src/pre.zag ../build/frozen_src/rx1.zag ../build/frozen_src/rx2.zag ../build/frozen_src/rx3.zag ../build/frozen_src/rx4.zag > ../build/rx_unit.zag
znc ../build/rx_unit.zag -o ../build/rx 2>../build/rx_build.log || { echo "RX BUILD FAILED"; tail -5 ../build/rx_build.log; exit 1; }
DIGEST=$(sha256sum ../build/rx | cut -d' ' -f1)
FROZEN="c478c02a5358541a2afa7b33e40916befcf6475c849be1555f369a388f61ca4e"
if [ "$DIGEST" != "$FROZEN" ]; then
  echo "FROZEN DIGEST MISMATCH: $DIGEST"
  exit 1
fi
echo "learner digest OK (frozen)"
# own harness programs
cat pre2.zag adv2.zag > ../build/adv2_unit.zag
znc ../build/adv2_unit.zag -o ../build/adv2 2>../build/adv2_build.log || { echo "ADV2 BUILD FAILED"; tail -5 ../build/adv2_build.log; exit 1; }
cat pre2.zag answer2.zag > ../build/answer2_unit.zag
znc ../build/answer2_unit.zag -o ../build/answer2 2>../build/answer2_build.log || { echo "ANSWER2 BUILD FAILED"; tail -5 ../build/answer2_build.log; exit 1; }
cat pre2.zag score2.zag > ../build/score2_unit.zag
znc ../build/score2_unit.zag -o ../build/score2 2>../build/score2_build.log || { echo "SCORE2 BUILD FAILED"; tail -5 ../build/score2_build.log; exit 1; }
echo "build2 ok"
sha256sum ../build/rx ../build/adv2 ../build/answer2 ../build/score2 | tee ../build/bin2.sha256
# deterministic rebuild check on own units
cp ../build/adv2 ../build/adv2_a && znc ../build/adv2_unit.zag -o ../build/adv2_b 2>/dev/null
cmp ../build/adv2_a ../build/adv2_b && echo "ADV2 REBUILD IDENTICAL"
cp ../build/score2 ../build/score2_a && znc ../build/score2_unit.zag -o ../build/score2_b 2>/dev/null
cmp ../build/score2_a ../build/score2_b && echo "SCORE2 REBUILD IDENTICAL"
rm -f ../build/adv2_a ../build/adv2_b ../build/score2_a ../build/score2_b
