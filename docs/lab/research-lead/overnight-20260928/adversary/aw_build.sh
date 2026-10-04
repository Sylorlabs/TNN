#!/bin/sh
# aw_build.sh -- assemble one adversary world from FROZEN sources + adversary lib.
# Pure shell orchestration. No computation.
set -eu
R=/Users/Shared/micah/Documents/TNN/.worktrees/adversary/docs/lab/research-lead/overnight-20260928
W=$R/adversary
FROZEN_COGOPS="$R/cogops_rescueaware/c15_base.zag $R/cogops_learnosc2/c8_learn.zag"
T2LIB=$W/tnn2_lib_slice.zag
for name in "$@"; do
  case "$name" in
    aw0[1-9]|aw1*) SRC=$W/$name.zag ;;
    *) echo "unknown $name" >&2; exit 2 ;;
  esac
  OUT=$W/$name.full.zag
  if grep -q "tnn2_init\|res_op\|t2_trial" "$SRC"; then
    cat "$T2LIB" $W/adv_lib.zag "$SRC" > "$OUT"
  else
    cat $FROZEN_COGOPS $W/adv_lib.zag "$SRC" > "$OUT"
  fi
  echo "--- $name: main count (must be 1): $(grep -c '^fn main(' "$OUT")"
done
