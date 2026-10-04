#!/bin/bash
# p6_build_all.sh -- orchestration only. All science is pure Zag.
#
#   ./p6_build_all.sh gcsource   # build + 3x determinism on the world builder
#   ./p6_build_all.sh corpus A 3 # build corpora for set A into corpus.txt
#   ./p6_build_all.sh check     # (not built: learner incomplete)
#
# The learner translation unit (p6_corpus.zag + p6_learner.zag + p6_induce.zag
# + p6_train.zag) was NOT completed. See REPORT.md section 5.

set -u
LANE=/Users/Shared/micah/Documents/TNN/.worktrees/p6pushdown/docs/lab/research-lead/overnight-20260928/p6_pushdown
. /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh
ZB=/Users/Shared/micah/Documents/TNN/TNN/tools/zbuild.sh
cd "$LANE" || exit 2

case "${1:-}" in
  gcsource)
    cat p6_io.zag p6_lang.zag p6_ckcore.zag p6_gencorpus.zag p6_gcmain.zag > _p6_gencorpus.zag
    $ZB "$LANE/_p6_gencorpus.zag" --rep 3
    ;;
  corpus)
    cat p6_io.zag p6_lang.zag p6_ckcore.zag p6_gencorpus.zag p6_gcmain.zag > _p6_gencorpus.zag
    $ZB "$LANE/_p6_gencorpus.zag" >/dev/null || exit 1
    cp "corpus_${2}_s${3}.txt" corpus.txt
    cp "seed_${2}.txt" seed.txt
    echo "staged corpus_${2}_s${3}.txt -> corpus.txt"
    ;;
  *)
    echo "usage: p6_build_all.sh {gcsource|corpus SET STAGE}" >&2
    exit 2
    ;;
esac
