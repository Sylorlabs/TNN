#!/bin/zsh
set -eu
cd /Users/Shared/micah/Documents/TNN/TNN
E=Research/R33_NATIVE_N19_RUNTIME_BOUNDARY/RECOVERY_20260915_C/INDEPENDENT_NATIVE_LANE_C_2
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
i=400
run after_hashes 0 perl "$E/after_hashes.pl"
for set in canonical protected closeout; do run ${set}_before_after 0 cmp "$E/$set.before.sha256" "$E/$set.after.sha256"; done
run recovery_preserved_final 0 shasum -a 256 -c "$E/recovery.before.sha256"
git diff --binary > "$E/git.final.diff"
run tracked_preserved_final 0 cmp "$E/git.before.diff" "$E/git.final.diff"
shasum -a 256 "$E/bin/"* > "$E/binary.sha256"
shasum -a 256 "$E/sources/"* > "$E/source.sha256"
find "$E/logs" -type f -exec shasum -a 256 {} + > "$E/logs.sha256"
printf 'failures=%s commands=%s\n' "$failures" "$((i-400))" > "$E/final_checks.summary.txt"
cat "$E/final_checks.summary.txt"
exit $((failures != 0))
