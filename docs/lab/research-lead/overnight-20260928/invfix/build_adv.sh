#!/bin/sh
# build_adv.sh -- build every adversary world against both engines.
# Engine choice is the ONLY thing that differs; the world file is byte-identical.
# usage: sh build_adv.sh <t2|cog> <frozen|iv> <world>
set -e
D=/Users/Shared/micah/Documents/TNN/.worktrees/invfix/docs/lab/research-lead/overnight-20260928/invfix
R=/Users/Shared/micah/Documents/TNN/.worktrees/invfix/docs/lab/research-lead/overnight-20260928
ZNC=/Users/Shared/micah/Documents/TNN/.bin/znc
kind=$1; eng=$2; world=$3
out="$D/adv/${world}.${eng}"
mkdir -p "$D/adv"
if [ "$kind" = "t2" ]; then
  if [ "$eng" = "frozen" ]; then
    head -917 "$R/compression_exec/tnn2_frozen_ref.zag" > "$out.zag"
  else
    cat "$D/iv_tnn2.zag" > "$out.zag"
  fi
  cat "$D/adv_copy/adv_lib.zag" "$D/adv_copy/$world.zag" >> "$out.zag"
else
  if [ "$eng" = "frozen" ]; then
    cat "$R/cogops_rescueaware/c15_base.zag" "$R/cogops_learnosc2/c8_learn.zag" > "$out.zag"
  else
    cat "$D/iv_c15_base.zag" "$D/iv_inv.zag" "$D/iv_c8_learn.zag" > "$out.zag"
  fi
  cat "$D/adv_copy/adv_lib.zag" "$D/adv_copy/$world.zag" >> "$out.zag"
fi
cd "$D/adv"
$ZNC --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache "$world.$eng.zag" >/dev/null
echo "built adv/$world.$eng"
