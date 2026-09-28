#!/usr/bin/env bash
# RUN_MANIFEST.txt: sha256 of every battery run output + pair byte-identity.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
RUNS="$HERE/runs"
OUT="$HERE/RUN_MANIFEST.txt"
ARMS="predictive_surprise fixed_window_4 fixed_window_8 fixed_window_16 fixed_window_64 adaptive_mdl adaptive_mdl_8 grounded_adaptive_mdl hierarchical_mdl raw_micro random_chunks"
{
echo "B-T1 battery run manifest (closeout reproduction, 2026-09-21)"
echo "binary: units/r0/impl/arms/arms.zag + additive R-7 leg, built with znc_linux_x86_64_abed8aa1 --no-zagd --no-analyze --no-foreground-cache"
echo "corpora: pg100.txt sha256=3cf4b3d44ee14cff4e14e78e2ad3318eff76f3f7f2afc3cee6bb925879110a37"
echo "         sqlite3.c sha256=b1dd5d74ec7f29055a6684fa06fb3c2f6821c87dd38f9a458dfd2e8a1db28189"
echo ""
fail=0
for arm in $ARMS; do
  for corp in pg100 sqlite3c; do
    a="$RUNS/${arm}__${corp}__r1.seg"; b="$RUNS/${arm}__${corp}__r2.seg"
    ha=$(sha256sum "$a" | cut -d' ' -f1); hb=$(sha256sum "$b" | cut -d' ' -f1)
    sa=$(stat -c%s "$a"); sb=$(stat -c%s "$b")
    if [ "$ha" = "$hb" ]; then st="IDENTICAL"; else st="MISMATCH"; fail=$((fail+1)); fi
    echo "$arm $corp r1 sha256=$ha bytes=$sa"
    echo "$arm $corp r2 sha256=$hb bytes=$sb pair=$st"
  done
done
echo ""
echo "pair_mismatches=$fail"
} | tee "$OUT"
exit $fail
