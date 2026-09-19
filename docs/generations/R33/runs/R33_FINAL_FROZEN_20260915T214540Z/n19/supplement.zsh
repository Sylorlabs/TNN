#!/bin/zsh
set -eu
cd /Users/Shared/micah/Documents/TNN/TNN
E=/Users/Shared/micah/Documents/TNN/TNN/Research/R33_FINAL_INTEGRATION_20260915T_REQUAL_214145Z/n19
integer i=200 failures=0
run() {
 local label=$1 expected=$2; shift 2
 i=$((i+1)); local stem="$E/logs/${i}_${label}"
 printf '%q ' "$@" > "$stem.command"; printf '\n' >> "$stem.command"
 set +e; "$@" > "$stem.stdout" 2> "$stem.stderr"; local rc=$?; set -e
 printf '%s\n' "$rc" > "$stem.exit"
 printf '%s expected=%s actual=%s\n' "$label" "$expected" "$rc" >> "$E/supplement.results.txt"
 if [[ $rc != $expected ]]; then failures=$((failures+1)); fi
}
run build_corners 0 /Users/Shared/micah/Documents/zag/znc "$E/sources/lane_c_v6_corners.zag" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$E/bin/lane_c_corners"
mkdir "$E/roots/corners_a" "$E/roots/corners_b"
run corners_a 0 "$E/bin/lane_c_corners" independent-corners "$E/roots/corners_a"
run corners_b 0 "$E/bin/lane_c_corners" independent-corners "$E/roots/corners_b"
run malformed_cli 2 "$E/bin/lane_c_corners" unknown-operation
printf 'failures=%s commands=%s\n' "$failures" "$((i-200))" > "$E/supplement.summary.txt"
cat "$E/supplement.summary.txt"
exit $((failures != 0))
