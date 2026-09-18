#!/bin/zsh
set -eu
cd /Users/Shared/micah/Documents/TNN/TNN
E=Research/R33_NATIVE_N19_RUNTIME_BOUNDARY/RECOVERY_20260915_C/INDEPENDENT_FRESH_1409
integer i=0 failures=0
run() {
 local label=$1 expected=$2; shift 2
 i=$((i+1)); local stem="$E/logs/${i}_${label}"
 printf '%q ' "$@" > "$stem.command"; printf '\n' >> "$stem.command"
 set +e; "$@" > "$stem.stdout" 2> "$stem.stderr"; local rc=$?; set -e
 printf '%s\n' "$rc" > "$stem.exit"
 printf '%s expected=%s actual=%s\n' "$label" "$expected" "$rc" >> "$E/results.results.txt"
 if [[ $rc != $expected ]]; then failures=$((failures+1)); fi
}
# Existing additive log directory; final rounds use fresh roots.
run build_qual 0 /Users/Shared/micah/Documents/zag/znc "$E/sources/n19_qual_driver_v3_recovery.zag" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$E/bin/n19_qual"
run build_host 0 /Users/Shared/micah/Documents/zag/znc "$E/sources/n19_host_v2_tests.zag" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$E/bin/n19_host_tests"
i=100
run independent_build 0 /Users/Shared/micah/Documents/zag/znc "$E/sources/c_independent_faults.zag" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$E/bin/c_independent_faults"
for round in a b; do
 mkdir "$E/roots/$round/independent"
 run independent_fault_$round 0 "$E/bin/c_independent_faults" "$E/roots/$round/independent"
done
run canonical_after 0 shasum -a 256 -c "$E/canonical.before.sha256"
run protected_after 0 shasum -a 256 -c "$E/protected.before.sha256"
run historical_after 0 shasum -a 256 -c "$E/closeout.before.sha256"
awk '{print $2}' "$E/canonical.before.sha256" | while IFS= read -r item; do shasum -a 256 "$item"; done > "$E/canonical.after.sha256"
awk '{print $2}' "$E/protected.before.sha256" | while IFS= read -r item; do shasum -a 256 "$item"; done > "$E/protected.after.sha256"
printf 'extra_failures=%s extra_commands=%s\n' "$failures" "$((i-100))" > "$E/extra.summary.txt"
exit $((failures != 0))
