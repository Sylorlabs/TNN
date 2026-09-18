#!/bin/zsh
set -u
E=/tmp/r33_final_push_20260915_1409/a-native-ZwVMZJZc
COMP=/Users/Shared/micah/Documents/zag/znc
mkdir -p "$E/original_sources"
cp -R "$E/sources/Research" "$E/original_sources/"
run() {
 local label=$1 rc=0
 shift
 print -r -- "cwd=$PWD command=${(q)@}" >> "$E/commands.txt"
 "$@" > "$E/$label.stdout" 2> "$E/$label.stderr" || rc=$?
 print -r -- "$label,$rc" >> "$E/exits.csv"
 return $rc
}
for pair in 'v68 outer_learner_packet_bridge_v68_tests' 'v73 zag_checkpoint_sliceparam_repro_v73'; do
 label=${pair%% *}; source_name=${pair#* }
 source_path="$E/original_sources/Research/R33_CONTINUING_LIFE_V1/$source_name.zag"
 cp "$E/$label.original.zag" "$source_path"
 run "exact_original_$label.compile" "$COMP" "$source_path" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$E/exact_original_$label" || exit 1
 run "exact_original_$label.run" "$E/exact_original_$label"
 done
