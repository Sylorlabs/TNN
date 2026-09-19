#!/bin/zsh
set -eu
cd /Users/Shared/micah/Documents/TNN/TNN
E=/Users/Shared/micah/Documents/TNN/TNN/Research/R33_FINAL_INTEGRATION_20260915T2145Z/n19
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
i=300
run build_all_children 0 /Users/Shared/micah/Documents/zag/znc "$E/sources/lane_c_all_children.zag" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$E/bin/lane_c_all_children"
mkdir "$E/roots/all_children" "$E/roots/all_children/crash" "$E/roots/all_children/resource"
Q="$E/bin/lane_c_all_children"
B="$E/bin/n19_repaired"
run wait_all_children 0 "$Q" wait-tests
run crash_all_children 0 "$Q" crash-matrix "$B" "$E/roots/all_children/crash"
run fsize_all_children 0 "$Q" resource "$B" "$E/roots/all_children/resource"
run cpu_all_children 0 "$Q" cpu-ceiling "$B" "$E/roots/all_children/resource"
printf 'failures=%s commands=%s\n' "$failures" "$((i-300))" > "$E/reap.summary.txt"
cat "$E/reap.summary.txt"
exit $((failures != 0))
