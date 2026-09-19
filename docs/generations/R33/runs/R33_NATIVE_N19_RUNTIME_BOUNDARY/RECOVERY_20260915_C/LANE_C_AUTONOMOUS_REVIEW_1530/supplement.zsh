#!/bin/zsh
set -eu
cd /Users/Shared/micah/Documents/TNN/TNN
E=Research/R33_NATIVE_N19_RUNTIME_BOUNDARY/RECOVERY_20260915_C/LANE_C_AUTONOMOUS_REVIEW_1530
integer i=400 failures=0
run() {
 local label=$1 expected=$2; shift 2
 i=$((i+1)); local stem="$E/logs/${i}_${label}"
 printf '%q ' "$@" > "$stem.command"; printf '\n' >> "$stem.command"
 set +e; "$@" > "$stem.stdout" 2> "$stem.stderr"; local rc=$?; set -e
 printf '%s\n' "$rc" > "$stem.exit"
 printf '%s expected=%s actual=%s\n' "$label" "$expected" "$rc" >> "$E/supplement.results.txt"
 if [[ $rc != $expected ]]; then failures=$((failures+1)); fi
}
run build_faults 0 /Users/Shared/micah/Documents/zag/znc "$E/sources/c_independent_faults.zag" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$E/bin/c_faults"
run build_corners 0 /Users/Shared/micah/Documents/zag/znc "$E/sources/lane_c_v6_corners.zag" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$E/bin/c_corners"
for round in x y; do
 mkdir "$E/roots/fault_$round" "$E/roots/corners_$round"
 run faults_$round 0 "$E/bin/c_faults" "$E/roots/fault_$round"
 run corners_$round 0 "$E/bin/c_corners" independent-corners "$E/roots/corners_$round"
done
run malformed_cli 2 "$E/bin/n19_repaired" unknown-operation
run canonical_preserved 0 shasum -a 256 -c "$E/canonical.before.sha256"
run protected_preserved 0 shasum -a 256 -c "$E/protected.before.sha256"
printf "failures=%s commands=%s\n" "$failures" "$((i-400))" > "$E/supplement.summary.txt"
exit $((failures != 0))
