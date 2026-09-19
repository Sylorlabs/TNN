#!/bin/zsh
set -u
ROOT=/Users/Shared/micah/Documents/TNN/TNN
E=/Users/Shared/micah/Documents/TNN/TNN/Research/R33_FINAL_INTEGRATION_20260915T2145Z
COMP=/Users/Shared/micah/Documents/zag/znc
cd "$ROOT"
mkdir -p "$E/sources" "$E/runtime_v92"
freeze() {
 local file=$1 rel=${1#$ROOT/} imported resolved
 [[ -f "$E/sources/$rel" ]] && return 0
 mkdir -p "$E/sources/${rel:h}"
 cp "$file" "$E/sources/$rel"
 while IFS= read -r imported; do
  resolved=$(realpath "${file:h}/$imported")
  [[ "$resolved" == "$ROOT/"* ]] || return 1
  freeze "$resolved" || return 1
 done < <(sed -n 's/^@import("\([^"]*\)").*/\1/p' "$file")
}
run() {
 local label=$1 rc=0
 shift
 print -r -- "cwd=$PWD command=${(q)@}" >> "$E/commands.txt"
 "$@" > "$E/$label.stdout" 2> "$E/$label.stderr" || rc=$?
 print -r -- "$label,$rc" >> "$E/exits.csv"
 return $rc
}
compile() {
 run "$1.compile" "$COMP" "$2" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$E/$1"
}
shasum -a 256 "$COMP" > "$E/compiler.before.sha256"
for pair in 'v68 outer_learner_packet_bridge_v68_tests' 'v73 zag_checkpoint_sliceparam_repro_v73' 'v70 zag_checkpoint_ptr_repro_v70' 'v71 zag_checkpoint_module_repro_v71' 'v72 zag_checkpoint_frame_repro_v72'; do
 label=${pair%% *}; source_name=${pair#* }
 source_rel="Research/R33_CONTINUING_LIFE_V1/$source_name.zag"
 freeze "$ROOT/$source_rel" || exit 99
 compile "$label" "$E/sources/$source_rel" || exit 1
 run "$label.run" "$E/$label" || exit 1
 if [[ "$label" == v68 || "$label" == v73 ]]; then
  old="$ROOT/Research/R33_CLOSEOUT_20260915T174458Z/sources/$source_rel"
  cp "$old" "$E/$label.original.zag"
  sed "s@\"checkpoint.zag\"@\"$E/sources/Research/R33_CONTINUING_LIFE_V1/checkpoint.zag\"@" "$old" > "$E/original_$label.zag"
  compile "original_$label" "$E/original_$label.zag" || exit 1
  run "original_$label.run" "$E/original_$label"
  sed 's/CL_CHECKPOINT_HEADER;/CL_CHECKPOINT_HEADER();/g' "$E/original_$label.zag" > "$E/minimal_$label.zag"
  compile "minimal_$label" "$E/minimal_$label.zag" || exit 1
  run "minimal_$label.run" "$E/minimal_$label" || exit 1
  run "$label.patch" diff -u "$old" "$E/sources/$source_rel"
 fi
 done
source_rel=Research/R33_NATIVE_N17_R27_CONTINUITY/V92_STATE_IMAGE_QUAL/state_image_qual_v92.zag
freeze "$ROOT/$source_rel" || exit 99
compile v92 "$E/sources/$source_rel" || exit 1
for mode in selftest write read write-corrupt read-corrupt write-truncated read-truncated write-packet read-packet write-packet-corrupt read-packet-corrupt write-packet-truncated read-packet-truncated; do
 run "v92.$mode" "$E/v92" "$mode" "$E/runtime_v92" || exit 1
 done
freeze "$ROOT/Research/R33_CONTINUING_LIFE_V1/driver.zag" || exit 99
sed -e "s@Research/R33_CONTINUING_LIFE_V1/ENGINEERING_06@/Users/Shared/micah/Documents/TNN/TNN/Research/R33_FINAL_INTEGRATION_20260915T2145Z/runtime_continuing@g" -e "s@/Users/Shared/micah/Documents/TNN/TNN/Research/R33_CONTINUING_LIFE_V1/BUILD_01/continuing_life@$E/continuing@g" -e "s@\"tests.zag\"@\"$E/sources/Research/R33_CONTINUING_LIFE_V1/tests.zag\"@" -e "s@\"../R33_NATIVE_PROCESS_V3.zag\"@\"$E/sources/Research/R33_NATIVE_PROCESS_V3.zag\"@" "$E/sources/Research/R33_CONTINUING_LIFE_V1/driver.zag" > "$E/continuing.zag"
compile continuing "$E/continuing.zag" || exit 1
run continuing.supervise "$E/continuing" supervise || exit 1
