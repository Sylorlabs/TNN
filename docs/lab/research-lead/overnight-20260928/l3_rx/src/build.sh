#!/bin/sh
# build.sh -- L3-RX build. Pure Zag; pinned znc only; safebin PATH.
# Single-file compilation units; sha256 recorded; deterministic rebuild check.
set -e
export PATH="$HOME/safebin"
HERE=$(dirname "$0")
cd "$HERE"
mkdir -p ../build
cat pre.zag rx1.zag rx2.zag rx3.zag rx4.zag > ../build/rx_unit.zag
znc ../build/rx_unit.zag -o ../build/rx 2>../build/rx_build.log || { echo "RX BUILD FAILED"; tail -5 ../build/rx_build.log; exit 1; }
znc adv.zag -o ../build/adv 2>../build/adv_build.log || { echo "ADV BUILD FAILED"; tail -5 ../build/adv_build.log; exit 1; }
znc answer.zag -o ../build/answer 2>../build/answer_build.log || { echo "ANSWER BUILD FAILED"; tail -5 ../build/answer_build.log; exit 1; }
znc mem.zag -o ../build/mem 2>../build/mem_build.log || { echo "MEM BUILD FAILED"; tail -5 ../build/mem_build.log; exit 1; }
cat pre.zag score.zag > ../build/score_unit.zag
znc ../build/score_unit.zag -o ../build/score 2>../build/score_build.log || { echo "SCORE BUILD FAILED"; tail -5 ../build/score_build.log; exit 1; }
cat pre.zag audit.zag > ../build/audit_unit.zag
znc ../build/audit_unit.zag -o ../build/audit 2>../build/audit_build.log || { echo "AUDIT BUILD FAILED"; tail -5 ../build/audit_build.log; exit 1; }
cat pre.zag verdict.zag > ../build/verdict_unit.zag
znc ../build/verdict_unit.zag -o ../build/verdict 2>../build/verdict_build.log || { echo "VERDICT BUILD FAILED"; tail -5 ../build/verdict_build.log; exit 1; }
echo "build ok"
sha256sum ../build/rx ../build/adv ../build/answer ../build/mem ../build/score ../build/audit ../build/verdict | tee ../build/bin.sha256
# deterministic rebuild check
cp ../build/rx ../build/rx1 && znc ../build/rx_unit.zag -o ../build/rx2 2>/dev/null
cmp ../build/rx1 ../build/rx2 && echo "REBUILD IDENTICAL"
rm -f ../build/rx1 ../build/rx2
