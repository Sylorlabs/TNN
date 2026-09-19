#!/bin/zsh
set -u
E=/Users/Shared/micah/Documents/TNN/TNN/Research/R33_FINAL_INTEGRATION_20260915T2145Z
ROOT=/Users/Shared/micah/Documents/TNN/TNN
COMP=/Users/Shared/micah/Documents/zag/znc
run() {
 local label=$1 rc=0
 shift
 print -r -- "cwd=$PWD command=${(q)@}" >> "$E/commands.txt"
 "$@" > "$E/$label.stdout" 2> "$E/$label.stderr" || rc=$?
 print -r -- "$label,$rc" >> "$E/exits.csv"
 return $rc
}
for source_name in outer_learner_packet_bridge_v68_tests zag_checkpoint_sliceparam_repro_v73; do
 run "direct_$source_name.source_unchanged" cmp "$ROOT/Research/R33_CONTINUING_LIFE_V1/$source_name.zag" "$E/sources/Research/R33_CONTINUING_LIFE_V1/$source_name.zag" || exit 1
 run "direct_$source_name.compile" "$COMP" "$ROOT/Research/R33_CONTINUING_LIFE_V1/$source_name.zag" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$E/direct_$source_name" || exit 1
 run "direct_$source_name.run" "$E/direct_$source_name" || exit 1
 done
run checkpoint_unchanged cmp "$ROOT/Research/R33_CONTINUING_LIFE_V1/checkpoint.zag" "$E/sources/Research/R33_CONTINUING_LIFE_V1/checkpoint.zag" || exit 1
run storage_unchanged cmp "$ROOT/Research/R33_CONTINUING_LIFE_V1/storage.zag" "$E/sources/Research/R33_CONTINUING_LIFE_V1/storage.zag" || exit 1
