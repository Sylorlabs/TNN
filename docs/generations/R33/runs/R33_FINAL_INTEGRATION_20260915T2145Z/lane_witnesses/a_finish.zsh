#!/bin/zsh
set -u
ROOT=/Users/Shared/micah/Documents/TNN/TNN
E=/tmp/r33_final_push_20260915_1409/a-native-ZwVMZJZc
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
PHYSICAL=$(realpath "$E")
for mode in write read write-corrupt read-corrupt write-truncated read-truncated write-packet read-packet write-packet-corrupt read-packet-corrupt write-packet-truncated read-packet-truncated; do
 run "v92.physical.$mode" "$E/v92" "$mode" "$PHYSICAL/runtime_v92" || exit 1
 done
freeze "$ROOT/Research/R33_CONTINUING_LIFE_V1/driver.zag" || exit 99
sed -e "s@Research/R33_CONTINUING_LIFE_V1/ENGINEERING_06@$PHYSICAL/runtime_continuing@g" -e "s@/Users/Shared/micah/Documents/TNN/TNN/Research/R33_CONTINUING_LIFE_V1/BUILD_01/continuing_life@$PHYSICAL/continuing@g" -e "s@\"tests.zag\"@\"$E/sources/Research/R33_CONTINUING_LIFE_V1/tests.zag\"@" -e "s@\"../R33_NATIVE_PROCESS_V3.zag\"@\"$E/sources/Research/R33_NATIVE_PROCESS_V3.zag\"@" "$E/sources/Research/R33_CONTINUING_LIFE_V1/driver.zag" > "$E/continuing.zag"
compile continuing "$E/continuing.zag"
if [[ -x "$E/continuing" ]]; then run continuing.supervise "$E/continuing" supervise; fi
sed 's@/tmp/r33_final_push_20260915_1409/lane_a/@/tmp/r33_final_push_20260915_1409/a-native-ZwVMZJZc/@g' /tmp/r33_final_push_20260915_1409/lane_a/constant_probe.zag > "$E/constant_probe.zag"
compile constant_probe "$E/constant_probe.zag" || exit 1
run constant_probe.run "$E/constant_probe" || exit 1
run original_v73.disassembly otool -tvV "$E/original_v73" || exit 1
run repaired_v73.disassembly otool -tvV "$E/v73" || exit 1
shasum -a 256 "$COMP" > "$E/compiler.after.sha256"
run compiler_unchanged cmp "$E/compiler.before.sha256" "$E/compiler.after.sha256" || exit 1
